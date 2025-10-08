let currentProfile = null;
const API_URL = 'http://localhost:5000';
let darkMode = localStorage.getItem('darkMode') === 'true';
let board = [], turn = "X";
let p = {X: "J1", O: "J2"};
let score = {X: 0, O: 0, D: 0};
let games = 0;
let nextStarter = "X";
let gameOver = false; // 🚩 control para bloquear tablero
let winningCells = []; // 🔥 nuevas casillas ganadoras
let timerInterval, seconds = 0;
let moveHistory = [];


const win = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
const q = id => document.getElementById(id);

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

  document.body.className = "game";

  score.X = score.O = score.D = 0;
  games = 0;
  clearHistory();
  updateScore();
  restart();


  initTheme(); 
}


function initTheme() {
    document.body.classList.toggle('dark', darkMode);
    updateThemeButton();

}

function setFirstTurn(choice) {
  if(choice === "R") {
    turn = Math.random() < 0.5 ? "X" : "O";
  } else {
    turn = choice;
  }

  nextStarter = turn; // guardamos para alternancia
  q("firstTurnModal").style.display = "none"; // cerramos modal
  q("game").style.display = "block"; // vamos al tablero
  restart(); // inicia la partida con 'turn' elegido
}

function draw() {
  q("board").innerHTML = "";
  board.forEach((v, i) => {
    let b = document.createElement("button");
    b.className = "cell";

    // asignar símbolo
    if (v === "X") b.textContent = p.symX;
    if (v === "O") b.textContent = p.symO;

    // aplicar color de jugador
    if (v === "X") b.style.background = q("colorX").value, b.style.color="white";
    if (v === "O") b.style.background = q("colorO").value, b.style.color="white";

    // 🔥 resaltar si está en línea ganadora
    if (winningCells.includes(i)) {
      b.classList.add("winner");
    }

    b.onclick = () => move(i);
    if (gameOver) b.disabled = true;
    q("board").appendChild(b);
  });

  // mostrar turno solo si no terminó la partida
  if (!gameOver) {
    q("turn").textContent = "Turno: " + p[turn] + " (" + turn + ")";
  } else {
    q("turn").textContent = "";
  }
  updateUndoButton();
}



function move(i) {
  if (board[i]) {
    showModal("Esa casilla ya está ocupada");
    return;
  }

  q("btnNames").disabled = true;
  saveMove(i, turn);

  board[i] = turn;

  let r = check();

  if (r.over) {
    stopTimer();
    games++;
    gameOver = true;

    if (r.w) {
      q("status").textContent = "Ganó " + p[r.w];
      score[r.w]++;
      winningCells = r.combo; // 🔥 guardar casillas ganadoras
      addHistory("Ganó " + p[r.w], r.w);
    } else {
      q("status").textContent = "Empate";
      score.D++;
      winningCells = []; // empate → no hay casillas
      addHistory("Empate", null);
    }

    nextStarter = nextStarter === "X" ? "O" : "X";
    q("btnNames").disabled = false;
    updateScore();
  } else {
    turn = turn === "X" ? "O" : "X";
  }

  draw();
}

function check() {
  for (let [a, b, c] of win) {
    if (board[a] && board[a] == board[b] && board[a] == board[c]) {
      return {over: 1, w: board[a], combo: [a,b,c]}; // 🔥 devolver también la combinación
    }
  }
  return board.every(Boolean) ? {over: 1} : {over: 0};
}

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

function restart() {
  board = Array(9).fill("");
  gameOver = false;
  winningCells = []; // 🔥 limpiar al reiniciar

  moveHistory = [];
  q("status").textContent = "";
  turn = nextStarter;
  q("turn").textContent = "Turno: " + p[turn] + " (" + turn + ")";
  draw();
  q("btnNames").disabled = false;
  startTimer();
}

