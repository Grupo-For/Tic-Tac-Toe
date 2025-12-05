  // Lógica principal del juego
  function start() {
    let name1 = q("p1").value.trim() || "J1";
    let name2 = q("p2").value.trim() || "J2";
    let col1 = q("colorX").value;
    let col2 = q("colorO").value;
    if (!setSymbols()) return;

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
    q("firstTurnModal").classList.add("show");

    document.body.className = "game";

    score.X = score.O = score.D = 0;
    games = 0;
    clearHistory();
    updateScore();
    restart();

    initTheme(); 
  }

  function setFirstTurn(choice) {
    if(choice === "R") {
      turn = Math.random() < 0.5 ? "X" : "O";
    } else {
      turn = choice;
    }

    nextStarter = turn;
    q("firstTurnModal").classList.remove("show");
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
    updateUndoButton();
  }

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
        
        if (currentProfile) {
          await updateProfileStats(r.w === 'X' ? 'victoria' : 'derrota');
        }
        
        addHistory("Ganó " + p[r.w], r.w);
      } else {
        q("status").textContent = "Empate";
        score.D++;
        winningCells = [];
        
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