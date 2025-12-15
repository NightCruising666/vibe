from flask import Blueprint, request

from ..extensions import db
from ..models import Admin
from ..utils.responses import success, error

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return error("Username and password required", 400)

    admin = Admin.query.filter_by(username=username).first()
    if not admin or not admin.check_password(password):
        return error("Invalid credentials", 401)

    # Simple token placeholder; in production replace with JWT/session
    token = f"token-{admin.id}"
    return success({"token": token, "admin": admin.to_dict()})


@bp.route("/logout", methods=["POST"])
def logout():
    return success({"message": "logged out"})
