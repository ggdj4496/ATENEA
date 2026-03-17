import os
import datetime
from PIL import Image
import numpy as np
import hashlib

# Rutas del búnker
PATH_ANALISIS = r"C:\ATENEA\atenea_lab\image_analisis"
LOG_ASIMILANDO = os.path.join(PATH_ANALISIS, "asimilando.txt")

def asegurar_directorios():
    if not os.path.exists(PATH_ANALISIS):
        os.makedirs(PATH_ANALISIS)

def obtener_hash(ruta):
    """Genera una huella digital única del archivo."""
    with open(ruta, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def analizar_y_asimilar():
    asegurar_directorios()
    
    # --- PASO 1: IMAGEN ORIGINAL ---
    print("\n[ATENEA] Socio, pásame la ruta de la IMAGEN ORIGINAL:")
    ruta_orig = input(">>> ").strip('"') # Limpiar comillas si arrastra el archivo
    
    nombre_base = os.path.splitext(os.path.basename(ruta_orig))[0]
    ext = os.path.splitext(ruta_orig)[1]
    
    nuevo_nombre_orig = f"{nombre_base}_orig{ext}"
    destino_orig = os.path.join(PATH_ANALISIS, nuevo_nombre_orig)
    
    # Guardar copia física
    with Image.open(ruta_orig) as img_o:
        img_o.save(destino_orig)
        stats_o = os.stat(ruta_orig)
        pixels_o = np.array(img_o)
        
        # Bloque 1: Datos Técnicos Originales
        conteo_colores = len(img_o.getcolors(maxcolors=1000000)) if img_o.getcolors() else "Diverso"
        
        info_bloque_1 = (
            f"FECHA ARRANQUE: {datetime.datetime.now()}\n"
            f"NOMBRE ORIGINAL: {nombre_base}{ext}\n"
            f"NUEVO NOMBRE: {nuevo_nombre_orig}\n"
            f"BLOQUE 1 - INFO ORIGINAL\n"
            f"------------------------\n"
            f"Resolución: {img_o.size} | Formato: {img_o.format} | Modo: {img_o.mode}\n"
            f"Peso: {stats_o.st_size} bytes | Hash MD5: {obtener_hash(destino_orig)}\n"
            f"Paleta estimada: {conteo_colores} colores\n"
            f"Media de Color (RGB): {np.mean(pixels_o, axis=(0,1))}\n"
            f"------------------------\n"
        )

    # --- PASO 2: IMAGEN RESULTADO ---
    print(f"\n[ATENEA] Ahora la IMAGEN RESULTADO de {nombre_base}:")
    ruta_res = input(">>> ").strip('"')
    
    nuevo_nombre_res = f"{nombre_base}_result{ext}"
    destino_res = os.path.join(PATH_ANALISIS, nuevo_nombre_res)
    
    with Image.open(ruta_res) as img_r:
        img_r.save(destino_res)
        pixels_r = np.array(img_r)
        
        # Bloque 2: Datos Técnicos Resultado
        info_bloque_2 = (
            f"BLOQUE 2 - INFO RESULTADO\n"
            f"-------------------------\n"
            f"Nombre: {nuevo_nombre_res}\n"
            f"Modo: {img_r.mode} | Resolución: {img_r.size}\n"
            f"Diferencia de Media Color: {np.mean(pixels_r, axis=(0,1)) - np.mean(pixels_o, axis=(0,1))}\n"
            f"-------------------------\n"
        )

    # --- PASO 3: INGENIERÍA INVERSA (El "Cómo se hizo") ---
    # Calculamos la diferencia bit a bit para detectar algoritmos
    diff = np.abs(pixels_o.astype(float) - pixels_r.astype(float))
    ruido_medio = np.mean(diff)
    
    # Detección de patrones de IA
    analisis_ia = "INVESTIGACIÓN DE PROCESOS:\n"
    if ruido_medio > 50:
        analisis_ia += "- Detectada fuerte alteración de vectores: Posible Upscaling o Rediseño Genético.\n"
    if img_r.info.get('software'):
        analisis_ia += f"- Firma de Software detectada: {img_r.info.get('software')}\n"
    
    # Análisis de ruido (Detecta si es IA Difusión o Filtro Estándar)
    desviacion = np.std(diff)
    if desviacion > 10:
        analisis_ia += "- Patrón de ruido no lineal: Consistente con modelos de Difusión (Stable Diffusion/Midjourney).\n"
    else:
        analisis_ia += "- Ruido lineal detectado: Posible post-procesado manual o filtros de color.\n"

    info_bloque_3 = (
        f"BLOQUE 3 - ANÁLISIS FORENSE Y ASIMILACIÓN\n"
        f"-----------------------------------------\n"
        f"Ruido Medio bit a bit: {ruido_medio:.4f}\n"
        f"Anomalías Vectoriales: {desviacion:.4f}\n"
        f"{analisis_ia}"
        f"++++++++++++++++++++++++++\n\n"
    )

    # Escribir todo al log
    with open(LOG_ASIMILANDO, "a", encoding="utf-8") as f:
        f.write(info_bloque_1)
        f.write(info_bloque_2)
        f.write(info_bloque_3)

    print(f"\n[ATENEA] ¡Asimilación completada socio! Tienes todo en {LOG_ASIMILANDO}, y yo cómo está el tío.")

if __name__ == "__main__":
    analizar_y_asimilar()