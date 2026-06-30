from flask import Flask, render_template, request, jsonify
from services.image_service import procesar_imagen, procesar_grilla

app = Flask(__name__)

RESOLUCIONES_VALIDAS = {100, 300, 500, 800}
BITS_VALIDOS = {1, 8, 24}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/procesar-imagen", methods=["POST"])
def api_procesar_imagen():
    if "imagen" not in request.files:
        return jsonify({"error": "No se recibió ninguna imagen"}), 400

    imagen = request.files["imagen"]
    resolucion = int(request.form.get("resolucion", 500))
    bits = int(request.form.get("bits", 8))

    if resolucion not in RESOLUCIONES_VALIDAS:
        return jsonify({"error": "Resolución inválida"}), 400
    if bits not in BITS_VALIDOS:
        return jsonify({"error": "Profundidad de bits inválida"}), 400

    try:
        resultado = procesar_imagen(imagen, resolucion, bits)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/grilla-resoluciones", methods=["POST"])
def api_grilla_resoluciones():
    """
    Devuelve la misma imagen procesada en las 4 resoluciones disponibles,
    con la profundidad de bits elegida por el usuario.
    """
    if "imagen" not in request.files:
        return jsonify({"error": "No se recibió ninguna imagen"}), 400

    imagen = request.files["imagen"]
    bits = int(request.form.get("bits", 8))

    if bits not in BITS_VALIDOS:
        return jsonify({"error": "Profundidad de bits inválida"}), 400

    try:
        resultado = procesar_grilla(imagen, bits)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)