from config import NOMBRE_BOT
from respuestas import RESPUESTAS

import unicodedata

# Configuración del bot
NOMBRE_BOT = "pirataDeCuliacanBot"

# Diccionario ampliado de sinónimos
SINONIMOS = {
    "altar": "ofrenda",
    "panteon": "tumba",
    "cementerio": "tumba",
    "calaca": "catrina",
    "huesos": "pan",
    "panecito": "pan",
    "perrito": "mascotas",
    "gatito": "mascotas",
    "animales": "mascotas",
    "origen": "historia",
    "tradicion": "historia",
    "mexico": "regiones",
    "oaxaca": "regiones",
    "michoacan": "regiones",
    "rimas": "calaveritas",
    "poema": "calaveritas",
    "halloween": "comparacion",
    "canciones": "musica",
    "cancion": "musica",
    "sones": "musica",
    "melodias": "musica",
    "recomiendas": "musica",
    "recomendar": "musica"
}

# Intenciones principales y sus palabras clave (¡Quitamos "cuales" de aquí para que sea seguimiento!)
INTENCIONES = {
    "historia": [
        "dia de muertos", "origen", "historia", "celebra", "noviembre", 
        "de donde viene", "antiguo", "aztecas", "prehispanico"
    ],
    "ofrenda": [
        "ofrenda", "altar", "vela", "flores", "cempasuchil", "agua", "sal", 
        "copal", "papel picado", "comida", "elementos"
    ],
    "catrina": [
        "catrina", "calaca", "garbancera", "jose guadalupe posada", "diego rivera"
    ],
    "pan": [
        "pan", "pan de muerto", "huesitos", "azucar", "ajonjoli"
    ],
    "mascotas": [
        "mascota", "perro", "gato", "animales", "perritos", "gatitos", "fallecio"
    ],
    "sincretismo": [
        "espanoles", "catolicos", "religion", "conquista", "mezcla", "espana"
    ],
    "regiones": [
        "estado", "michoacan", "janitzio", "oaxaca", "xochimilco", "mixquic"
    ],
    "calaveritas": [
        "calaverita", "rimas", "verso", "poema", "inventar", "chusca"
    ],
    "comparacion": [
        "halloween", "gringo", "diferencia", "es lo mismo", "disfraces"
    ],
    "filosofia": [
        "por que se burlan", "miedo a la muerte", "triste", "tabu", "alegria"
    ],
    "musica": [
        "musica", "cancion", "canciones", "cantar", "sones", "corridos", "banda", 
        "coco", "melodias", "recomiendas", "recomendar"
    ]
}

