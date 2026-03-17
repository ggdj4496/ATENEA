import exifread
from skimage import measure
import numpy as np
from PIL import Image

def analizar_diferencias_imagen(ruta_original, ruta_resultado, dir_salida):
    tags_original = analisis_forense_avanzado(ruta_original)
    tags_resultado = analisis_forense_avanzado(ruta_resultado)

    print("--- METADATOS IMAGEN ORIGINAL ---")
    for tag in tags_original.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail'): # Excluir miniaturas
            print(f"Key: {tag}, value: {tags_original[tag]}")

    print("--- METADATOS IMAGEN RESULTADO ---")
    for tag in tags_resultado.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):
            print(f"Key: {tag}, value: {tags_resultado[tag]}")

    entropia_original = calcular_entropia(ruta_original)
    entropia_resultado = calcular_entropia(ruta_resultado)

    print("--- ANÁLISIS DE ENTROPÍA ---")
    print(f"Entropía Imagen Original: {entropia_original:.4f}")
    print(f"Entropía Imagen Resultado: {entropia_resultado:.4f}")
    print(f"Diferencia de Entropía: {abs(entropia_original - entropia_resultado):.4f}")

def analisis_forense_avanzado(ruta_imagen):
    with open(ruta_imagen, 'rb') as f:
        tags = exifread.process_file(f)
        return tags

def calcular_entropia(ruta_imagen):
    img = Image.open(ruta_imagen).convert('L') # Convertir a escala de grises
    img_array = np.array(img)
    entropia = measure.shannon_entropy(img_array)
    return entropia