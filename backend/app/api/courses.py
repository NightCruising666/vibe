from flask import Blueprint, request

from ..extensions import db
from ..models import Course
from ..utils.responses import success, error
from ..utils.pagination import get_pagination_args, paginate_query

bp = Blueprint("courses", __name__)


@bp.route("", methods=["GET"])
def list_courses():
    page, size = get_pagination_args()
    query = Course.query.order_by(Course.id.desc())
    data = paginate_query(query, page, size)
    return success(data)


@bp.route("/<int:course_id>", methods=["GET"])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return error("Course not found", 404)
    return success(course.to_dict())


@bp.route("", methods=["POST"])
def create_course():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return error("Course name is required", 400)
    course = Course(name=name, description=data.get("description"), credit=data.get("credit"))
    db.session.add(course)
    db.session.commit()
    return success(course.to_dict(), status_code=201)


@bp.route("/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return error("Course not found", 404)
    data = request.get_json() or {}
    course.name = data.get("name", course.name)
    course.description = data.get("description", course.description)
    course.credit = data.get("credit", course.credit)
    db.session.commit()
    return success(course.to_dict())


@bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return error("Course not found", 404)
    db.session.delete(course)
    db.session.commit()
    return success({"deleted": course_id})
