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
        # This calls the llama3 model running locally on your laptop
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': f"You are a helpful library assistant for KRMU. Answer this concise question: {user_message}"
            },
        ])
        
        return {"response": response['message']['content']}
    except Exception as e:
        return {"error": str(e)}, 500
    
if __name__ == '__main__':
    app.run(debug=True)