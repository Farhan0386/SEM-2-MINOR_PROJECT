import sqlite3

# 1. Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect("library.db")

# 2. Create a cursor (used to execute SQL commands)
cursor = conn.cursor()

# 3. Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    copies INTEGER
)
""")

# 4. INSERT two books
# cursor.execute("""
# INSERT INTO books (title, author, copies)
# VALUES ('MATHS','R.D SHARMA',6)
# """)
# 5. DELETE two books

# cursor.execute("DELETE FROM books WHERE book_id=3")
cursor.execute("DELETE FROM books WHERE book_id=4")

# 6. Save changes
conn.commit()

# 7. Close the connection
conn.close()

print("Database and table created successfully.")
