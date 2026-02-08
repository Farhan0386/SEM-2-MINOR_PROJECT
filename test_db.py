import sqlite3

#                                    1. Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect("library.db")

#                                    2. Create a cursor (used to execute SQL commands)
cursor = conn.cursor()

#                                     3. Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    department TEXT,
    copies INTEGER
              
)
""")

#                                     4. INSERT  books
# cursor.execute("""
# INSERT INTO books (title, author, department, copies)
# VALUES ('ENGLISH','R.D GUPTA','ARTS',6)
# """)


#                                     5. DELETE two books 
# cursor.execute("DELETE FROM books WHERE book_id=3")
# cursor.execute("DELETE FROM books WHERE book_id=4")



#                                     6. PRINT ALL BOOKS FROM THE TABLE
# cursor.execute("SELECT * FROM books")
# rows=cursor.fetchall()
# for row in rows:
#     print(row)



#                                     7. PRINT A BOOK WITH A SPECIFIC ID
# cursor.execute("SELECT * FROM books WHERE book_id=1")
# row = cursor.fetchone()
# if row:
#     print(row)



#                                     8. PRINT A BOOK WITH A SPECIFIC TITLE
# cursor.execute("select * from books where title='MATHS'")
# row=cursor.fetchall()
# for i in row:
#     print(i)

#                                     9. Issue a command to update the number of copies of a book with a specific ID
# cursor.execute("""
# update books set copies =copies-1 where book_id=1
# """)



#                                     9. Issue a command to update the number of copies of a book with a specific ID
# cursor.execute("""
# update books set copies =copies+1 where book_id=1
# """)



#                                     10. Rename the column "departement" to "department"
# cursor.execute("""
# ALTER TABLE books
# RENAME COLUMN departement TO department
# """)

#                                     11. update the department of a book with a specific ID
# cursor.execute("""
# UPDATE books
# SET department = 'CSE'
# WHERE book_id = 1
# """)


#                                     12. Save changes BY THIS COMMIT() FUNCTION WE CAN SAVE ALL OPERATIONS IN THE DATABASE
# conn.commit()


#                                     13. Close the connection BY THIS CLOSE() FUNCTION WE CAN CLOSE THE CONNECTION TO THE DATABASE
# conn.close()

# print("Database and table created successfully.")
