from flask import Flask, render_template, request
import database

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/add", methods=["POST"])
def add_book():
    title = request.form["title"]
    author = request.form["author"]
    department = request.form["department"]
    copies = request.form["copies"]

    database.insert_book(title, author, department, copies)

    return "Book added successfully!"

if __name__ == "__main__":
    app.run(debug=True)
