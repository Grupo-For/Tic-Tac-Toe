"""
routes/health.py
Endpoint para verificar el estado del servidor
"""

from flask import jsonify


def health_check():
    """
    Verifica que el servidor esté funcionando
    """
    return jsonify({
        "status": "OK",
        "database": "SQLite con SQLAlchemy ORM",
        "message": "Servidor funcionando correctamente"
    }), 200