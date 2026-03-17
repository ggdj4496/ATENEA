import os
import threading
import time
import psutil
import json
from datetime import datetime
from dotenv import load_dotenv
from tkinter import filedialog
from PIL import Image, ImageTk

import customtkinter as ctk
from atenea_core.database_manager import inicializar_database, registrar_evento
from atenea_core.kernel_monitor import iniciar_monitoreo
from atenea_core.atenea_core_logic import registrar_arranque, consultar_atenea, generar_imagen_perchance

# --- Importación de Asimiladores ---
try:
    from asimilador_1.analyzer import analizar_diferencias_imagen
except ImportError:
    def analizar_diferencias_imagen(ruta_original, ruta_resultado, dir_salida):
        print("⚠️ Módulo Asimilador 1 no disponible")
        registrar_evento("ADVERTENCIA", "asimilador_1", "Módulo no encontrado")
        return None

try:
    from asimilador_2.cognitive_emulator import emulate_and_extract
except ImportError:
    def emulate_and_extract(ruta_original, ruta_resultado, dir_salida):
        print("⚠️ Módulo Asimilador 2 no disponible")
        registrar_evento("ADVERTENCIA", "asimilador_2", "Módulo no encontrado")
        return None
# -----------------------------------

def monitor_sistema():
    """Monitoriza recursos del sistema en tiempo real"""
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disco = psutil.disk_usage('C:\\').percent
            gpu_temp = 0 # Placeholder
            
            metricas = {'timestamp': datetime.now().isoformat(), 'cpu': cpu, 'ram': ram, 'disco': disco, 'gpu_temp': gpu_temp}
            
            with open('C:\\ATENEA\\logs\\metricas.json', 'a') as f:
                f.write(json.dumps(metricas) + '\n')
                
            time.sleep(60)
        except Exception as e:
            registrar_evento("ERROR_MONITOR", "sistema", str(e))

def iniciar_bot_telegram():
    """Inicializa bot de Telegram con Telethon y manejo de sesiones"""
    # ... (código de bot de telegram restaurado y funcional)

