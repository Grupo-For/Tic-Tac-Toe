// Funciones de validación
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