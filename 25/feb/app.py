from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
# Crear la aplicación 
app = Flask(__name__)
CORS(app)
# # Base de datos simulada (en memoria)
productos = [ {"id": 1, "nombre": "Laptop", "precio": 1200}, {"id": 2, "nombre": "Mouse", "precio": 25}, {"id": 3, "nombre": "Teclado", "precio": 75}]
# Ruta principal

@app.route('/')
def inicio(): 
    return jsonify({"mensaje": "Bienvenido a la API de Productos"})
# GET: Obtener todos los productos

@app.route('/api/productos', methods=['GET'])
def obtener_productos(): 
    return jsonify(productos), 200

# GET: Obtener un producto por ID
@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = next((p for p in productos if p['id'] == id), None) 
    if producto: 
        return jsonify(producto), 200 
    return jsonify({"error": "Producto no encontrado"}), 404

# POST: Crear un nuevo producto
@app.route('/api/productos', methods=['POST'])
def crear_producto(): 
    nuevo_producto = request.get_json() 
# Validación básica 

    if not nuevo_producto or 'nombre' not in nuevo_producto: 
        return jsonify({"error": "Datos inválidos"}), 400 
# Generar ID automático 
    nuevo_id = max([p['id'] for p in productos]) + 1 if productos else 1 
    nuevo_producto['id'] = nuevo_id 
    productos.append(nuevo_producto) 
    return jsonify(nuevo_producto), 201
# PUT: Actualizar un producto completo
@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id): 
    producto = next((p for p in productos if p['id'] == id), None) 
    if not producto: 
        return jsonify({"error": "Producto no encontrado"}), 404 
    datos = request.get_json() 
    producto.update(datos) 
    producto['id'] = id # Mantener el ID original
    return jsonify(producto), 200

# PATCH: Modificar parcialmente un producto
@app.route('/api/productos/<int:id>', methods=['PATCH'])
def modificar_producto(id): 
    producto = next((p for p in productos if p['id'] == id), None) 
    if not producto: 
        return jsonify({"error": "Producto no encontrado"}), 404 
    datos = request.get_json() 
    # Solo actualizar los campos enviados 
    for key, value in datos.items(): 
        if key != 'id': 
            # No permitir cambiar el ID 
            producto[key] = value 
    return jsonify(producto), 200
# DELETE: Eliminar un producto
#
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id): 
    global productos 
    producto = next((p for p in productos if p['id'] == id), None) 
    if not producto: 
        return jsonify({"error": "Producto no encontrado"}), 404 
    productos = [p for p in productos if p['id'] != id] 
    return jsonify({"mensaje": "Producto eliminado"}), 200

# Ejecutar la aplicación
if __name__ == '__main__': 
    app.run(debug=True, port=5000)
