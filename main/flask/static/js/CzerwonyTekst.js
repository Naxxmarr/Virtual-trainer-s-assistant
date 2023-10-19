document.addEventListener("DOMContentLoaded", function () {
  var selectElements = document.querySelectorAll("#zawodnik-select");

  function checkDuplicateZawodnik() {
    var selectedZawodnicy = new Set();
    var duplicateZawodnicy = new Set();

    selectElements.forEach(function (select) {
      var selectedOption = select.querySelector("option:checked");
      var selectedText = selectedOption.textContent.trim();
      var selectedName = selectedText.split(",")[0];

      if (selectedName !== "") {
        if (selectedZawodnicy.has(selectedName)) {
          duplicateZawodnicy.add(selectedName);
        } else {
          selectedZawodnicy.add(selectedName);
        }
      }
    });
    selectElements.forEach(function (select) {
      var row = select.closest("tr");
      var selectedOption = select.querySelector("option:checked");
      var selectedText = selectedOption.textContent.trim();
      var selectedName = selectedText.split(",")[0];

      if (selectedName !== "") {
        if (duplicateZawodnicy.has(selectedName)) {
          row.classList.add("red-row");
        } else {
          row.classList.remove("red-row");
        }
      }
    });
  }

  selectElements.forEach(function (select) {
    select.addEventListener("change", checkDuplicateZawodnik);
  });

  checkDuplicateZawodnik();
});
