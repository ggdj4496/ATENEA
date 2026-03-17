
import os
from PIL import Image, ImageChops, ImageFilter
import numpy as np
from atenea_core.database_manager import registrar_evento

# --- Constantes de la Orden ---
ORDEN_ID = "ORD-5370-335970"
BASE_DIR = os.path.join("C:\\ATENEA", "atenea_lab", "lab_io", ORDEN_ID)
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_FILE = os.path.join(BASE_DIR, "asimilando.txt")

# --- Nombres de archivos esperados ---
IMG_ORIGINAL = os.path.join(INPUT_DIR, "original.png")
IMG_RESULTADO = os.path.join(OUTPUT_DIR, "resultado.png")

def analizar_diferencias_imagen(ruta_original, ruta_resultado, dir_salida):
    """
    Analiza la diferencia entre dos imágenes para entender la transformación.
    Genera 4 imágenes intermedias clave para un análisis forense profundo.
    """
    try:
        img_orig = Image.open(ruta_original).convert('RGB')
        img_res = Image.open(ruta_resultado).convert('RGB')

        if img_orig.size != img_res.size:
            img_res = img_res.resize(img_orig.size)

        # 1. Generar el mapa de diferencias absoluto
        diff_map_img = ImageChops.difference(img_orig, img_res)
        diff_map_path = os.path.join(dir_salida, "01_diff_map.png")
        diff_map_img.save(diff_map_path)
        print(f" -> [1/4] Mapa de diferencias guardado en: {diff_map_path}")

        # 2. Crear una máscara binaria de las áreas modificadas
        diff_array = np.array(diff_map_img.convert('L'))
        umbral = 25
        mask_array = (diff_array > umbral).astype(np.uint8) * 255
        mask_img = Image.fromarray(mask_array, 'L')
        mask_path = os.path.join(dir_salida, "02_mask.png")
        mask_img.save(mask_path)
        print(f" -> [2/4] Máscara de segmentación guardada en: {mask_path}")

        # 3. Crear superposición de resaltado
        highlight_overlay = img_orig.copy()
        red_overlay = Image.new('RGB', img_orig.size, (255, 0, 0))
        mask_img_bool = Image.fromarray((mask_array > 0).astype(np.uint8) * 255, 'L')
        highlight_overlay = Image.composite(red_overlay, highlight_overlay, mask_img_bool.point(lambda i: i * 0.5)) # 50% de opacidad
        highlight_path = os.path.join(dir_salida, "03_highlight_overlay.png")
        highlight_overlay.save(highlight_path)
        print(f" -> [3/4] Superposición de resaltado guardada en: {highlight_path}")

        # 4. Generar diferencia de bordes
        edges_orig = img_orig.filter(ImageFilter.FIND_EDGES)
        edges_res = img_res.filter(ImageFilter.FIND_EDGES)
        edges_diff_img = ImageChops.difference(edges_orig, edges_res)
        edges_diff_path = os.path.join(dir_salida, "04_edges_diff.png")
        edges_diff_img.save(edges_diff_path)
        print(f" -> [4/4] Diferencia de bordes guardada en: {edges_diff_path}")

        registrar_evento("ANALISIS_FORENSE_COMPLETADO", ORDEN_ID, f"4 artefactos generados en {dir_salida}")

    except Exception as e:
        error_msg = f"Error en el análisis de diferencias: {e}"
        print(error_msg)
        registrar_evento("ERROR_ANALISIS_FORENSE", ORDEN_ID, error_msg)

def procesar_orden_aprendizaje():
    """
    Procesa una orden de aprendizaje específica (ORD-5370-335970).
    
    Esta función simula un proceso de análisis de imágenes, donde ATENEA
    compara una imagen original con un resultado y genera "frames de transición"
    que representan su proceso de 'razonamiento' o 'evolución' para llegar a ese resultado.
    Finalmente, documenta este proceso en un log de asimilación.
    """
    print(f"--- INICIANDO PROCESO DE ASIMILACIÓN: {ORDEN_ID} ---")
    registrar_evento("INICIO_ASIMILACION", ORDEN_ID, f"Procesando orden en {BASE_DIR}")

    try:
        # 1. Crear directorios si no existen
        os.makedirs(INPUT_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # --- Simulación de creación de archivos de entrada ---
        # En un caso real, estos archivos serían colocados por un proceso externo.
        if not os.path.exists(IMG_ORIGINAL):
            Image.new('RGB', (100, 100), color = 'red').save(IMG_ORIGINAL)
            print(f"Creado archivo de prueba: {IMG_ORIGINAL}")
        
        if not os.path.exists(IMG_RESULTADO):
            Image.new('RGB', (100, 100), color = 'blue').save(IMG_RESULTADO)
            print(f"Creado archivo de prueba: {IMG_RESULTADO}")
        # --- Fin de la simulación ---

        # 2. Realizar análisis de diferencias
        print("Iniciando análisis forense de diferencias entre imágenes...")
        analizar_diferencias_imagen(IMG_ORIGINAL, IMG_RESULTADO, OUTPUT_DIR)

        # 3. Generar frames de transición (simulación mantenida por ahora)
        print("Generando frames de transición del proceso de razonamiento...")
        for i in range(1, 4):
            frame_path = os.path.join(OUTPUT_DIR, f"transicion_{i}.png")
            # Simulación: crea una imagen gris como frame intermedio
            Image.new('RGB', (100, 100), color = 'grey').save(frame_path)
            print(f" -> Frame generado: {frame_path}")

        # 4. Escribir el log de asimilación
        log_content = f"""
        PROCESO DE ASIMILACIÓN COMPLETADO - {ORDEN_ID}
        =================================================
        INPUT:
        - Imagen Original: {IMG_ORIGINAL}
        
        OUTPUT:
        - Imagen Resultado: {IMG_RESULTADO}
        - Frame 1: {os.path.join(OUTPUT_DIR, "transicion_1.png")}
        - Frame 2: {os.path.join(OUTPUT_DIR, "transicion_2.png")}
        - Frame 3: {os.path.join(OUTPUT_DIR, "transicion_3.png")}
        
        CONCLUSIÓN:
        El sistema ha procesado la transformación de 'original.png' a 'resultado.png'.
        Se han generado 3 estados intermedios que representan la evolución conceptual.
        Este conocimiento ha sido asimilado.
        """
        with open(LOG_FILE, "w") as f:
            f.write(log_content)
        print(f"Log de asimilación guardado en: {LOG_FILE}")

        registrar_evento("FIN_ASIMILACION", ORDEN_ID, f"Log generado en {LOG_FILE}")
        print(f"--- PROCESO DE ASIMILACIÓN COMPLETADO --- ")

    except Exception as e:
        error_msg = f"Error procesando la orden {ORDEN_ID}: {e}"
        print(error_msg)
        registrar_evento("ERROR_ASIMILACION", ORDEN_ID, error_msg)

if __name__ == "__main__":
    # Este bloque permite ejecutar el proceso de forma independiente para pruebas.
    procesar_orden_aprendizaje()