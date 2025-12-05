"""
config/db_config.py
Configuración de parámetros de la base de datos MySQL
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


def get_database_config():
    """
    Obtiene la configuración de la base de datos desde variables de entorno
    
    Returns:
        dict: Diccionario con la configuración de la BD
    """
    return {
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),  # Por defecto XAMPP no tiene password
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '3306'),
        'name': os.getenv('DB_NAME', 'tictactoe_db')
    }


def build_database_uri():
    """
    Construye la URI de conexión a MySQL
    
    Returns:
        str: URI de conexión completa
    """
    config = get_database_config()
    
    # Construir URI de conexión
    database_uri = (
        f"mysql+pymysql://{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}/{config['name']}"
        f"?charset=utf8mb4"
    )
    
    return database_uri


def get_sqlalchemy_config():
    """
    Obtiene la configuración de SQLAlchemy
    
    Returns:
        dict: Diccionario con configuración de SQLAlchemy
    """
    return {
        'SQLALCHEMY_DATABASE_URI': build_database_uri(),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ECHO': False,  # Cambiar a True para ver queries SQL
        'SQLALCHEMY_POOL_RECYCLE': 280,  # Reconectar cada 280 segundos
        'SQLALCHEMY_POOL_TIMEOUT': 20
    }