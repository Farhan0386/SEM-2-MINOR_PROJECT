import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def get_connection():
    return sqlite3.connect("library.db")

def init_db():
    """Initializes the database with books and users tables."""
    conn = get_connection()
    cursor = conn.cursor()
    # Books Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            department TEXT NOT NULL,
            copies INTEGER NOT NULL
        )
    """)
    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def create_user(name, email, password):
    """Hashes password and saves user to DB."""
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = generate_password_hash(password)
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                       (name, email, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Email already exists
    finally:
        conn.close()

def verify_user(email, password):
    """Checks if user exists and password matches."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[3], password):
        return user # Returns (id, name, email, password)
    return None

# Keep your existing insert_book, get_all_books, and search functions here...