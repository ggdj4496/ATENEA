import sqlite3
import os
import datetime

DB_PATH = r"C:\ATENEA\atenea_core\database\atenea_mind.db"

def inicializar_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla: Guion de Vida (Historial de aprendizaje y trabajo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guion_vida (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            accion TEXT,
            archivo_afectado TEXT,
            conocimiento_adquirido TEXT
        )
    ''')

    # Tabla: Mapeo de Estructuras de Bots
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_structures_mapped (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_origen TEXT,
            texto_boton TEXT,
            datos_callback TEXT UNIQUE
        )
    ''')
    
    # Tabla: Registro de Funciones (Lo extraído de bots)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funciones_asimiladas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_origen TEXT,
            nombre_funcion TEXT,
            descripcion_tecnica TEXT,
            ruta_txt_aprendizaje TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def registrar_evento(accion, archivo="", conocimiento=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO guion_vida (fecha, accion, archivo_afectado, conocimiento_adquirido)
        VALUES (?, ?, ?, ?)
    ''', (fecha, accion, archivo, conocimiento))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    inicializar_database()
    registrar_evento("SISTEMA", "atenea_mind.db", "Inicialización de la base de conocimientos local.")