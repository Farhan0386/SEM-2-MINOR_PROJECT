import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def get_connection():
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect("library.db")

def init_db():
    """Initializes all required tables: books, users, and transactions."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Books Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            department TEXT NOT NULL,
            copies INTEGER NOT NULL
        )
    """)
    
    # 2. Users Table (for Student/User login)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # 3. Transactions Table (for Issue/Return tracking)
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

# --- Book Management (Admin Features) ---

def insert_book(title, author, department, copies):
    """Adds a new book to the inventory."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, department, copies)
        VALUES (?, ?, ?, ?)
    """, (title, author, department, copies))
    conn.commit()
    conn.close()

def get_all_books():
    """Retrieves all books from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def get_book_by_id(book_id):
    """Fetches a single book's details for editing."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    return book

def update_book(book_id, title, author, department, copies):
    """Updates existing book details."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books 
        SET title = ?, author = ?, department = ?, copies = ?
        WHERE id = ?
    """, (title, author, department, copies, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    """Removes a book from the inventory."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

def search_books_by_query(query):
    """Searches books by title, author, or department."""
    conn = get_connection()
    cursor = conn.cursor()
    search_term = f"%{query}%"
    cursor.execute("""
        SELECT * FROM books 
        WHERE title LIKE ? OR author LIKE ? OR department LIKE ?
    """, (search_term, search_term, search_term))
    results = cursor.fetchall()
    conn.close()
    return results

# --- User Authentication ---

def create_user(name, email, password):
    """Hashes the password and saves a new user."""
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
    """Verifies user credentials using password hashing."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[3], password):
        return user 
    return None

# --- Issue and Return Logic ---

def issue_book(book_id, student_name):
    """Records a book issue and reduces inventory count by 1."""
    conn = get_connection()
    cursor = conn.cursor()
    # Check if copies are available
    cursor.execute("SELECT copies FROM books WHERE id = ?", (book_id,))
    res = cursor.fetchone()
    if res and res[0] > 0:
        # Record transaction
        cursor.execute("INSERT INTO transactions (book_id, student_name, action) VALUES (?, ?, 'issue')", 
                       (book_id, student_name))
        # Update copy count
        cursor.execute("UPDATE books SET copies = copies - 1 WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def return_book(book_id, student_name):
    """Records a book return and increases inventory count by 1."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (book_id, student_name, action) VALUES (?, ?, 'return')", 
                   (book_id, student_name))
    cursor.execute("UPDATE books SET copies = copies + 1 WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()