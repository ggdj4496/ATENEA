
import time
from atenea_core.database_manager import registrar_evento

def iniciar_bot():
    """
    Inicializa y mantiene en funcionamiento el bot de Telegram.
    Esta función contendrá el bucle principal del cliente Telethon,
    escuchando y respondiendo a los mensajes de los usuarios.
    """
    registrar_evento("HILO TELEGRAM", "atenea_telegram/bot.py", "Cliente de Telegram iniciado y en escucha.")
    print("ATENEA :: Hilo de Telegram... [ONLINE]")
    
    # Bucle simulado para mantener el bot 'vivo'
    try:
        while True:
            # Aquí iría la lógica de escucha de Telethon (client.run_until_disconnected())
            time.sleep(5)
            print("Bot de Telegram: Ciclo de escucha completado.")
    except KeyboardInterrupt:
        print("Bot de Telegram: Desconectando...")