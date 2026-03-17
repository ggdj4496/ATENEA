import os
from dotenv import load_dotenv
from atenea_core.database_manager import inicializar_database
from atenea_core.kernel_monitor import iniciar_monitoreo
from atenea_core.atenea_core_logic import registrar_arranque
from atenea_bridge.console import iniciar_consola

def main():
    """Punto de entrada principal para la aplicación Atenea."""
    observer = None  # Inicializar observer a None
    try:
        # Cargar variables de entorno
        load_dotenv()

        # Inicializar la base de datos
        inicializar_database()

        # Registrar el arranque en el log
        registrar_arranque()

        # Iniciar el monitor de archivos del kernel
        observer = iniciar_monitoreo()
        print("Atenea está viva. El Kernel está monitorizando el sistema de archivos.")
        print("Escribe 'exit' para terminar.")

        # Iniciar la consola interactiva
        iniciar_consola(observer)

    except Exception as e:
        print(f"ERROR CRÍTICO EN EL ARRANQUE DE ATENEA: {e}")
        # Aquí podrías añadir un log de errores más detallado si fuera necesario
    finally:
        # Asegurarse de que el observer se detiene correctamente al salir
        if observer and observer.is_alive():
            observer.stop()
            observer.join()
        print("Atenea se ha desconectado. Fin de la sesión.")

if __name__ == "__main__":
    main()