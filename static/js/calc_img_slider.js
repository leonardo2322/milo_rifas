document.addEventListener("DOMContentLoaded", () => {
  const sliderTrack = document.querySelector(".slider-track");
  const slides = document.querySelectorAll(".slide");

  if (sliderTrack && slides.length > 0) {
    sliderTrack.style.width = `${slides.length * 100}%`;
    slides.forEach((slide) => {
      slide.style.width = `${100 / slides.length}%`;
    });
  }
});
