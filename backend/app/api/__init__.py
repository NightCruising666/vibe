from flask import Blueprint, Flask

from .auth import bp as auth_bp
from .home import bp as home_bp
from .profile import bp as profile_bp
from .admins import bp as admins_bp
from .students import bp as students_bp
from .classes import bp as classes_bp
from .courses import bp as courses_bp
from .scores import bp as scores_bp
from .tasks import bp as tasks_bp
from .materials import bp as materials_bp
from .feedback import bp as feedback_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(home_bp, url_prefix="/api/home")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(admins_bp, url_prefix="/api/admins")
    app.register_blueprint(students_bp, url_prefix="/api/students")
    app.register_blueprint(classes_bp, url_prefix="/api/classes")
    app.register_blueprint(courses_bp, url_prefix="/api/courses")
    app.register_blueprint(scores_bp, url_prefix="/api/scores")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(materials_bp, url_prefix="/api/materials")
    app.register_blueprint(feedback_bp, url_prefix="/api/feedback")
