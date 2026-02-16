import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import database  

# 1. APPLICATION SETUP
app = Flask(__name__)
app.secret_key = 'aura_secret_key_123' 

# 2. FILE UPLOAD CONFIGURATION
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize the database tables on startup
database.init_db()

# --- General Routes ---

@app.route('/')
def home():
    return render_template('home.html')

# --- User Authentication (Students) ---

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
    session.clear()
    return redirect(url_for('home'))

# --- Admin Authentication ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
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
    if not session.get('admin_logged_in'):
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("Admin logged out successfully.", "info")
    return redirect(url_for('home'))

# --- Unified Admin Book Management (With Image Upload) ---

@app.route('/admin/add_book', methods=['GET', 'POST'])
def add_book():
    """Handles adding a new book with ISBN, Description, and Cover Image."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        # Get textual data
        title = request.form.get('title')
        author = request.form.get('author')
        department = request.form.get('department')
        copies = request.form.get('copies')
        isbn = request.form.get('isbn')
        description = request.form.get('description')
        
        # Handle File Upload logic
        file = request.files.get('image')
        filename = "default_book.png" # Standard default image
        
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Call database function with all 7 parameters
        database.insert_book(title, author, department, copies, isbn, description, filename)
        flash(f"Book '{title}' added with image successfully!", "success")
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin.html') 

@app.route('/admin/manage_inventory')
def manage_inventory():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    all_books = database.get_all_books()
    return render_template('manage_books.html', books=all_books)

# --- Issue & Return Logic ---

@app.route('/admin/issue_return', methods=['GET', 'POST'])
def issue_return():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        book_id = request.form.get('book_id')
        student_name = request.form.get('student_name')
        action = request.form.get('action') 

        if action == 'issue':
            if database.issue_book(book_id, student_name):
                flash(f"Book issued to {student_name}.", "success")
            else:
                flash("Error: No copies available for issue.", "danger")
        else:
            database.return_book(book_id, student_name)
            flash(f"Book returned by {student_name}.", "info")
            
        return redirect(url_for('admin_dashboard'))

    books = database.get_all_books()
    return render_template('issue_return.html', books=books)

if __name__ == '__main__':
     app.run(debug=True)