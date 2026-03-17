def iniciar_consola(observer):
    """Inicia una consola interactiva para recibir comandos del usuario."""
    try:
        while True:
            comando = input("> ")
            if comando.lower() == 'exit':
                print("Desconectando Atenea...")
                break
            # Aquí se podrían procesar otros comandos en el futuro
            else:
                print(f"Comando desconocido: {comando}")
    finally:
        # Asegurarse de que el observer se detiene al salir de la consola
        if observer and observer.is_alive():
            observer.stop()
            observer.join()