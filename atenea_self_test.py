
import unittest
import threading
import time
from unittest.mock import patch, MagicMock

# Mockear los módulos que no queremos ejecutar realmente durante el test
# Esto es crucial para aislar el componente que estamos probando (el lanzador).

# Mock para la base de datos
mock_db = MagicMock()

# Mock para el monitor de archivos
mock_monitor = MagicMock()

# Mock para el bot de Telegram
mock_bot = MagicMock()

# Mock para la UI
mock_ui = MagicMock()

# Aplicamos los mocks a nivel de módulo para que cualquier import de estos
# en el código bajo prueba use nuestras versiones falsas.
modules = {
    "atenea_core.database_manager.inicializar_database": mock_db,
    "atenea_core.kernel_monitor.iniciar_monitoreo": mock_monitor,
    "atenea_telegram.bot.iniciar_bot": mock_bot,
    "atenea_bridge.ui.iniciar_ui": mock_ui,
    "dotenv.load_dotenv": MagicMock() # Evitamos que intente cargar un .env real
}

class TestAteneaSelfTest(unittest.TestCase):

    @patch.dict("sys.modules", modules)
    def test_sistem-inicia_hilos_correctamente(self):
        """
        Verifica que el main() de atenea_launcher.py inicia correctamente
        los tres hilos principales (Kernel, Telegram, UI) y que estos
        son llamados como se espera.
        """
        print("\n--- EJECUTANDO TEST: Verificación de arranque de hilos ---")
        
        # Importamos el lanzador DESPUÉS de aplicar los parches
        from atenea_launcher import main
        
        # Creamos un mock para la función join del hilo de la UI
        # para evitar que el test se quede bloqueado esperando a que la UI termine.
        with patch.object(threading.Thread, 'join') as mock_join:
            
            # Ejecutamos el main en un hilo separado para que no bloquee el test.
            # El main de Atenea está diseñado para correr indefinidamente hasta que la UI se cierre.
            main_thread = threading.Thread(target=main)
            main_thread.start()
            
            # Damos un pequeño margen para que los hilos dentro de main() arranquen
            time.sleep(1)

            # --- ASERCIONES ---
            # 1. Verificar que el monitor del kernel fue iniciado.
            try:
                mock_monitor.assert_called_once()
                print("[OK] El monitor del Kernel fue iniciado.")
            except AssertionError as e:
                self.fail(f"[FALLO] El monitor del Kernel no fue iniciado como se esperaba. {e}")

            # 2. Verificar que el bot de Telegram fue iniciado.
            try:
                mock_bot.assert_called_once()
                print("[OK] El bot de Telegram fue iniciado.")
            except AssertionError as e:
                self.fail(f"[FALLO] El bot de Telegram no fue iniciado como se esperaba. {e}")

            # 3. Verificar que la UI fue iniciada.
            try:
                mock_ui.assert_called_once()
                print("[OK] La interfaz gráfica (UI) fue iniciada.")
            except AssertionError as e:
                self.fail(f"[FALLO] La UI no fue iniciada como se esperaba. {e}")

            # 4. Verificamos que el programa principal espera a que el hilo de la UI termine.
            try:
                mock_join.assert_called_once()
                print("[OK] El hilo principal espera correctamente al cierre de la UI (join). ")
            except AssertionError as e:
                self.fail(f"[FALLO] El programa no esperó a que la UI terminara. {e}")

            print("--- TEST COMPLETADO: Todos los módulos principales se lanzaron correctamente. ---")

if __name__ == "__main__":
    unittest.main()