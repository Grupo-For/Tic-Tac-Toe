"""
config/db_init.py
Inicialización de la base de datos y creación de tablas
"""

from flask_sqlalchemy import SQLAlchemy
from config.db_config import get_sqlalchemy_config, get_database_config

db = SQLAlchemy()


def init_db(app):
    """
    Inicializa la conexión a la base de datos MySQL
    
    Args:
        app: Instancia de Flask
    """
    
    # Aplicar configuración de SQLAlchemy
    config = get_sqlalchemy_config()
    for key, value in config.items():
        app.config[key] = value
    
    # Inicializar SQLAlchemy
    db.init_app(app)
    
    # Crear tablas
    with app.app_context():
        try:
            # Probar conexión
            db.engine.connect()
            
            # Obtener configuración para mostrar
            db_config = get_database_config()
            
            print("=" * 60)
            print("✅ CONEXIÓN A MYSQL EXITOSA")
            print("=" * 60)
            print(f"📊 Base de datos: {db_config['name']}")
            print(f"🖥️  Host: {db_config['host']}:{db_config['port']}")
            print(f"👤 Usuario: {db_config['user']}")
            print("=" * 60)
            
            # Crear todas las tablas
            db.create_all()
            print("✅ Tablas creadas/verificadas exitosamente")
            print("=" * 60)
            
        except Exception as e:
            print("=" * 60)
            print("❌ ERROR AL CONECTAR CON MYSQL")
            print("=" * 60)
            print(f"Error: {str(e)}")
            print("\n🔍 POSIBLES SOLUCIONES:")
            print("1. Verifica que XAMPP MySQL esté iniciado")
            print("2. Verifica que la base de datos 'tictactoe_db' exista")
            print("3. Verifica usuario y contraseña en .env")
            print("4. Verifica que pymysql esté instalado: pip install pymysql")
            print("5. Verifica el puerto (por defecto 3306)")
            print("=" * 60)
            raise