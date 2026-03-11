from . import db

# -------------------- SCHOOL MODEL --------------------
class School(db.Model):
    __tablename__ = "school"

    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(200), nullable=False)
    
    students = db.relationship("Student", backref="school", lazy=True)

    def __repr__(self):
        return f"<School {self.school_name}>"


# -------------------- STUDENT MODEL --------------------

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    father_name = db.Column(db.String(100))
    student_class = db.Column(db.String(50))
    roll_no = db.Column(db.String(20))
    address = db.Column(db.String(200))
    mobile = db.Column(db.String(15))
    photo = db.Column(db.String(200))

    school_id = db.Column(db.Integer, db.ForeignKey("school.id"), nullable=True)

    def __repr__(self):
        return f"<Student {self.name}>"