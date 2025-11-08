from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'perfiles.json')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"perfiles": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/perfiles', methods=['POST'])
def crear_perfil():
    data = request.json
    db = load_data()
    
    if not data.get('nombre') or not data.get('nombre_perfil'):
        return jsonify({"error": "Nombre y nombre_perfil son requeridos"}), 400
    
    for perfil in db['perfiles']:
        if perfil['nombre_perfil'] == data['nombre_perfil']:
            return jsonify({"error": "El nombre de perfil ya existe"}), 400
    
    nuevo_perfil = {
        "id": len(db['perfiles']) + 1,
        "nombre": data['nombre'],
        "nombre_perfil": data['nombre_perfil'],
        "tipo_perfil": data.get('tipo_perfil', 'jugador'),
        "historial_partidas": [],
        "estadisticas": {
            "victorias": 0,
            "empates": 0,
            "derrotas": 0,
            "partidas_jugadas": 0
        },
        "preferencias": data.get('preferencias', {
            "colorX": "#ff4d4d",
            "colorO": "#4dff4d",
            "symbolX": "X",
            "symbolO": "O"
        }),
        "fecha_creacion": datetime.now().isoformat()
    }
    
    db['perfiles'].append(nuevo_perfil)
    save_data(db)
    
    return jsonify({"mensaje": "Perfil creado", "perfil": nuevo_perfil}), 201

@app.route('/perfiles', methods=['GET'])
def listar_perfiles():
    db = load_data()
    return jsonify(db)

@app.route('/perfiles/<int:perfil_id>', methods=['GET'])
def obtener_perfil(perfil_id):
    db = load_data()
    perfil = next((p for p in db['perfiles'] if p['id'] == perfil_id), None)
    
    if perfil:
        return jsonify(perfil)
    else:
        return jsonify({"error": "Perfil no encontrado"}), 404

@app.route('/perfiles/<int:perfil_id>', methods=['PUT'])
def actualizar_perfil(perfil_id):
    data = request.json
    db = load_data()
    
    perfil = next((p for p in db['perfiles'] if p['id'] == perfil_id), None)
    if not perfil:
        return jsonify({"error": "Perfil no encontrado"}), 404
    
    campos_permitidos = ['nombre', 'nombre_perfil', 'preferencias']
    for campo in campos_permitidos:
        if campo in data:
            perfil[campo] = data[campo]
    
    if 'estadisticas' in data:
        perfil['estadisticas'].update(data['estadisticas'])
    
    if 'nueva_partida' in data:
        partida = data['nueva_partida']
        partida['fecha'] = datetime.now().isoformat()
        perfil['historial_partidas'].append(partida)
    
    save_data(db)
    return jsonify({"mensaje": "Perfil actualizado", "perfil": perfil})

@app.route('/perfiles/<int:perfil_id>', methods=['DELETE'])
def eliminar_perfil(perfil_id):
    db = load_data()
    perfil = next((p for p in db['perfiles'] if p['id'] == perfil_id), None)
    
    if not perfil:
        return jsonify({"error": "Perfil no encontrado"}), 404
    
    db['perfiles'] = [p for p in db['perfiles'] if p['id'] != perfil_id]
    save_data(db)
    
    return jsonify({"mensaje": "Perfil eliminado"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)