import sqlite3
from sqlite3 import Error
import os

def create_connection():
    """
    Crea o conecta a la base de datos SQLite en la carpeta del proyecto.
    Devuelve un objeto de conexión o None si hay error.
    """
    conn = None
    try:
        # Ruta absoluta para la base de datos
        db_path = os.path.join(os.path.dirname(__file__), "quadra.db")
        print(f"\n[DEBUG] Conectando a BD en: {os.path.abspath(db_path)}")
        
        conn = sqlite3.connect(db_path)
        # Activar claves foráneas
        conn.execute("PRAGMA foreign_keys = ON")
        print("[DEBUG] ¡Conexión exitosa a SQLite!")
        return conn
    
    except Error as e:
        print(f"[ERROR] Fallo al conectar a SQLite: {e}")
        return None

def create_tables(conn):
    """
    Crea todas las tablas necesarias si no existen.
    Incluye:
    - food_stands (puestos de comida)
    - reviews (reseñas)
    - users (usuarios)
    """
    tables = {
        "food_stands": """
        CREATE TABLE IF NOT EXISTS food_stands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            latitude REAL,
            longitude REAL,
            photo_path TEXT,
            user_creator TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        "reviews": """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stand_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER CHECK (rating BETWEEN 1 AND 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stand_id) REFERENCES food_stands(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """,
        "users": """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    }
    
    try:
        cursor = conn.cursor()
        # Verificar si las tablas ya existen
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        # Crear tablas faltantes
        for table_name, sql in tables.items():
            if table_name not in existing_tables:
                print(f"[DEBUG] Creando tabla: {table_name}")
                cursor.execute(sql)
        
        conn.commit()
        print("[DEBUG] Todas las tablas verificadas/creadas correctamente.")
        
    except Error as e:
        print(f"[ERROR] Fallo al crear tablas: {e}")
        conn.rollback()

def verify_tables(conn):
    """Verifica que todas las tablas existan y tengan las columnas necesarias."""
    required_columns = {
        "food_stands": ["id", "name", "user_creator"],
        "reviews": ["id", "stand_id", "user_id", "rating"],
        "users": ["id", "username", "password"]
    }
    
    try:
        cursor = conn.cursor()
        for table, columns in required_columns.items():
            cursor.execute(f"PRAGMA table_info({table});")
            existing_columns = [col[1] for col in cursor.fetchall()]
            
            for col in columns:
                if col not in existing_columns:
                    raise Error(f"Columna faltante: {table}.{col}")
                    
        print("[DEBUG] Todas las tablas y columnas verificadas.")
        return True
        
    except Error as e:
        print(f"[ERROR] Verificación fallida: {e}")
        return False

# --- Código de prueba (opcional) ---
if __name__ == "__main__":
    print("\n--- Probando database.py ---")
    conn = create_connection()
    if conn:
        create_tables(conn)
        if verify_tables(conn):
            print("[DEBUG] Prueba completada. Estructura de BD correcta.")
        conn.close()