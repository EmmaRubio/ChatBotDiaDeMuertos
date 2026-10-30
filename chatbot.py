import random
import re
import unicodedata
 
from config import (
    NOMBRE_BOT, PALABRAS_SALIDA, MAX_PALABRAS_SALIDA, LARGO_MINIMO_PREFIJO,
    MAX_PALABRAS_RESPUESTA_CORTA, MAX_LARGO_DESTINATARIO,
    LINEA_DE_LA_VIDA, EMERGENCIAS,
)

from respuestas import (
    SINONIMOS, CONTENIDO, SUBTEMAS,
    PLANTILLAS_CALAVERITA, DESTINATARIOS_NO_VALIDOS,
    CONVERSACION, SALUDO_INICIAL, DESPEDIDAS,
    AFIRMATIVAS, NEGATIVAS, RESPUESTAS_NEGATIVAS,
    FRASES_SEGUIMIENTO, NO_ENTENDI, VACIO,
    CRISIS, CASOS_DELICADOS,
)
 
 
def limpiar_texto(texto):
    """Minúsculas, sin acentos, sin signos (¿?¡!,.) y sin espacios repetidos."""
    texto = texto.lower().strip()
    # NFD separa la letra de su acento ("é" -> "e" + "´"); luego quitamos los acentos.
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    # Todo lo que no sea letra, número o espacio se vuelve espacio.
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    # Dejamos un solo espacio entre palabras.
    return " ".join(texto.split())
 
 
def aplicar_sinonimos(mensaje):
    """Cambia cada PALABRA COMPLETA por su sinónimo (si tiene uno)."""
    return " ".join(SINONIMOS.get(palabra, palabra) for palabra in mensaje.split())
 
 
def contiene(mensaje, palabra):
    """
    ¿Aparece 'palabra' en el mensaje como palabra completa?
    - Palabras cortas (menos de LARGO_MINIMO_PREFIJO letras): deben ser exactas.
      Así "pan" no se confunde con "es-pan-oles".
    - Palabras largas: basta que sea el INICIO de una palabra.
      Así "mascota" también encuentra "mascotas".
    """
    if len(palabra) >= LARGO_MINIMO_PREFIJO:
        return (" " + palabra) in (" " + mensaje)
    return (" " + palabra + " ") in (" " + mensaje + " ")
 
 
def contiene_alguna(mensaje, palabras):
    """True si el mensaje contiene al menos una de las palabras/frases."""
    return any(contiene(mensaje, p) for p in palabras)
 
 
def puntuar_temas(mensaje, solo=None):
    """
    Da puntos a cada tema según las palabras clave encontradas.
    Una frase de 3 palabras ("pan de muerto") vale 3 puntos: es más específica.
    Si 'solo' es una lista, únicamente puntúa esos temas.
    """
    puntos = {}
    for nombre, datos in CONTENIDO.items():
        if solo is not None and nombre not in solo:
            continue
        puntos[nombre] = sum(
            len(p.split()) for p in datos["palabras_clave"] if contiene(mensaje, p)
        )
    return puntos
 
 
def temas_ganadores(mensaje, solo=None):
    """Lista de temas con el puntaje más alto (más de uno = empate). Vacía si nadie suma."""
    puntos = puntuar_temas(mensaje, solo)
    if not puntos or max(puntos.values()) == 0:
        return []
    maximo = max(puntos.values())
    return [nombre for nombre, p in puntos.items() if p == maximo]
 
 
def _es_corto(mensaje):
    return len(mensaje.split()) <= MAX_PALABRAS_RESPUESTA_CORTA
 
 
def es_negativo(mensaje):
    """Respuesta corta tipo 'no', 'luego', 'así está bien'."""
    return _es_corto(mensaje) and contiene_alguna(mensaje, NEGATIVAS)
 
 
def es_afirmativo(mensaje):
    """Respuesta corta tipo 'sí', 'va', 'dale'."""
    return _es_corto(mensaje) and not es_negativo(mensaje) and contiene_alguna(mensaje, AFIRMATIVAS)
 
 
def es_frase_seguimiento(mensaje):
    """¿Pide continuar con el tema actual? ('cuéntame más', 'y qué más')."""
    return contiene_alguna(mensaje, FRASES_SEGUIMIENTO)
 
 
