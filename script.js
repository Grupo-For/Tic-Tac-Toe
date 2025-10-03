let board = [], turn = "X";
let p = {X: "J1", O: "J2"};
let score = {X: 0, O: 0, D: 0};
let games = 0;
let nextStarter = "X";
let gameOver = false;
let winningCells = [];

// 🆕 Historial de movimientos para deshacer
let moveHistory = [];

// Variables para rachas
let currentStreak = {X: 0, O: 0};
let bestStreak = {X: 0, O: 0};
let lastWinner = null;

const win = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
const q = id => document.getElementById(id);
// 🆕 ---- Función para cambiar temas ----
function changeTheme(theme) {
  document.body.className = document.body.classList.contains('game') ? 'game' : 'start';
  document.body.classList.add('theme-' + theme);
}

// ---- Modal confirmaciones ----
function showModal(msg, buttons=[]) {
  q("modal-msg").textContent = msg;
  let btns = q("modal-buttons");
  btns.innerHTML = "";
  buttons.forEach(b => {
    let btn = document.createElement("button");
    btn.textContent = b.text;
    btn.onclick = () => { b.action(); closeModal(); };
    btns.appendChild(btn);
  });
  q("modal").style.display = "block";
}
function closeModal() { q("modal").style.display = "none"; }

function confirmAction(action) {
  if (action === "reset") {
    showModal("¿Seguro que deseas reiniciar el marcador?", [
      {text:"Sí", action: resetScore},
      {text:"No", action: ()=>{}}
    ]);
  } else if (action === "new") {
    showModal("¿Seguro que deseas iniciar un nuevo juego?", [
      {text:"Sí", action: newGame},
      {text:"No", action: ()=>{}}
    ]);
  }
}

// ---- Inicio del juego
function start() {
  let name1 = q("p1").value.trim() || "J1";
  let name2 = q("p2").value.trim() || "J2";
  let col1 = q("colorX").value;
  let col2 = q("colorO").value;
  if (!setSymbols()) return;

  // Validaciones
  if (name1.length > 12 || name2.length > 12) {
    showModal("Los nombres no pueden superar 12 caracteres");
    return;
  }
  if (name1 === name2) {
    showModal("Los nombres de los jugadores no pueden ser iguales");
    return;
  }
  if (col1 === col2) {
    showModal("Cada jugador debe tener un color distinto");
    return;
  }

  p.X = name1;
  p.O = name2;

  q("n1").textContent = p.X;
  q("n2").textContent = p.O;

  q("register").style.display = "none";
  q("game").style.display = "block";
  q("firstTurnModal").style.display = "block";

    // 🆕 Mantener el tema al cambiar de pantalla
  let currentTheme = q("themeSelector").value;
  document.body.classList.add('theme-' + currentTheme);
  document.body.className = "game";

  score.X = score.O = score.D = 0;
  games = 0;
  clearHistory();
  updateScore();
  restart();
}

function setFirstTurn(choice) {
  if(choice === "R") {
    turn = Math.random() < 0.5 ? "X" : "O";
  } else {
    turn = choice;
  }

  nextStarter = turn;
  q("firstTurnModal").style.display = "none";
  q("game").style.display = "block";
  restart();
}

function draw() {
  q("board").innerHTML = "";
  board.forEach((v, i) => {
    let b = document.createElement("button");
    b.className = "cell";

    if (v === "X") b.textContent = p.symX;
    if (v === "O") b.textContent = p.symO;

    if (v === "X") b.style.background = q("colorX").value, b.style.color="white";
    if (v === "O") b.style.background = q("colorO").value, b.style.color="white";

    if (winningCells.includes(i)) {
      b.classList.add("winner");
    }

    b.onclick = () => move(i);
    if (gameOver) b.disabled = true;
    q("board").appendChild(b);
  });

  if (!gameOver) {
    q("turn").textContent = "Turno: " + p[turn] + " (" + turn + ")";
  } else {
    q("turn").textContent = "";
  }
  
  // 🆕 Actualizar estado del botón deshacer
  updateUndoButton();
}

function move(i) {
  if (board[i]) {
    showModal("Esa casilla ya está ocupada");
    return;
  }

  q("btnNames").disabled = true;
  
  // 🆕 Guardar el estado antes del movimiento
  saveMove(i, turn);
  
  board[i] = turn;

  let r = check();

  if (r.over) {
    games++;
    gameOver = true;

    if (r.w) {
      q("status").textContent = "Ganó " + p[r.w];
      score[r.w]++;
      winningCells = r.combo;
      addHistory("Ganó " + p[r.w], r.w);
      updateStreak(r.w);
    } else {
      q("status").textContent = "Empate";
      score.D++;
      winningCells = [];
      addHistory("Empate", null);
      updateStreak(null);
    }

    nextStarter = nextStarter === "X" ? "O" : "X";
    q("btnNames").disabled = false;
    updateScore();
  } else {
    turn = turn === "X" ? "O" : "X";
  }

  draw();
}

// 🆕 Función para guardar un movimiento en el historial
function saveMove(position, player) {
  moveHistory.push({
    position: position,
    player: player,
    boardState: [...board]
  });
}

// 🆕 Función para deshacer el último movimiento
function undoMove() {
  if (moveHistory.length === 0 || gameOver) {
    return;
  }
  let lastMove = moveHistory.pop();
  board = [...lastMove.boardState];
  turn = lastMove.player;
  draw();
}

