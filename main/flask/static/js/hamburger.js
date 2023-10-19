const rozMenu = document.querySelector(".roz-menu");
const navbar = document.querySelector(".navbar");

rozMenu.addEventListener("click", () => {
  navbar.classList.toggle("active");
});
