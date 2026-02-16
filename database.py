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

# Add to database.py

def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

def update_book(book_id, title, author, department, copies):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books 
        SET title = ?, author = ?, department = ?, copies = ?
        WHERE id = ?
    """, (title, author, department, copies, book_id))
    conn.commit()
    conn.close()

# New Table for Issue/Return
def create_transaction_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            student_name TEXT,
            action TEXT, -- 'issue' or 'return'
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    """)
    conn.commit()
    conn.close()