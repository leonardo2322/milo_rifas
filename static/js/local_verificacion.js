document.addEventListener("DOMContentLoaded", function () {
  const data = JSON.parse(localStorage.getItem("numeros_seleccionados"));

  if (!data || !data.numeros || data.numeros.length === 0) {
    // No hay selección válida
    window.location.href = "/seleccionar_numero/";
    return;
  }

  const tiempoActual = Date.now();
  const tiempoGuardado = data.timestamp || 0;
  const diferenciaMinutos = (tiempoActual - tiempoGuardado) / (1000 * 60);

  if (diferenciaMinutos > 15) {
    // 15 minutos, por ejemplo
    // Si pasaron más de 15 minutos, consideramos la selección inválida
    localStorage.removeItem("numeros_seleccionados");
    window.location.href = "/seleccionar_numero/";
  }
});
