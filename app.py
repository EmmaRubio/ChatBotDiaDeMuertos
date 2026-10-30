from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from chatbot import Chatbot

app = Flask(__name__)

bot = Chatbot()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/mensaje", methods=["POST"])
def mensaje():

    datos = request.get_json()

    texto = datos["mensaje"]

    respuesta = bot.responder(texto)

    return jsonify({
        "respuesta": respuesta
    })


if __name__ == "__main__":
    app.run(debug=True)
