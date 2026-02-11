from flask import Flask, render_template, request, redirect, url_for
import database  
import ollama  

app = Flask(__name__)

# --- Routes ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        department = request.form['department']
        copies = request.form['copies']
        database.insert_book(title, author, department, copies)
        return redirect(url_for('view_books'))
    
    return render_template('admin.html')

@app.route('/view')
def view_books():
    all_books = database.get_all_books() 
    return render_template('view_books.html', books=all_books)

@app.route('/search', methods=['GET', 'POST'])
def search_books():
    search_results = None
    query = ""
    
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            search_results = database.search_books_by_query(query)
            
    return render_template('search_books.html', results=search_results, query=query)

# --- AI Integration Routes ---

@app.route('/chat')
def ai_chat():
    return render_template('ai_chat.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return {"error": "No message provided"}, 400

    try:
        # 1. Fetch the real inventory from your database
        all_books = database.get_all_books()
        
        # 2. Convert the database rows into a text list the AI can read
        if all_books:
            inventory_text = "\n".join([f"- '{book[1]}' by {book[2]} (Copies: {book[4]})" for book in all_books])
        else:
            inventory_text = "The library is currently completely empty. No books exist in the database."

        # 3. Create a strict, grounded prompt
        grounded_prompt = f"""You are the strict KRMU Library Assistant AI. 
You must ONLY answer questions based on the exact inventory list below. 
Do not invent, guess, or assume we have any other books. If the user asks for a book or category not in this list, explicitly tell them it is not available.

CURRENT ACTUAL INVENTORY:
{inventory_text}

User Question: {user_message}"""

        # 4. Send the grounded prompt to your local model
        response = ollama.chat(model='phi3', messages=[
            {
                'role': 'user',
                'content': grounded_prompt
            },
        ])
        
        return {"response": response['message']['content']}
    except Exception as e:
        return {"error": str(e)}, 500
    
if __name__ == '__main__':
    app.run(debug=True)