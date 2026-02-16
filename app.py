import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key"   # Required for sessions

# --------------------
# Database Initialization
# --------------------

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# --------------------
# Routes
# --------------------

@app.route('/')
def home():
    return render_template('index.html')


# --------------------
# Register Route (With Password Hashing)
# --------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
            conn.close()
            return "User Registered Successfully"
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists"

    return render_template("register.html")


# --------------------
# Login Route (Secure Password Check)
# --------------------

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()

        # user[2] = stored hashed password
        if user and check_password_hash(user[2], password):
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Credentials"

    return render_template("login.html")


# --------------------
# Protected Dashboard
# --------------------

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return f"Welcome {session['username']}! You are logged in."
    else:
        return redirect(url_for("login"))


# --------------------
# Logout Route
# --------------------

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


# --------------------
# Run App
# --------------------

if __name__ == '__main__':
    app.run(debug=True)
