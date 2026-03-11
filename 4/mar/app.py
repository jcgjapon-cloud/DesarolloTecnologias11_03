import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    """Establece una conexión con la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE)
    # Permite acceder a las columnas por nombre como un diccionario
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Obtiene todas las tareas de la base de datos."""
    conn = get_db_connection()
    tasks_rows = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    conn.close()
    
    # Convertimos los objetos Row de SQLite a diccionarios de Python
    tasks = [dict(row) for row in tasks_rows]
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Obtiene una tarea específica por su ID."""
    conn = get_db_connection()
    task_row = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    
    if task_row is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    task = dict(task_row)
    return jsonify(task)



@app.route('/tasks', methods=['POST'])
def create_task():
    """Crea una nueva tarea."""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "El título es obligatorio"}), 400
    
    title = data['title']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"id": new_id, "title": title, "completed": 0}), 201

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

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Elimina una tarea por su ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    
    if deleted == 0:
        return jsonify({"error": "Tarea no encontrada"}), 404
        
    return jsonify({"message": "Tarea eliminada exitosamente"})

if __name__ == '__main__':
    # Ejecutamos la aplicación en modo desarrollo
    app.run(debug=True, port=5000)