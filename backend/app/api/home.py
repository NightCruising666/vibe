from flask import Blueprint

from ..utils.responses import success

bp = Blueprint("home", __name__)


@bp.route("/info", methods=["GET"])
def info():
    return success({"copyright": "Student Management System"})
