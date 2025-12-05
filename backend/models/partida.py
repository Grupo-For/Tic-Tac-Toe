"""
models/partida.py
Modelo de Partida (historial de juegos)
"""

from config.db_init import db
from datetime import datetime


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