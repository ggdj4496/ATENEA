# ATENEA - Módulo de Telegram
# Este archivo contendrá toda la lógica de interacción con la API de Telegram usando Telethon.

import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
from atenea_core_logic import registrar_estructura_bot
from asimilador_1.analyzer import analizar_diferencias_imagen
from asimilador_2.cognitive_emulator import emulate_and_extract
import subprocess

load_dotenv()

API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

# Cliente de Telethon
client = TelegramClient('atenea_bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- Decorador de Blindaje de Administrador ---
def admin_only(func):
    async def wrapper(event):
        if event.sender_id == ADMIN_ID:
            await func(event)
        else:
            print(f"[Acceso Denegado] Intento de uso por usuario no autorizado: {event.sender_id}")
    return wrapper

# --- Manejador de Mapeo de Estructuras ---
@client.on(events.NewMessage(func=lambda e: e.is_private and e.forward))
@admin_only
async def mapear_botones_enemigos(event):
    if event.message.buttons:
        bot_origen = event.message.forward.from_name
        await event.respond(f"**[ATENEA]** Estructura de `{bot_origen}` detectada. Asimilando botones...")
        for row in event.message.buttons:
            for button in row:
                texto = button.text
                datos_callback = button.data.decode('utf-8')
                if registrar_estructura_bot(bot_origen, texto, datos_callback):
                    print(f"[Asimilador] Botón '{texto}' de '{bot_origen}' mapeado.")
        await event.respond("**[ATENEA]** Mapeo completado. La estructura ha sido guardada en `atenea_mind.db`.")

# --- Manejador de Ejecución Directa ---
@client.on(events.CallbackQuery)
@admin_only
async def ejecutar_analisis_local(event):
    await event.answer("⚙️ Procesamiento local activado...")
    mensaje_original = await event.get_message()
    if mensaje_original and mensaje_original.photo:
        await event.edit("**[ATENEA]** 📥 Imagen recibida. Analizando estructura...")
        ruta_descarga = await client.download_media(mensaje_original.photo, file="asimilador_input/")
        
        # Llamada REAL al Asimilador 1
        await event.edit("**[ATENEA]** ⚙️ Procesamiento local activado (Asimilador 1: Análisis Forense)...", buttons=None)
        
        # Definimos las rutas de salida
        output_dir = "C:\\ATENEA\\atenea_lab\\lab_io\\telegram_output"
        os.makedirs(output_dir, exist_ok=True)

        # Ejecutamos el análisis (usando la misma imagen como original y resultado para la prueba)
        analizar_diferencias_imagen(ruta_descarga, ruta_descarga, output_dir)

        # Por ahora, simplemente reenviamos la imagen original como resultado.
        # En un futuro, aquí se enviaría la imagen procesada o un informe.
        await client.send_file(event.chat_id, ruta_descarga, caption="**[ATENEA]** ✅ Análisis Forense completado.")
        os.remove(ruta_descarga)