def extraer_destinatario(mensaje_original):
    """
    Busca "para ..." en el mensaje original (con acentos y mayúsculas) y devuelve
    a quién va dirigida la calaverita. Ejemplo:
      "una calaverita para mi profesor de matemáticas que deja tarea"
      -> "mi profesor de matemáticas"
    Devuelve None si no encuentra algo válido.
    """
    patron = re.compile(
        r"\bpara\s+(.+?)(?:\s+que\s|\s+porque\s|[,.?!;:]|$)", re.IGNORECASE
    )
    coincidencia = patron.search(mensaje_original)
    if not coincidencia:
        return None
    return _validar_destinatario(coincidencia.group(1))
 
 
def _validar_destinatario(texto):
    """Limpia y valida el texto; devuelve None si no sirve."""
    texto = texto.strip(" .,;:¿?¡!\"'")
    if len(texto) < 3 or len(texto) > MAX_LARGO_DESTINATARIO:
        return None
    if limpiar_texto(texto) in DESTINATARIOS_NO_VALIDOS:
        return None
    return texto
 
 
def unir_con_y(elementos):
    """['a', 'b', 'c'] -> 'a, b y c'."""
    if len(elementos) <= 1:
        return "".join(elementos)
    return ", ".join(elementos[:-1]) + " y " + elementos[-1]
 
 
