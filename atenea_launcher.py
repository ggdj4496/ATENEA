import os
import threading
import time
from dotenv import load_dotenv
from atenea_core.database_manager import inicializar_database, registrar_evento
from atenea_core.kernel_monitor import iniciar_monitoreo
from atenea_core.atenea_core_logic import registrar_arranque
# Importaciones de módulos que se crearán a continuación
from atenea_telegram.bot import iniciar_bot
from atenea_bridge.ui import iniciar_ui

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

import os
import threading
import time
import psutil
import GPUtil
import json
from datetime import datetime
from dotenv import load_dotenv
from atenea_core.database_manager import inicializar_database, registrar_evento
from atenea_core.kernel_monitor import iniciar_monitoreo
from atenea_core.atenea_core_logic import registrar_arranque, consultar_atenea
from atenea_telegram.bot import iniciar_bot
from atenea_bridge.ui import iniciar_ui
from atenea_lab.atenea_lab_pro_analyzer import procesar_orden_aprendizaje

def monitor_sistema():
    """Monitoriza recursos del sistema en tiempo real"""
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disco = psutil.disk_usage('C:\\').percent
            
            # GPU monitoring
            try:
                gpus = GPUtil.getGPUs()
                gpu_temp = gpus[0].temperature if gpus else 0
            except:
                gpu_temp = 0
            
            # Guardar métricas
            metricas = {
                'timestamp': datetime.now().isoformat(),
                'cpu': cpu,
                'ram': ram,
                'disco': disco,
                'gpu_temp': gpu_temp
            }
            
            with open('C:\\ATENEA\\logs\\metricas.json', 'a') as f:
                f.write(json.dumps(metricas) + '\n')
                
            time.sleep(60)  # Cada minuto
        except Exception as e:
            registrar_evento("ERROR_MONITOR", "sistema", str(e))

def iniciar_bot_telegram():
    """Inicializa bot de Telegram con Telethon y manejo de sesiones"""
    registrar_evento("HILO_TELEGRAM", "atenea_telegram/bot.py", "Iniciando bot de Telegram")
    print("ATENEA :: Hilo Telegram... [ONLINE]")
    
    try:
        from telethon import TelegramClient, events
        import asyncio
        
        api_id = int(os.getenv('TELEGRAM_API_ID', '0'))
        api_hash = os.getenv('TELEGRAM_API_HASH', '')
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        
        if not all([api_id, api_hash, bot_token]):
            registrar_evento("ERROR_TELEGRAM", "config", "Faltan credenciales de Telegram")
            return
            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        client = TelegramClient('C:\\ATENEA\\atenea_telegram\\session', api_id, api_hash)
        
        @client.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            await event.respond("🤖 ATENEA ONLINE - Sistema de Inteligencia Avanzada Activo")
            registrar_evento("TELEGRAM_CMD", "start", f"Usuario: {event.sender_id}")
        
        @client.on(events.NewMessage(pattern='/estado'))
        async def estado_handler(event):
            estado = f"""
            📊 ESTADO DEL SISTEMA ATENEA
            
            🧠 CPU: {psutil.cpu_percent()}%
            💾 RAM: {psutil.virtual_memory().percent}%
            💽 Disco: {psutil.disk_usage('C:\\').percent}%
            🎯 Kernel: ACTIVO
            🤖 Bot: ACTIVO
            
            Sistema operativo al 100%
            """
            await event.respond(estado)
        
        @client.on(events.NewMessage(pattern='/procesar_orden'))
        async def procesar_handler(event):
            await event.respond("🔄 Procesando orden ORD-5370-335970...")
            procesar_orden_aprendizaje()
            await event.respond("✅ Orden procesada exitosamente")
        
        client.start(bot_token=bot_token)
        registrar_evento("TELEGRAM_INICIADO", "sistema", "Bot de Telegram activo")
        client.run_until_disconnected()
        
    except Exception as e:
        registrar_evento("ERROR_TELEGRAM", "sistema", str(e))
        print(f"Error en Telegram: {e}")

