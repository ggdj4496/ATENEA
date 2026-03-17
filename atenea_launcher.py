import os
import threading
import time
import psutil
import json
from datetime import datetime
from dotenv import load_dotenv
from atenea_core.database_manager import inicializar_database, registrar_evento
from atenea_core.kernel_monitor import iniciar_monitoreo
from atenea_core.atenea_core_logic import registrar_arranque, consultar_atenea

# Importar funciones de procesamiento
try:
    from atenea_lab.atenea_lab_pro_analyzer import procesar_orden_aprendizaje
except ImportError:
    def procesar_orden_aprendizaje():
        print("⚠️ Módulo de laboratorio no disponible")
        registrar_evento("ADVERTENCIA", "laboratorio", "Módulo atenea_lab no encontrado")

def monitor_sistema():
    """Monitoriza recursos del sistema en tiempo real"""
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disco = psutil.disk_usage('C:\\').percent
            
            # GPU monitoring (sin GPUtil para evitar errores)
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

        @client.on(events.NewMessage(pattern='/generar_imagen(?: (.*))?'))
        async def generar_imagen_handler(event):
            prompt = event.pattern_match.group(1)
            if not prompt:
                await event.respond("Por favor, proporciona una descripción para la imagen. Uso: /generar_imagen <descripción>")
                return

            await event.respond(f"🎨 Generando imagen para: '{prompt}'...")
            
            # Llamar a la función del núcleo en un hilo separado para no bloquear el bot
            loop = asyncio.get_event_loop()
            try:
                imagen_url = await loop.run_in_executor(None, generar_imagen_perchance, prompt)
                
                if "Error" in imagen_url:
                    await event.respond(f"❌ {imagen_url}")
                else:
                    # Enviar la URL como un mensaje. Telegram la previsualizará.
                    await event.respond(f"🖼️ ¡Imagen generada!\n{imagen_url}")
                    registrar_evento("IMAGEN_GENERADA", "perchance", f"Prompt: '{prompt}' -> URL: {imagen_url}")

            except Exception as e:
                await event.respond("❌ Ocurrió un error inesperado al generar la imagen.")
                registrar_evento("ERROR_IMAGEN", "perchance", str(e))
        
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
    
    try:
        import customtkinter as ctk
        
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

                # Frame de generación de imágenes
                self.image_frame = ctk.CTkFrame(self.main_frame)
                self.image_frame.pack(fill="x", padx=20, pady=10)

                self.image_prompt_entry = ctk.CTkEntry(
                    self.image_frame,
                    placeholder_text="Introduce el prompt para generar una imagen...",
                    width=400,
                    font=ctk.CTkFont(size=14)
                )
                self.image_prompt_entry.pack(side="left", padx=(0, 10), expand=True, fill="x")

                self.generar_imagen_btn = ctk.CTkButton(
                    self.image_frame,
                    text="🎨 Generar Imagen (Perchance)",
                    command=self.generar_imagen,
                    font=ctk.CTkFont(size=14)
                )
                self.generar_imagen_btn.pack(side="left")

                
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

            def generar_imagen(self):
                prompt = self.image_prompt_entry.get()
                if not prompt:
                    self.log("⚠️ Por favor, introduce un prompt para generar la imagen.")
                    return

                self.log(f"🎨 Solicitando imagen para: '{prompt}'...")
                
                # Ejecutar en un hilo para no bloquear la UI
                threading.Thread(target=self._generar_imagen_thread, args=(prompt,), daemon=True).start()

            def _generar_imagen_thread(self, prompt):
                imagen_url = generar_imagen_perchance(prompt)
                if "Error" in imagen_url:
                    self.log(f"❌ {imagen_url}")
                else:
                    self.log(f"🖼️ ¡Imagen generada! Puedes verla en: {imagen_url}")
                
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
        
        app = AteneaGUI()
        app.run()
        
    except Exception as e:
        registrar_evento("ERROR_UI", "sistema", str(e))
        print(f"Error en UI: {e}")

def main():
    """
    Función principal que coordina el inicio de todos los módulos del sistema ATENEA.
    Se ejecuta al lanzar el script atenea_launcher.py
    """
    print("🚀 INICIANDO ATENEA - SISTEMA DE INTELIGENCIA AVANZADA")
    print("=" * 60)
    
    try:
        # 1. Cargar configuración desde .env
        print("📋 Cargando configuración...")
        load_dotenv()
        
        # 2. Inicializar base de datos
        print("🗄️ Inicializando base de datos...")
        inicializar_database()
        
        # 3. Registrar arranque en el log
        print("📝 Registrando evento de arranque...")
        registrar_arranque()
        
        # 4. Iniciar monitor de archivos
        print("👁️ Iniciando monitor de archivos...")
        hilo_monitor = threading.Thread(target=iniciar_monitoreo, name="MonitorArchivos", daemon=True)
        hilo_monitor.start()
        
        # 5. Iniciar monitor del sistema
        print("📊 Iniciando monitor del sistema...")
        hilo_sistema = threading.Thread(target=monitor_sistema, name="MonitorSistema", daemon=True)
        hilo_sistema.start()
        
        # 6. Iniciar bot de Telegram
        print("🤖 Iniciando bot de Telegram...")
        hilo_telegram = threading.Thread(target=iniciar_bot_telegram, name="TelegramBot", daemon=True)
        hilo_telegram.start()
        
        print("✅ ATENEA :: Kernel iniciado... [ONLINE]")
        print("✅ ATENEA :: Hilo Monitor... [ONLINE]")
        print("✅ ATENEA :: Hilo Telegram... [ONLINE]")
        
        # 7. Iniciar interfaz gráfica (esto bloqueará el hilo principal)
        print("🖥️ Iniciando interfaz gráfica...")
        iniciar_interfaz_grafica()
        
    except KeyboardInterrupt:
        print("\n⏹️ Deteniendo ATENEA...")
        registrar_evento("APAGADO", "sistema", "ATENEA detenido por el usuario")
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        registrar_evento("ERROR_CRITICO", "sistema", str(e))

if __name__ == "__main__":
    main()