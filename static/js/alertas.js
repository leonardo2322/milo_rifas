/**
 * @param {string} message - Mensaje a mostrar en la alerta.
 * @param {string} info - Información adicional que se mostrará en la alerta.
 * @param {string} [icono="warning"] - Icono de la alerta (por defecto "warning").
 */

export const alertas = (buttons_submit, message, info, icono = "warning") => {
  const botones = buttons_submit;

  botones.forEach((btn) => {
    btn.addEventListener("click", function (event) {
      event.preventDefault();

      const formTarget = event.target.closest("form");
      if (!formTarget) {
        console.error(`Formulario con selector ${event.target} no encontrado.`);

        return;
      }

      Swal.fire({
        title: info,
        text: message,
        icon: icono,
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: `¿Deseas continuar con ${info}?`,
      }).then((result) => {
        if (result.isConfirmed) {
          formTarget.submit();
        }
      });
    });
  });
};
export function mostrarAlerta(message, info, icono = "warning") {
  Swal.fire({
    title: info,
    text: message,
    icon: icono,
    confirmButtonColor: "#3085d6",
    confirmButtonText: "Aceptar",
  });
}
