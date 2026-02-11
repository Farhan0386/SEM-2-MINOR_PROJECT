import sqlite3
import csv
import os

def import_books_from_csv():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    seen_books = set()

    # 1. Dynamically calculate the absolute path to the folder where this script lives
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Safely join the path to the CSV file
    file_path = os.path.join(base_dir, 'DATA CLEANING OF DATASET', 'Library_cleaned.xlsx - Sheet1.csv')
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                title = row['book_Title']
                author = row['book_authors_AuthorName']
                
                book_identifier = f"{title}-{author}"
                
                if book_identifier not in seen_books:
                    department = row.get('library_branch_BranchName', 'General Library')
                    copies = int(row['book_copies_No_Of_Copies'])
                    
                    cursor.execute("""
                        INSERT INTO books (title, author, department, copies)
                        VALUES (?, ?, ?, ?)
                    """, (title, author, department, copies))
                    
                    seen_books.add(book_identifier)
                    print(f"Imported: '{title}' by {author}")

        conn.commit()
        print(f"\n✅ Successfully imported {len(seen_books)} unique books!")
        
    except FileNotFoundError:
        print(f"Error: Still cannot find the file at:\n{file_path}")
        print("Please check if the folder or file name has a typo.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        conn.close()

if __name__ == '__main__':
    import_books_from_csv()