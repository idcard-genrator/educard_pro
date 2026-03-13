# app/models.py
from . import db
from flask_login import UserMixin

# 🔹 User model for Flask-Login authentication
class User(db.Model, UserMixin):
    __tablename__ = 'users'  # table name optional
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# 🔹 Optional: Student model for your PDF generation
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(50), unique=True, nullable=False)
    course = db.Column(db.String(100), nullable=True)
    photo = db.Column(db.String(200), nullable=True)  # photo path
    logo = db.Column(db.String(200), nullable=True)   # logo path

    def __repr__(self):
        return f"<Student {self.name} | {self.roll_no}>"