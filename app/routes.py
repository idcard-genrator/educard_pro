# app/routes.py
from flask import Blueprint, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
import os
from .models import Student

main = Blueprint('main', __name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/add-student', methods=['GET', 'POST'])
def add_student():
    # Example logic for adding student
    if request.method == 'POST':
        # Fetch data from form
        name = request.form['name']
        photo_file = request.files['photo']

        # Save photo in static/uploads
        photo_path = os.path.join(BASE_DIR, '..', 'static', 'uploads', photo_file.filename)
        photo_file.save(photo_path)

        # Save student to DB (if you have DB logic)
        student = Student(name=name, photo=photo_file.filename)
        from . import db
        db.session.add(student)
        db.session.commit()

        return "Student added successfully!"
    return render_template('add_student.html')

@main.route('/generate-pdf/<int:student_id>')
def generate_pdf(student_id):
    from . import db
    student = Student.query.get_or_404(student_id)

    pdf_path = os.path.join(BASE_DIR, '..', 'id_card_{}.pdf'.format(student.id))
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    elements = []

    # Logo
    logo_path = os.path.join(BASE_DIR, '..', 'static', 'logo.png')
    elements.append(Image(logo_path, width=100, height=100))

    elements.append(Spacer(1, 20))
    
    # Student photo
    student_photo_path = os.path.join(BASE_DIR, '..', 'static', 'uploads', student.photo)
    elements.append(Image(student_photo_path, width=100, height=100))

    elements.append(Spacer(1, 20))

    # Student Name
    elements.append(Paragraph("Name: {}".format(student.name), style=None))
    
    doc.build(elements)

    return send_file(pdf_path, as_attachment=True)