"""
Program: David_Brown_Assignment6.py
Author: David Brown
Date: 5/2/26
Purpose: Create one Flask app using Flask, SQLAlchemy, CRUD, REST API, JSON, and GET method calculator
"""

"""
Q1. What does db.session.commit() do?

It saves the changes to the database. If I add, update, or delete a record, commit makes that change permanent.

Q2. Why do we use JSON in APIs?

We use JSON because it is easy for apps to send and receive data. It is also readable and works well between web pages, servers, and databases.
"""

from flask import Flask, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy


"""
Step 1:
Create a Flask app and connect to a SQLite database.
"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment6.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


"""
Lab 1:
Student Records CRUD App
This model stores student names and courses.
"""

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)


"""
Lab 2:
Book Management REST API
This model stores book titles and authors.
"""

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))


"""
Create the database tables.
"""

with app.app_context():
    db.create_all()


"""
Home Page:
Shows links to each part of the assignment.
"""

@app.route('/')
def home():
    students = Student.query.all()

    student_list = ""

    for student in students:
        student_list += f"""
        <p>
            {student.name} - {student.course}
            <a href="/delete_student/{student.id}">Delete</a>
        </p>
        """

    return f"""
    <html>
    <head>
        <title>Assignment 6 Flask App</title>
    </head>

    <body>
        <h1>Assignment 6 Flask App</h1>

        <h2>Student Records</h2>

        {student_list}

        <br>

        <a href="/student_form">Add Student</a>

        <br><br>

        <a href="/calc">Open Calculator</a>

        <br><br>

        <a href="/book_form">Add Book</a>

        <br><br>

        <a href="/books">View Books JSON</a>
    </body>
    </html>
    """


"""
Lab 1:
Student form page.
"""

@app.route('/student_form')
def student_form():
    return """
    <html>
    <head>
        <title>Add Student</title>
    </head>

    <body>
        <h1>Add Student</h1>

        <form action="/add" method="POST">
            <label>Student Name:</label>
            <input type="text" name="name" required>

            <br><br>

            <label>Course:</label>
            <input type="text" name="course" required>

            <br><br>

            <button type="submit">Add Student</button>
        </form>

        <br>

        <a href="/">Back Home</a>
    </body>
    </html>
    """


"""
Lab 1:
Add student route.
This route uses POST to add a new student.
"""

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    course = request.form['course']

    new_student = Student(name=name, course=course)

    db.session.add(new_student)
    db.session.commit()

    return redirect(url_for('home'))


"""
Lab 1:
Delete student route.
This shows the delete part of CRUD.
"""

@app.route('/delete_student/<int:id>')
def delete_student(id):
    student = Student.query.get(id)

    if student:
        db.session.delete(student)
        db.session.commit()

    return redirect(url_for('home'))


"""
Lab 2:
GET endpoint.
This shows all books as JSON.
"""

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()

    return jsonify([
        {
            "id": book.id,
            "title": book.title,
            "author": book.author
        }
        for book in books
    ])


"""
Lab 2:
POST endpoint.
This adds a new book using JSON.
This route is for API testing.
"""

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    new_book = Book(
        title=data['title'],
        author=data['author']
    )

    db.session.add(new_book)
    db.session.commit()

    return {"message": "Book added"}


"""
Lab 2:
DELETE endpoint.
This deletes a book by id.
"""

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)

    if book:
        db.session.delete(book)
        db.session.commit()
        return {"message": "Deleted"}

    return {"message": "Book not found"}


"""
Lab 2:
Book form page.
This lets me add a book from the browser.
"""

@app.route('/book_form')
def book_form():
    return """
    <html>
    <head>
        <title>Add Book</title>
    </head>

    <body>
        <h1>Add Book</h1>

        <form action="/add_book_form" method="POST">
            <label>Book Title:</label>
            <input type="text" name="title" required>

            <br><br>

            <label>Author:</label>
            <input type="text" name="author" required>

            <br><br>

            <button type="submit">Add Book</button>
        </form>

        <br>

        <a href="/">Back Home</a>
    </body>
    </html>
    """


"""
Lab 2:
Add book from browser form.
This adds a book and sends me to the JSON page.
"""

@app.route('/add_book_form', methods=['POST'])
def add_book_form():
    title = request.form['title']
    author = request.form['author']

    new_book = Book(title=title, author=author)

    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for('get_books'))


"""
Lab 3:
Calculator form.
This uses GET method only.
"""

@app.route('/calc')
def calc():
    return """
    <html>
    <head>
        <title>Simple Calculator</title>
    </head>

    <body>
        <h1>Simple Calculator</h1>

        <form action="/result" method="GET">
            <label>Number 1:</label>
            <input type="number" name="num1" required>

            <br><br>

            <label>Number 2:</label>
            <input type="number" name="num2" required>

            <br><br>

            <label>Operation:</label>
            <select name="operation">
                <option value="add">Add</option>
                <option value="subtract">Subtract</option>
                <option value="multiply">Multiply</option>
            </select>

            <br><br>

            <button type="submit">Calculate</button>
        </form>

        <br>

        <a href="/">Back Home</a>
    </body>
    </html>
    """


"""
Lab 3:
Result page.
This uses request.args to get values from the URL.
"""

@app.route('/result')
def result():
    num1 = float(request.args.get('num1'))
    num2 = float(request.args.get('num2'))
    operation = request.args.get('operation')

    if operation == "add":
        answer = num1 + num2
        symbol = "+"

    elif operation == "subtract":
        answer = num1 - num2
        symbol = "-"

    elif operation == "multiply":
        answer = num1 * num2
        symbol = "*"

    else:
        answer = "Invalid operation"
        symbol = "?"

    return f"""
    <html>
    <head>
        <title>Calculator Result</title>
    </head>

    <body>
        <h1>Calculator Result</h1>

        <p>{num1} {symbol} {num2} = {answer}</p>

        <br>

        <a href="/calc">Try Again</a>

        <br><br>

        <a href="/">Back Home</a>
    </body>
    </html>
    """


"""
Run the Flask app.
"""

if __name__ == '__main__':
    app.run()
