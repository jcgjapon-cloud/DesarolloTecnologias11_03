import sqlite3

def setup_database():
    """Script independiente para crear la base de datos y su esquema inicial."""
    try:
        # Se conecta al archivo (lo crea si no existe)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Creamos la tabla de tareas
        print("Creando tabla 'tasks'...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Insertar algunos datos de prueba (Seed data)
        cursor.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)", 
                       ("Aprender sobre persistencia", 1))
        cursor.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)", 
                       ("Configurar SQLite con Flask", 0))

        conn.commit()
        print("Base de datos inicializada con éxito.")
        
    except sqlite3.Error as e:
        print(f"Error al configurar la base de datos: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    setup_database()