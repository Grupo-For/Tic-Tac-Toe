"""
routes/eliminar_perfil.py
Endpoint para eliminar un perfil permanentemente
"""

from flask import jsonify
from config.db_init import db
from models import Perfil


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