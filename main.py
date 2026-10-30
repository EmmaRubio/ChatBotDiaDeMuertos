from chatbot import generar_respuesta
from config import NOMBRE_BOT, PALABRA_SALIDA

print(f"🤖 Bienvenido a {NOMBRE_BOT}")
print(f"Escribe '{PALABRA_SALIDA}' para terminar.\n")

while True:

    mensaje = input("Tú: ")

    if mensaje.lower() == PALABRA_SALIDA:
        print(f"{NOMBRE_BOT}: ¡Hasta luego!")
        break

    respuesta = generar_respuesta(mensaje)

    print(respuesta)