const inputImagen = document.getElementById("inputImagen");
const selectResolucion = document.getElementById("selectResolucion");
const selectBits = document.getElementById("selectBits");
const btnProcesar = document.getElementById("btnProcesar");
const mensajeImagen = document.getElementById("mensajeImagen");

const imagenOriginal = document.getElementById("imagenOriginal");
const imagenDigitalizada = document.getElementById("imagenDigitalizada");

const tamanoOriginal = document.getElementById("tamanoOriginal");
const tamanoDigitalizado = document.getElementById("tamanoDigitalizado");
const porcentaje = document.getElementById("porcentaje");

btnProcesar.addEventListener("click", async () => {
    mensajeImagen.textContent = "";

    const archivo = inputImagen.files[0];

    if (!archivo) {
        mensajeImagen.textContent = "Primero tenés que cargar una imagen.";
        return;
    }

    const formData = new FormData();
    formData.append("imagen", archivo);
    formData.append("resolucion", selectResolucion.value);
    formData.append("bits", selectBits.value);

    try {
        btnProcesar.disabled = true;
        btnProcesar.textContent = "Procesando...";

        const respuesta = await fetch("/api/procesar-imagen", {
            method: "POST",
            body: formData
        });

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            mensajeImagen.textContent = datos.error || "Ocurrió un error.";
            return;
        }

        imagenOriginal.src = datos.original;
        imagenDigitalizada.src = datos.digitalizada;

        tamanoOriginal.textContent = datos.tamano_original_kb;
        tamanoDigitalizado.textContent = datos.tamano_digitalizada_kb;
        porcentaje.textContent = datos.porcentaje;

    } catch (error) {
        mensajeImagen.textContent = "No se pudo procesar la imagen.";
        console.error(error);
    } finally {
        btnProcesar.disabled = false;
        btnProcesar.textContent = "Digitalizar";
    }
});