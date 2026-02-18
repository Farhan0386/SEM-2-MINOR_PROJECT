import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def get_connection():
    return sqlite3.connect("library.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Books Table with ISBN, Description, and Images
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            department TEXT NOT NULL,
            copies INTEGER NOT NULL,
            isbn TEXT,
            description TEXT,
            image_filename TEXT
        )
    """)
    # Users Table for student registration
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    # Transactions Table for Issue/Return tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            student_name TEXT,
            action TEXT, 
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    """)
    conn.commit()
    conn.close()

def insert_book(title, author, dept, copies, isbn, desc, filename):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, department, copies, isbn, description, image_filename)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, author, dept, copies, isbn, desc, filename))
    conn.commit()
    conn.close()

def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def get_books_by_department(dept):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE department = ?", (dept,))
    books = cursor.fetchall()
    conn.close()
    return books

def issue_book(book_id, student_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT copies FROM books WHERE id = ?", (book_id,))
    res = cursor.fetchone()
    if res and res[0] > 0:
        cursor.execute("INSERT INTO transactions (book_id, student_name, action) VALUES (?, ?, 'issue')", (book_id, student_name))
        cursor.execute("UPDATE books SET copies = copies - 1 WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def return_book(book_id, student_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (book_id, student_name, action) VALUES (?, ?, 'return')", (book_id, student_name))
    cursor.execute("UPDATE books SET copies = copies + 1 WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

def create_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = generate_password_hash(password)
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user[3], password):
        return user
    return None