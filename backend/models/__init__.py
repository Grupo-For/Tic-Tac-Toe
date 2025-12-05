"""
models/__init__.py
Exporta todos los modelos para que puedan importarse desde models/
"""

from models.perfil import Perfil
from models.estadistica import Estadistica
from models.preferencia import Preferencia
from models.partida import Partida

__all__ = ['Perfil', 'Estadistica', 'Preferencia', 'Partida']