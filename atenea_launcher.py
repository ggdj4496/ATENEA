import os
import sys
import ctypes
import subprocess
import datetime
import time

# --- REGLA DE ORO: CONTROL DE PRIVILEGIOS ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_privileges():
    if not is_admin():
        print(">>> [SISTEMA] Elevando privilegios a nivel KERNEL/ADMIN...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

# --- CONFIGURACIÓN DE RUTAS ---
RAIZ = r"C:\ATENEA"
ESTRUCTURA = [
    r"C:\ATENEA\atenea_core",
    r"C:\ATENEA\atenea_core\database",
    r"C:\ATENEA\atenea_bridge",
    r"C:\ATENEA\atenea_security",
    r"C:\ATENEA\atenea_lab",
    r"C:\ATENEA\atenea_lab\image_analisis",
    r"C:\ATENEA\atenea_lab\bots_investigados",
    r"C:\ATENEA\atenea_lab\learning_functions",
    r"C:\ATENEA\atenea_bot"
]

def verificar_integridad():
    print(f"\n{'='*50}")
    print(f"   SISTEMA ATENEA - CHEQUEO DE INTEGRIDAD")
    print(f"{'='*50}")
    
    # 1. Verificar carpetas (Edición no destructiva)
    for ruta in ESTRUCTURA:
        if not os.path.exists(ruta):
            os.makedirs(ruta)
            print(f"[NUEVO] Carpeta creada: {ruta}")
        else:
            print(f"[OK] Integridad confirmada: {ruta}")

    # 2. Verificar existencia de archivos clave
    archivos_clave = [
        os.path.join(RAIZ, "atenea_core", "database_manager.py"),
        os.path.join(RAIZ, "atenea_bridge", "console_gui.py")
    ]
    
    for archivo in archivos_clave:
        if os.path.exists(archivo):
            print(f"[FILE] Detectado archivo crítico: {os.path.basename(archivo)}")
        else:
            print(f"[!] Aviso: El archivo {os.path.basename(archivo)} aún no ha sido generado.")

def iniciar_sistema():
    elevate_privileges()
    verificar_integridad()
    
    print("\n>>> Iniciando Database y Monitoreo...")
    # Aquí es donde el arrancador llama al Bridge
    # subprocess.Popen([sys.executable, r"C:\ATENEA\atenea_bridge\console_gui.py"])
    
    print(f">>> [{datetime.datetime.now()}] ATENEA ONLINE. Esperando órdenes en consola.")

if __name__ == "__main__":
    iniciar_sistema()
    # Mantenemos la consola abierta para ver el proceso de arranque
    input("\nPresiona ENTER para minimizar el núcleo...")