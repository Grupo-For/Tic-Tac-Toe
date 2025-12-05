"""
routes/listar_perfiles.py
Endpoint para listar todos los perfiles registrados
"""

from flask import jsonify
from models import Perfil


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