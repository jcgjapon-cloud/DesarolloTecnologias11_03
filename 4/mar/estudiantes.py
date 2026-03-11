import sqlite3
from turtle import title
from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    """Establece una conexión con la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE)
    # Permite acceder a las columnas por nombre como un diccionario
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    """Obtiene todos los estudiantes de la base de datos."""
    conn = get_db_connection()
    estudiantes_rows = conn.execute('SELECT * FROM Estudiantes ORDER BY id DESC').fetchall()
    conn.close()
    
    estudiantes = [dict(row) for row in estudiantes_rows]
    return jsonify(estudiantes)

@app.route('/estudiantes/<int:estudiante_id>', methods=['GET'])
def get_estudiante(estudiante_id):
    """Obtiene un estudiante específico por su ID."""
    conn = get_db_connection()
    estudiante_row = conn.execute('SELECT * FROM Estudiantes WHERE id = ?', (estudiante_id,)).fetchone()
    conn.close()
    
    if estudiante_row is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    estudiante = dict(estudiante_row)
    return jsonify(estudiante)



@app.route('/estudiantes', methods=['POST'])
def create_task():
    """Crea una nueva tarea."""
    data = request.get_json()
    
    if not data or 'nombre' not in data:
        return jsonify({"error": "El nombre es obligatorio"}), 400
    
    nombre = data['nombre']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Estudiantes (nombre) VALUES (?)', (nombre,))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"id": new_id, "nombre": nombre, "completed": 0}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Actualiza el estado de una tarea (completada o no)."""
    data = request.get_json()
    completed = data.get('completed')
    
    if completed is None:
        return jsonify({"error": "Faltan datos para actualizar"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (completed, task_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    
    if updated == 0:
        return jsonify({"error": "Tarea no encontrada"}), 404
        
    return jsonify({"message": "Tarea actualizada correctamente"})

@app.route('/estudiantes/<int:estudiante_id>', methods=['DELETE'])
def delete_estudiante(estudiante_id):
    """Elimina un estudiante por su ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Estudiantes WHERE id = ?', (estudiante_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    
    if deleted == 0:
        return jsonify({"error": "Estudiante no encontrado"}), 404
        
    return jsonify({"message": "Estudiante eliminado exitosamente"})

if __name__ == '__main__':
    # Ejecutamos la aplicación en modo desarrollo
    app.run(debug=True, port=5000)