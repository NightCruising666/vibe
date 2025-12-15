from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Admin(db.Model, TimestampMixin):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ClassModel(db.Model, TimestampMixin):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    grade = db.Column(db.String(64))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "grade": self.grade,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Student(db.Model, TimestampMixin):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(16))
    birthday = db.Column(db.Date)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"))
    clazz = db.relationship("ClassModel", backref=db.backref("students", lazy=True))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birthday": self.birthday.isoformat() if self.birthday else None,
            "class_id": self.class_id,
            "class_name": self.clazz.name if self.clazz else None,
        }


class Course(db.Model, TimestampMixin):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    credit = db.Column(db.Integer)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "credit": self.credit,
        }


class Score(db.Model, TimestampMixin):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    score = db.Column(db.Float)

    student = db.relationship("Student", backref=db.backref("scores", lazy=True))
    course = db.relationship("Course", backref=db.backref("scores", lazy=True))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "score": self.score,
            "student_name": self.student.name if self.student else None,
            "course_name": self.course.name if self.course else None,
        }


class Task(db.Model, TimestampMixin):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
        }


class Material(db.Model, TimestampMixin):
    __tablename__ = "materials"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(256))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "file_path": self.file_path,
        }


class Feedback(db.Model, TimestampMixin):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(128))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "contact": self.contact,
        }


class UserProfile(db.Model, TimestampMixin):
    __tablename__ = "user_profiles"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"), unique=True)
    full_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))

    admin = db.relationship("Admin", backref=db.backref("profile", uselist=False))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
        }
