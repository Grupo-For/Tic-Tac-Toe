"""
app_orm.py
Aplicación Flask con SQLAlchemy ORM - Versión mejorada con base de datos

IMPLEMENTACIÓN FASE GREEN:
- Código mínimo para hacer pasar las pruebas TDD
- Uso de ORM en lugar de JSON
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from models import db, Perfil, Estadistica, Preferencia, Partida
from database import init_db

app = Flask(__name__)
CORS(app)

# Inicializar base de datos
init_db(app)


# ============================================
# ENDPOINT: CREAR PERFIL (POST /perfiles)
# ============================================

@app.route('/perfiles', methods=['POST'])
def crear_perfil():
    """
    Crea un nuevo perfil de usuario
    
    FASE GREEN: Implementación que hace pasar las pruebas TDD
    
    Request Body:
        {
            "nombre": "Juan Pérez",
            "nombre_perfil": "juan_gamer",
            "tipo_perfil": "jugador"  // opcional
        }
    
    Returns:
        201: Perfil creado exitosamente
        400: Datos inválidos o nombre duplicado
        500: Error del servidor
    """
    try:
        data = request.get_json()
        
        # VALIDACIÓN 1: Campos requeridos
        nombre = data.get('nombre', '').strip()
        nombre_perfil = data.get('nombre_perfil', '').strip()
        
        if not nombre or not nombre_perfil:
            return jsonify({
                "error": "Nombre y nombre_perfil son requeridos"
            }), 400
        
        # VALIDACIÓN 2: Verificar que nombre_perfil no exista
        perfil_existente = Perfil.query.filter_by(nombre_perfil=nombre_perfil).first()
        if perfil_existente:
            return jsonify({
                "error": "El nombre de perfil ya existe"
            }), 400
        
        # CREAR PERFIL usando ORM
        tipo_perfil = data.get('tipo_perfil', 'jugador')
        nuevo_perfil = Perfil(
            nombre=nombre,
            nombre_perfil=nombre_perfil,
            tipo_perfil=tipo_perfil
        )
        
        # GUARDAR en base de datos
        db.session.add(nuevo_perfil)
        db.session.commit()
        
        # RETORNAR respuesta exitosa
        return jsonify({
            "mensaje": "Perfil creado",
            "perfil": nuevo_perfil.to_dict()
        }), 201
    
    except IntegrityError as e:
        # Error de constraint de BD (ej: UNIQUE)
        db.session.rollback()
        return jsonify({
            "error": "El nombre de perfil ya existe"
        }), 400
    
    except Exception as e:
        # Error inesperado
        db.session.rollback()
        return jsonify({
            "error": f"Error interno del servidor: {str(e)}"
        }), 500


# ============================================
# ENDPOINT: LISTAR PERFILES (GET /perfiles)
# ============================================

@app.route('/perfiles', methods=['GET'])
def listar_perfiles():
    """
    Obtiene todos los perfiles registrados
    
    Returns:
        200: Lista de perfiles
    """
    try:
        # Obtener todos los perfiles usando ORM
        perfiles = Perfil.query.all()
        
        return jsonify({
            "perfiles": [perfil.to_dict() for perfil in perfiles]
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": f"Error al obtener perfiles: {str(e)}"
        }), 500


# ============================================
# ENDPOINT: OBTENER PERFIL (GET /perfiles/:id)
# ============================================

@app.route('/perfiles/<int:perfil_id>', methods=['GET'])
def obtener_perfil(perfil_id):
    """
    Obtiene un perfil específico por ID
    
    Args:
        perfil_id: ID del perfil
    
    Returns:
        200: Perfil encontrado
        404: Perfil no encontrado
    """
    try:
        # Buscar perfil por ID usando ORM
        perfil = Perfil.query.get(perfil_id)
        
        if perfil:
            return jsonify(perfil.to_dict()), 200
        else:
            return jsonify({
                "error": "Perfil no encontrado"
            }), 404
    
    except Exception as e:
        return jsonify({
            "error": f"Error al obtener perfil: {str(e)}"
        }), 500


# ============================================
# ENDPOINT: ACTUALIZAR PERFIL (PUT /perfiles/:id)
# ============================================

@app.route('/perfiles/<int:perfil_id>', methods=['PUT'])
def actualizar_perfil(perfil_id):
    """
    Actualiza información de un perfil
    
    Args:
        perfil_id: ID del perfil
    
    Request Body:
        {
            "nombre": "Nuevo nombre",
            "estadisticas": {...},
            "preferencias": {...},
            "nueva_partida": {...}
        }
    
    Returns:
        200: Perfil actualizado
        404: Perfil no encontrado
    """
    try:
        data = request.get_json()
        
        # Buscar perfil
        perfil = Perfil.query.get(perfil_id)
        if not perfil:
            return jsonify({
                "error": "Perfil no encontrado"
            }), 404
        
        # Actualizar campos básicos
        if 'nombre' in data:
            perfil.nombre = data['nombre'].strip()
        
        if 'nombre_perfil' in data:
            nuevo_nombre_perfil = data['nombre_perfil'].strip()
            # Verificar que no exista otro perfil con ese nombre
            existe = Perfil.query.filter(
                Perfil.nombre_perfil == nuevo_nombre_perfil,
                Perfil.id != perfil_id
            ).first()
            
            if existe:
                return jsonify({
                    "error": "El nombre de perfil ya existe"
                }), 400
            
            perfil.nombre_perfil = nuevo_nombre_perfil
        
        # Actualizar estadísticas
        if 'estadisticas' in data and perfil.estadisticas:
            stats_data = data['estadisticas']
            if 'victorias' in stats_data:
                perfil.estadisticas.victorias = stats_data['victorias']
            if 'empates' in stats_data:
                perfil.estadisticas.empates = stats_data['empates']
            if 'derrotas' in stats_data:
                perfil.estadisticas.derrotas = stats_data['derrotas']
            if 'partidas_jugadas' in stats_data:
                perfil.estadisticas.partidas_jugadas = stats_data['partidas_jugadas']
        
        # Actualizar preferencias
        if 'preferencias' in data and perfil.preferencias:
            prefs_data = data['preferencias']
            if 'colorX' in prefs_data:
                perfil.preferencias.colorX = prefs_data['colorX']
            if 'colorO' in prefs_data:
                perfil.preferencias.colorO = prefs_data['colorO']
            if 'symbolX' in prefs_data:
                perfil.preferencias.symbolX = prefs_data['symbolX']
            if 'symbolO' in prefs_data:
                perfil.preferencias.symbolO = prefs_data['symbolO']
        
        # Agregar nueva partida al historial
        if 'nueva_partida' in data:
            partida_data = data['nueva_partida']
            nueva_partida = Partida(
                perfil_id=perfil.id,
                resultado=partida_data.get('resultado'),
                duracion=partida_data.get('duracion'),
                movimientos=partida_data.get('movimientos'),
                jugador_x=partida_data.get('jugadores', {}).get('X'),
                jugador_o=partida_data.get('jugadores', {}).get('O')
            )
            db.session.add(nueva_partida)
        
        # Guardar cambios
        db.session.commit()
        
        return jsonify({
            "mensaje": "Perfil actualizado",
            "perfil": perfil.to_dict()
        }), 200
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            "error": "Error de integridad de datos"
        }), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"Error al actualizar perfil: {str(e)}"
        }), 500


# ============================================
# ENDPOINT: ELIMINAR PERFIL (DELETE /perfiles/:id)
# ============================================

@app.route('/perfiles/<int:perfil_id>', methods=['DELETE'])
def eliminar_perfil(perfil_id):
    """
    Elimina un perfil permanentemente
    
    Args:
        perfil_id: ID del perfil
    
    Returns:
        200: Perfil eliminado
        404: Perfil no encontrado
    """
    try:
        # Buscar perfil
        perfil = Perfil.query.get(perfil_id)
        
        if not perfil:
            return jsonify({
                "error": "Perfil no encontrado"
            }), 404
        
        # Eliminar usando ORM (cascade elimina relaciones)
        db.session.delete(perfil)
        db.session.commit()
        
        return jsonify({
            "mensaje": "Perfil eliminado"
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"Error al eliminar perfil: {str(e)}"
        }), 500


# ============================================
# ENDPOINT: HEALTH CHECK
# ============================================

@app.route('/health', methods=['GET'])
def health_check():
    """
    Verifica que el servidor esté funcionando
    """
    return jsonify({
        "status": "OK",
        "database": "SQLite con SQLAlchemy ORM",
        "message": "Servidor funcionando correctamente"
    }), 200


# ============================================
# MANEJO DE ERRORES GLOBALES
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint no encontrado"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        "error": "Error interno del servidor"
    }), 500


# ============================================
# INICIO DEL SERVIDOR
# ============================================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 SERVIDOR FLASK CON ORM INICIANDO...")
    print("="*50)
    print("📊 Base de datos: MYSql")
    print("🔧 ORM: SQLAlchemy")
    print("🧪 Testing: pytest + TDD")
    print("🌐 URL: http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)