# Base de datos estructurada por niveles (Respuesta inicial + Detalles de seguimiento)
CONTENIDO = {
    "historia": {
        "principal": (
            "El Día de Muertos es una de las tradiciones más chidas de México bro. "
            "No es una fiesta triste, sino una celebración colorida donde recordamos y honramos "
            "a los seres queridos que ya se fueron."
        ),
        "seguimiento": [
            "Para profundizar: combina la visión de los pueblos mesoamericanos (que veían la muerte como una etapa del ciclo) con la influencia católica traída por los españoles.",
            "¿Sabías que antes se celebraba en agosto durante todo un mes? Con la llegada de España se movió a noviembre para coincidir con el calendario católico."
        ]
    },
    "ofrenda": {
        "principal": (
            "Una ofrenda o altar es una guía llena de simbolismo para honrar a quienes se adelantaron bro."
        ),
        "seguimiento": [
            "Cada nivel del altar tiene sentido: el piso representa la tierra, el medio el purgatorio y el cielo arriba. Además, se pone un vaso con agua para calmar la sed de las ánimas tras su largo viaje.",
            "También se incluye sal para purificar el espíritu y un caminito de pétalos de cempasúchil para que no se pierdan rumbo a casa."
        ]
    },
    "catrina": {
        "principal": (
            "La famosa 'Calavera Garbancera' fue creada por José Guadalupe Posada bro "
            "a principios del siglo XX como una crítica satírica a los mexicanos que querían aparentar ser europeos."
        ),
        "seguimiento": [
            "Posada la dibujó sin ropa para mostrar que, al final, ricos o pobres, todos calzamos igual ante la muerte.",
            "Años después, Diego Rivera la inmortalizó con su sombrero elegante y estola de plumas en su mural 'Sueño de una tarde dominical en la Alameda Central', bautizándola oficialmente como 'La Catrina'."
        ]
    },
    "pan": {
        "principal": (
            "El pan de muerto es delicioso y cada parte tiene un significado especial: "
            "la bolita de arriba representa el cráneo y las tiras simulan los huesos."
        ),
        "seguimiento": [
            "Las cuatro tiras de los huesos también representan los cuatro puntos cardinales consagrados a los dioses prehispánicos (como Tezcatlipoca o Tláloc).",
            "El toque de azúcar roja o ajonjolí simboliza las lágrimas derramadas por los que ya no están."
        ]
    },
    "mascotas": {
        "principal": (
            "¡Claro que se les pone ofrenda bro! Los animalitos también se merecen su espacio especial "
            "el 27 de octubre para recordar el amor incondicional que nos dieron."
        ),
        "seguimiento": [
            "Puedes colocarles sus croquetas favoritas, agua fresca, un juguetito que les encantaba y una veladora pequeña.",
            "Se cree que los perritos son nuestros fieles guías para cruzar al Mictlán, por lo que honrarlos es una hermosa forma de agradecerles."
        ]
    },
    "sincretismo": {
        "principal": (
            "Es una mezcla fascinante de culturas (sincretismo). Los pueblos indígenas ya tenían rituales "
            "dedicados a sus muertos y los españoles trajeron el calendario católico de Fieles Difuntos."
        ),
        "seguimiento": [
            "Fechas como el 1 y 2 de noviembre fueron establecidas por la Iglesia Católica para unirse con las celebraciones prehispánicas que ya existían en esas épocas de cosecha.",
            "Esta fusión hizo que la muerte se viera con una mezcla de respeto sagrado y fiesta popular."
        ]
    },
    "regiones": {
        "principal": (
            "Aunque todo México lo celebra, cada estado tiene su magia única. "
            "Por ejemplo, Janitzio en Michoacán o Mixquic en la CDMX viven la tradición de forma impresionante."
        ),
        "seguimiento": [
            "En Janitzio, la gente hace procesiones nocturnas en lanchas iluminadas con miles de velas hacia el panteón de la isla.",
            "En Oaxaca se arman comparsas con música de banda y disfraces increíbles que duran toda la madrugada."
        ]
    },
    "calaveritas": {
        "principal": (
            "Las calaveritas literarias son rimas irónicas y divertidas donde personificamos a la Muerte "
            "llevándose a alguien de forma chusca."
        ),
        "seguimiento": [
            "Ejemplo:\n*La huesuda andaba buscando por toda la secundaria,\n a ver quién debía tareas en la clase de matemáticas.*\n",
            "¿Quieres que inventemos una personalizada para algún amigo o maestro?"
        ]
    },
    "comparacion": {
        "principal": (
            "No son lo mismo. Halloween (31 de octubre) tiene raíces celtas enfocadas en disfraces para espantar monstruos. "
            "El Día de Muertos (1 y 2 de noviembre) es una tradición mexicana de memoria y altares."
        ),
        "seguimiento": [
            "Mientras Halloween busca asustar y pedir dulces con un toque de misterio, el Día de Muertos busca acoger con alegría y respeto a las almas de nuestros seres queridos.",
            "Ambas fechas conviven cerca en el calendario, pero su significado cultural es completamente distinto."
        ]
    },
    "filosofia": {
        "principal": (
            "En México no nos burlamos de la muerte por falta de respeto, sino como una forma de perderle el miedo "
            "y aceptarla como parte natural de la existencia."
        ),
        "seguimiento": [
            "Las calaveritas de azúcar o el pan con forma de huesos nos recuerdan que, tarde o temprano, todos terminaremos igual, así que lo mejor es vivir con alegría.",
            "Es una forma de vencer al olvido: mientras recuerdes a alguien con amor, esa persona sigue viva en tu memoria."
        ]
    },
    "musica": {
        "principal": (
            "La música del Día de Muertos simboliza la conexión entre vivos y difuntos, mezclando raíces indígenas "
            "y católicas para honrar y celebrar el tránsito al más allá. Las canciones más representativas "
            "no son solo las de Coco; México es tan diverso que vale la pena explorar nuestra propia riqueza musical."
        ),
        "seguimiento": [
            "Te recomiendo escuchar: *La Martiniana* (un son istmeño precioso), *Canción Mixteca*, el himno fúnebre tradicional *Dios Nunca Muere*, y *La Bruja* con su toque jarochísimo.",
            "También están clásicos modernos y populares como *Amor Eterno* de Juan Gabriel o *Las Golondrinas*, ideales para recordar a los que ya se fueron con muchísimo sentimiento."
        ]
    }
}

