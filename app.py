from flask import Flask, render_template, request, redirect, url_for, session, flash
import database  

app = Flask(__name__)
# Set a single secret key once
app.secret_key = 'aura_secret_key_123' 

# Initialize DB on startup
database.init_db()

# --- General Routes ---

@app.route('/')
def home():
    return render_template('home.html')

# --- User Authentication ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = f"{request.form.get('first_name')} {request.form.get('last_name')}"
        email = request.form.get('email')
        password = request.form.get('password')
        
        if database.create_user(name, email, password):
            flash("Account created! Please login.")
            return redirect(url_for('login'))
        flash("Email already registered.")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = database.verify_user(email, password)
        
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('home'))
        flash("Invalid credentials.")
    return render_template('login.html')

@app.route('/logout')
def user_logout():
    """Cleared duplicate function name conflict by renaming to user_logout."""
    session.clear()
    return redirect(url_for('home'))

# --- Admin Authentication ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Hardcoded credentials for now
        if username == "admin" and password == "password123":
            session['admin_logged_in'] = True
            session['user_name'] = "Administrator"
            flash("Welcome back, Admin!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid Admin Credentials.", "danger")
            
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    # Protection: check if admin is logged in
    if not session.get('admin_logged_in'):
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/admin/logout')
def admin_logout():
    # Clear admin status but keep user session if needed, 
    # or use session.clear() to log out of everything.
    session.pop('admin_logged_in', None)
    flash("Admin logged out successfully.", "info")
    return redirect(url_for('home'))
# --- Admin Book Management ---

@app.route('/admin/add_book', methods=['GET', 'POST'])
def add_book():
    """Route to handle adding a new book to the library."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        # Collect data from the form
        title = request.form.get('title')
        author = request.form.get('author')
        department = request.form.get('department')
        copies = request.form.get('copies')
        
        # Save to database
        database.insert_book(title, author, department, copies)
        flash(f"Book '{title}' added successfully!", "success")
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin.html') # This is your 'Add Book' form

@app.route('/admin/manage_inventory')
def manage_inventory():
    """Displays all books with options to edit or delete."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    # Fetch all books from DB
    all_books = database.get_all_books()
    return render_template('manage_books.html', books=all_books)

# --- Issue & Return Backend Logic ---

@app.route('/admin/issue_book', methods=['POST'])
def process_issue():
    """Backend logic to issue a book to a student."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    book_id = request.form.get('book_id')
    student_name = request.form.get('student_name')
    
    # Call the issue function which also reduces copy count
    if database.issue_book(book_id, student_name):
        flash("Book issued successfully!", "success")
    else:
        flash("Failed to issue book. Check if copies are available.", "danger")
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/return_book', methods=['POST'])
def process_return():
    """Backend logic to return a book."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    book_id = request.form.get('book_id')
    student_name = request.form.get('student_name')
    
    # Call the return function which increases copy count
    database.return_book(book_id, student_name)
    flash("Book returned successfully!", "info")
    
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
     app.run(debug=True)