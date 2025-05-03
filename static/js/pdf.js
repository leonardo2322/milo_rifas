function getImageAsDataURL(url, callback) {
  const img = new Image();
  img.crossOrigin = "anonymous";
  img.onload = function () {
    const canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;
    const ctx = canvas.getContext("2d");

    // Dibujar imagen original
    ctx.drawImage(img, 0, 0);

    // Obtener pixeles y aplicar filtro blanco y negro
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    for (let i = 0; i < data.length; i += 4) {
      // Calcular escala de grises (luminosidad)
      const gray = 0.3 * data[i] + 0.59 * data[i + 1] + 0.11 * data[i + 2];
      data[i] = data[i + 1] = data[i + 2] = gray;
    }

    ctx.putImageData(imageData, 0, 0);

    const dataUrl = canvas.toDataURL("image/jpeg");
    callback(dataUrl);
  };
  img.onerror = function () {
    console.error("No se pudo cargar la imagen:", url);
    callback(null);
  };
  img.src = url;
}

function descargarFactura(nombreImagen, cliente, descripcionProducto) {
  getImageAsDataURL(nombreImagen, function (dataUrl) {
    if (!dataUrl) {
      alert("Error al cargar la imagen.");
      return;
    }

    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF();
    const pageWidth = pdf.internal.pageSize.getWidth();
    const margin = 10;
    let yPosition = margin;

    // Agregar la imagen convertida a base64
    pdf.addImage(dataUrl, "JPEG", margin, yPosition, 60, 40);
    yPosition += 50;

    // Agregar el nombre del cliente
    pdf.setFontSize(16);
    pdf.setFont("helvetica", "bold");
    pdf.text(cliente, margin, yPosition);
    yPosition += 10;

    // Agregar la descripción
    pdf.setFontSize(12);
    pdf.setFont("helvetica", "normal");
    const splitDescription = pdf.splitTextToSize(
      descripcionProducto,
      pageWidth - 2 * margin
    );
    splitDescription.forEach((line) => {
      pdf.text(line, margin, yPosition);
      yPosition += 5;
    });

    pdf.save(`factura_${cliente}.pdf`);
  });
}
