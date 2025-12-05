"""
models/estadistica.py
Modelo de Estadísticas del jugador
"""

from config.db_init import db


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