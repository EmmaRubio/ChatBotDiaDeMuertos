import sys
 
from chatbot import Chatbot
from config import NOMBRE_BOT
 
 
def main():
    # Para que los emojis se vean bien en la consola (sobre todo en Windows)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
 
    bot = Chatbot()
    print(f"\n Te la bienvenida el {NOMBRE_BOT}  (escribe 'salir' para terminar)\n")
    print(f"{NOMBRE_BOT}: {bot.saludo_inicial()}\n")
 
    while not bot.terminado:
        try:
            entrada = input("Tú: ")
        except (EOFError, KeyboardInterrupt):  # Ctrl+D / Ctrl+C
            print(f"\n{NOMBRE_BOT}: ¡Nos vemos! ")
            break
        print(f"\n{NOMBRE_BOT}: {bot.responder(entrada)}\n")
 
 
if __name__ == "__main__":
    main()