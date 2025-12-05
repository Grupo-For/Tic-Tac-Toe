"""
test_crear_perfil.py
Pruebas TDD para la funcionalidad de Crear Perfil

CICLO TDD:
1. RED: Escribir pruebas que fallan
2. GREEN: Implementar código mínimo para que pasen
3. REFACTOR: Mejorar el código manteniendo las pruebas verdes
"""

import pytest
import json
from app_orm import app, db
from models import Perfil, Estadistica, Preferencia

# ============================================
# CONFIGURACIÓN DE FIXTURES
# ============================================

@pytest.fixture
def client():
    """
    Fixture que crea un cliente de prueba para Flask
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # BD en memoria
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Crear tablas
        yield client
        with app.app_context():
            db.drop_all()  # Limpiar después de cada test


@pytest.fixture
def init_database():
    """
    Fixture que inicializa la base de datos para cada test
    """
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


# ============================================
# FASE RED: PRUEBAS QUE FALLAN INICIALMENTE
# ============================================

class TestCrearPerfilRED:
    """
    Estas pruebas se escriben PRIMERO, antes de implementar el código
    Inicialmente todas fallarán (RED)
    """
    
    def test_crear_perfil_exitoso(self, client):
        """
        RED: Prueba básica de creación de perfil con datos válidos
        Debe retornar 201 y el perfil creado
        """
        data = {
            'nombre': 'Juan Pérez',
            'nombre_perfil': 'juan_gamer',
            'tipo_perfil': 'jugador'
        }
        
        response = client.post('/perfiles',
                               data=json.dumps(data),
                               content_type='application/json')
        
        assert response.status_code == 201
        json_data = response.get_json()
        
        assert json_data['mensaje'] == 'Perfil creado'
        assert json_data['perfil']['nombre'] == 'Juan Pérez'
        assert json_data['perfil']['nombre_perfil'] == 'juan_gamer'
        assert json_data['perfil']['tipo_perfil'] == 'jugador'
        assert 'id' in json_data['perfil']
    
    
    def test_crear_perfil_sin_nombre(self, client):
        """
        RED: Validación - Rechazar perfil sin nombre
        Debe retornar 400 con mensaje de error
        """
        data = {
            'nombre': '',
            'nombre_perfil': 'juan_gamer'
        }
        
        response = client.post('/perfiles',
                               data=json.dumps(data),
                               content_type='application/json')
        
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'error' in json_data
        assert 'requerido' in json_data['error'].lower()
    
    
    def test_crear_perfil_sin_nombre_perfil(self, client):
        """
        RED: Validación - Rechazar perfil sin nombre_perfil
        Debe retornar 400 con mensaje de error
        """
        data = {
            'nombre': 'Juan Pérez',
            'nombre_perfil': ''
        }
        
        response = client.post('/perfiles',
                               data=json.dumps(data),
                               content_type='application/json')
        
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'error' in json_data
    
    
    def test_crear_perfil_nombre_duplicado(self, client):
        """
        RED: Validación - Rechazar nombre de perfil duplicado
        Debe retornar 400 con mensaje específico
        """
        # Crear primer perfil
        data1 = {
            'nombre': 'Juan Pérez',
            'nombre_perfil': 'juan_gamer'
        }
        client.post('/perfiles',
                    data=json.dumps(data1),
                    content_type='application/json')
        
        # Intentar crear otro con mismo nombre_perfil
        data2 = {
            'nombre': 'Pedro López',
            'nombre_perfil': 'juan_gamer'
        }
        response = client.post('/perfiles',
                               data=json.dumps(data2),
                               content_type='application/json')
        
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'error' in json_data
        assert 'existe' in json_data['error'].lower()
    
    
    def test_perfil_tiene_estadisticas_inicializadas(self, client):
        """
        RED: El perfil debe tener estadísticas en 0 al crearse
        """
        data = {
            'nombre': 'María López',
            'nombre_perfil': 'maria_pro'
        }
        
        response = client.post('/perfiles',
                               data=json.dumps(data),
                               content_type='application/json')
        
        json_data = response.get_json()
        stats = json_data['perfil']['estadisticas']
        
        assert stats['victorias'] == 0
        assert stats['empates'] == 0
        assert stats['derrotas'] == 0
        assert stats['partidas_jugadas'] == 0
    
    
    def test_perfil_tiene_preferencias_por_defecto(self, client):
        """
        RED: El perfil debe tener preferencias por defecto al crearse
        """
        data = {
            'nombre': 'Carlos Ruiz',
            'nombre_perfil': 'carlos_king'
        }
        
        response = client.post('/perfiles',
                               data=json.dumps(data),
                               content_type='application/json')
        
        json_data = response.get_json()
        prefs = json_data['perfil']['preferencias']
        
        assert prefs['colorX'] == '#ff4d4d'
        assert prefs['colorO'] == '#4dff4d'
        assert prefs['symbolX'] == 'X'
        assert prefs['symbolO'] == 'O'
    
    
    def test_perfil_tiene_fecha_creacion(self, client):
        """
        RED: El perfil debe registrar fecha de creación
        """
        data = {
            'nombre': 'Ana Torres',
            'nombre_perfil': 'ana_player'
        }
        
        response = client.post('/perfiles',
                               data=json.dumps(data),
                               content_type='application/json')
        
        json_data = response.get_json()
        assert 'fecha_creacion' in json_data['perfil']
    
    
    def test_nombre_perfil_unico_en_bd(self, client):
        """
        RED: Verificar que el nombre_perfil sea UNIQUE en BD
        """
        with app.app_context():
            # Crear dos perfiles con mismo nombre_perfil directamente en BD
            perfil1 = Perfil('Usuario1', 'mismo_nombre')
            db.session.add(perfil1)
            db.session.commit()
            
            perfil2 = Perfil('Usuario2', 'mismo_nombre')
            db.session.add(perfil2)
            
            # Debe lanzar excepción por constraint UNIQUE
            with pytest.raises(Exception):
                db.session.commit()


# ============================================
# FASE GREEN: PRUEBAS DESPUÉS DE IMPLEMENTAR
# ============================================

class TestCrearPerfilGREEN:
    """
    Después de implementar el código, estas pruebas deben pasar (GREEN)
    """
    
    def test_integracion_completa(self, client):
        """
        GREEN: Prueba de integración completa del flujo
        """
        # Crear perfil
        data = {
            'nombre': 'Test User',
            'nombre_perfil': 'test_user_123'
        }
        
        response = client.post('/perfiles',
                               data=json.dumps(data),
                               content_type='application/json')
        
        assert response.status_code == 201
        
        # Verificar que se puede obtener el perfil creado
        perfil_id = response.get_json()['perfil']['id']
        
        response_get = client.get(f'/perfiles/{perfil_id}')
        assert response_get.status_code == 200
        
        perfil_data = response_get.get_json()
        assert perfil_data['nombre_perfil'] == 'test_user_123'
    
    
    def test_multiples_perfiles(self, client):
        """
        GREEN: Crear múltiples perfiles diferentes
        """
        perfiles = [
            {'nombre': 'User1', 'nombre_perfil': 'user1'},
            {'nombre': 'User2', 'nombre_perfil': 'user2'},
            {'nombre': 'User3', 'nombre_perfil': 'user3'}
        ]
        
        for perfil_data in perfiles:
            response = client.post('/perfiles',
                                   data=json.dumps(perfil_data),
                                   content_type='application/json')
            assert response.status_code == 201
        
        # Verificar que todos se crearon
        response_list = client.get('/perfiles')
        json_data = response_list.get_json()
        assert len(json_data['perfiles']) == 3


# ============================================
# FASE REFACTOR: PRUEBAS DE CÓDIGO MEJORADO
# ============================================

class TestCrearPerfilREFACTOR:
    """
    Después de refactorizar, todas las pruebas deben seguir pasando
    Además, agregamos pruebas de casos edge
    """
    
    def test_nombre_con_espacios(self, client):
        """
        REFACTOR: Manejar nombres con espacios correctamente
        """
        data = {
            'nombre': '  Juan   Pérez  ',
            'nombre_perfil': 'juan_gamer'
        }
        
        response = client.post('/perfiles',
                               data=json.dumps(data),
                               content_type='application/json')
        
        assert response.status_code == 201
        json_data = response.get_json()
        # Debe hacer trim automático
        assert json_data['perfil']['nombre'] == 'Juan   Pérez'
    
    
    def test_nombre_perfil_case_sensitive(self, client):
        """
        REFACTOR: Verificar que nombre_perfil sea case-sensitive
        """
        data1 = {'nombre': 'User1', 'nombre_perfil': 'TestUser'}
        data2 = {'nombre': 'User2', 'nombre_perfil': 'testuser'}
        
        response1 = client.post('/perfiles',
                                data=json.dumps(data1),
                                content_type='application/json')
        response2 = client.post('/perfiles',
                                data=json.dumps(data2),
                                content_type='application/json')
        
        # Ambos deben crearse (son diferentes)
        assert response1.status_code == 201
        assert response2.status_code == 201
    
    
    def test_caracteres_especiales_nombre(self, client):
        """
        REFACTOR: Aceptar caracteres especiales en nombres
        """
        data = {
            'nombre': 'José María Ñoño',
            'nombre_perfil': 'jose_maria'
        }
        
        response = client.post('/perfiles',
                               data=json.dumps(data),
                               content_type='application/json')
        
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['perfil']['nombre'] == 'José María Ñoño'
    
    
    def test_tipo_perfil_por_defecto(self, client):
        """
        REFACTOR: Si no se envía tipo_perfil, debe ser 'jugador'
        """
        data = {
            'nombre': 'Test User',
            'nombre_perfil': 'test_default'
        }
        
        response = client.post('/perfiles',
                               data=json.dumps(data),
                               content_type='application/json')
        
        json_data = response.get_json()
        assert json_data['perfil']['tipo_perfil'] == 'jugador'


# ============================================
# EJECUCIÓN DE PRUEBAS
# ============================================

if __name__ == '__main__':
    """
    Ejecutar todas las pruebas con pytest
    
    Comandos:
    - pytest test_crear_perfil.py -v                    # Modo verbose
    - pytest test_crear_perfil.py -v --tb=short         # Traceback corto
    - pytest test_crear_perfil.py::TestCrearPerfilRED   # Solo clase RED
    - pytest test_crear_perfil.py -k "exitoso"          # Solo tests con "exitoso"
    """
    pytest.main([__file__, '-v', '--tb=short'])