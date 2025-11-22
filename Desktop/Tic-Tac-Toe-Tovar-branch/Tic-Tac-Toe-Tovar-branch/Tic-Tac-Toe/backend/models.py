# models.py
"""
Modelos ORM para SQLAlchemy - Compatible con MySQL
"""

from database import db
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
        self.estadisticas = Estadistica()
        
        # Inicializar preferencias por defecto
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


class Estadistica(db.Model):
    __tablename__ = 'estadisticas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfiles.id', ondelete='CASCADE'), 
                         unique=True, nullable=False)
    victorias = db.Column(db.Integer, default=0, nullable=False)
    empates = db.Column(db.Integer, default=0, nullable=False)
    derrotas = db.Column(db.Integer, default=0, nullable=False)
    partidas_jugadas = db.Column(db.Integer, default=0, nullable=False)
    
    def to_dict(self):
        return {
            'victorias': self.victorias,
            'empates': self.empates,
            'derrotas': self.derrotas,
            'partidas_jugadas': self.partidas_jugadas
        }
    
    def __repr__(self):
        return f'<Estadistica perfil_id={self.perfil_id}>'


class Preferencia(db.Model):
    __tablename__ = 'preferencias'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfiles.id', ondelete='CASCADE'), 
                         unique=True, nullable=False)
    colorX = db.Column(db.String(20), default='#ff4d4d', nullable=False)
    colorO = db.Column(db.String(20), default='#4dff4d', nullable=False)
    symbolX = db.Column(db.String(5), default='X', nullable=False)
    symbolO = db.Column(db.String(5), default='O', nullable=False)
    
    def to_dict(self):
        return {
            'colorX': self.colorX,
            'colorO': self.colorO,
            'symbolX': self.symbolX,
            'symbolO': self.symbolO
        }
    
    def __repr__(self):
        return f'<Preferencia perfil_id={self.perfil_id}>'


class Partida(db.Model):
    __tablename__ = 'partidas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfiles.id', ondelete='CASCADE'), 
                         nullable=False, index=True)
    resultado = db.Column(db.String(20), nullable=False)  # 'victoria', 'derrota', 'empate'
    duracion = db.Column(db.Integer, default=0)  # en segundos
    movimientos = db.Column(db.Integer, default=0, nullable=False)
    jugador_x = db.Column(db.String(100))
    jugador_o = db.Column(db.String(100))
    fecha = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'resultado': self.resultado,
            'duracion': self.duracion,
            'movimientos': self.movimientos,
            'jugadores': {
                'X': self.jugador_x,
                'O': self.jugador_o
            },
            'fecha': self.fecha.isoformat() if self.fecha else None
        }
    
    def __repr__(self):
        return f'<Partida {self.id} - {self.resultado}>'