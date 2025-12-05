// Funciones de perfil de usuario
async function listAllProfiles() {
  try {
    const response = await fetch(`${API_URL}/perfiles`);
    const data = await response.json();
    
    if (data.perfiles && data.perfiles.length > 0) {
      let profilesList = "Perfiles registrados:\n";
      data.perfiles.forEach(profile => {
        profilesList += `- ${profile.nombre_perfil} (${profile.nombre})\n`;
      });
      showModal(profilesList);
    } else {
      showModal("No hay perfiles registrados aún.");
    }
  } catch (error) {
    showModal("Error al cargar los perfiles: " + error.message);
  }
}

function openProfileModal() {
    q('profileModal').classList.add("show"); 
    if (currentProfile) {
        showProfileInfo();
    } else {
        showLoginForm();
    }
}

function closeProfileModal() {
    q('profileModal').classList.remove("show");
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

async function deleteCurrentProfile() {
  if (!currentProfile) {
    showModal("No hay perfil activo para eliminar");
    return;
  }
  
  showModal(`¿Estás seguro de eliminar el perfil "${currentProfile.nombre_perfil}"? Esta acción no se puede deshacer.`, [
    {
      text: "Sí, eliminar",
      action: async () => {
        try {
          const response = await fetch(`${API_URL}/perfiles/${currentProfile.id}`, {
            method: 'DELETE'
          });
          
          if (response.ok) {
            showModal("Perfil eliminado correctamente");
            logoutProfile();
          } else {
            const error = await response.json();
            showModal("Error al eliminar perfil: " + error.error);
          }
        } catch (error) {
          showModal("Error de conexión: " + error.message);
        }
      }
    },
    {
      text: "Cancelar",
      action: () => {}
    }
  ]);
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
    const response = await fetch(`${API_URL}/perfiles/${currentProfile.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        estadisticas: stats,
        nueva_partida: {
          resultado: resultado,
          duracion: seconds,
          jugadores: { X: p.X, O: p.O },
          movimientos: moveHistory.length,
          fecha: new Date().toISOString()
        },
        preferencias: {
          colorX: q('colorX').value,
          colorO: q('colorO').value,
          symbolX: q('symbolX').value,
          symbolO: q('symbolO').value
        }
      })
    });
    
    if (response.ok) {
      const updatedProfile = await response.json();
      currentProfile = updatedProfile.perfil;
      showProfileInfo();
    }
  } catch (error) {
    console.error('Error al actualizar estadísticas:', error);
  }
}