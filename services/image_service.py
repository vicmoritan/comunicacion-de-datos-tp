from PIL import Image
import numpy as np
import base64
from io import BytesIO
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

RESOLUCIONES_GRILLA = [100, 300, 500, 800]

def imagen_a_base64(imagen):
    buffer = BytesIO()
    imagen.save(buffer, format="PNG")
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return (
        f"data:image/png;base64,{imagen_base64}",
        len(buffer.getvalue())
    )

def cuantizar_imagen(imagen, bits):
    if bits == 24:
        return imagen.convert("RGB")

    if bits == 8:
        return imagen.convert("L").convert("RGB")

    if bits == 1:
        imagen_gris = imagen.convert("L")
        arreglo = np.array(imagen_gris)
        arreglo_binario = np.where(arreglo > 127, 255, 0).astype(np.uint8)
        return Image.fromarray(arreglo_binario).convert("RGB")

    return imagen

def histograma_base64(imagen):
    """Histograma en escala de grises (legado, no usado en la UI nueva)."""
    imagen_gris = imagen.convert("L")
    plt.figure(figsize=(4, 3))
    plt.hist(np.array(imagen_gris).flatten(), bins=256)
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    plt.close()
    return (
        "data:image/png;base64," +
        base64.b64encode(buffer.getvalue()).decode()
    )

def histograma_rgb_base64(imagen):
    """
    Histograma con tres curvas superpuestas: R (rojo), G (verde), B (azul).
    Si la imagen está cuantizada en escala de grises, los tres canales
    serán idénticos y se verá una sola curva gris.
    """
    arreglo = np.array(imagen.convert("RGB"))

    fig, ax = plt.subplots(figsize=(4, 3))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    canales = [
        (arreglo[:, :, 0], "#e05c5c", "R"),
        (arreglo[:, :, 1], "#5ce07a", "G"),
        (arreglo[:, :, 2], "#5ca8e0", "B"),
    ]

    for datos, color, etiqueta in canales:
        ax.plot(
            np.bincount(datos.flatten(), minlength=256),
            color=color,
            alpha=0.85,
            linewidth=1.2,
            label=etiqueta
        )

    ax.set_xlim(0, 255)
    ax.set_xlabel("Intensidad", color="#aaa", fontsize=8)
    ax.set_ylabel("Píxeles", color="#aaa", fontsize=8)
    ax.tick_params(colors="#aaa", labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")
    ax.legend(
        fontsize=7,
        facecolor="#1a1a2e",
        edgecolor="#333",
        labelcolor="white"
    )

    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=100)
    plt.close()

    return (
        "data:image/png;base64," +
        base64.b64encode(buffer.getvalue()).decode()
    )

def procesar_imagen(archivo_imagen, resolucion, bits):
    imagen_original = Image.open(archivo_imagen).convert("RGB")
    ancho_original, alto_original = imagen_original.size

    tamano_teorico_original_bits = (ancho_original * alto_original * 24)
    tamano_teorico_digitalizado_bits = (resolucion * resolucion * bits)
    tamano_original_kb = round(tamano_teorico_original_bits / 8 / 1024, 2)
    tamano_digitalizada_kb = round(tamano_teorico_digitalizado_bits / 8 / 1024, 2)

    original_base64, tamano_original = imagen_a_base64(imagen_original)

    imagen_reducida = imagen_original.resize((resolucion, resolucion))
    imagen_digitalizada = cuantizar_imagen(imagen_reducida, bits)

    digitalizada_base64, tamano_digitalizada = imagen_a_base64(imagen_digitalizada)

    porcentaje = round((tamano_digitalizada / tamano_original) * 100, 2)

    hist_original = histograma_rgb_base64(imagen_original)
    hist_digitalizada = histograma_rgb_base64(imagen_digitalizada)

    return {
        "original": original_base64,
        "digitalizada": digitalizada_base64,
        "tamano_original_kb": tamano_original_kb,
        "tamano_digitalizada_kb": tamano_digitalizada_kb,
        "resolucion_original": f"{ancho_original}x{alto_original}",
        "resolucion_final": f"{resolucion}x{resolucion}",
        "porcentaje": porcentaje,
        "resolucion": resolucion,
        "bits": bits,
        "histograma_original": hist_original,
        "histograma_digitalizada": hist_digitalizada
    }

def procesar_grilla(archivo_imagen, bits):
    """
    Procesa la misma imagen con las 4 resoluciones disponibles y devuelve
    una lista de objetos para mostrar en modo grilla.
    La imagen se lee una sola vez para no releer el stream 4 veces.
    """
    imagen_original = Image.open(archivo_imagen).convert("RGB")
    resultados = []

    for res in RESOLUCIONES_GRILLA:
        imagen_reducida = imagen_original.resize((res, res))
        imagen_cuantizada = cuantizar_imagen(imagen_reducida, bits)
        img_b64, _ = imagen_a_base64(imagen_cuantizada)
        tamano_kb = round((res * res * bits) / 8 / 1024, 2)

        resultados.append({
            "resolucion": res,
            "imagen": img_b64,
            "tamano_kb": tamano_kb
        })

    return resultados