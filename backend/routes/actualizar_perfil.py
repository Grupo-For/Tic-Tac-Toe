"""
routes/actualizar_perfil.py
Endpoint para actualizar información del perfil y estadísticas
"""

from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from config.db_init import db
from models import Perfil, Partida


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