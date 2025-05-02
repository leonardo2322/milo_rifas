document.addEventListener("DOMContentLoaded", () => {
  const banco_name = document.querySelectorAll(".banco-label");
  const detallesContainer = document.getElementById("detalles-banco");
  console.log("Botones de copiar:", detallesContainer); // Para depuración
  banco_name.forEach((banco_name) => {
    banco_name.addEventListener("click", function () {
      const nombre = this.dataset.nombre || "";
      const titular = this.dataset.titular || "";
      const tipo = this.dataset.tipo || "";
      const cedula = this.dataset.cedula || "";
      const cuenta = this.dataset.numero_cuenta || "";
      const telefono = this.dataset.telefono || "";
      const correo = this.dataset.correo || "";

      let detallesHtml = `<h5 class="text-center">Detalles de ${nombre}:</h5><ul class="list-group bg-transparent p-5 text-center " style="max-width: 100%;">`;

      if (cuenta && cuenta !== "None") {
        detallesHtml += `
    <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
      <span><strong>Cuenta:</strong> ${cuenta}</span>
      <button class="btn btn-sm btn-outline-primary copiar-btn ms-2" data-text="${cuenta}">Copiar</button>
    </li>`;
      }
      if (titular && titular !== "None") {
        detallesHtml += `
    <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
      <span><strong>Titular:</strong> ${titular}</span>
      <button class="btn btn-sm btn-outline-primary copiar-btn ms-3" data-text="${titular}">Copiar</button>
    </li>`;
      }
      if (tipo && tipo !== "None") {
        detallesHtml += `
    <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
      <span><strong>Tipo:</strong> ${tipo}</span>
      <button class="btn btn-sm btn-outline-primary copiar-btn ms-3" data-text="${tipo}">Copiar</button>
    </li>`;
      }
      if (cedula && cedula !== "None") {
        detallesHtml += `
    <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
      <span><strong>Cédula:</strong> ${cedula}</span>
      <button class="btn btn-sm btn-outline-primary copiar-btn ms-3" data-text="${cedula}">Copiar</button>
    </li>`;
      }
      if (telefono && telefono !== "None") {
        detallesHtml += `
    <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
      <span><strong>Teléfono:</strong> ${telefono} </span>
      <button class="btn btn-sm btn-outline-primary copiar-btn ms-3" data-text="${telefono}">Copiar</button>
    </li>`;
      }
      if (correo && correo !== "None") {
        detallesHtml += `
    <li class="list-group-item bg-transparent d-flex justify-content-between align-items-center">
      <span><strong>Correo:</strong> ${correo}</span>
      <button class="btn btn-sm btn-outline-primary copiar-btn ms-3" data-text="${correo}">Copiar</button>
    </li>`;
      }

      detallesHtml += `</ul>`;

      detallesContainer.innerHTML = detallesHtml;
    });
  });
  detallesContainer.addEventListener("click", (e) => {
    const boton = e.target.closest(".copiar-btn");
    console.log("Botón de copiar clicado:", boton); // Para depuración
    if (boton) {
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
    }
  });
});
