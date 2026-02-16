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

# --- Admin Functionality ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Hardcoded credentials for administration
        if username == "admin" and password == "password123":
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_login.html', error="Invalid Credentials")
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    # Simple access control
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/admin/delete/<int:book_id>')
def delete_book_route(book_id):
    if not session.get('logged_in'): 
        return redirect(url_for('admin_login'))
    database.delete_book(book_id)
    return redirect(url_for('manage_books'))

@app.route('/admin/logout')
def admin_logout():
    """Renamed from 'logout' to prevent conflict with the user logout function."""
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
     app.run(debug=True)