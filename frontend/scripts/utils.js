// Funciones de utilidad y tema
function updateScore() {
  q("s1").textContent = score.X;
  q("s2").textContent = score.O;
  q("draws").textContent = score.D;

  q("n1").textContent = p.X;
  q("n2").textContent = p.O;

  if (!gameOver) {
    q("turn").textContent = "Turno: " + p[turn] + " (" + turn + ")";
  }
}

function initTheme() {
  document.body.classList.toggle('dark', darkMode);
  updateThemeButton();
}

function toggleTheme() {
  darkMode = !darkMode;
  document.body.classList.toggle('light', !darkMode);
  localStorage.setItem('darkMode', darkMode);
  updateThemeButton();
}

function updateThemeButton() {
  const btn = q('themeToggle');
  if (darkMode) {
    btn.textContent = '☀️ Modo Claro';
    btn.style.background = '#333';
    btn.style.color = 'white';
  } else {
    btn.textContent = '🌙 Modo Oscuro';
    btn.style.background = '#f0f0f0';
    btn.style.color = 'black';
  }
}