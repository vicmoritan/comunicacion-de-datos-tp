const inputImagen       = document.getElementById("inputImagen");
const selectResolucion  = document.getElementById("selectResolucion");
const selectBits        = document.getElementById("selectBits");
const btnProcesar       = document.getElementById("btnProcesar");
const mensajeImagen     = document.getElementById("mensajeImagen");
const checkGrilla       = document.getElementById("checkGrilla");

const vistaComparacion  = document.getElementById("vistaComparacion");
const vistaGrilla       = document.getElementById("vistaGrilla");

const imagenOriginal    = document.getElementById("imagenOriginal");
const imagenDigitalizada = document.getElementById("imagenDigitalizada");

const tamanoOriginal    = document.getElementById("tamanoOriginal");
const tamanoDigitalizado = document.getElementById("tamanoDigitalizado");
const porcentaje        = document.getElementById("porcentaje");

const resOriginal       = document.getElementById("resOriginal");
const resFinal          = document.getElementById("resFinal");
const bitsInfo          = document.getElementById("bitsInfo");
const grillaBits        = document.getElementById("grillaBits");

const histOriginal      = document.getElementById("histOriginal");
const histDigitalizada  = document.getElementById("histDigitalizada");

const btnDescargar      = document.getElementById("btnDescargar");
const grillaContenido   = document.getElementById("grillaContenido");

// ── Toggle: mostrar/ocultar selector de resolución según modo ──────────────
checkGrilla.addEventListener("change", () => {
    selectResolucion.disabled = checkGrilla.checked;
    selectResolucion.style.opacity = checkGrilla.checked ? "0.4" : "1";
});

// ── Botón principal ────────────────────────────────────────────────────────
btnProcesar.addEventListener("click", async () => {
    mensajeImagen.textContent = "";

    const archivo = inputImagen.files[0];
    if (!archivo) {
        mensajeImagen.textContent = "Primero tenés que cargar una imagen.";
        return;
    }

    if (archivo.size > 5 * 1024 * 1024) {
        mensajeImagen.textContent = "La imagen no debe superar 5 MB.";
        return;
    }

    btnProcesar.disabled = true;
    btnProcesar.textContent = "Procesando…";

    try {
        if (checkGrilla.checked) {
            await procesarGrilla(archivo);
        } else {
            await procesarNormal(archivo);
        }
    } catch (error) {
        mensajeImagen.textContent = "No se pudo procesar la imagen.";
        console.error(error);
    } finally {
        btnProcesar.disabled = false;
        btnProcesar.textContent = "Digitalizar";
    }
});

// ── Modo normal ────────────────────────────────────────────────────────────
async function procesarNormal(archivo) {
    const formData = new FormData();
    formData.append("imagen", archivo);
    formData.append("resolucion", selectResolucion.value);
    formData.append("bits", selectBits.value);

    const respuesta = await fetch("/api/procesar-imagen", {
        method: "POST",
        body: formData
    });

    const datos = await respuesta.json();

    if (!respuesta.ok) {
        mensajeImagen.textContent = datos.error || "Ocurrió un error.";
        return;
    }

    // Mostrar vista normal, ocultar grilla
    vistaComparacion.style.display = "";
    vistaGrilla.style.display = "none";

    imagenOriginal.src      = datos.original;
    imagenDigitalizada.src  = datos.digitalizada;

    histOriginal.src        = datos.histograma_original;
    histDigitalizada.src    = datos.histograma_digitalizada;

    tamanoOriginal.textContent    = datos.tamano_original_kb;
    tamanoDigitalizado.textContent = datos.tamano_digitalizada_kb;
    porcentaje.textContent        = datos.porcentaje;

    resOriginal.textContent = datos.resolucion_original;
    resFinal.textContent    = datos.resolucion_final;
    bitsInfo.textContent    = datos.bits;

    btnDescargar.href = datos.digitalizada;
}

// ── Modo grilla ────────────────────────────────────────────────────────────
async function procesarGrilla(archivo) {
    const formData = new FormData();
    formData.append("imagen", archivo);
    formData.append("bits", selectBits.value);

    const respuesta = await fetch("/api/grilla-resoluciones", {
        method: "POST",
        body: formData
    });

    const datos = await respuesta.json();

    if (!respuesta.ok) {
        mensajeImagen.textContent = datos.error || "Ocurrió un error.";
        return;
    }

    // Mostrar vista grilla, ocultar comparación normal
    vistaComparacion.style.display = "none";
    vistaGrilla.style.display = "";

    grillaBits.textContent = selectBits.value;

    // Construir tarjetas
    grillaContenido.innerHTML = "";

    datos.forEach(item => {
        const tarjeta = document.createElement("div");
        tarjeta.className = "grilla-tarjeta";

        const img = document.createElement("img");
        img.src = item.imagen;
        img.alt = `${item.resolucion}×${item.resolucion}`;
        img.className = "preview";

        const titulo = document.createElement("h3");
        titulo.textContent = `${item.resolucion} × ${item.resolucion} px`;

        const info = document.createElement("p");
        info.className = "grilla-info";
        info.textContent = `Tamaño teórico: ${item.tamano_kb} KB`;

        const link = document.createElement("a");
        link.href = item.imagen;
        link.download = `digitalizada_${item.resolucion}px.png`;
        link.textContent = "Descargar";
        link.className = "grilla-link";

        tarjeta.appendChild(img);
        tarjeta.appendChild(titulo);
        tarjeta.appendChild(info);
        tarjeta.appendChild(link);
        grillaContenido.appendChild(tarjeta);
    });
}