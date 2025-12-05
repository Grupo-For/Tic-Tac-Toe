"""
app_orm.py
Aplicación Flask con SQLAlchemy ORM - Versión organizada

IMPLEMENTACIÓN FASE GREEN:
- Código mínimo para hacer pasar las pruebas TDD
- Uso de ORM en lugar de JSON
- Código separado por funcionalidades
"""

from flask import Flask
from flask_cors import CORS
from database import init_db
from error_handlers import register_error_handlers

# Importar las funciones de los endpoints
from routes.crear_perfil import crear_perfil
from routes.listar_perfiles import listar_perfiles
from routes.obtener_perfil import obtener_perfil
from routes.actualizar_perfil import actualizar_perfil
from routes.eliminar_perfil import eliminar_perfil
from routes.health import health_check

app = Flask(__name__)
CORS(app)

# Inicializar base de datos
init_db(app)

# Registrar manejadores de errores
register_error_handlers(app)


# ============================================
# REGISTRAR RUTAS
# ============================================

# 1. CREAR PERFIL (POST /perfiles)
app.add_url_rule('/perfiles', 'crear_perfil', crear_perfil, methods=['POST'])

# 2. LISTAR PERFILES (GET /perfiles)
app.add_url_rule('/perfiles', 'listar_perfiles', listar_perfiles, methods=['GET'])

# 3. OBTENER PERFIL - INICIAR SESIÓN (GET /perfiles/:id)
app.add_url_rule('/perfiles/<int:perfil_id>', 'obtener_perfil', obtener_perfil, methods=['GET'])

# 4. ACTUALIZAR PERFIL Y ESTADÍSTICAS (PUT /perfiles/:id)
app.add_url_rule('/perfiles/<int:perfil_id>', 'actualizar_perfil', actualizar_perfil, methods=['PUT'])

# 5. ELIMINAR PERFIL (DELETE /perfiles/:id)
app.add_url_rule('/perfiles/<int:perfil_id>', 'eliminar_perfil', eliminar_perfil, methods=['DELETE'])

# HEALTH CHECK
app.add_url_rule('/health', 'health_check', health_check, methods=['GET'])


# ============================================
# INICIO DEL SERVIDOR
# ============================================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 SERVIDOR FLASK CON ORM INICIANDO...")
    print("="*50)
    print("📊 Base de datos: MySQL")
    print("🔧 ORM: SQLAlchemy")
    print("🧪 Testing: pytest + TDD")
    print("🌐 URL: http://localhost:5000")
    print("="*50)
    print("\n📋 FUNCIONALIDADES DISPONIBLES:")
    print("1. ✅ Crear perfil de usuario")
    print("2. ✅ Iniciar sesión con perfil")
    print("3. ✅ Actualizar estadísticas automáticamente")
    print("4. ✅ Eliminar perfil")
    print("5. ✅ Listar todos los perfiles")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)