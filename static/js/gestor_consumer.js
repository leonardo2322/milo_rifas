const socket = new WebSocket("ws://" + window.location.host + "/ws/numeros/");
socket.onopen = function (e) {
  console.log("Conectado al WebSocket!");
};

socket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  console.log("Mensaje recibido:", data);

  if (data.tipo === "numeros_iniciales") {
    actualizarNumerosDisponibles(data.numeros);
  } else if (data.tipo === "seleccionado") {
    marcarNumeroComoOcupado(data.numero);
  } else if (data.tipo === "liberado") {
    marcarNumeroComoDisponible(data.numero);
  }
};

socket.onclose = function (e) {
  console.log("WebSocket cerrado");
};

function seleccionarNumero(numeroId) {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(
      JSON.stringify({
        tipo: "seleccionar_numero",
        numero_id: numeroId,
      })
    );
  } else {
    console.error(
      "WebSocket no está abierto. Estado actual:",
      socket.readyState
    );
  }
}

function liberarNumero(numero_id) {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(
      JSON.stringify({
        tipo: "liberar_numero",
        numero_id: numero_id,
      })
    );
  } else {
    console.error(
      "WebSocket no está abierto. Estado actual:",
      socket.readyState
    );
  }
}
function toggleSelection(button) {
  const numeroId = button.getAttribute("data-numero");

  // Enviar al servidor que el usuario ha seleccionado el número
  seleccionarNumero(numeroId);
}
function actualizarNumeroEstado(numeroId, estado) {
  const button = document.getElementById(`numero_${numeroId}`);

  if (estado === "ocupado") {
    button.classList.remove("btn-outline-warning");
    button.classList.add("btn-secondary", "disabled");
  } else {
    button.classList.remove("btn-secondary", "disabled");
    button.classList.add("btn-outline-warning");
  }
}
