from PIL import Image
import numpy as np
import base64
from io import BytesIO


def imagen_a_base64(imagen):
    buffer = BytesIO()
    imagen.save(buffer, format="PNG")
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{imagen_base64}", len(buffer.getvalue())


def cuantizar_imagen(imagen, bits):
    arreglo = np.array(imagen)

    if bits == 24:
        return imagen

    niveles = 2 ** bits

    if bits == 1:
        imagen_gris = imagen.convert("L")
        arreglo_gris = np.array(imagen_gris)
        arreglo_cuantizado = np.where(arreglo_gris > 127, 255, 0).astype(np.uint8)
        return Image.fromarray(arreglo_cuantizado).convert("RGB")

    factor = 256 // niveles
    arreglo_cuantizado = (arreglo // factor) * factor
    arreglo_cuantizado = arreglo_cuantizado.astype(np.uint8)

    return Image.fromarray(arreglo_cuantizado)


def procesar_imagen(archivo_imagen, resolucion, bits):
    imagen_original = Image.open(archivo_imagen).convert("RGB")

    original_base64, tamano_original = imagen_a_base64(imagen_original)

    imagen_reducida = imagen_original.resize((resolucion, resolucion))
    imagen_digitalizada = cuantizar_imagen(imagen_reducida, bits)

    digitalizada_base64, tamano_digitalizada = imagen_a_base64(imagen_digitalizada)

    porcentaje = round((tamano_digitalizada / tamano_original) * 100, 2)

    return {
        "original": original_base64,
        "digitalizada": digitalizada_base64,
        "tamano_original_kb": round(tamano_original / 1024, 2),
        "tamano_digitalizada_kb": round(tamano_digitalizada / 1024, 2),
        "porcentaje": porcentaje,
        "resolucion": resolucion,
        "bits": bits
    }