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
