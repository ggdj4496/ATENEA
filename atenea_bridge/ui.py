
import customtkinter as ctk
from atenea_core.database_manager import registrar_evento

def iniciar_ui():
    """
    Crea y ejecuta la interfaz gráfica principal de ATENEA.
    Utiliza CustomTkinter para ofrecer una ventana con controles básicos
    y visualización de estado del sistema.
    """
    registrar_evento("HILO UI", "atenea_bridge/ui.py", "Interfaz gráfica de usuario iniciada.")
    print("ATENEA :: Hilo de UI... [ONLINE]")

    app = ctk.CTk()
    app.title("ATENEA - Consola de Mando")
    app.geometry("800x600")

    # --- Widgets de la Interfaz ---
    label = ctk.CTkLabel(app, text="ATENEA KERNEL STATUS: ONLINE", font=("Roboto", 16))
    label.pack(pady=20, padx=20)

    textbox = ctk.CTkTextbox(app, width=760, height=400)
    textbox.pack(padx=20, pady=10)
    textbox.insert("0.0", "Sistema iniciado. Esperando logs...\n")

    # --- Bucle Principal de la App ---
    app.mainloop()

    print("Ventana de UI cerrada. Finalizando hilo de interfaz.")