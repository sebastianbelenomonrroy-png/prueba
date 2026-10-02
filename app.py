from flask import Flask, render_template, request
import random
import requests

from clases.ejercicios import ParImpar, TablaMultiplicar, AdivinaNumero

app = Flask(__name__)
app.secret_key = "clave-flask-ejercicios"

PHP_API_URL = "http://127.0.0.1:8000/guardar.php"


def guardar_en_postgres(ejercicio, entrada, resultado):
    """Envía el resultado al API PHP, que lo guarda en PostgreSQL."""
    try:
        respuesta = requests.post(
            PHP_API_URL,
            json={
                "ejercicio": ejercicio,
                "entrada": entrada,
                "resultado": resultado
            },
            timeout=3
        )
        return respuesta.ok
    except requests.RequestException:
        return False


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    resultado = ""

    if request.method == "POST":
        try:
            numero = int(request.form["numero"])
            ejercicio = ParImpar(numero)
            resultado = ejercicio.resolver()
            guardar_en_postgres("Par o impar", str(numero), resultado)
        except ValueError:
            resultado = "Por favor, escribe un número válido."

    return render_template("ejercicio1.html", resultado=resultado)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    tabla = []
    numero = ""

    if request.method == "POST":
        try:
            numero = int(request.form["numero"])
            ejercicio = TablaMultiplicar(numero)
            tabla = ejercicio.resolver()
            guardar_en_postgres(
                "Tabla de multiplicar",
                str(numero),
                " | ".join(tabla)
            )
        except ValueError:
            tabla = ["Por favor, escribe un número válido."]

    return render_template("ejercicio2.html", tabla=tabla, numero=numero)


@app.route("/ejercicio3", methods=["GET", "POST"])
def ejercicio3():
    # Se guarda un número secreto en la sesión del navegador.
    from flask import session

    if "numero_secreto" not in session:
        session["numero_secreto"] = random.randint(1, 100)

    resultado = ""

    if request.method == "POST":
        try:
            intento = int(request.form["numero"])
            juego = AdivinaNumero(session["numero_secreto"])
            resultado = juego.comprobar(intento)

            guardar_en_postgres(
                "Adivina el número",
                str(intento),
                resultado
            )

            if juego.acertado:
                # Preparar una nueva partida para el siguiente intento.
                session["numero_secreto"] = random.randint(1, 100)

        except ValueError:
            resultado = "Por favor, escribe un número válido."

    return render_template("ejercicio3.html", resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)
