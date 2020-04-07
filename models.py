import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)

class User(db.Model):
    __tablename__ = "users"
    name = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey("users.name"), nullable=False)
    isbn = db.Column(db.String, db.ForeignKey("books.isbn"),nullable=False)
    mark = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String, nullable=True)
