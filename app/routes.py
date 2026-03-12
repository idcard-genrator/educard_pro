print("ROUTES FILE LOADED")
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app,send_file
from werkzeug.utils import secure_filename
from . import db
from .models import Student,School
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from flask import send_file
from weasyprint import HTML
from flask import make_response

main = Blueprint('main', __name__)

@main.route('/')
def home():
    print("hello")
    return redirect(url_for('main.add_student'))

# Add Student
@main.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        father_name = request.form['father_name']
        student_class = request.form['student_class']
        roll_no = request.form['roll_no']
        address = request.form['address']
        mobile = request.form['mobile']
        school_name = request.form['school_name']
        photo = request.files['photo']
        school=School.query.filter_by(school_name=school_name).first()

        if not school:
            school = School(school_name=school_name)
            db.session.add(school)
            db.session.commit()

        filename = None
        if photo and photo.filename != '':
            filename = secure_filename(photo.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            photo.save(upload_path)

        new_student = Student(
            name=name,
            father_name=father_name,
            student_class=student_class,
            roll_no=roll_no,
            address=address,
            mobile=mobile,
            photo=filename,
            school_id=school.id
        )
        db.session.add(new_student)
        db.session.commit()
        flash("Student added successfully!")
        return redirect(url_for('main.add_student'))

    return render_template('add_student.html')

@main.route('/download-id-card/<int:student_id>')
def download_id_card(student_id):

    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

    student = Student.query.get_or_404(student_id)

    rendered = render_template("id_card.html", student=student)

    pdf = HTML(string=rendered,base_url=request.url_root).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=id_card_{student.id}.pdf'

    return response



# View Students
@main.route('/view-students')
def view_students():
    students = Student.query.all()
    print("Student from DB:",students)
    return render_template('view_students.html', students=students)

@main.route('/search', methods=['GET', 'POST'])
def search_student():
    if request.method == 'POST':
        name = request.form.get('name')
        students = Student.query.filter(Student.name.contains(name)).all()
        return render_template('view_students.html', students=students)
    return redirect(url_for('view_students'))

# Edit Student
@main.route('/edit-student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.name = request.form['name']
        
        # Pehle Class
        student.student_class = request.form['student_class']
        
        # Fir Roll No
        student.roll_no = request.form['roll_no']

        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '':
                from werkzeug.utils import secure_filename
                import os
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/uploads', filename))
                student.photo = filename

        db.session.commit()
        return redirect(url_for('main.view_students'))

    return render_template('edit_student.html', student=student)
# Delete Student
@main.route('/delete-student/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!")
    return redirect(url_for('main.view_students'))

# ID Card
@main.route('/id-card/<int:id>')
def id_card(id):
    student = Student.query.get(id)
    print("Student Date:",student)
    return render_template('id_card.html', student=student)