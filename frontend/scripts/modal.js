// Funciones de modales y confirmaciones
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
  q("modal").classList.add("show");
}

function closeModal() { 
  q("modal").classList.remove("show");
}

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

function openNameModal() {
  q("nameX").value = p.X;
  q("nameO").value = p.O;
  q("nameError").textContent = "";
  q("nameModal").classList.add("show");
}

function closeNameModal() { 
  q("nameModal").classList.remove("show");
}

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

function openStats() {
  let total = games || 1;
  let porcX = ((score.X / total) * 100).toFixed(1);
  let porcO = ((score.O / total) * 100).toFixed(1);
  let porcD = ((score.D / total) * 100).toFixed(1);

  q("statsX").textContent = `${p.X} (${p.symX}): ${score.X} victorias (${porcX}%)`;
  q("statsO").textContent = `${p.O} (${p.symO}): ${score.O} victorias (${porcO}%)`;
  q("statsDraws").textContent = `Empates: ${score.D} (${porcD}%)`;

  q("statsModal").classList.add("show");
}

function closeStats() {
  q("statsModal").classList.remove("show");
}