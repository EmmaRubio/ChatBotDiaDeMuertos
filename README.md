# Pirata de Culiacán Bot

Chatbot educativo sobre el Día de Muertos desarrollado en Python.

Su objetivo es ayudar a estudiantes de secundaria a aprender sobre la historia, tradiciones, simbolismos y expresiones culturales relacionadas con el Día de Muertos mediante conversaciones naturales e interactivas.

---

# Objetivo

Desarrollar un chatbot capaz de responder preguntas sobre el Día de Muertos utilizando técnicas básicas de Procesamiento de Lenguaje Natural (NLP), manteniendo una conversación contextual y amigable para adolescentes de entre 12 y 15 años.

El sistema busca explicar de manera clara y sencilla temas como:

- Historia del Día de Muertos.
- Ofrendas.
- Catrinas.
- Pan de muerto.
- Mascotas y ofrendas.
- Música tradicional.
- Calaveritas literarias.
- Tradiciones regionales.
- Diferencias entre Halloween y Día de Muertos.
- Filosofía mexicana sobre la muerte.

---

# Tecnologías utilizadas

- Python 3
- Visual Studio Code
- Git
- GitHub

Bibliotecas utilizadas:

```python
random
re
unicodedata
```

No se utilizan dependencias externas.

---

# Estructura del proyecto

```text
ChatBotDiaDeMuertos/
│
├── main.py
├── chatbot.py
├── respuestas.py
├── config.py
├── README.md
├── requirements.txt
└── .gitignore
```

## main.py

Punto de entrada del sistema.

Responsabilidades:

- Iniciar la conversación.
- Mostrar mensajes de bienvenida.
- Gestionar el ciclo principal del chatbot.

---

## chatbot.py

Contiene la lógica principal.

Responsabilidades:

- Limpieza de texto.
- Procesamiento de lenguaje natural.
- Detección de temas.
- Manejo del contexto.
- Generación de respuestas.
- Gestión de preguntas de seguimiento.

---

## respuestas.py

Contiene la base de conocimiento.

Responsabilidades:

- Definir temas.
- Definir sinónimos.
- Definir respuestas.
- Definir conversaciones casuales.
- Definir casos delicados.
- Definir plantillas de calaveritas.

---

## config.py

Archivo de configuración global.

Responsabilidades:

- Nombre del chatbot.
- Palabras de salida.
- Configuración de límites.
- Frases predefinidas.

---

# Arquitectura

```text
Usuario
   ↓
Interfaz (main.py)
   ↓
Procesamiento NLP
   ↓
Detección de intención
   ↓
Memoria de contexto
   ↓
Motor de respuestas
   ↓
Usuario
```

---

# Características implementadas

## Flujo conversacional

El chatbot mantiene conversaciones mediante un ciclo continuo hasta que el usuario decide salir.

---

## NLP básico

Implementa:

- Conversión a minúsculas.
- Eliminación de acentos.
- Eliminación de caracteres especiales.
- Sustitución de sinónimos.
- Detección de palabras clave.

---

## Clasificación de temas

Puede identificar preguntas relacionadas con:

- Historia
- Ofrendas
- Catrinas
- Pan de muerto
- Mascotas
- Sincretismo
- Regiones
- Calaveritas
- Comparación con Halloween
- Filosofía de la muerte
- Música

---

## Memoria de contexto

Recuerda el tema actual de la conversación para responder preguntas de seguimiento como:

```text
Usuario:
¿Qué es una ofrenda?

Bot:
...

Usuario:
¿Y qué más?
```

---

## Proactividad

Sugiere nuevos temas relacionados durante la conversación.

Ejemplo:

```text
¿Sabías que el pan de muerto tiene un significado especial?
```

---

## Actividad social

Puede responder a mensajes como:

```text
Hola
Gracias
¿Cómo estás?
Adiós
```

---

## Casos delicados

Reconoce situaciones emocionales relacionadas con pérdidas de mascotas o seres queridos y responde de manera respetuosa.

---

## Generador de calaveritas

Puede crear calaveritas literarias personalizadas para:

- Amigos
- Profesores
- Familiares
- Compañeros

---

# Instalación

Clonar el repositorio:

```bash
git clone https://github.com/EmmaRubio/ChatBotDiaDeMuertos.git
```

Entrar al proyecto:

```bash
cd ChatBotDiaDeMuertos
```

Ejecutar:

```bash
python main.py
```

---

# Ejemplo de uso

```text
Tú:
¿Qué es una ofrenda?

Bot:
Una ofrenda o altar es una guía llena de simbolismo para honrar a quienes se adelantaron.

Tú:
¿Y qué lleva?

Bot:
Una ofrenda suele llevar flores de cempasúchil, velas, fotografías, comida y objetos que le gustaban al difunto.
```

---

# Funcionalidades actuales

- Conversación por consola.
- NLP básico.
- Detección de intención.
- Contexto conversacional.
- Seguimiento de temas.
- Respuestas educativas.
- Casos delicados.
- Calaveritas automáticas.


Actualmente el chatbot:

- No utiliza Inteligencia Artificial generativa.
- No aprende de nuevas conversaciones.
- No almacena conversaciones.
- No utiliza bases de datos.
- No cuenta con interfaz gráfica.
- Depende de palabras clave para identificar temas.


# Autores
Acatitlán SanJuan Jazmín


Emmanuel Rubio Sánchez


Proyecto desarrollado para la materia de Sistemas Inteligentes.