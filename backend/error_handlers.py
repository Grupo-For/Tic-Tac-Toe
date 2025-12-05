"""
error_handlers.py
Manejo de errores globales de la aplicación
"""

from flask import jsonify
from config.db_init import db


def register_error_handlers(app):
    """
    Registra los manejadores de errores en la aplicación Flask
    
    Args:
        app: Instancia de Flask
    """
    
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