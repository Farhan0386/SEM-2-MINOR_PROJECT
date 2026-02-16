from flask import Flask, render_template, request, redirect, url_for, session, flash
import database  

app = Flask(__name__)
app.secret_key = 'aura_secret_key_123' # Required for sessions

# Initialize DB on startup
database.init_db()

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
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
     app.run(debug=True)