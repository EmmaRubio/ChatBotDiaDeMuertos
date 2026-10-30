from config import NOMBRE_BOT
from respuestas import RESPUESTAS

import unicodedata


def limpiar_texto(texto):
    """
    Convierte a minúsculas y elimina acentos.
    """

    texto = texto.lower()

    texto = ''.join(
        caracter
        for caracter in unicodedata.normalize('NFD', texto)
        if unicodedata.category(caracter) != 'Mn'
    )

    return texto

def generar_respuesta(mensaje):

    mensaje = limpiar_texto(mensaje)

    for sinonimo, palabra_real in SINONIMOS.items():

        if sinonimo in mensaje:
            mensaje = palabra_real

    for palabra_clave, respuesta in RESPUESTAS.items():

        if palabra_clave in mensaje:
            return f"{NOMBRE_BOT}: {respuesta}"

    return f"{NOMBRE_BOT}: Lo siento, todavía no tengo información sobre ese tema."

SINONIMOS = {
    "altar": "ofrenda",
    "calaca": "catrina",
    "pan": "pan de muerto"
}