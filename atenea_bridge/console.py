import customtkinter as ctk
import os
import threading

ctk.set_appearance_mode("dark")

class AteneaBridge(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ATENEA SYSTEM - CONTROL PANEL")
        self.geometry("1000x600")

        # Layout: Sidebar y Main
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.lbl_logo = ctk.CTkLabel(self.sidebar, text="ATENEA BOT", font=("Orbitron", 20, "bold"))
        self.lbl_logo.pack(pady=20)

        # BOTONES DE CONTROL
        self.btn_sync = ctk.CTkButton(self.sidebar, text="SINCRONIZAR", fg_color="#1f538d", command=self.sync_atenea)
        self.btn_sync.pack(pady=10, padx=20)

        # MAIN CONSOLE
        self.console_frame = ctk.CTkFrame(self, fg_color="#101010")
        self.console_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.log_txt = ctk.CTkTextbox(self.console_frame, font=("Consolas", 12), text_color="#00FF41")
        self.log_txt.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_txt.insert("0.0", ">>> SISTEMA DE CONTROL ATENEA ONLINE...\n")

    def sync_atenea(self):
        self.log_txt.insert("end", ">>> Conectando con atenea_agent_bot... Sincronizando.\n")
        # Aquí llamaríamos al arranque de Telegram

if __name__ == "__main__":
    app = AteneaBridge()
    app.mainloop()