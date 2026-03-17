import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import atenea_core.database_manager as db

class AteneaHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            rel_path = os.path.relpath(event.src_path, r"C:\ATENEA")
            # Registramos en la DB para que Atenea "sepa" qué ha cambiado
            db.registrar_evento("MODIFICACIÓN", rel_path, "Cambio detectado por el Kernel Monitor")
            print(f">>> [KERNEL] Archivo modificado: {rel_path}")

def iniciar_monitoreo():
    path = r"C:\ATENEA"
    event_handler = AteneaHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    return observer