from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        return f"Login attempt for {username}"
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.methods=="POST":
         username=request.form["username"]
         password=request.form["password"]
         return f"Login attempt for {username}"
    return render_template("register.html")

if __name__=='__main__':
    app.run(debug=True)