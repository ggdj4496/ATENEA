from telethon import TelegramClient, events
import caja_fuerte as cf
import atenea_core as core
import sys

# Inicializamos el log de arranque
core.registrar_arranque()

# Creamos el cliente de Telegram
try:
    client = TelegramClient('atenea_session', cf.API_ID, cf.API_HASH).start(bot_token=cf.BOT_TOKEN)
except Exception as e:
    core.logger.error(f"Error crítico al iniciar Telegram: {e}")
    sys.exit(1)

@client.on(events.NewMessage)
async def handler(event):
    # Monitorizamos quién escribe
    user_msg = event.raw_text
    sender = await event.get_sender()
    sender_name = getattr(sender, 'first_name', 'Desconocido')
    
    core.logger.info(f"MENSAJE DE {sender_name} (ID: {event.sender_id}): {user_msg}")
    
    # Efecto "Escribiendo..."
    async with client.action(event.chat_id, 'typing'):
        respuesta = core.consultar_atenea(user_msg)
        await event.respond(respuesta)
        core.logger.info(f"RESPUESTA ENVIADA A {sender_name}")

if __name__ == "__main__":
    print(f"--- PUENTE {cf.AGENT_NAME} ACTIVADO ---")
    print("El log rotativo de 50MB está registrando la actividad...")
    client.run_until_disconnected()