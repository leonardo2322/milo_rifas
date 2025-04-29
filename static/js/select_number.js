let seleccionados = [];

if (localStorage.getItem("numeros_seleccionados")) {
  const data = JSON.parse(localStorage.getItem("numeros_seleccionados"));
  const tiempoActual = Date.now();

  // Si el timestamp ha expirado (por ejemplo, más de 30 minutos)
  if (data.timestamp && tiempoActual - data.timestamp > 1800000) {
    // 30 minutos en milisegundos
    alert("Tu selección ha expirado, por favor selecciona nuevamente.");
    localStorage.removeItem("numeros_seleccionados");
  } else {
    seleccionados = data?.numeros || [];
  }
}

function toggleSelection(btn) {
  btn.disabled = true;
  btn.classList.remove("btn-outline-warning");
  btn.classList.add("btn-outline-secondary");
  const numero = btn.dataset.numero;

  if (seleccionados.includes(numero)) {
    seleccionados = seleccionados.filter((n) => n !== numero);
  } else {
    seleccionados.push(numero);
  }

  // Guardar la selección con un timestamp para control de expiración
  localStorage.setItem(
    "numeros_seleccionados",
    JSON.stringify({ numeros: seleccionados, timestamp: Date.now() })
  );
}

function verificarDisponibilidadYFinalizar(event) {
  event.preventDefault();
  const numerosSeleccionados =
    JSON.parse(localStorage.getItem("numeros_seleccionados"))?.numeros || [];
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
      body: JSON.stringify({ numeros: numerosSeleccionados }),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken, // Asegúrate de incluir el CSRF token
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.disponibles) {
          // Si los números están disponibles, redirige a la vista de comprobante
          window.location.href = "/comprobante/";
        } else {
          const noDisponibles = data.no_disponibles.join(", ");
          alert(
            `Algunos de los números seleccionados no están disponibles: ${noDisponibles}. Por favor, elige otros.`
          );
        }
      })
      .catch((error) => {
        console.error("Ocurrió un error:", error);
        alert(
          "Hubo un error al intentar verificar los números. Inténtalo de nuevo."
        );
      });
  } else {
    alert("Debes seleccionar al menos un número.");
  }
}
