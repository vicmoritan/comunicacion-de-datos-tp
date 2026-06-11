from flask import Flask, render_template, request, jsonify
from services.image_service import procesar_imagen
app = Flask(__name__)


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

    try:
        resultado = procesar_imagen(imagen, resolucion, bits)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)