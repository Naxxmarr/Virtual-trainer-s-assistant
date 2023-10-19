function openModal(modalId) {
  document.querySelector(`#${modalId}`).style.display = "block";
}

function closeModal(modalId) {
  document.querySelector(`#${modalId}`).style.display = "none";
}

window.onclick = function (event) {
  if (event.target.classList.contains("modal")) {
    event.target.style.display = "none";
  }
};
