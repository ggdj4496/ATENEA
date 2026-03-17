import os
import sys
from telethon import TelegramClient, events, Button
import asyncio
# Importamos tu database para registrar lo que pasa desde el móvil
import atenea_core.database_manager as db 

# --- CONFIGURACIÓN DE ACCESO ---
# Estos datos los sacas de tu archivo .env en atenea_security
API_ID = 'TU_API_ID' 
API_HASH = 'TU_API_HASH'
BOT_TOKEN = 'TU_BOT_TOKEN'

client = TelegramClient('atenea_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    # El saludo solo ocurre cuando hay sincronización real
    db.registrar_evento("TELEGRAM", "Sincronización", "Usuario inició mando a distancia")
    await event.respond(
        "🚀 **ATENEA ONLINE - KERNEL SYNC**\n\nSocio, el puente está activo. "
        "Tengo control sobre C:\\ATENEA y los módulos de asimilación.",
        buttons=[
            [Button.inline("🧬 Asimilar Bot", b"asimilar"), Button.inline("📸 Análisis O/R", b"analisis")],
            [Button.inline("🖥️ Estado PC", b"status"), Button.inline("🎨 Perchance Pro", b"perchance")]
        ]
    )

@client.on(events.CallbackQuery)
async def callback_handler(event):
    if event.data == b"status":
        # Comando de Windows enviado desde Telegram
        memoria = os.popen('systeminfo | findstr /C:"Total Physical Memory"').read()
        await event.answer(f"PC Status:\n{memoria}", alert=True)

@client.on(events.NewMessage)
async def general_handler(event):
    if event.is_private:
        # Aquí es donde Atenea usa su IA para responderte
        # core.procesar_con_ia(event.text)
        pass

if __name__ == "__main__":
    print(">>> [BRIDGE] Mando a distancia de Telegram activo...")
    client.run_until_disconnected()