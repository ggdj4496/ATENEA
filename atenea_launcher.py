import os
import datetime
import numpy as np
from PIL import Image
from atenea_core.database_manager import registrar_evento

PATH_LAB = r"C:\ATENEA\atenea_lab\image_analisis"

def generar_pasos_intermedios(img_o, img_r, nombre_base):
    """Genera 3 estados intermedios del proceso de asimilación."""
    arr_o = np.array(img_o).astype(float)
    arr_r = np.array(img_r.resize(img_o.size)).astype(float)

    for i, paso in enumerate([0.25, 0.50, 0.75], 1):
        inter_arr = (1 - paso) * arr_o + paso * arr_r
        inter_img = Image.fromarray(inter_arr.astype(np.uint8))
        inter_img.save(os.path.join(PATH_LAB, f"{nombre_base}_paso_{i}.png"))

def iniciar_analisis_forense(ruta_original, ruta_resultado):
    if not os.path.exists(PATH_LAB): os.makedirs(PATH_LAB)

    nombre_base = os.path.splitext(os.path.basename(ruta_original))[0]
    
    # 1. Procesar y Renombrar
    with Image.open(ruta_original) as img_o, Image.open(ruta_resultado) as img_r:
        img_o.save(os.path.join(PATH_LAB, f"{nombre_base}_orig.png"))
        img_r.save(os.path.join(PATH_LAB, f"{nombre_base}_result.png"))
        
        # Generar las 3 claves visuales
        generar_pasos_intermedios(img_o, img_r, nombre_base)

        # 2. Análisis de Píxeles y Ruido
        diff = np.abs(np.array(img_o).astype(float) - np.array(img_r.resize(img_o.size)).astype(float))
        ruido_medio = np.mean(diff)
        
        # 3. Escritura del LOG de Asimilación
        log_path = os.path.join(PATH_LAB, "asimilando.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"ASIMILACIÓN: {nombre_base} | FECHA: {datetime.datetime.now()}\n")
            f.write(f"DATOS ORIG: {img_o.size} {img_o.mode}\n")
            f.write("-" * 20 + "\n")
            f.write(f"ANÁLISIS DE PROCESO: Ruido detectado {ruido_medio:.2f}\n")
            f.write(f"VECTOR DE CAMBIO: {'IA Difusión detectada' if ruido_medio > 40 else 'Filtro Algorítmico'}\n")
            f.write("+" * 20 + "\n\n")

    registrar_evento("LAB", nombre_base, "Imagen asimilada y despiezada en 3 pasos.")
    return f"Socio, {nombre_base} ha sido asimilada. Mira la carpeta image_analisis."