function resetScore() {
  score.X = score.O = score.D = 0;
  games = 0;
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
  closeNameModal(); // 🔥 cerrar modal
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

  // Primer try/catch → longitud
  try {
    validateMaxLength(p1Symbol, p2Symbol);
  } catch (err) {
    showModal(err.message);
    return false;
  }

  // Segundo try/catch → que no sean iguales
  try {
    validateDifferent(p1Symbol, p2Symbol);
  } catch (err) {
    showModal(err.message);
    return false;
  }

  // Si pasa todas las validaciones → se guardan
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

  // 🔥 actualizar también turno
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
    c1.style.background = "#999"; // gris para empate
  }
}
function clearHistory() {
  q("history").innerHTML = "<tr><th>#</th><th>Resultado</th></tr>";
}

function saveMove(position, player) {
  moveHistory.push({
    position: position,
    player: player,
    boardState: [...board]
  });
}

function undoMove() {
  if (moveHistory.length === 0 || gameOver) {
    return;
  }
  let lastMove = moveHistory.pop();
  board = [...lastMove.boardState];
  turn = lastMove.player;
  draw();
}

function updateUndoButton() {
  let undoBtn = q("btnUndo");
  if (undoBtn) {
    undoBtn.disabled = moveHistory.length === 0 || gameOver;
  }
}
// ---- NUEVA FUNCIÓN ESTADÍSTICAS ----
function openStats() {
  let total = games || 1; // evitar división entre 0
  let porcX = ((score.X / total) * 100).toFixed(1);
  let porcO = ((score.O / total) * 100).toFixed(1);
  let porcD = ((score.D / total) * 100).toFixed(1);

  q("statsX").textContent = `${p.X} (${p.symX}): ${score.X} victorias (${porcX}%)`;
  q("statsO").textContent = `${p.O} (${p.symO}): ${score.O} victorias (${porcO}%)`;
  q("statsDraws").textContent = `Empates: ${score.D} (${porcD}%)`;

  q("statsModal").style.display = "block";
}

function closeStats() {
  q("statsModal").style.display = "none";
}


function toggleTheme() {
    darkMode = !darkMode;
    document.body.classList.toggle('dark', darkMode);
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
// ---- Funciones de Perfil ----
function openProfileModal() {
    q('profileModal').style.display = 'block';
    if (currentProfile) {
        showProfileInfo();
    } else {
        showLoginForm();
    }
}

function closeProfileModal() {
    q('profileModal').style.display = 'none';
}

function showLoginForm() {
    q('profileLogin').style.display = 'block';
    q('profileCreate').style.display = 'none';
    q('profileInfo').style.display = 'none';
    q('profileError').textContent = '';
}

function showCreateForm() {
    q('profileLogin').style.display = 'none';
    q('profileCreate').style.display = 'block';
    q('profileInfo').style.display = 'none';
    q('profileError').textContent = '';
}

function showProfileInfo() {
    q('profileLogin').style.display = 'none';
    q('profileCreate').style.display = 'none';
    q('profileInfo').style.display = 'block';
    q('profileError').textContent = '';
    
    if (currentProfile) {
        q('profileDisplayName').textContent = currentProfile.nombre;
        q('profileDisplayPerfil').textContent = currentProfile.nombre_perfil;
        const stats = currentProfile.estadisticas;
        q('profileStats').textContent = 
            `Victorias: ${stats.victorias} | Empates: ${stats.empates} | Derrotas: ${stats.derrotas}`;
    }
}

async function loginProfile() {
    const profileName = q('loginName').value.trim();
    if (!profileName) {
        q('profileError').textContent = 'Ingresa tu nombre de perfil';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/perfiles`);
        const data = await response.json();
        
        const profile = data.perfiles.find(p => p.nombre_perfil === profileName);
        if (profile) {
            currentProfile = profile;
            updateProfileDisplay();
            showProfileInfo();
            loadProfilePreferences();
        } else {
            q('profileError').textContent = 'Perfil no encontrado';
        }
    } catch (error) {
        q('profileError').textContent = 'Error al conectar con el servidor';
        console.error('Error:', error);
    }
}

async function createProfile() {
    const nombre = q('createNombre').value.trim();
    const nombrePerfil = q('createPerfil').value.trim();
    
    if (!nombre || !nombrePerfil) {
        q('profileError').textContent = 'Completa todos los campos';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/perfiles`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nombre: nombre,
                nombre_perfil: nombrePerfil,
                tipo_perfil: 'jugador'
            })
        });

        if (response.ok) {
            const data = await response.json();
            currentProfile = data.perfil;
            updateProfileDisplay();
            showProfileInfo();
            q('createNombre').value = '';
            q('createPerfil').value = '';
        } else {
            const error = await response.json();
            q('profileError').textContent = error.error || 'Error al crear perfil';
        }
    } catch (error) {
        q('profileError').textContent = 'Error al conectar con el servidor';
        console.error('Error:', error);
    }
}

