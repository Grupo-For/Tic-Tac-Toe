// Funciones de historial de movimientos
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