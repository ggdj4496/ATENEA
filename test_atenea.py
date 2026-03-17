import unittest
import os
import sqlite3
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from atenea_core.database_manager import inicializar_database, DB_PATH
from atenea_core.kernel_monitor import iniciar_monitoreo
# Importar 'main' desde el launcher para probar el flujo de arranque
from atenea_launcher import main as atenea_main

class TestAteneaStartup(unittest.TestCase):

    def setUp(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def tearDown(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        db_dir = os.path.dirname(DB_PATH)
        if os.path.exists(db_dir) and not os.listdir(db_dir):
            os.rmdir(db_dir)

    def test_database_initialization(self):
        """Prueba que la base de datos se inicializa correctamente."""
        try:
            inicializar_database()
            self.assertTrue(os.path.exists(DB_PATH))
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='guion_vida';")
            self.assertIsNotNone(cursor.fetchone())
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='funciones_asimiladas';")
            self.assertIsNotNone(cursor.fetchone())
            conn.close()
        except Exception as e:
            self.fail(f"inicializar_database() generó una excepción inesperada: {e}")

    # Patch de todas las funciones que main llama, para aislar load_dotenv
    @patch('atenea_launcher.iniciar_consola')
    @patch('atenea_launcher.iniciar_monitoreo')
    @patch('atenea_launcher.registrar_arranque')
    @patch('atenea_launcher.inicializar_database')
    @patch('atenea_launcher.load_dotenv')
    def test_main_calls_load_dotenv(self, mock_load_dotenv, mock_init_db, mock_reg_arranque, mock_init_mon, mock_init_consola):
        """Prueba que la función principal llama a load_dotenv."""
        try:
            atenea_main()
        except Exception as e:
            # La prueba no debe fallar por excepciones controladas en main
            pass
        mock_load_dotenv.assert_called_once()

    # Corregido: El patch debe apuntar a donde se USA el objeto
    @patch('atenea_core.kernel_monitor.Observer')
    def test_kernel_monitor_startup(self, MockObserver):
        """Prueba que el monitor del kernel se inicia correctamente."""
        mock_observer_instance = MockObserver.return_value
        mock_observer_instance.schedule = MagicMock()
        mock_observer_instance.start = MagicMock()

        try:
            observer = iniciar_monitoreo()
            MockObserver.assert_called_once()
            # Ahora 'observer' es una instancia del mock, así que usamos el mock para verificar
            mock_observer_instance.schedule.assert_called_once()
            mock_observer_instance.start.assert_called_once()
        except Exception as e:
            self.fail(f"iniciar_monitoreo() generó una excepción inesperada: {e}")

if __name__ == '__main__':
    unittest.main()