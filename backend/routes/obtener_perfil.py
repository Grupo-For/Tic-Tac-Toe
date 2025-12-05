"""
routes/obtener_perfil.py
Endpoint para obtener un perfil específico por ID (Iniciar sesión)
"""

from flask import jsonify
from models import Perfil


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