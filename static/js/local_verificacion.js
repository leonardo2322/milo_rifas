document.addEventListener("DOMContentLoaded", function () {
  function verificarExpiracion() {
    const currentPath = window.location.pathname; // Obtiene la ruta actual

    const rawData = localStorage.getItem("numeros_seleccionados");
    let data = null;

    if (rawData) {
      try {
        data = JSON.parse(rawData);
      } catch (error) {
        console.error("Error parsing localStorage data", error);
        localStorage.removeItem("numeros_seleccionados");
      }
    } else {
      if (currentPath !== "/seleccionar_numero/") {
        window.location.href = "/seleccionar_numero/";
      }
      return;
    }

    // Verifica el tiempo
    const tiempoActual = Date.now();
    const tiempoGuardado = data.timestamp || 0;
    const diferenciaMinutos = (tiempoActual - tiempoGuardado) / (1000 * 60);

    if (diferenciaMinutos > 30) {
      localStorage.removeItem("numeros_seleccionados");
      if (currentPath !== "/seleccionar_numero/") {
        window.location.href = "/seleccionar_numero/";
      }
      return;
    }
  }
  verificarExpiracion();
  setInterval(verificarExpiracion, 1800000);
});
