import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import database

app = Flask(__name__)
app.secret_key = 'aura_secret_key_123'

# File Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

database.init_db()

# --- Admin Authentication ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        if user == "admin" and pw == "password123":
            session['admin_logged_in'] = True
            flash("Welcome back, Admin!", "success")
            return redirect(url_for('admin_dashboard'))
        flash("Invalid Credentials.", "danger")
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("Admin logged out successfully.", "info")
    return redirect(url_for('home'))

# --- Admin Resource Management ---

@app.route('/admin/add_book', methods=['GET', 'POST'])
def add_book():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        dept = request.form.get('department')
        copies = request.form.get('copies')
        isbn = request.form.get('isbn')
        desc = request.form.get('description')
        
        file = request.files.get('image')
        filename = "default_book.png"
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        database.insert_book(title, author, dept, copies, isbn, desc, filename)
        flash(f"'{title}' added to {dept} inventory!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin.html')

@app.route('/admin/inventory')
def manage_inventory():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    dept_filter = request.args.get('department')
    if dept_filter:
        books = database.get_books_by_department(dept_filter)
    else:
        books = database.get_all_books()
        
    return render_template('manage_books.html', books=books, current_dept=dept_filter)

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
                flash("Error: No copies available!", "danger")
        else:
            database.return_book(book_id, student_name)
            flash(f"Book returned by {student_name}.", "info")
            
        return redirect(url_for('admin_dashboard'))

    books = database.get_all_books()
    return render_template('issue_return.html', books=books)

# --- General Routes (Home/Register/Login) ---

@app.route('/')
def home():
    return render_template('home.html')

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

if __name__ == '__main__':
    app.run(debug=True)