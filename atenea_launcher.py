import os
import sys
import threading
import time
import subprocess
import ctypes
from atenea_core.database_manager import inicializar_database, registrar_evento

# REGLA: Privilegios de Administrador para control de Kernel
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def lanzar_componente(comando):
    """Lanza un proceso y lo mantiene vivo."""
    subprocess.Popen([sys.executable] + comando)

def iniciar_sistema_total():
    if not is_admin():
        print(">>> [!] Elevando privilegios... Acepta el aviso de Windows.")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    print(f"{'='*40}")
    print("   ATENEA AGENT - INICIANDO SECUENCIA ROOT")
    print(f"{'='*40}")

    # 1. Inicializar Cerebro (DB)
    inicializar_database()
    registrar_evento("SISTEMA", "Kernel", "Arranque maestro iniciado desde Launcher")

    # 2. Lanzar Monitor de Integridad (En segundo plano)
    # Importante: El monitor vigila cambios en C:\ATENEA
    from atenea_core.kernel_monitor import iniciar_monitoreo
    monitor_thread = threading.Thread(target=iniciar_monitoreo, daemon=True)
    monitor_thread.start()
    print(">>> [OK] Kernel Monitor activo (Vigilando VS Code)")

    # 3. Lanzar Bridge (Interfaz Visual) y Telegram
    print(">>> [OK] Desplegando Consola Visual...")
    lanzar_componente([r"C:\ATENEA\atenea_bridge\console.py"])
    
    print(">>> [OK] Sincronizando atenea_telegram...")
    lanzar_componente([r"C:\ATENEA\atenea_telegram\atenea_telegram.py"])

    print(f"\n>>> [{time.strftime('%H:%M:%S')}] TODO ONLINE. ATENEA está viva.")
    
    # Mantener el proceso padre vivo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n>>> Apagando sistema de forma segura...")

if __name__ == "__main__":
    iniciar_sistema_total()