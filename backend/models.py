"""
models.py
Modelos ORM para SQLAlchemy - Compatible con MySQL
Versión organizada - importa modelos separados
"""

from config.db_init import db
from models.perfil import Perfil
from models.estadistica import Estadistica
from models.preferencia import Preferencia
from models.partida import Partida

# Exportar para que otros archivos puedan importar desde models.py
__all__ = ['db', 'Perfil', 'Estadistica', 'Preferencia', 'Partida']