# Variables de control de estado de la sesión
ULTIMA_INTENCION = None
INDICE_SEGUIMIENTO = 0

def limpiar_texto(texto):
    """Convierte el texto a minúsculas, elimina espacios extra y acentos."""
    texto = texto.lower().strip()
    return ''.join(
        caracter for caracter in unicodedata.normalize('NFD', texto)
        if unicodedata.category(caracter) != 'Mn'
    )

def detectar_intencion(mensaje):
    """Identifica la intención del usuario aplicando sinónimos y palabras clave."""
    for sinomimo, objetivo in SINONIMOS.items():
        if sinomimo in mensaje:
            mensaje = mensaje.replace(sinomimo, objetivo)

    for intencion, palabras in INTENCIONES.items():
        for palabra in palabras:
            if palabra in mensaje:
                return intencion
    return None

def es_frase_seguimiento(mensaje):
    """Detecta frases cortas de continuidad conversacional (incluyendo 'cuales', 'como', etc.)."""
    frases_seguimiento = [
        "y que", "que mas", "cuentame mas", "explicame mas", "y luego", 
        "por que", "como", "detalle", "mas", "a ver", "platicame", 
        "cual", "cuales", "y eso", "eso que es", "y que mas", "y despues",
        "recomienda", "recomiendas"
    ]
    return any(f in mensaje for f in frases_seguimiento)

def generar_respuesta(mensaje):
    """Procesa el mensaje priorizando nuevas intenciones reales antes de evaluar el seguimiento."""
    global ULTIMA_INTENCION, INDICE_SEGUIMIENTO
    
    mensaje_limpio = limpiar_texto(mensaje)
    
    # 1. Verificamos si es una frase de seguimiento Y hay una intención activa
    # (Esto se evalúa ANTES para que palabras como "cuales" o "recomiendas" avancen en el tema actual)
    if es_frase_seguimiento(mensaje_limpio) and ULTIMA_INTENCION:
        datos_intencion = CONTENIDO[ULTIMA_INTENCION]
        lista_seguimiento = datos_intencion["seguimiento"]
        
        if INDICE_SEGUIMIENTO < len(lista_seguimiento):
            respuesta = lista_seguimiento[INDICE_SEGUIMIENTO]
            INDICE_SEGUIMIENTO += 1
            return f"{NOMBRE_BOT}: {respuesta}"
        else:
            return f"{NOMBRE_BOT}: ¡Ya te conté todo lo principal sobre este tema! ¿Quieres que hablemos de otra cosa como la música, el pan de muerto, las catrinas o las mascotas?"

    # 2. Si no es seguimiento, comprobamos si introduce un TEMA NUEVO completamente distinto
    nueva_intencion = detectar_intencion(mensaje_limpio)
    
    if nueva_intencion:
        ULTIMA_INTENCION = nueva_intencion
        INDICE_SEGUIMIENTO = 0  # Reiniciar el índice de seguimiento para el nuevo tema
        return f"{NOMBRE_BOT}: {CONTENIDO[nueva_intencion]['principal']}"

    # 3. Si no entra en ninguna categoría
    return (
        f"{NOMBRE_BOT}: ¡Mmm, esa pregunta está interesante pero no la capté bien! "
        "Prueba preguntándome sobre la música, la ofrenda, la historia, el pan de muerto, las mascotas o las catrinas."
    )

# --- Bloque principal para ejecución en consola ---
if __name__ == "__main__":
    print(f"🤖 Bienvenido a {NOMBRE_BOT}")
    print("Escribe 'salir' para terminar.\n")
    
    while True:
        entrada_usuario = input("Tú: ")
        if entrada_usuario.lower() in ["salir", "exit", "adios"]:
            print(f"{NOMBRE_BOT}: ¡Nos vemos! Que disfrutes mucho el Día de Muertos.")
            break
        
        respuesta_bot = generar_respuesta(entrada_usuario)
        print(f"\n{respuesta_bot}\n")