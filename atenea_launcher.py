import os
import threading
import time
from dotenv import load_dotenv
from atenea_core.database_manager import inicializar_database, registrar_evento
from atenea_core.kernel_monitor import iniciar_monitoreo
from atenea_core.atenea_core_logic import registrar_arranque
# Importaciones de módulos que se crearán a continuación
# from atenea_telegram.bot import iniciar_bot
# from atenea_bridge.ui import iniciar_ui

def iniciar_bot_telegram():
    """
    Inicializa y ejecuta el cliente del bot de Telegram en un hilo dedicado.
    Esta función se encargará de la comunicación con la API de Telegram.
    """
    registrar_evento("HILO TELEGRAM", "atenea_telegram/bot.py", "Módulo de comunicación con Telegram iniciado.")
    print("Iniciando módulo de Telegram...")
    # iniciar_bot() # Esta función contendrá el bucle del cliente Telethon.

def iniciar_interfaz_grafica():
    """
    Lanza la interfaz gráfica de usuario (GUI) construida con CustomTkinter.
    Este será el hilo principal de interacción con el usuario.
    """
    registrar_evento("HILO UI", "atenea_bridge/ui.py", "Interfaz gráfica de usuario iniciada.")
    print("Iniciando interfaz gráfica (CustomTkinter)...")
    # iniciar_ui() # Esta función iniciará el mainloop de customtkinter.

def main():
    """
    Punto de entrada principal para ATENEA.
    Orquesta el arranque de todos los módulos principales en hilos separados
    para una operación concurrente y resiliente.
    """
    try:
        load_dotenv()
        inicializar_database()
        registrar_arranque()
        registrar_evento("ARRANQUE SISTEMA", "atenea_launcher.py", "Sistema ATENEA iniciado. Orquestando hilos.")

        # --- Creación y Arranque de Hilos ---
        print("ATENEA :: Lanzando módulos principales en hilos concurrentes...")

        # Hilo 1: Monitor de archivos del Kernel (Watchdog)
        # Es un hilo daemon para que no bloquee la salida del programa.
        kernel_thread = threading.Thread(target=iniciar_monitoreo, name="KernelMonitorThread", daemon=True)
        
        # Hilo 2: Bot de Telegram (Telethon)
        # telegram_thread = threading.Thread(target=iniciar_bot_telegram, name="TelegramBotThread", daemon=True)

        # Hilo 3: Interfaz Gráfica de Usuario (CustomTkinter)
        # Este hilo no es daemon. La aplicación principal terminará cuando la ventana de la GUI se cierre.
        # ui_thread = threading.Thread(target=iniciar_interfaz_grafica, name="UIThread")

        kernel_thread.start()
        # telegram_thread.start()
        # ui_thread.start()
        
        registrar_evento("HILO KERNEL", "atenea_core/kernel_monitor.py", "Monitor de archivos iniciado.")
        print("ATENEA :: Hilo de Kernel... [ONLINE]")
        # print("ATENEA :: Hilo de Telegram... [ONLINE]")
        # print("ATENEA :: Hilo de UI... [ONLINE]")
        print("\nATENEA está viva. Todos los módulos están operativos.")

        # El hilo principal se une al hilo de la UI.
        # El programa esperará aquí hasta que la ventana principal se cierre.
        # ui_thread.join()

        # Bucle temporal para mantener el programa principal vivo mientras no hay UI
        while kernel_thread.is_alive():
            time.sleep(1)

    except Exception as e:
        print(f"ERROR CRÍTICO EN EL ARRANQUE DE ATENEA: {e}")
        registrar_evento("ERROR CRÍTICO", "atenea_launcher.py", str(e))
    finally:
        print("ATENEA se ha desconectado. Fin de la sesión.")

if __name__ == "__main__":
    main()