class Chatbot:
    def __init__(self):
        self.ultima_intencion = None   # tema del que hablamos ahora
        self.indice_seguimiento = 0    # cuántos detalles ya dimos de ese tema
        self.temas_vistos = set()      # temas que ya tocamos (para no repetir sugerencias)
        self.esperando = None          # pregunta pendiente: {"tipo": ..., "datos": ...}
        self.ultima_sugerencia = None  # para no repetir la misma sugerencia seguida
        self.calaveritas_hechas = 0    # para variar las plantillas de calaverita
        self.terminado = False         # True cuando el usuario se despide
 
    def saludo_inicial(self):
        return SALUDO_INICIAL.format(nombre=NOMBRE_BOT)
 
    def responder(self, mensaje):
        """Recibe lo que escribió el usuario y devuelve el texto de respuesta."""
        limpio = limpiar_texto(mensaje)
        if not limpio:
            return VACIO
        procesado = aplicar_sinonimos(limpio)
 
        # 1. ¿Se despide?
        if len(limpio.split()) <= MAX_PALABRAS_SALIDA and contiene_alguna(limpio, PALABRAS_SALIDA):
            self.terminado = True
            return random.choice(DESPEDIDAS)
 
        # 2. ¿Hay una situación de riesgo? (prioridad máxima)
        if self._hay_crisis(limpio):
            self.esperando = None
            return CRISIS["respuesta"].format(linea=LINEA_DE_LA_VIDA, emergencias=EMERGENCIAS)
 
        # 3. ¿Está contestando una pregunta que el bot hizo antes?
        respuesta = self._resolver_pendiente(mensaje, limpio, procesado)
        if respuesta:
            return respuesta
 
        # 4. ¿Es un caso delicado (duelo)?
        respuesta = self._caso_delicado(procesado)
        if respuesta:
            return respuesta
 
        # 5. Temas, charla casual, seguimiento...
        return self._responder_tema(mensaje, limpio, procesado)
 
    def _hay_crisis(self, limpio):
        return (
            contiene_alguna(limpio, CRISIS["palabras_clave"])
            and not contiene_alguna(limpio, CRISIS["exclusiones"])
        )
 
    def _caso_delicado(self, procesado):
        for caso in CASOS_DELICADOS.values():
            # El mensaje debe tener al menos una palabra de CADA grupo
            if all(contiene_alguna(procesado, grupo) for grupo in caso["grupos"]):
                if caso["tema"]:
                    self.ultima_intencion = caso["tema"]
                    self.indice_seguimiento = 0
                    self.temas_vistos.add(caso["tema"])
                tipo, datos = caso["pendiente"]
                self.esperando = {"tipo": tipo, "datos": datos}
                return caso["respuesta"]
        return None

    def _resolver_pendiente(self, mensaje, limpio, procesado):
        if not self.esperando:
            return None
        pendiente = self.esperando
        self.esperando = None  # lo limpiamos; si hace falta, se vuelve a poner
        tipo, datos = pendiente["tipo"], pendiente["datos"]
 
        # El bot preguntó "¿para quién es la calaverita?"
        if tipo == "calaverita_destinatario":
            if es_negativo(limpio):
                return random.choice(RESPUESTAS_NEGATIVAS)
            if es_afirmativo(limpio):
                self.esperando = pendiente
                return "¡Va! ¿Para quién la hacemos? Por ejemplo: 'mi profe de mate' o 'mi amigo Luis'."
            if "?" in mensaje:  # parece una pregunta nueva, no un nombre
                return None
            destinatario = extraer_destinatario(mensaje) or _validar_destinatario(mensaje)
            return self._entregar_calaverita(destinatario) if destinatario else None
 
        # El bot preguntó "¿te refieres a A o a B?"
        if tipo == "aclarar":
            return self._resolver_aclaracion(datos, limpio, procesado)
 
        # Preguntas de sí/no
        if es_negativo(limpio):
            return random.choice(RESPUESTAS_NEGATIVAS)
        if es_afirmativo(limpio):
            if tipo == "tema":
                return self._dar_tema(datos)
            if tipo == "seguir":
                return self._dar_seguimiento()
            if tipo == "calaverita_otra":
                return self._entregar_calaverita(datos)
        return None  # no era respuesta a lo pendiente: seguimos el flujo normal
 
    def _resolver_aclaracion(self, candidatos, limpio, procesado):
        a, b = candidatos
        if contiene_alguna(limpio, ["los dos", "las dos", "ambos", "ambas"]):
            return self._dar_tema(a, siguiente=b)
        if contiene_alguna(limpio, ["primero", "primera", "1"]):
            return self._dar_tema(a)
        if contiene_alguna(limpio, ["segundo", "segunda", "2"]):
            return self._dar_tema(b)
        ganadores = temas_ganadores(procesado, solo=[a, b])
        if len(ganadores) == 1:
            return self._dar_tema(ganadores[0])
        return None
    
    def _responder_tema(self, mensaje, limpio, procesado):

        for palabra, respuesta in SUBTEMAS.items():
         if contiene(procesado, palabra):
            return respuesta

         if "volver a ver" in procesado and ("familiar" in procesado or "abuelita" in procesado or "persona" in procesado):
          return (
        "Esa es una pregunta que muchas personas se hacen. "
        "Las respuestas dependen de las creencias de cada quien. "
        "Algunas religiones creen en un reencuentro después de la muerte, "
        "mientras que la ciencia no puede confirmarlo. "
        "Lo que sí podemos hacer es mantener vivos los recuerdos de quienes amamos."
        )
        if "foto" in procesado and (
    "altar" in procesado
    or "ofrenda" in procesado
):
         return (
        "Tienes razón: una fotografía no hace regresar físicamente a una persona. "
        "Su función es recordarla, compartir historias sobre ella y mantener viva su memoria dentro de la familia."
    )

        ganadores = temas_ganadores(procesado)
 
        # Si solo dice "día de muertos" (sin nada más específico): pregunta general.
        if not ganadores and contiene(procesado, "dia de muertos"):
            ganadores = ["historia"]
 
        # EMPATE: si uno es el tema actual, gana por contexto; si no, preguntamos.
        if len(ganadores) > 1:
            if self.ultima_intencion in ganadores:
                ganadores = [self.ultima_intencion]
            else:
                return self._preguntar_aclaracion(ganadores[0], ganadores[1])
 
        nueva = ganadores[0] if ganadores else None
 
        # Calaveritas: si trae destinatario ("para mi profe"), la escribimos ya.
        if nueva == "calaveritas":
            destinatario = extraer_destinatario(mensaje)
            if destinatario:
                return self._entregar_calaverita(destinatario)
 
        if nueva and nueva != self.ultima_intencion:
            return self._dar_tema(nueva)          # tema NUEVO
        if nueva and nueva == self.ultima_intencion:
            return self._dar_seguimiento()        # mismo tema: damos más detalle
 
        # Charla casual (hola, gracias, ayuda)
        charla = self._charla(procesado)
        if charla:
            return charla
 
        # "Cuéntame más" sin tema de por medio
        if es_frase_seguimiento(limpio):
            if self.ultima_intencion:
                return self._dar_seguimiento()
            return f"¿Sobre qué quieres que te cuente más? Puedo hablar sobre {self._menu_temas()}."
 
        return random.choice(NO_ENTENDI).format(temas=self._menu_temas())
 
    def _dar_tema(self, tema, siguiente=None):
        """Da la respuesta principal de un tema y deja listo el contexto."""
        self.ultima_intencion = tema
        self.indice_seguimiento = 0
        self.temas_vistos.add(tema)
 
        if tema == "calaveritas":
            # Tema especial: después de explicar, esperamos a quién va dirigida
            self.esperando = {"tipo": "calaverita_destinatario", "datos": None}
            return CONTENIDO[tema]["principal"]
 
        texto = CONTENIDO[tema]["principal"]
        if siguiente:
            self.esperando = {"tipo": "tema", "datos": siguiente}
            texto += f"\n\nDespués, si quieres, vemos {CONTENIDO[siguiente]['etiqueta']}. ¿Va?"
        else:
            texto += self._sugerencia(tema)
        return texto
 
    def _dar_seguimiento(self):
        """Siguiente detalle del tema actual."""
        tema = self.ultima_intencion
        detalles = CONTENIDO[tema]["seguimiento"]
 
        if self.indice_seguimiento < len(detalles):
            texto = detalles[self.indice_seguimiento]
            self.indice_seguimiento += 1
            if self.indice_seguimiento == len(detalles):  # era el último: proponemos algo nuevo
                texto += self._sugerencia(tema)
            return texto
 
        # Ya no hay más detalles
        texto = "Ya te conté lo más importante de este tema. 😄"
        sugerencia = self._sugerencia(tema)
        if sugerencia:
            return texto + sugerencia
        return texto + f" ¿Quieres que veamos {self._menu_temas()}?"
 

    def _sugerencia(self, tema):
        """
        Propone un tema relacionado que el usuario aún no ha visto (proactividad)
        y deja una pregunta pendiente: si responde "sí", se lo contamos.
        """
        for texto, destino in CONTENIDO[tema]["sugerencias"]:
            if destino not in self.temas_vistos and texto != self.ultima_sugerencia:
                self.ultima_sugerencia = texto
                self.esperando = {"tipo": "tema", "datos": destino}
                return "\n\n" + texto
        return ""
 
    def _preguntar_aclaracion(self, a, b):
        """Hay empate entre dos temas: se lo preguntamos al usuario."""
        self.esperando = {"tipo": "aclarar", "datos": (a, b)}
        return (
            f"Mmm, ¿quieres que te platique sobre {CONTENIDO[a]['etiqueta']} "
            f"o sobre {CONTENIDO[b]['etiqueta']}?"
        )
 
    def _menu_temas(self):
        """Hasta 3 temas que aún no vimos, escritos de forma natural: 'a, b y c'."""
        nuevos = [t for t in CONTENIDO if t not in self.temas_vistos]
        elegidos = (nuevos or list(CONTENIDO))[:3]
        return unir_con_y([CONTENIDO[t]["etiqueta"] for t in elegidos])
 
    def _charla(self, procesado):
        for datos in CONVERSACION.values():
            if contiene_alguna(procesado, datos["palabras_clave"]):
                return random.choice(datos["respuestas"]).format(
                    nombre=NOMBRE_BOT, temas=self._menu_temas()
                )
        return None
 
    def _entregar_calaverita(self, destinatario):
        plantilla = PLANTILLAS_CALAVERITA[self.calaveritas_hechas % len(PLANTILLAS_CALAVERITA)]
        self.calaveritas_hechas += 1
        self.ultima_intencion = "calaveritas"
        self.indice_seguimiento = 0
        self.temas_vistos.add("calaveritas")
        self.esperando = {"tipo": "calaverita_otra", "datos": destinatario}
        return (
            "¡Va! Aquí está tu calaverita, con mucho cariño:\n\n"
            + plantilla.format(x=destinatario)
            + "\n\n¿Quieres otra versión?"
        )