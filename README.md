# Tic Tac Toe - Integración Backend

## Integrantes:
- Jean Piero 
- Maycol Aldo
- Tracy
- Anghie 
- Juan

## Nueva Funcionalidad:
Integración con backend Flask para gestión de perfiles de jugadores. Los usuarios pueden crear perfiles personalizados que almacenan estadísticas, historial de partidas, preferencias de colores y símbolos. El sistema guarda automáticamente los resultados de cada partida y permite gestionar múltiples perfiles de jugadores.

## Cómo instalar aplicativo:

### Backend (Python)
1. Instalar Python 3.8+
2. Navegar a la carpeta backend: `cd backend`
3. Instalar dependencias: `pip install -r requirements.txt`

### Frontend
1. El frontend funciona en cualquier navegador moderno
2. No requiere instalación adicional

## Cómo ejecutar:

1. **Backend**: 
   ```bash
   cd backend
   python app.py

## Lista de Endpoints implementados:

- `POST /perfiles` - Crear nuevo perfil de jugador
- `GET /perfiles` - Listar todos los perfiles registrados
- `GET /perfiles/{id}` - Obtener perfil específico por ID
- `PUT /perfiles/{id}` - Actualizar perfil (estadísticas, historial, preferencias)
- `DELETE /perfiles/{id}` - Eliminar perfil permanentemente