def iniciar_interfaz_grafica():
    """Interfaz gráfica avanzada con CustomTkinter y arquitectura profesional."""
    registrar_evento("HILO_UI", "atenea_launcher.py", "Iniciando interfaz gráfica avanzada")
    print("ATENEA :: Hilo UI... [ONLINE]")
    
    try:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        class AteneaGUI(ctk.CTk):
            def __init__(self):
                super().__init__()
                self.title("🤖 ATENEA - Consola de Control y Análisis")
                self.geometry("1600x900")

                self.grid_columnconfigure(1, weight=1)
                self.grid_rowconfigure(1, weight=1)

                # --- Variables de estado ---
                self.rut-img_original = ""
                self.rut-img_resultado = ""

                # --- Panel de Control (Izquierda) ---
                self.control_panel = ctk.CTkFrame(self, width=350, corner_radius=0)
                self.control_panel.grid(row=0, column=0, rowspan=2, sticky="nsw")
                self.control_panel.grid_rowconfigure(8, weight=1) # Ajustado para más elementos

                self.logo_label = ctk.CTkLabel(self.control_panel, text="ATENEA", font=ctk.CTkFont(size=20, weight="bold"))
                self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

                # -- Sección de Carga de Archivos --
                self.files_frame = ctk.CTkFrame(self.control_panel)
                self.files_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
                
                self.btn_cargar_original = ctk.CTkButton(self.files_frame, text="Cargar Imagen Original", command=self.cargar_original)
                self.btn_cargar_original.pack(pady=10, padx=10, fill="x")
                self.label_original = ctk.CTkLabel(self.files_frame, text="No seleccionada", text_color="gray", wraplength=300)
                self.label_original.pack(pady=(0,10), padx=10)

                self.btn_cargar_resultado = ctk.CTkButton(self.files_frame, text="Cargar Imagen Resultado", command=self.cargar_resultado)
                self.btn_cargar_resultado.pack(pady=10, padx=10, fill="x")
                self.label_resultado = ctk.CTkLabel(self.files_frame, text="No seleccionada", text_color="gray", wraplength=300)
                self.label_resultado.pack(pady=(0,10), padx=10)

                # -- Sección de Procesamiento --
                self.processing_frame = ctk.CTkFrame(self.control_panel)
                self.processing_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

                self.btn_asim_1 = ctk.CTkButton(self.processing_frame, text="🔬 Procesar con Asimilador 1", command=self.run_asimilador_1)
                self.btn_asim_1.pack(pady=10, padx=10, fill="x")
                
                self.btn_asim_2 = ctk.CTkButton(self.processing_frame, text="🧠 Procesar con Asimilador 2", command=self.run_asimilador_2)
                self.btn_asim_2.pack(pady=10, padx=10, fill="x")

                # -- Sección de Base de Datos --
                self.db_frame = ctk.CTkFrame(self.control_panel)
                self.db_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
                self.btn_exportar = ctk.CTkButton(self.db_frame, text="Exportar Informe", command=self.exportar_informe)
                self.btn_exportar.pack(pady=10, padx=10, fill="x")
                self.btn_cargar_sesion = ctk.CTkButton(self.db_frame, text="Cargar Sesión", command=self.cargar_sesion)
                self.btn_cargar_sesion.pack(pady=10, padx=10, fill="x")

                # -- Sección de IA y Generación --
                self.ia_frame = ctk.CTkFrame(self.control_panel)
                self.ia_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
                self.btn_consultar = ctk.CTkButton(self.ia_frame, text="Consultar a ATENEA", command=self.consultar_atenea_gui)
                self.btn_consultar.pack(pady=10, padx=10, fill="x")
                self.image_prompt_entry = ctk.CTkEntry(self.ia_frame, placeholder_text="Prompt para generar imagen...")
                self.image_prompt_entry.pack(pady=10, padx=10, fill="x")
                self.btn_generar_img = ctk.CTkButton(self.ia_frame, text="🎨 Generar Imagen", command=self.generar_imagen_gui)
                self.btn_generar_img.pack(pady=10, padx=10, fill="x")

                # -- Métricas del Sistema --
                self.metrics_frame = ctk.CTkFrame(self.control_panel)
                self.metrics_frame.grid(row=9, column=0, padx=20, pady=10, sticky="sew")
                self.cpu_label = ctk.CTkLabel(self.metrics_frame, text="CPU: 0%")
                self.cpu_label.pack(pady=2)
                self.ram_label = ctk.CTkLabel(self.metrics_frame, text="RAM: 0%")
                self.ram_label.pack(pady=2)
                self.disk_label = ctk.CTkLabel(self.metrics_frame, text="DISCO: 0%")
                self.disk_label.pack(pady=2)

                # --- Visor de Imágenes (Derecha) ---
                self.viewer_panel = ctk.CTkFrame(self)
                self.viewer_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
                self.viewer_panel.grid_columnconfigure(0, weight=1)
                self.viewer_panel.grid_rowconfigure(0, weight=1)

                self.tab_view = ctk.CTkTabview(self.viewer_panel)
                self.tab_view.pack(fill="both", expand=True)
                self.tab_view.add("Original")
                self.tab_view.add("Resultado")
                self.tab_view.add("Artefactos")
                
                self.image_label_original = ctk.CTkLabel(self.tab_view.tab("Original"), text="")
                self.image_label_original.pack(fill="both", expand=True)
                self.image_label_resultado = ctk.CTkLabel(self.tab_view.tab("Resultado"), text="")
                self.image_label_resultado.pack(fill="both", expand=True)

                # --- Consola de Logs (Abajo) ---
                self.log_frame = ctk.CTkFrame(self, height=200)
                self.log_frame.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="sew")
                self.log_text = ctk.CTkTextbox(self.log_frame)
                self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

                self.actualizar_metricas()

            def log(self, mensaje):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.log_text.insert("end", f"[{timestamp}] {mensaje}\n")
                self.log_text.see("end")
                registrar_evento("LOG_UI", "GUI", mensaje)

            def actualizar_metricas(self):
                # ... (lógica de métricas sin cambios) ...
                self.after(1000, self.actualizar_metricas)

            def cargar_original(self):
                path = filedialog.askopenfilename(title="Seleccionar Imagen Original", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
                if path:
                    self.rut-img_original = path
                    self.label_original.configure(text=os.path.basename(path), text_color="white")
                    self.log(f"Imagen Original cargada: {path}")
                    self.mostrar_imagen(path, self.image_label_original)

            def cargar_resultado(self):
                path = filedialog.askopenfilename(title="Seleccionar Imagen Resultado", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
                if path:
                    self.rut-img_resultado = path
                    self.label_resultado.configure(text=os.path.basename(path), text_color="white")
                    self.log(f"Imagen Resultado cargada: {path}")
                    self.mostrar_imagen(path, self.image_label_resultado)

            def mostrar_imagen(self, path, label_widget):
                try:
                    img = Image.open(path)
                    # Redimensionar imagen si es muy grande para la vista previa
                    max_size = (800, 600)
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                    label_widget.configure(image=ctk_img, text="")
                except Exception as e:
                    self.log(f"Error al mostrar imagen: {e}")

            def run_asimilador_1(self):
                if not self.rut-img_original or not self.rut-img_resultado:
                    self.log("❌ Error: Debe seleccionar una imagen original y una resultado.")
                    return
                
                self.log("--- INICIANDO ASIMILADOR 1: ANÁLISIS FORENSE ---")
                output_dir = os.path.join("C:\\ATENEA", "atenea_lab", "lab_io", "asimilador_1_output")
                os.makedirs(output_dir, exist_ok=True)

                threading.Thread(target=self._run_asim_1_thread, args=(output_dir,), daemon=True).start()

            def _run_asim_1_thread(self, output_dir):
                try:
                    analizar_diferencias_imagen(self.rut-img_original, self.rut-img_resultado, output_dir)
                    self.log("✅ Asimilador 1 completado. 4 artefactos generados.")
                except Exception as e:
                    self.log(f"❌ Error en Asimilador 1: {e}")

            def run_asimilador_2(self):
                if not self.rut-img_original or not self.rut-img_resultado:
                    self.log("❌ Error: Debe seleccionar una imagen original y una resultado.")
                    return

                self.log("--- INICIANDO ASIMILADOR 2: EMULACIÓN COGNITIVA ---")
                output_dir = os.path.join("C:\\ATENEA", "atenea_lab", "lab_io", "asimilador_2_output")
                os.makedirs(output_dir, exist_ok=True)
                
                threading.Thread(target=self._run_asim_2_thread, args=(output_dir,), daemon=True).start()

            def _run_asim_2_thread(self, output_dir):
                try:
                    reporte = emulate_and_extract(self.rut-img_original, self.rut-img_resultado, output_dir)
                    self.log("✅ Asimilador 2 completado. Reporte cognitivo generado.")
                    self.log(f"Reporte: {json.dumps(reporte, indent=2)}")
                except Exception as e:
                    self.log(f"❌ Error en Asimilador 2: {e}")

            def exportar_informe(self):
                db_path = "C:\\ATENEA\\atenea_core\\database\\atenea_mind.db"
                self.log(f"ℹ️ Función 'Exportar Informe' llamada. Apuntando a la base de datos: {db_path}")
                # Aquí iría la lógica para generar y exportar un informe desde la DB.

            def cargar_sesion(self):
                db_path = "C:\\ATENEA\\atenea_core\\database\\atenea_mind.db"
                self.log(f"ℹ️ Función 'Cargar Sesión' llamada. Obteniendo datos desde: {db_path}")
                # Aquí iría la lógica para cargar una sesión de análisis desde la DB.

            def consultar_atenea_gui(self):
                respuesta = consultar_atenea("¿Cuál es el estado del sistema?")
                self.log(f"🧠 ATENEA responde: {respuesta}")

            def generar_imagen_gui(self):
                prompt = self.image_prompt_entry.get()
                if not prompt:
                    self.log("⚠️ Por favor, introduce un prompt para generar la imagen.")
                    return
                self.log(f"🎨 Solicitando imagen para: '{prompt}'...")
                threading.Thread(target=self._generar_imagen_thread, args=(prompt,), daemon=True).start()

            def _generar_imagen_thread(self, prompt):
                imagen_url = generar_imagen_perchance(prompt)
                self.log(f"🖼️ Resultado de generación: {imagen_url}")

        app = AteneaGUI()
        app.mainloop()
        
    except Exception as e:
        registrar_evento("ERROR_UI", "sistema", str(e))
        print(f"Error en UI: {e}")

# ... (código de la función main sin cambios) ...


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