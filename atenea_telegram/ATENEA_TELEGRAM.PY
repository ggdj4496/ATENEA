from telethon import Button

async def mostrar_menu_principal(event):
    botones = [
        [Button.inline("🤖 Modelos IA Gratuitos", b"modelos")],
        [Button.inline("🧬 Asimilado de Funciones", b"menu_asimilado")],
        [Button.inline("📸 Análisis Orig/Result", b"analisis_lab")],
        [Button.inline("🎨 Perchance (No Filter)", b"perchance")]
    ]
    await event.respond("📊 **MENÚ DE CONTROL ATENEA**", buttons=botones)

# Lógica para la carpeta dinámica de investigación
def preparar_investigacion_bot(nombre_bot):
    path_bot = os.path.join(r"C:\ATENEA\atenea_lab\bots_investigados", nombre_bot)
    if not os.path.exists(path_bot):
        os.makedirs(path_bot)
        # Creamos el TXT que irá creciendo
        with open(os.path.join(path_bot, "extraccion_adn.txt"), "w") as f:
            f.write(f"INVESTIGACIÓN INICIADA: {nombre_bot}\n{'='*30}\n")
    return path_bot