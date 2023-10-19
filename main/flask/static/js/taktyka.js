var canvas = document.getElementById("field");
var ctx = canvas.getContext("2d");
ctx.beginPath();
ctx.rect(0, 0, canvas.width, canvas.height);
ctx.fillStyle = "#060";
ctx.fill();
ctx.lineWidth = 1;
ctx.strokeStyle = "#FFF";
ctx.stroke();
ctx.closePath();

ctx.fillStyle = "#FFF";
ctx.beginPath();
ctx.moveTo(canvas.width / 2, 0);
ctx.lineTo(canvas.width / 2, canvas.height);
ctx.stroke();
ctx.closePath();
ctx.beginPath();
ctx.arc(canvas.width / 2, canvas.height / 2, 73, 0, 2 * Math.PI, false);
ctx.stroke();
ctx.closePath();
ctx.beginPath();
ctx.arc(canvas.width / 2, canvas.height / 2, 2, 0, 2 * Math.PI, false);
ctx.fill();
ctx.closePath();

ctx.beginPath();
ctx.rect(0, (canvas.height - 322) / 2, 132, 322);
ctx.stroke();
ctx.closePath();
ctx.beginPath();
ctx.rect(0, (canvas.height - 146) / 2, 44, 146);
ctx.stroke();
ctx.closePath();
ctx.beginPath();
ctx.moveTo(1, canvas.height / 2 - 22);
ctx.lineTo(1, canvas.height / 2 + 22);
ctx.lineWidth = 2;
ctx.stroke();
ctx.closePath();
ctx.lineWidth = 1;

ctx.beginPath();
ctx.arc(88, canvas.height / 2, 1, 0, 2 * Math.PI, true);
ctx.fill();
ctx.closePath();
ctx.beginPath();
ctx.arc(88, canvas.height / 2, 73, 0.29 * Math.PI, 1.71 * Math.PI, true);
ctx.stroke();
ctx.closePath();

ctx.beginPath();
ctx.rect(canvas.width - 132, (canvas.height - 322) / 2, 132, 322);
ctx.stroke();
ctx.closePath();
ctx.beginPath();
ctx.rect(canvas.width - 44, (canvas.height - 146) / 2, 44, 146);
ctx.stroke();
ctx.closePath();
ctx.beginPath();
ctx.moveTo(canvas.width - 1, canvas.height / 2 - 22);
ctx.lineTo(canvas.width - 1, canvas.height / 2 + 22);
ctx.lineWidth = 2;
ctx.stroke();
ctx.closePath();
ctx.lineWidth = 1;
ctx.beginPath();
ctx.arc(canvas.width - 88, canvas.height / 2, 1, 0, 2 * Math.PI, true);
ctx.fill();
ctx.closePath();
ctx.beginPath();
ctx.arc(
  canvas.width - 88,
  canvas.height / 2,
  73,
  0.71 * Math.PI,
  1.29 * Math.PI,
  false
);
ctx.stroke();
ctx.closePath();

ctx.beginPath();
ctx.arc(0, 0, 8, 0, 0.5 * Math.PI, false);
ctx.stroke();
ctx.closePath();
ctx.beginPath();
ctx.arc(0, canvas.height, 8, 0, 2 * Math.PI, true);
ctx.stroke();
ctx.closePath();
ctx.beginPath();
ctx.arc(canvas.width, 0, 8, 0.5 * Math.PI, 1 * Math.PI, false);
ctx.stroke();
ctx.closePath();
ctx.beginPath();
ctx.arc(canvas.width, canvas.height, 8, 1 * Math.PI, 1.5 * Math.PI, false);
var redCount = 0;
var blueCount = 0;

canvas.addEventListener("mousedown", function (event) {
  var rect = canvas.getBoundingClientRect();
  var x = event.clientX - rect.left;
  var y = event.clientY - rect.top;

  if (event.button === 0 && redCount < 11) {
    var player = document.createElement("div");
    player.className = "player red";
    player.style.left = x + "px";
    player.style.top = y + "px";
    document.getElementById("field-container").appendChild(player);
    redCount++;
    player.addEventListener("mousedown", startDrag);
    player.addEventListener("mouseup", stopDrag);
  } else if (event.button === 2 && blueCount < 11) {
    var player = document.createElement("div");
    player.className = "player blue";
    player.style.left = x + "px";
    player.style.top = y + "px";
    document.getElementById("field-container").appendChild(player);
    blueCount++;
    player.addEventListener("contextmenu", function (event) {
      event.preventDefault();
    });
    player.addEventListener("mousedown", startDrag);
    player.addEventListener("mouseup", stopDrag);
  }
});

var activePlayer;

function startDrag(event) {
  if (
    (this.classList.contains("red") && event.button === 0) ||
    (this.classList.contains("blue") && event.button === 2)
  ) {
    activePlayer = this;
    var rect = canvas.getBoundingClientRect();
    var x = event.clientX - rect.left;
    var y = event.clientY - rect.top;
    this.offsetX = x - parseInt(this.style.left, 10);
    this.offsetY = y - parseInt(this.style.top, 10);
  }
}

function stopDrag(event) {
  activePlayer = null;
  if (
    (this.classList.contains("red") && event.button === 0) ||
    (this.classList.contains("blue") && event.button === 2)
  ) {
    event.preventDefault();
  }
}

canvas.addEventListener("mousemove", function (event) {
  if (activePlayer) {
    var rect = canvas.getBoundingClientRect();
    var x = event.clientX - rect.left;
    var y = event.clientY - rect.top;
    activePlayer.style.left = x - activePlayer.offsetX + "px";
    activePlayer.style.top = y - activePlayer.offsetY + "px";
  }
});

canvas.addEventListener("contextmenu", function (event) {
  event.preventDefault();
});
