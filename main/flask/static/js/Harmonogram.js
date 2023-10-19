document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");
  var calendar = new FullCalendar.Calendar(calendarEl, {
    locale: "pl",
    headerToolbar: {
      left: "prev,next today",
      center: "title",
      right: "dayGridMonth,timeGridWeek,timeGridDay",
    },
    initialDate: "2023-01-12",
    navLinks: true,
    selectable: true,
    selectMirror: true,
    select: function (arg) {
      var title = prompt("Nazwa zdarzenia:");
      if (title) {
        var eventData = {
          title: title,
          start: arg.start,
          end: arg.end,
          allDay: arg.allDay,
        };

        fetch("/events", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(eventData),
        })
          .then(function (response) {
            return response.json();
          })
          .then(function (data) {
            eventData.id = data.id;
            calendar.addEvent(eventData);
          })
          .catch(function (error) {
            console.error("Wystąpił błąd podczas tworzenia zdarzenia:", error);
          });
      }
      calendar.unselect();
    },
    eventClick: function (arg) {
      if (confirm("Czy chcesz usunąć zdarzenie?")) {
        fetch("/events/" + arg.event.id, {
          method: "DELETE",
        })
          .then(function () {
            arg.event.remove();
          })
          .catch(function (error) {
            console.error("Wystąpił błąd podczas usuwania zdarzenia:", error);
          });
      } else {
        var title = prompt("Nowa nazwa zdarzenia:", arg.event.title);
        if (title) {
          var eventData = {
            title: title,
            start: arg.event.start,
            end: arg.event.end,
            allDay: arg.event.allDay,
          };

          fetch("/events/" + arg.event.id, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(eventData),
          })
            .then(function () {
              arg.event.setProp("title", title);
            })
            .catch(function (error) {
              console.error(
                "Wystąpił błąd podczas aktualizowania zdarzenia:",
                error
              );
            });
        }
      }
    },
    editable: true,
    dayMaxEvents: true,
    timeZone: "Europe/Warsaw",
  });

  calendar.render();

  fetch("/get-events")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      var events = data.events;
      calendar.addEventSource(events);
    })
    .catch(function (error) {
      console.error("Wystąpił błąd podczas pobierania wydarzeń:", error);
    });
});
