// Funciones del temporizador
function startTimer() {
  clearInterval(timerInterval);
  seconds = 0;
  q("timer").textContent = "⏱ Tiempo: 0s";
  timerInterval = setInterval(() => {
    seconds++;
    q("timer").textContent = "⏱ Tiempo: " + seconds + "s";
  }, 1000);
}

function stopTimer() {
  clearInterval(timerInterval);
}