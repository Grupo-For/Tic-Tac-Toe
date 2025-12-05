"""
routes/crear_perfil.py
Endpoint para crear un nuevo perfil de usuario
"""

from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from config.db_init import db
from models import Perfil


def crear_perfil():
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