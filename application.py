import os
import requests

from flask import Flask, render_template, jsonify, request
from models import *
from flask import session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import *
from sqlalchemy import and_, or_



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)



# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    

    counter = User.query.filter(and_(User.name==username, User.password==password)).count()

    if counter == 1:

        session['username'] = username
        return render_template("search.html")

    else:
      return render_template("error.html", message="Username or password is wrong")

@app.route("/register", methods=["GET","POST"])
def register():
    return render_template("register.html")

@app.route("/store", methods=["POST"])
def store():
    username = request.form.get("username")
    password = request.form.get("password")
    count = User.query.filter(User.name==username).count()

    if count > 0:
        return render_template("error.html",message="Username exists, please choose another name.")
    else:
        user = User(name=username, password=password)
        db.add(user)
        db.commit()
        return render_template("index.html",message="注册成功")

@app.route("/search", methods=["POST"])
def search():
    isbn = request.form.get("isbn")
    bookname = request.form.get("bookname")
    author = request.form.get("author")

    per="%"
    counter = Book.query.filter(and_(Book.isbn.like(per+isbn+per),Book.title.like(per+bookname+per),Book.author.like(per+author+per))).count()

    if counter > 0:
        books = Book.query.filter(and_(Book.isbn.like(per+isbn+per),Book.title.like(per+bookname+per),Book.author.like(per+author+per))).all()
        return render_template("books.html", books=books)
    else:
        return render_template("error.html", message="No such book")

@app.route("/books/<isbn>")
def book(isbn):

    book = Book.query.get(isbn)
    if book is None:
        return render_template("error.html", message="No such book")
    else:
        reviews = Review.query.filter(Review.isbn==isbn).all()
        counter = Review.query.filter(and_(Review.isbn==isbn),(Review.username==session['username'])).count()
        return render_template("book.html", book=book, remarks=reviews,counter=counter)

@app.route("/comment/<isbn>", methods=["POST"])
def comment(isbn):

        # Get form information.
        mark = request.form.get("mark")
        text = request.form.get("text")
        username = session['username']
    

        review = Review(username=username, isbn=isbn, mark=mark, text=text)
        db.add(review)
        db.commit()
        return render_template("search.html")

@app.route("/logout", methods=["POST"])
def logout():
    # remove the username from the session if it's there
    session.pop('username',None)
    return render_template("index.html")

@app.route("/api/books/<isbn>")
def flight_api(isbn):
    """Return details about a single flight."""

    # Make sure flight exists.
    book = Book.query.get(isbn)
    if book is None:
        abort(404)
    # Get the number of reviews.
    reviewnumber = Review.query.filter(Review.isbn==isbn).count()
    return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": reviewnumber
        })

if __name__ == "__main__":
    app.run()