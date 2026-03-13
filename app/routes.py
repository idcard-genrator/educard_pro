from flask import render_template, request, redirect, url_for, flash, make_response, current_app
from app.models import Student
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import os
from io import BytesIO

# Dusra route - add student
@main.route('/add-student', methods=['GET', 'POST'])
def add_student():
    return render_template("add_student.html")


# View students route
@main.route('/view-students')
def view_students():
    students = Student.query.all()
    return render_template("view_students.html", students=students)


# Edit student route
@main.route('/edit-student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.class_name = request.form['class_name']
        # Add more fields as required
        # db.session.commit()  # Don't forget to commit changes in real code
        flash('Student updated successfully!', 'success')
        return redirect(url_for('main.view_students'))
    return render_template("edit_student.html", student=student)


# 👇 ID Card PDF Download route
@main.route('/download-id-card/<int:student_id>')
def download_id_card(student_id):
    student = Student.query.get_or_404(student_id)

    from io import BytesIO
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    import os

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    # 🔹 Absolute paths for logo & photo
    base_dir = os.path.abspath(os.path.dirname(__file__))
    logo_path = os.path.join(base_dir, '..', 'static', 'logo.png')
    student_photo_path = os.path.join(base_dir, '..', 'static', 'uploads', student.photo)

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=100, height=100)
        elements.append(logo)
        elements.append(Spacer(1, 12))

    if os.path.exists(student_photo_path):
        photo = Image(student_photo_path, width=150, height=150)
        elements.append(photo)
        elements.append(Spacer(1, 12))

    # Student info
    elements.append(Paragraph(f"<b>Name:</b> {student.name}", styles['Normal']))
    elements.append(Paragraph(f"<b>Class:</b> {student.class_name}", styles['Normal']))
    elements.append(Paragraph(f"<b>ID:</b> {student.id}", styles['Normal']))

    pdf.build(elements)

    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=id_card_{student.id}.pdf'

    return response