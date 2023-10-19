$(document).ready(function () {
  var fromData;
  $("#doajax").submit(function (e) {
    e.preventDefault();
    formData = $(this).serialize();
    sendAjaxRequest(formData, "#thebest");
  });

  $("#doajax2").submit(function (e) {
    e.preventDefault();
    console.log("Przycisk Wyszukaj został kliknięty.");
    formData = $(this).serialize();
    sendAjaxRequest(formData, "#thebest2");
  });

  $("#doajax3").submit(function (e) {
    e.preventDefault();
    console.log("Przycisk Wyszukaj został kliknięty.");
    formData = $(this).serialize();
    sendAjaxRequest(formData, "#thebest3");
  });

  function sendAjaxRequest(formData, resultId) {
    $.ajax({
      type: "POST",
      url: "/matchhim",
      data: formData,
      dataType: "json",
      success: function (response) {
        if (response.naj_obronca) {
          var naj_obroncaHTML = `
                      <h2>Najlepszy środkowy obrońca:</h2>
                      <p>Imię i Nazwisko: <strong>${response.naj_obronca.Imie}</strong></p>
                      <p>Wzrost: ${response.naj_obronca.Wzrost}</p>
                      <p>Pozycja: ${response.naj_obronca.Pozycja}</p>
                      <p>Siła: ${response.naj_obronca.Sila}</p>
                      <p>Szybkość: ${response.naj_obronca.Szybkosc}</p>
                      <p>Drybling: ${response.naj_obronca.Drybling}</p>
                      <p>Defensywa: ${response.naj_obronca.Defensywa}</p>
                      <p>Podania: ${response.naj_obronca.Podania}</p>
                      <p>Strzał: ${response.naj_obronca.Strzaly}</p>
                      <p>Preferowana noga: ${response.naj_obronca.Preferowana_Noga}</p>
                      <p>Wynik ogólny: ${response.naj_obronca.score}</p>
                  `;
          $(resultId).html(naj_obroncaHTML);
        } else if (response.naj_lewyOB) {
          var naj_lewyOBHTML = `
                      <h2>Najlepszy lewy obrońca:</h2>
                      <p>Imię i Nazwisko: <strong>${response.naj_lewyOB.Imie}</strong></p>
                      <p>Wzrost: ${response.naj_lewyOB.Wzrost}</p>
                      <p>Pozycja: ${response.naj_lewyOB.Pozycja}</p>
                      <p>Siła: ${response.naj_lewyOB.Sila}</p>
                      <p>Szybkość: ${response.naj_lewyOB.Szybkosc}</p>
                      <p>Drybling: ${response.naj_lewyOB.Drybling}</p>
                      <p>Defensywa: ${response.naj_lewyOB.Defensywa}</p>
                      <p>Podania: ${response.naj_lewyOB.Podania}</p>
                      <p>Strzał: ${response.naj_lewyOB.Strzaly}</p>
                      <p>Preferowana noga: ${response.naj_lewyOB.Preferowana_Noga}</p>
                      <p>Wynik ogólny: ${response.naj_lewyOB.score}</p>
                  `;
          $(resultId).html(naj_lewyOBHTML);
        } else if (response.naj_prawyOB) {
          var naj_prawyOBHTML = `
                      <h2>Najlepszy prawy obrońca:</h2>
                      <p>Imię i Nazwisko:<strong>${response.naj_prawyOB.Imie}</strong></p>
                      <p>Wzrost: ${response.naj_prawyOB.Wzrost}</p>
                      <p>Pozycja: ${response.naj_prawyOB.Pozycja}</p>
                      <p>Siła: ${response.naj_prawyOB.Sila}</p>
                      <p>Szybkość: ${response.naj_prawyOB.Szybkosc}</p>
                      <p>Drybling: ${response.naj_prawyOB.Drybling}</p>
                      <p>Defensywa: ${response.naj_prawyOB.Defensywa}</p>
                      <p>Podania: ${response.naj_prawyOB.Podania}</p>
                      <p>Strzał: ${response.naj_prawyOB.Strzaly}</p>
                      <p>Preferowana noga: ${response.naj_prawyOB.Preferowana_Noga}</p>
                      <p>Wynik ogólny: ${response.naj_prawyOB.score}</p>

                  `;
          $(resultId).html(naj_prawyOBHTML);
        } else if (response.naj_bramkarz) {
          var naj_bramkarzOBHTML = `
                      <h2>Najlepszy prawy obrońca:</h2>
                      <p>Imię i Nazwisko: <strong>${response.naj_bramkarz.Imie}</strong></p>
                      <p>Wzrost: ${response.naj_bramkarz.Wzrost}</p>
                      <p>Pozycja: ${response.naj_bramkarz.Pozycja}</p>
                      <p>Siła: ${response.naj_bramkarz.Sila}</p>
                      <p>Szybkość: ${response.naj_bramkarz.Szybkosc}</p>
                      <p>Drybling: ${response.naj_bramkarz.Drybling}</p>
                      <p>Defensywa: ${response.naj_bramkarz.Defensywa}</p>
                      <p>Podania: ${response.naj_bramkarz.Podania}</p>
                      <p>Strzał: ${response.naj_bramkarz.Strzaly}</p>
                      <p>Preferowana noga: ${response.naj_bramkarz.Preferowana_Noga}</p>
                      <p>Wynik ogólny: ${response.naj_bramkarz.score}</p>

                  `;
          $(resultId).html(naj_bramkarzOBHTML);
        } else if (response.naj_spd) {
          var naj_spdHTML = `
                      <h2>Najlepszy defensywny pomocnik :</h2>
                      <p>Imię i Nazwisko: <strong>${response.naj_spd.Imie}</strong></p>
                      <p>Wzrost: ${response.naj_spd.Wzrost}</p>
                      <p>Pozycja: ${response.naj_spd.Pozycja}</p>
                      <p>Siła: ${response.naj_spd.Sila}</p>
                      <p>Szybkość: ${response.naj_spd.Szybkosc}</p>
                      <p>Drybling: ${response.naj_spd.Drybling}</p>
                      <p>Defensywa: ${response.naj_spd.Defensywa}</p>
                      <p>Podania: ${response.naj_spd.Podania}</p>
                      <p>Strzał: ${response.naj_spd.Strzaly}</p>
                      <p>Preferowana noga: ${response.naj_spd.Preferowana_Noga}</p>
                      <p>Wynik ogólny: ${response.naj_spd.score}</p>
          `;
          $(resultId).html(naj_spdHTML);
        } else if (response.naj_sp) {
          var naj_spHTML = `
                      <h2>Najlepszy środkowy pomocnik :</h2>
                      <p>Imię i Nazwisko: <strong>${response.naj_sp.Imie}</strong></p>
                      <p>Wzrost: ${response.naj_sp.Wzrost}</p>
                      <p>Pozycja: ${response.naj_sp.Pozycja}</p>
                      <p>Siła: ${response.naj_sp.Sila}</p>
                      <><p>Szybkość: ${response.naj_sp.Szybkosc}</p>
                      <><p>Drybling: ${response.naj_sp.Drybling}</p>
                      <p>Defensywa: ${response.naj_sp.Defensywa}</p>
                      <><p>Podania: ${response.naj_sp.Podania}</p>
                      <><p>Strzał: ${response.naj_sp.Strzaly}</p>
                      <p>Preferowana noga: ${response.naj_sp.Preferowana_Noga}</p>
                      <p>Wynik ogólny: ${response.naj_sp.score}</p>
          `;
          $(resultId).html(naj_spHTML);
        } else if (response.naj_spo) {
          var naj_spoHTML = `
                      <h2>Najlepszy ofensywny pomocnik :</h2>
                      <p>Imię i Nazwisko: <strong>${response.naj_spo.Imie}</strong></p>
                      <p>Wzrost: ${response.naj_spo.Wzrost}</p>
                      <p>Pozycja: ${response.naj_spo.Pozycja}</p>
                      <p>Siła: ${response.naj_spo.Sila}</p>
                      <p>Szybkość: ${response.naj_spo.Szybkosc}</p>
                      <p>Drybling: ${response.naj_spo.Drybling}</p>
                      <p>Defensywa: ${response.naj_spo.Defensywa}</p>
                      <p>Podania: ${response.naj_spo.Podania}</p>
                      <p>Strzał: ${response.naj_spo.Strzaly}</p>
                      <p>Preferowana noga: ${response.naj_spo.Preferowana_Noga}</p>
                      <p>Wynik ogólny: ${response.naj_spo.score}</p>
          `;
          $(resultId).html(naj_spoHTML);
        } else if (response.naj_pp) {
          var naj_ppHTML = `
                      <h2>Najlepszy prawy pomocnik :</h2>
                      <p>Imię i Nazwisko: <strong>${response.naj_pp.Imie}</strong></p>
                      <p>Wzrost: ${response.naj_pp.Wzrost}</p>
                      <p>Pozycja: ${response.naj_pp.Pozycja}</p>
                      <p>Siła: ${response.naj_pp.Sila}</p>
                      <p>Szybkość: ${response.naj_pp.Szybkosc}</p>
                      <p>Drybling: ${response.naj_pp.Drybling}</p>
                      <p>Defensywa: ${response.naj_pp.Defensywa}</p>
                      <p>Podania: ${response.naj_pp.Podania}</p>
                      <p>Strzał: ${response.naj_pp.Strzaly}</p>
                      <p>Preferowana noga: ${response.naj_pp.Preferowana_Noga}</p>
                      <p>Wynik ogólny: ${response.naj_pp.score}</p>
          `;
          $(resultId).html(naj_ppHTML);
        } else if (response.naj_lp) {
          var naj_lpHTML = `
                      <h2>Najlepszy lewy pomocnik :</h2>
                      <p>Imię i Nazwisko: <strong>${response.naj_lp.Imie}</strong></p>
                      <p>Wzrost: ${response.naj_lp.Wzrost}</p>
                      <p>Pozycja: ${response.naj_lp.Pozycja}</p>
                      <p>Siła: ${response.naj_lp.Sila}</p>
                      <p>Szybkość: ${response.naj_lp.Szybkosc}</p>
                      <p>Drybling: ${response.naj_lp.Drybling}</p>
                      <p>Defensywa: ${response.naj_lp.Defensywa}</p>
                      <p>Podania: ${response.naj_lp.Podania}</p>
                      <p>Strzał: ${response.naj_lp.Strzaly}</p>
                      <p>Preferowana noga: ${response.naj_lp.Preferowana_Noga}</p>
                      <p>Wynik ogólny: ${response.naj_lp.score}</p>
          `;
          $(resultId).html(naj_lpHTML);
        } else if (response.naj_ls) {
          var naj_lsHTML = `
                      <h2>Najlepszy lewy skrzydłowy :</h2>
                      <p>Imię i Nazwisko: <strong>${response.naj_ls.Imie}</strong></p>
                      <p>Wzrost: ${response.naj_ls.Wzrost}</p>
                      <p>Pozycja: ${response.naj_ls.Pozycja}</p>
                      <p>Siła: ${response.naj_ls.Sila}</p>
                      <p>Szybkość: ${response.naj_ls.Szybkosc}</p>
                      <p>Drybling: ${response.naj_ls.Drybling}</p>
                      <p>Defensywa: ${response.naj_ls.Defensywa}</p>
                      <p>Podania: ${response.naj_ls.Podania}</p>
                      <p>Strzał: ${response.naj_ls.Strzaly}</p>
                      <p>Preferowana noga: ${response.naj_ls.Preferowana_Noga}</p>
                      <p>Wynik ogólny: ${response.naj_ls.score}</p>
          `;
          $(resultId).html(naj_lsHTML);
        } else if (response.naj_ps) {
          var naj_psHTML = `
                      <h2>Najlepszy prawy skrzydłowy :</h2>
                      <p>Imię i Nazwisko: <strong>${response.naj_ps.Imie}</strong></p>
                      <p>Wzrost: ${response.naj_ps.Wzrost}</p>
                      <p>Pozycja: ${response.naj_ps.Pozycja}</p>
                      <p>Siła: ${response.naj_ps.Sila}</p>
                      <p>Szybkość: ${response.naj_ps.Szybkosc}</p>
                      <p>Drybling: ${response.naj_ps.Drybling}</p>
                      <p>Defensywa: ${response.naj_ps.Defensywa}</p>
                      <p>Podania: ${response.naj_ps.Podania}</p>
                      <p>Strzał: ${response.naj_ps.Strzaly}</p>
                      <p>Preferowana noga: ${response.naj_ps.Preferowana_Noga}</p>
                      <p>Wynik ogólny: ${response.naj_ps.score}</p>
          `;
          $(resultId).html(naj_psHTML);
        } else if (response.naj_n) {
          var naj_nHTML = `
                      <h2>Najlepszy napastnik :</h2>
                      <p>Imię i Nazwisko: <strong>${response.naj_n.Imie}</strong></p>
                      <p>Wzrost: ${response.naj_n.Wzrost}</p>
                      <p>Pozycja: ${response.naj_n.Pozycja}</p>
                      <p>Siła: ${response.naj_n.Sila}</p>
                      <p>Szybkość: ${response.naj_n.Szybkosc}</p>
                      <p>Drybling: ${response.naj_n.Drybling}</p>
                      <p>Defensywa: ${response.naj_n.Defensywa}</p>
                      <p>Podania: ${response.naj_n.Podania}</p>
                      <p>Strzał: ${response.naj_n.Strzaly}</p>
                      <p>Preferowana noga: ${response.naj_n.Preferowana_Noga}</p>
                      <p>Wynik ogólny: ${response.naj_n.score}</p>
          `;
          $(resultId).html(naj_nHTML);
        }
        $("#nextdefenders").html(response);
        $("#nextdefenders2").html(response);
        $("#nextdefenders3").html(response);

        var resztaHTML = "";
        for (var i = 0; i < response.reszta.length; i++) {
          var zawodnik = response.reszta[i];
          resztaHTML += `
          <option value="${zawodnik.Imie}">
        ${zawodnik.Imie}, Wynik: ${zawodnik.score}
           </option>
            `;
        }
        $("#reszta-obroncow").html(resztaHTML);
        $("#reszta-obroncow2").html(resztaHTML);
        $("#reszta-obroncow3").html(resztaHTML);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.log("Błąd żądania AJAX:", textStatus, errorThrown);
      },
    });
  }
});
