"""
models/preferencia.py
Modelo de Preferencias de usuario (colores y símbolos)
"""

from config.db_init import db


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