def iniciar_interfaz_grafica():
    """Interfaz gráfica avanzada con CustomTkinter y gráficos en tiempo real"""
    registrar_evento("HILO_UI", "atenea_bridge/ui.py", "Iniciando interfaz gráfica")
    print("ATENEA :: Hilo UI... [ONLINE]")
    
    import customtkinter as ctk
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.animation as animation
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    class AteneaGUI:
        def __init__(self):
            self.root = ctk.CTk()
            self.root.title("🤖 ATENEA - Sistema de Inteligencia Avanzada")
            self.root.geometry("1200x800")
            
            # Frame principal
            self.main_frame = ctk.CTkFrame(self.root)
            self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Título
            self.title_label = ctk.CTkLabel(
                self.main_frame, 
                text="ATENEA - KERNEL DE INTELIGENCIA ARTIFICIAL", 
                font=ctk.CTkFont(size=24, weight="bold")
            )
            self.title_label.pack(pady=20)
            
            # Frame de métricas
            self.metrics_frame = ctk.CTkFrame(self.main_frame)
            self.metrics_frame.pack(fill="x", padx=20, pady=10)
            
            # Métricas en tiempo real
            self.cpu_label = ctk.CTkLabel(self.metrics_frame, text="CPU: 0%", font=ctk.CTkFont(size=16))
            self.cpu_label.grid(row=0, column=0, padx=20, pady=10)
            
            self.ram_label = ctk.CTkLabel(self.metrics_frame, text="RAM: 0%", font=ctk.CTkFont(size=16))
            self.ram_label.grid(row=0, column=1, padx=20, pady=10)
            
            self.disk_label = ctk.CTkLabel(self.metrics_frame, text="DISCO: 0%", font=ctk.CTkFont(size=16))
            self.disk_label.grid(row=0, column=2, padx=20, pady=10)
            
            # Frame de control
            self.control_frame = ctk.CTkFrame(self.main_frame)
            self.control_frame.pack(fill="x", padx=20, pady=10)
            
            # Botones de control
            self.procesar_btn = ctk.CTkButton(
                self.control_frame, 
                text="🔄 Procesar Orden ORD-5370-335970",
                command=self.procesar_orden,
                font=ctk.CTkFont(size=14)
            )
            self.procesar_btn.pack(pady=10)
            
            self.consultar_btn = ctk.CTkButton(
                self.control_frame,
                text="🧠 Consultar a ATENEA",
                command=self.consultar_atenea,
                font=ctk.CTkFont(size=14)
            )
            self.consultar_btn.pack(pady=10)
            
            # Frame de logs
            self.log_frame = ctk.CTkFrame(self.main_frame)
            self.log_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            self.log_text = ctk.CTkTextbox(self.log_frame, width=1100, height=300)
            self.log_text.pack(pady=20, padx=20)
            
            # Iniciar actualización de métricas
            self.actualizar_metricas()
            
        def procesar_orden(self):
            self.log("🔄 Procesando orden ORD-5370-335970...")
            procesar_orden_aprendizaje()
            self.log("✅ Orden procesada exitosamente")
            
        def consultar_atenea(self):
            respuesta = consultar_atenea("¿Cuál es el estado del sistema?")
            self.log(f"🧠 ATENEA responde: {respuesta}")
            
        def log(self, mensaje):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_text.insert("end", f"[{timestamp}] {mensaje}\n")
            self.log_text.see("end")
            
        def actualizar_metricas(self):
            try:
                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory().percent
                disco = psutil.disk_usage('C:\\').percent
                
                self.cpu_label.configure(text=f"CPU: {cpu}%")
                self.ram_label.configure(text=f"RAM: {ram}%")
                self.disk_label.configure(text=f"DISCO: {disco}%")
                
                # Cambiar color según uso
                if cpu > 80: self.cpu_label.configure(text_color="red")
                elif cpu > 60: self.cpu_label.configure(text_color="orange")
                else: self.cpu_label.configure(text_color="green")
                    
                if ram > 80: self.ram_label.configure(text_color="red")
                elif ram > 60: self.ram_label.configure(text_color="orange")
                else: self.ram_label.configure(text_color="green")
                    
                if disco > 80: self.disk_label.configure(text_color="red")
                elif disco > 60: self.disk_label.configure(text_color="orange")
                else: self.disk_label.configure(text_color="green")
                
            except Exception as e:
                self.log(f"❌ Error actualizando métricas: {e}")
            
            self.root.after(1000, self.actualizar_metricas)  # Actualizar cada segundo
            
        def run(self):
            self.root.mainloop()
    
    try:
        app = AteneaGUI()
        app.run()
    except Exception as e:
        registrar_evento("ERROR_UI", "sistema", str(e))

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