# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, send_file, flash
from . import db
from .models import User, Student
from flask_login import login_required, current_user
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os

main = Blueprint('main', __name__)

# 🔹 Home Page
@main.route('/')
@login_required
def index():
    return render_template('index.html')

# 🔹 Add Student
@main.route('/add-student', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        roll_no = request.form.get('roll_no')
        course = request.form.get('course')
        photo_file = request.files.get('photo')
        logo_file = request.files.get('logo')

        # Save photo
        photo_path = None
        if photo_file:
            photo_path = os.path.join('static/uploads/photos', photo_file.filename)
            os.makedirs(os.path.dirname(photo_path), exist_ok=True)
            photo_file.save(photo_path)

        # Save logo
        logo_path = None
        if logo_file:
            logo_path = os.path.join('static/uploads/logos', logo_file.filename)
            os.makedirs(os.path.dirname(logo_path), exist_ok=True)
            logo_file.save(logo_path)

        student = Student(
            name=name,
            roll_no=roll_no,
            course=course,
            photo=photo_path,
            logo=logo_path
        )
        db.session.add(student)
        db.session.commit()
        flash("Student added successfully!", "success")
        return redirect(url_for('main.view_students'))

    return render_template('add_student.html')

# 🔹 View Students
@main.route('/view-students')
@login_required
def view_students():
    students = Student.query.all()
    return render_template('view_students.html', students=students)

# 🔹 Generate PDF
@main.route('/generate-pdf/<int:student_id>')
@login_required
def generate_pdf(student_id):
    student = Student.query.get_or_404(student_id)
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Logo
    if student.logo and os.path.exists(student.logo):
        logo = ImageReader(student.logo)
        c.drawImage(logo, 50, height - 100, width=100, height=50)

    # Student Photo
    if student.photo and os.path.exists(student.photo):
        photo = ImageReader(student.photo)
        c.drawImage(photo, width - 150, height - 150, width=100, height=100)

    # Student Info
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 200, f"Name: {student.name}")
    c.drawString(50, height - 230, f"Roll No: {student.roll_no}")
    if student.course:
        c.drawString(50, height - 260, f"Course: {student.course}")

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"{student.name}_card.pdf", mimetype='application/pdf')