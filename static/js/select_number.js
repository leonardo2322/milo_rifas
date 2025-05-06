import { mostrarAlerta } from "./alertas.js";

document.addEventListener("DOMContentLoaded", () => {
  const btnFinalizar = document.getElementById("btn-finalizar"); // Usa el ID o una clase
  const btnNumeros = document.querySelectorAll(".btn-numeros");
  btnNumeros.forEach((btn) => {
    btn.addEventListener("click", function () {
      toggleSelection(this);
    });
  });
  if (btnFinalizar) {
    btnFinalizar.addEventListener("click", verificarDisponibilidadYFinalizar);
  }
});
let seleccionados = [];
const inputNumeros = document.getElementById("input-numeros");
const tiempo_seleccion = document.getElementById("time_stamp");
function toggleSelection(btn) {
  console.log("Botón clicado:", btn);
  btn.classList.remove("btn-outline-warning");
  btn.classList.add("btn-outline-secondary");
  const numero = btn.dataset.numero;
  const time_stamp = new Date().toISOString();
  if (seleccionados.includes(numero)) {
    seleccionados = seleccionados.filter((n) => n !== numero);
    btn.classList.remove("btn-outline-secondary");
    btn.classList.add("btn-outline-warning");
  } else {
    seleccionados.push(numero);
  }
  inputNumeros.value = JSON.stringify(seleccionados);
  tiempo_seleccion.value = time_stamp;

  actualizarNumerosSeleccionados();
  // Guardar la selección con un timestamp para control de expiración
}
function actualizarNumerosSeleccionados() {
  const contenedor = document.getElementById("numeros-seleccion");
  contenedor.innerHTML = ""; // Limpiar el contenedor antes de agregar los números

  if (seleccionados.length > 0) {
    seleccionados.forEach((numero) => {
      const li = document.createElement("li");
      li.textContent = numero;
      contenedor.appendChild(li);
    });
  } else {
    const li = document.createElement("li");
    li.textContent = "No has seleccionado ningún número aún.";
    contenedor.appendChild(li);
  }
}

function verificarDisponibilidadYFinalizar(event) {
  event.preventDefault();

  let numerosSeleccionados = []; // Definir la variable antes de usarla

  if (inputNumeros.value.trim() !== "") {
    try {
      // Aseguramos que el valor de inputNumeros sea un JSON válido
      numerosSeleccionados = JSON.parse(inputNumeros.value); // Asignar los números seleccionados

      if (!Array.isArray(numerosSeleccionados)) {
        throw new Error("El valor no es un arreglo.");
      }
    } catch (error) {
      console.error("Error al parsear el input:", error);
      mostrarAlerta(
        "Los datos de los números están corruptos.",
        "Error en la selección",
        "error"
      );
      return;
    }
  } else {
    mostrarAlerta(
      "No has seleccionado ningún número.",
      "Selección vacía",
      "warning"
    );
    return;
  }

  const csrfToken = document.getElementById("csrf-token").value;

  if (!csrfToken) {
    alert(
      "No se encontró el token CSRF. Recarga la página e inténtalo de nuevo."
    );
    return;
  }

  if (numerosSeleccionados.length > 0) {
    // Verifica disponibilidad de los números seleccionados
    fetch("/verificar_numeros_disponibles/", {
      method: "POST",
      body: JSON.stringify({
        numeros: numerosSeleccionados,
        time_stamp: tiempo_seleccion.value,
      }),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken, // Asegúrate de incluir el CSRF token
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.disponibles) {
          // Si los números están disponibles, redirige a la vista de comprobante
          localStorage.setItem("paso_por_comprobante", "true");
          window.location.href = "/comprobante/";
        } else {
          const noDisponibles = data.no_disponibles.join(", ");
          mostrarAlerta(
            `Algunos de los números seleccionados no están disponibles: ${noDisponibles}. Por favor, elige otros.`,
            "Numero no disponible",
            "warning"
          );
        }
      })
      .catch((error) => {
        console.error("Ocurrió un error:", error);
        mostrarAlerta(
          "hubo un error verifica No has seleccionado ningún número.",
          "Selección vacía",
          "warning"
        );
      });
  } else {
    mostrarAlerta(
      "No has seleccionado ningún número.",
      "Selección vacía",
      "warning"
    );
  }
}

window.addEventListener("pageshow", function (event) {
  if (event.persisted) {
    const csrfToken = document.getElementById("csrf-token").value;
    // Si la página fue restaurada desde el caché, recarga el contenido
    fetch("/liberar-reservas/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken, // Asegúrate de tener este token si no usas @csrf_exempt
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("Reservas liberadas con éxito");
        } else {
          console.warn("No se pudo liberar reservas:", data.error);
        }
      })
      .catch((error) => {
        console.error("Error al liberar reservas:", error);
      });
  }
});
