import sqlite3
from atenea_core.database_manager import DB_PATH

def registrar_estructura_bot(bot_origen, texto_boton, datos_callback):
    """Registra la estructura de un botón de un bot enemigo en la base de datos."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO bot_structures_mapped (bot_origen, texto_boton, datos_callback)
            VALUES (?, ?, ?)
        """, (bot_origen, texto_boton, datos_callback))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"[ERROR DB] No se pudo registrar la estructura del bot: {e}")
        return False