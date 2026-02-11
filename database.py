import sqlite3

def get_connection():
    return sqlite3.connect("library.db")

def insert_book(title, author, department, copies):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO books (title, author, department, copies)
        VALUES (?, ?, ?, ?)
    """, (title, author, department, copies))
    conn.commit()
    conn.close()

def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    # Assuming your table has columns: id, title, author, department, copies
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def search_books_by_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    
    # The % symbols act as wildcards to match partial words
    search_term = f"%{query}%"
    
    cursor.execute("""
        SELECT * FROM books 
        WHERE title LIKE ? OR author LIKE ? OR department LIKE ?
    """, (search_term, search_term, search_term))
    
    results = cursor.fetchall()
    conn.close()
    return results