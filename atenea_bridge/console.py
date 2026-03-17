import customtkinter as ctk
import subprocess
import sys

ctk.set_appearance_mode("dark")

class AteneaConsole(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ATENEA AGENT - COMMAND CENTER")
        self.geometry("1100x700")

        # Configuración de Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Barra Lateral
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.lbl_title = ctk.CTkLabel(self.sidebar, text="ATENEA KERNEL", font=("Consolas", 20, "bold"))
        self.lbl_title.pack(pady=30)

        # Botones de Funciones (Lo que pediste)
        self.btn_asimilacion = ctk.CTkButton(self.sidebar, text="🧬 ASIMILACIÓN BOTS", command=self.open_lab)
        self.btn_asimilacion.pack(pady=10, padx=20)
        
        self.btn_perchance = ctk.CTkButton(self.sidebar, text="🎨 PERCHANCE PRO", command=self.open_perchance)
        self.btn_perchance.pack(pady=10, padx=20)

        # Monitor de Logs en tiempo real
        self.log_view = ctk.CTkTextbox(self, font=("Consolas", 13), text_color="#00FF41", fg_color="#050505")
        self.log_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.log_view.insert("0.0", ">>> KERNEL ADMIN ONLINE - PRIVILEGIOS ROOT ACTIVADOS\n")

    def open_lab(self):
        self.log_view.insert("end", ">>> Accediendo a atenea_lab: Preparando análisis orig/result...\n")
        
    def open_perchance(self):
        self.log_view.insert("end", ">>> Conectando con Perchance.ai: Bypass de filtros activo.\n")

if __name__ == "__main__":
    app = AteneaConsole()
    app.mainloop()