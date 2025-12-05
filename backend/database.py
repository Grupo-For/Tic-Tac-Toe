"""
database.py
Configuración de base de datos para Flask + SQLAlchemy + MySQL
Versión organizada - importa funcionalidades separadas
"""

from config.db_init import db, init_db
from config.db_test import test_connection

# Exportar para que otros archivos puedan importar desde database.py
__all__ = ['db', 'init_db', 'test_connection']


if __name__ == '__main__':
    """
    Ejecutar este archivo directamente para probar la conexión:
    python database.py
    """
    print("\n🔍 PROBANDO CONEXIÓN A MYSQL...")
    print("=" * 60)
    test_connection()