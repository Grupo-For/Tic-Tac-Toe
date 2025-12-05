"""
config/db_test.py
Funciones para probar la conexión a MySQL
"""

import pymysql


def test_connection():
    """
    Función auxiliar para probar la conexión sin Flask
    """
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
    python config/db_test.py
    """
    print("\n🔍 PROBANDO CONEXIÓN A MYSQL...")
    print("=" * 60)
    test_connection()