// 🆕 Función para actualizar el estado del botón deshacer
function updateUndoButton() {
  let undoBtn = q("btnUndo");
  if (undoBtn) {
    undoBtn.disabled = moveHistory.length === 0 || gameOver;
  }
}

function updateStreak(winner) {
  if (winner) {
    if (lastWinner === winner) {
      currentStreak[winner]++;
    } else {
      currentStreak.X = winner === "X" ? 1 : 0;
      currentStreak.O = winner === "O" ? 1 : 0;
    }
    
    if (currentStreak[winner] > bestStreak[winner]) {
      bestStreak[winner] = currentStreak[winner];
    }
    
    lastWinner = winner;
  } else {
    currentStreak.X = 0;
    currentStreak.O = 0;
    lastWinner = null;
  }
}

function check() {
  for (let [a, b, c] of win) {
    if (board[a] && board[a] == board[b] && board[a] == board[c]) {
      return {over: 1, w: board[a], combo: [a,b,c]};
    }
  }
  return board.every(Boolean) ? {over: 1} : {over: 0};
}

function restart() {
  board = Array(9).fill("");
  gameOver = false;
  winningCells = [];
  moveHistory = []; // 🆕 Limpiar historial de movimientos
  q("status").textContent = "";
  turn = nextStarter;
  q("turn").textContent = "Turno: " + p[turn] + " (" + turn + ")";
  draw();
  q("btnNames").disabled = false;
}

function resetScore() {
  score.X = score.O = score.D = 0;
  games = 0;
  currentStreak.X = currentStreak.O = 0;
  bestStreak.X = bestStreak.O = 0;
  lastWinner = null;
  updateScore();
  clearHistory();
  restart();
}

function newGame() {
  q("register").style.display = "block";
  q("game").style.display = "none";
  q("p1").value = "";
  q("p2").value = "";
  document.body.className = "start";
    // 🆕 Mantener el tema al volver al inicio
  let currentTheme = q("themeSelector").value;
  document.body.classList.add('theme-' + currentTheme);
}

// ---- Modal cambiar nombres ----
function openNameModal() {
  q("nameX").value = p.X;
  q("nameO").value = p.O;
  q("nameError").textContent = "";
  q("nameModal").style.display = "block";
}
function closeNameModal() { q("nameModal").style.display = "none"; }

function saveNames() {
  let nX = q("nameX").value.trim() || "J1";
  let nO = q("nameO").value.trim() || "J2";

  if (nX.length > 12 || nO.length > 12) {
    q("nameError").textContent = "Máximo 12 caracteres";
    return;
  }
  if (nX === nO) {
    q("nameError").textContent = "Los nombres deben ser distintos";
    return;
  }

  p.X = nX;
  p.O = nO;

  updateScore();
  restart();
  closeNameModal();
}

function validateMaxLength(p1Symbol, p2Symbol) {
  if (p1Symbol.length > 3 || p2Symbol.length > 3) {
    throw new Error("Los símbolos no pueden tener más de 3 caracteres");
  }
}

function validateDifferent(p1Symbol, p2Symbol) {
  if (p1Symbol === p2Symbol) {
    throw new Error("Los símbolos deben ser distintos");
  }
}

function setSymbols() {
  let p1Symbol = q("symbolX").value.trim() || "X";
  let p2Symbol = q("symbolO").value.trim() || "O";

  try {
    validateMaxLength(p1Symbol, p2Symbol);
  } catch (err) {
    showModal(err.message);
    return false;
  }

  try {
    validateDifferent(p1Symbol, p2Symbol);
  } catch (err) {
    showModal(err.message);
    return false;
  }

  p.symX = p1Symbol;
  p.symO = p2Symbol;
  return true;
}

// ---- Utilidades ----
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

function addHistory(text, winnerSymbol) {
  let row = q("history").insertRow(-1);
  let c1 = row.insertCell(0);
  let c2 = row.insertCell(1);

  c1.textContent = games;
  c2.textContent = text;

  if (winnerSymbol === "X") {
    c1.style.background = q("colorX").value;
  } else if (winnerSymbol === "O") {
    c1.style.background = q("colorO").value;
  } else {
    c1.style.background = "#999";
  }
}
function clearHistory() {
  q("history").innerHTML = "<tr><th>#</th><th>Resultado</th></tr>";
}
// ---- NUEVA FUNCIÓN ESTADÍSTICAS ----
function openStats() {
  let total = games || 1; // evitar división entre 0
  let porcX = ((score.X / total) * 100).toFixed(1);
  let porcO = ((score.O / total) * 100).toFixed(1);
  let porcD = ((score.D / total) * 100).toFixed(1);

  q("statsX").textContent = `${p.X} (${p.symX}): ${score.X} victorias (${porcX}%)<br>Racha actual: ${currentStreak.X} | Mejor racha: ${bestStreak.X}`;
  q("statsO").textContent = `${p.O} (${p.symO}): ${score.O} victorias (${porcO}%)<br>Racha actual: ${currentStreak.O} | Mejor racha: ${bestStreak.O}`;
  q("statsDraws").textContent = `Empates: ${score.D} (${porcD}%)`;

  q("statsModal").style.display = "block";
}

function closeStats() {
  q("statsModal").style.display = "none";
}
