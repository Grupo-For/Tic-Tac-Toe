# 🎮 Tic-Tac-Toe con TDD y ORM

Sistema de gestión de perfiles para juego Tic-Tac-Toe implementado con **Test-Driven Development (TDD)** y **SQLAlchemy ORM**.

---

## 📋 Contenido

- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Pruebas TDD](#pruebas-tdd)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [API Endpoints](#api-endpoints)

---

## 🛠️ Tecnologías

- **Python 3.8+**
- **Flask 2.3.3** - Framework web
- **SQLAlchemy** - ORM para base de datos
- **SQLite** - Base de datos
- **pytest** - Framework de testing
- **TDD** - Metodología de desarrollo

---

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone <repo>
cd tictactoe-tdd-orm
```

### 2. Crear entorno virtual (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 🚀 Ejecución

### Iniciar el servidor Flask

```bash
python app_orm.py
```

El servidor estará disponible en: `http://localhost:5000`

### Verificar que funciona

```bash
curl http://localhost:5000/health
```

Respuesta esperada:
```json
{
  "status": "OK",
  "database": "SQLite con SQLAlchemy ORM",
  "message": "Servidor funcionando correctamente"
}
```

---

## 🧪 Pruebas TDD

### Ejecutar todas las pruebas

```bash
pytest test_crear_perfil.py -v
```

### Ejecutar por fase TDD

**Fase RED (pruebas que inicialmente fallan):**
```bash
pytest test_crear_perfil.py::TestCrearPerfilRED -v
```

**Fase GREEN (después de implementar):**
```bash
pytest test_crear_perfil.py::TestCrearPerfilGREEN -v
```

**Fase REFACTOR (código mejorado):**
```bash
pytest test_crear_perfil.py::TestCrearPerfilREFACTOR -v
```

### Ejecutar prueba específica

```bash
pytest test_crear_perfil.py::TestCrearPerfilRED::test_crear_perfil_exitoso -v
```

### Ver cobertura de código

```bash
pytest test_crear_perfil.py --cov=app_orm --cov-report=html
```

---

## 📁 Estructura del Proyecto

```
tictactoe-tdd-orm/
│
├── models.py                 # Modelos ORM (Perfil, Estadistica, etc.)
├── database.py               # Configuración de base de datos
├── app_orm.py                # API Flask con ORM
├── test_crear_perfil.py      # Pruebas TDD
│
├── requirements.txt          # Dependencias
├── README.md                 # Este archivo
│
├── perfiles.db               # Base de datos SQLite (generada automáticamente)
└── __pycache__/              # Cache de Python
```

---

## 🔌 API Endpoints

### 1. Crear Perfil
**POST** `/perfiles`

```bash
curl -X POST http://localhost:5000/perfiles \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "nombre_perfil": "juan_gamer",
    "tipo_perfil": "jugador"
  }'
```

**Respuesta (201):**
```json
{
  "mensaje": "Perfil creado",
  "perfil": {
    "id": 1,
    "nombre": "Juan Pérez",
    "nombre_perfil": "juan_gamer",
    "tipo_perfil": "jugador",
    "fecha_creacion": "2025-10-26T10:30:00",
    "estadisticas": {
      "victorias": 0,
      "empates": 0,
      "derrotas": 0,
      "partidas_jugadas": 0
    },
    "preferencias": {
      "colorX": "#ff4d4d",
      "colorO": "#4dff4d",
      "symbolX": "X",
      "symbolO": "O"
    },
    "historial_partidas": []
  }
}
```

### 2. Listar Perfiles
**GET** `/perfiles`

```bash
curl http://localhost:5000/perfiles
```

### 3. Obtener Perfil Específico
**GET** `/perfiles/:id`

```bash
curl http://localhost:5000/perfiles/1
```

### 4. Actualizar Perfil
**PUT** `/perfiles/:id`

```bash
curl -X PUT http://localhost:5000/perfiles/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Carlos Pérez",
    "estadisticas": {
      "victorias": 5,
      "empates": 2,
      "derrotas": 1,
      "partidas_jugadas": 8
    }
  }'
```

### 5. Eliminar Perfil
**DELETE** `/perfiles/:id`

```bash
curl -X DELETE http://localhost:5000/perfiles/1
```

---

## 🔄 Ciclo TDD Implementado

### 1️⃣ RED - Escribir pruebas que fallan
```python
def test_crear_perfil_exitoso(self, client):
    data = {'nombre': 'Juan', 'nombre_perfil': 'juan_gamer'}
    response = client.post('/perfiles', json=data)
    assert response.status_code == 201  # ❌ FALLA (no existe el endpoint)
```

### 2️⃣ GREEN - Implementar código mínimo
```python
@app.route('/perfiles', methods=['POST'])
def crear_perfil():
    data = request.json
    nuevo_perfil = Perfil(data['nombre'], data['nombre_perfil'])
    db.session.add(nuevo_perfil)
    db.session.commit()
    return jsonify({'perfil': nuevo_perfil.to_dict()}), 201  # ✅ PASA
```

### 3️⃣ REFACTOR - Mejorar código
```python
@app.route('/perfiles', methods=['POST'])
def crear_perfil():
    data = request.json
    
    # Validaciones
    if not data.get('nombre') or not data.get('nombre_perfil'):
        return jsonify({'error': 'Campos requeridos'}), 400
    
    # Verificar duplicados
    existe = Perfil.query.filter_by(nombre_perfil=data['nombre_perfil']).first()
    if existe:
        return jsonify({'error': 'Perfil existe'}), 400
    
    # Crear perfil
    nuevo_perfil = Perfil(data['nombre'], data['nombre_perfil'])
    db.session.add(nuevo_perfil)
    db.session.commit()
    
    return jsonify({'perfil': nuevo_perfil.to_dict()}), 201  # ✅ SIGUE PASANDO
```

---

## 📊 Esquema de Base de Datos

```sql
-- Tabla perfiles
CREATE TABLE perfiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    nombre_perfil VARCHAR(50) UNIQUE NOT NULL,
    tipo_perfil VARCHAR(20) DEFAULT 'jugador',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla estadisticas
CREATE TABLE estadisticas (
    id INTEGER PRIMARY KEY,
    perfil_id INTEGER UNIQUE,
    victorias INTEGER DEFAULT 0,
    empates INTEGER DEFAULT 0,
    derrotas INTEGER DEFAULT 0,
    partidas_jugadas INTEGER DEFAULT 0,
    FOREIGN KEY (perfil_id) REFERENCES perfiles(id)
);

-- Tabla preferencias
CREATE TABLE preferencias (
    id INTEGER PRIMARY KEY,
    perfil_id INTEGER UNIQUE,
    colorX VARCHAR(7) DEFAULT '#ff4d4d',
    colorO VARCHAR(7) DEFAULT '#4dff4d',
    symbolX VARCHAR(3) DEFAULT 'X',
    symbolO VARCHAR(3) DEFAULT 'O',
    FOREIGN KEY (perfil_id) REFERENCES perfiles(id)
);

-- Tabla partidas
CREATE TABLE partidas (
    id INTEGER PRIMARY KEY,
    perfil_id INTEGER,
    resultado VARCHAR(20) NOT NULL,
    duracion INTEGER,
    movimientos INTEGER,
    jugador_x VARCHAR(50),
    jugador_o VARCHAR(50),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (perfil_id) REFERENCES perfiles(id)
);
```

---

## ✅ Validaciones Implementadas

- ✅ Nombre y nombre_perfil son requeridos
- ✅ Nombre de perfil debe ser único
- ✅ Trim automático de espacios
- ✅ Estadísticas se inicializan en 0
- ✅ Preferencias con valores por defecto
- ✅ Fecha de creación automática
- ✅ Manejo de errores con rollback

---

## 🐛 Troubleshooting

**Error: "No module named 'flask'"**
```bash
pip install -r requirements.txt
```

**Error: "Unable to open database file"**
- La base de datos se crea automáticamente al iniciar el servidor
- Verificar permisos de escritura en la carpeta

**Tests fallan**
```bash
# Limpiar cache
rm -rf __pycache__ .pytest_cache

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Recursos

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [pytest Documentation](https://docs.pytest.org/)
- [TDD Best Practices](https://martinfowler.com/bliki/TestDrivenDevelopment.html)

---

## 👥 Autor

**Universidad Continental - Construcción de Software**
- Docente: Mg. Roberto Zárate Mendoza
- Estudiantes:
      Huamaní Rodriguez Jean Piero
      Porras Torres Anghelina 
      Ramirez Soto Juan Diego
      Tovar Arias Michael Aldo
      Vila Quispe Tracy Anahi


---
