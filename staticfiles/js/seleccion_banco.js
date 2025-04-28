document.addEventListener("DOMContentLoaded", () => {
  const banco_name = document.querySelectorAll(".banco-label");
  const detallesContainer = document.getElementById("detalles-banco");
  const botonesCopiar = detallesContainer.querySelectorAll(".copiar-btn");

  banco_name.forEach((banco_name) => {
    banco_name.addEventListener("click", function () {
      const nombre = this.dataset.nombre || "";
      const titular = this.dataset.titular || "";
      const tipo = this.dataset.tipo || "";
      const cedula = this.dataset.cedula || "";
      const cuenta = this.dataset.numero_cuenta || "";
      const telefono = this.dataset.telefono || "";
      const correo = this.dataset.correo || "";

      let detallesHtml = `<h5>Detalles de <em>${nombre}</em>:</h5><ul class="list-group" style=" background-color:;">`;

      if (cuenta) {
        detallesHtml += `
    <li class="list-group-item d-flex justify-content-between align-items-center">
      <span><strong>Cuenta:</strong> ${cuenta}</span>
      <button class="btn btn-sm btn-outline-primary copiar-btn" data-text="${cuenta}">Copiar</button>
    </li>`;
      }
      if (titular) {
        detallesHtml += `
    <li class="list-group-item d-flex justify-content-between align-items-center">
      <span><strong>Titular:</strong> ${titular}</span>
      <button class="btn btn-sm btn-outline-primary copiar-btn" data-text="${titular}">Copiar</button>
    </li>`;
      }
      if (tipo) {
        detallesHtml += `
    <li class="list-group-item d-flex justify-content-between align-items-center">
      <span><strong>Tipo:</strong> ${tipo}</span>
      <button class="btn btn-sm btn-outline-primary copiar-btn" data-text="${tipo}">Copiar</button>
    </li>`;
      }
      if (cedula) {
        detallesHtml += `
    <li class="list-group-item d-flex justify-content-between align-items-center">
      <span><strong>Cédula:</strong> ${cedula}</span>
      <button class="btn btn-sm btn-outline-primary copiar-btn" data-text="${cedula}">Copiar</button>
    </li>`;
      }
      if (telefono) {
        detallesHtml += `
    <li class="list-group-item d-flex justify-content-between align-items-center">
      <span><strong>Teléfono:</strong> ${telefono}</span>
      <button class="btn btn-sm btn-outline-primary copiar-btn" data-text="${telefono}">Copiar</button>
    </li>`;
      }
      if (correo) {
        detallesHtml += `
    <li class="list-group-item d-flex justify-content-between align-items-center">
      <span><strong>Correo:</strong> ${correo}</span>
      <button class="btn btn-sm btn-outline-primary copiar-btn" data-text="${correo}">Copiar</button>
    </li>`;
      }

      detallesHtml += `</ul>`;

      detallesContainer.innerHTML = detallesHtml;
    });
  });

  botonesCopiar.forEach((boton) => {
    boton.addEventListener("click", () => {
      const texto = boton.getAttribute("data-text");
      navigator.clipboard
        .writeText(texto)
        .then(() => {
          boton.innerText = "Copiado!";
          setTimeout(() => {
            boton.innerText = "Copiar";
          }, 1500);
        })
        .catch((err) => {
          console.error("Error al copiar:", err);
        });
    });
  });
});
