import threading
import subprocess
import atenea_core.database_manager as db

def lanzar_telegram():
    subprocess.run(["python", r"C:\ATENEA\atenea_telegram\atenea_telegram.py"])

def lanzar_consola_visual():
    subprocess.run(["python", r"C:\ATENEA\atenea_bridge\console.py"])

def iniciar_atenea_total():
    print(">>> [SISTEMA] Iniciando Secuencia de Control Total...")
    db.inicializar_database()
    
    # Hilos para que todo funcione a la vez
    t1 = threading.Thread(target=lanzar_telegram)
    t2 = threading.Thread(target=lanzar_consola_visual)
    
    t1.start()
    t2.start()
    
    print(">>> [!] ATENEA está escuchando en Telegram y Windows. Sincronización completa.")

if __name__ == "__main__":
    iniciar_atenea_total()