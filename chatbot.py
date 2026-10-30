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

    intencion = detectar_intencion(mensaje)

    if intencion:
        return f"{NOMBRE_BOT}: {RESPUESTAS[intencion]}"

    return f"{NOMBRE_BOT}: No entendí tu pregunta. ¿Podrías explicarla de otra manera?"

SINONIMOS = {
    "altar": "ofrenda",
    "calaca": "catrina",
    "pan": "pan de muerto"
}

INTENCIONES = {
    "historia": [
        "dia de muertos",
        "origen",
        "historia",
        "celebra",
        "noviembre"
    ],

    "ofrenda": [
        "ofrenda",
        "altar",
        "vela",
        "flores",
        "cempasuchil"
    ],

    "catrina": [
        "catrina",
        "calaca"
    ],

    "pan": [
        "pan",
        "pan de muerto"
    ],

    "mascotas": [
        "mascota",
        "perro",
        "gato"
    ]
}

def detectar_intencion(mensaje):

    for intencion, palabras in INTENCIONES.items():

        for palabra in palabras:

            if palabra in mensaje:
                return intencion

    return None