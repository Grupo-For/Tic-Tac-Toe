"""
models/perfil.py
Modelo de Perfil de usuario
"""

from config.db_init import db
from datetime import datetime


class Perfil(db.Model):
    __tablename__ = 'perfiles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    nombre_perfil = db.Column(db.String(50), unique=True, nullable=False, index=True)
    tipo_perfil = db.Column(db.String(20), default='jugador')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones con cascade delete
    estadisticas = db.relationship('Estadistica', backref='perfil', uselist=False, 
                                   cascade='all, delete-orphan', lazy=True)
    preferencias = db.relationship('Preferencia', backref='perfil', uselist=False, 
                                   cascade='all, delete-orphan', lazy=True)
    partidas = db.relationship('Partida', backref='perfil', 
                               cascade='all, delete-orphan', lazy=True)
    
    def __init__(self, nombre, nombre_perfil, tipo_perfil='jugador'):
        self.nombre = nombre
        self.nombre_perfil = nombre_perfil
        self.tipo_perfil = tipo_perfil
        
        # Inicializar estadísticas por defecto
        from models.estadistica import Estadistica
        self.estadisticas = Estadistica()
        
        # Inicializar preferencias por defecto
        from models.preferencia import Preferencia
        self.preferencias = Preferencia()
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'nombre_perfil': self.nombre_perfil,
            'tipo_perfil': self.tipo_perfil,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'estadisticas': self.estadisticas.to_dict() if self.estadisticas else None,
            'preferencias': self.preferencias.to_dict() if self.preferencias else None,
            'partidas': [partida.to_dict() for partida in self.partidas] if self.partidas else []
        }
    
    def __repr__(self):
        return f'<Perfil {self.nombre_perfil}>'