# database.py
"""
Configuración de base de datos para Flask + SQLAlchemy + MySQL
"""

from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

db = SQLAlchemy()

def init_db(app):
    """
    Inicializa la conexión a la base de datos MySQL
    
    Args:
        app: Instancia de Flask
    """
    
    # OPCIÓN 1: Usar variables de entorno (RECOMENDADO)
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')  # Por defecto XAMPP no tiene password
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'tictactoe_db')
    
    # Construir URI de conexión
    database_uri = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4'
    
    # OPCIÓN 2: URI directo (para pruebas rápidas)
    # database_uri = 'mysql+pymysql://root:@localhost:3306/tictactoe_db?charset=utf8mb4'
    
    # Configuración de SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False  # Cambiar a True para ver queries SQL
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 280  # Reconectar cada 280 segundos
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
    
    # Inicializar SQLAlchemy
    db.init_app(app)
    
    # Crear tablas
    with app.app_context():
        try:
            # Probar conexión
            db.engine.connect()
            print("=" * 60)
            print("✅ CONEXIÓN A MYSQL EXITOSA")
            print("=" * 60)
            print(f"📊 Base de datos: {db_name}")
            print(f"🖥️  Host: {db_host}:{db_port}")
            print(f"👤 Usuario: {db_user}")
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

def test_connection():
    """
    Función auxiliar para probar la conexión sin Flask
    """
    import pymysql
    
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            port=3306,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL Version: {version[0]}")
            
            # Verificar si existe la base de datos
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if 'tictactoe_db' in databases:
                print("✅ Base de datos 'tictactoe_db' existe")
            else:
                print("⚠️  Base de datos 'tictactoe_db' NO existe")
                print("   Creándola...")
                cursor.execute("CREATE DATABASE tictactoe_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
                print("✅ Base de datos creada")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == '__main__':
    """
    Ejecutar este archivo directamente para probar la conexión:
    python database.py
    """
    print("\n🔍 PROBANDO CONEXIÓN A MYSQL...")
    print("=" * 60)
    test_connection()