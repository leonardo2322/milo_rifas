document.addEventListener("DOMContentLoaded", function () {
  const botones = document.querySelectorAll(".descargar-factura");

  botones.forEach((boton) => {
    boton.addEventListener("click", function (e) {
      e.preventDefault();

      const overlay = document.getElementById("loadingOverlay");
      if (overlay) overlay.style.display = "flex";

      const imagen = this.dataset.imagen;
      const cliente = this.dataset.cliente;
      const descripcion = this.dataset.descripcion;

      descargarFactura(imagen, cliente, descripcion);
    });
  });
});

function getImageAsDataURL(url, callback) {
  const img = new Image();
  img.crossOrigin = "anonymous";

  img.onload = function () {
    const canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;
    const ctx = canvas.getContext("2d");

    ctx.drawImage(img, 0, 0);

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    for (let i = 0; i < data.length; i += 4) {
      const gray = 0.3 * data[i] + 0.59 * data[i + 1] + 0.11 * data[i + 2];
      data[i] = data[i + 1] = data[i + 2] = gray;
    }

    ctx.putImageData(imageData, 0, 0);
    callback(canvas.toDataURL("image/jpeg"));
  };

  img.onerror = function () {
    console.error("No se pudo cargar la imagen:", url);
    callback(null);
  };

  img.src = url;
}

function descargarFactura(nombreImagen, cliente, descripcionProducto) {
  getImageAsDataURL(nombreImagen, function (dataUrl) {
    const overlay = document.getElementById("loadingOverlay");
    if (!dataUrl) {
      alert("Error al cargar la imagen.");
      if (overlay) overlay.style.display = "none";
      return;
    }

    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF({
      orientation: "portrait",
      unit: "mm", // también puede ser "in" para pulgadas
      format: [176, 176],
    });
    const pageWidth = pdf.internal.pageSize.getWidth();
    const margin = 10;
    let y = margin;

    // Imagen (centrada)
    const imgWidth = 60;
    const imgX = (pageWidth - imgWidth) / 2;
    pdf.addImage(dataUrl, "JPEG", imgX, y, imgWidth, 40);
    y += 50;

    // Nombre del cliente (centrado)
    pdf.setFontSize(16);
    pdf.setFont("helvetica", "bold");
    const clienteTextWidth = pdf.getTextWidth(cliente);
    pdf.text(cliente, (pageWidth - clienteTextWidth) / 2, y);
    y += 10;

    // Línea de separación
    pdf.setDrawColor(0); // negro
    pdf.line(margin, y, pageWidth - margin, y);
    y += 10;

    // Descripción (alineado a la izquierda pero con márgenes)
    pdf.setFontSize(12);
    pdf.setFont("helvetica", "normal");
    const splitDescripcion = pdf.splitTextToSize(
      descripcionProducto,
      pageWidth - 2 * margin
    );
    splitDescripcion.forEach((line) => {
      pdf.text(line, margin, y);
      y += 6;
    });

    y += 10;

    // Mensaje final centrado
    const mensajeFinal =
      "Estimado usuario le hacemos constatar que su pago ha sido revisado y comprobado. Con este comprobante de juego usted ya está participando en esta gran rifa y podrá reclamar su premio si llegase a ser el dichoso ganador. Sin más que decirle, gracias por participar en nuestra rifa. ¡Muchísima suerte!";

    pdf.setFont("helvetica", "italic");
    pdf.setFontSize(12);

    // Divide el texto en líneas de ancho manejable
    const maxTextWidth = pageWidth - 2 * margin;
    const mensajeLineas = pdf.splitTextToSize(mensajeFinal, maxTextWidth);

    // Centra cada línea individualmente
    mensajeLineas.forEach((linea) => {
      const textWidth = pdf.getTextWidth(linea);
      pdf.text(linea, (pageWidth - textWidth) / 2, y);
      y += 6; // Espaciado entre líneas
    });
    pdf.setDrawColor(150); // gris
    pdf.line(margin, y, pageWidth - margin, y);
    y += 10;
    // Guardar PDF
    const fechaActual = new Date().toLocaleDateString();
    const mensajeFinalExtra =
      "Siempre para servirle,\nSu fiel servidor: Rifas Milo\n\n© Rifas Milo - " +
      fechaActual;

    const lineasExtra = pdf.splitTextToSize(mensajeFinalExtra, maxTextWidth);
    lineasExtra.forEach((linea) => {
      const textWidth = pdf.getTextWidth(linea);
      pdf.text(linea, (pageWidth - textWidth) / 2, y);
      y += 6;
    });
    y += 10;
    pdf.setDrawColor(100);
    pdf.setLineWidth(0.5);
    pdf.rect(margin, y, pageWidth - 2 * margin, 30); // Rectángulo simple
    y += 20;
    pdf.setFontSize(10);
    pdf.setFont("helvetica", "italic");
    pdf.text(
      "Gracias por su confianza. ¡Nos vemos en la próxima rifa!",
      pageWidth / 2,
      y,
      {
        align: "center",
      }
    );

    pdf.save(`factura_${cliente}.pdf`);

    if (overlay) overlay.style.display = "none";
  });
}
