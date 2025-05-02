import { mostrarAlerta } from "./alertas.js";

document.addEventListener("DOMContentLoaded", function () {
  const boton_busqueda = document.getElementById("btn_busqueda_dni");
  const input_dni = document.getElementById("busqueda_dni");

  if (boton_busqueda) {
    boton_busqueda.addEventListener("click", function () {
      const dni = input_dni.value.trim();
      if (dni === "") {
        mostrarAlerta(
          "Por favor, ingresa un número de cédula.",
          "Error en la búsqueda",
          "error"
        );
        return;
      }
      // Aquí puedes agregar la lógica para buscar el cliente por DNI
      fetch(`/buscar_cliente/${dni}/`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Error en la búsqueda del cliente.");
          }
          return response.json();
        })
        .then((data) => {
          // Aquí puedes manejar la respuesta de la búsqueda
          console.log("Cliente encontrado:", data);
          if (data.estado) {
            window.location.href = "/seleccionar_numero/";
          }
          // Actualiza el formulario con los datos del cliente
        })
        .catch((error) => {
          console.error("Error al buscar el cliente:", error);
          mostrarAlerta(
            "No se encontró ningún cliente con ese número de cédula.",
            "Error en la búsqueda",
            "error"
          );
        });
    });
  }
});