function logoutProfile() {
    currentProfile = null;
    updateProfileDisplay();
    showLoginForm();
}

function updateProfileDisplay() {
    const display = q('current-profile');
    if (currentProfile) {
        display.textContent = `Perfil: ${currentProfile.nombre_perfil}`;
        display.style.color = 'green';
        display.style.fontWeight = 'bold';
    } else {
        display.textContent = 'Sin perfil activo';
        display.style.color = 'red';
    }
}

function loadProfilePreferences() {
    if (currentProfile && currentProfile.preferencias) {
        const prefs = currentProfile.preferencias;
        q('colorX').value = prefs.colorX || '#ff4d4d';
        q('colorO').value = prefs.colorO || '#4dff4d';
        q('symbolX').value = prefs.symbolX || 'X';
        q('symbolO').value = prefs.symbolO || 'O';
    }
}

// Modificar la función move para guardar estadísticas
async function move(i) {
    if (board[i]) {
        showModal("Esa casilla ya está ocupada");
        return;
    }

    q("btnNames").disabled = true;
    saveMove(i, turn);

    board[i] = turn;

    let r = check();

    if (r.over) {
        stopTimer();
        games++;
        gameOver = true;

        if (r.w) {
            q("status").textContent = "Ganó " + p[r.w];
            score[r.w]++;
            winningCells = r.combo;
            
            // Guardar estadísticas en el perfil
            if (currentProfile) {
                await updateProfileStats(r.w === 'X' ? 'victoria' : 'derrota');
            }
            
            addHistory("Ganó " + p[r.w], r.w);
        } else {
            q("status").textContent = "Empate";
            score.D++;
            winningCells = [];
            
            // Guardar estadísticas en el perfil
            if (currentProfile) {
                await updateProfileStats('empate');
            }
            
            addHistory("Empate", null);
        }

        nextStarter = nextStarter === "X" ? "O" : "X";
        q("btnNames").disabled = false;
        updateScore();
    } else {
        turn = turn === "X" ? "O" : "X";
    }

    draw();
}

async function updateProfileStats(resultado) {
    if (!currentProfile) return;

    const stats = { ...currentProfile.estadisticas };
    stats.partidas_jugadas++;
    
    if (resultado === 'victoria') {
        stats.victorias++;
    } else if (resultado === 'empate') {
        stats.empates++;
    } else {
        stats.derrotas++;
    }

    try {
        await fetch(`${API_URL}/perfiles/${currentProfile.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                estadisticas: stats,
                nueva_partida: {
                    resultado: resultado,
                    duracion: seconds,
                    jugadores: { X: p.X, O: p.O },
                    movimientos: moveHistory.length
                }
            })
        });
        
        // Actualizar perfil local
        currentProfile.estadisticas = stats;
    } catch (error) {
        console.error('Error al actualizar estadísticas:', error);
    }
}

// Inicializar display del perfil
updateProfileDisplay();
/ /   M e j o r a :   F e e d b a c k   v i s u a l   -    
  
 m i � r c o l e s ,   8   d e   o c t u b r e   d e   2 0 2 5   1 2 : 3 4 : 2 2   a . � m .  
  
  
 