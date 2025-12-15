from flask import Blueprint, request

from ..extensions import db
from ..models import ClassModel
from ..utils.responses import success, error
from ..utils.pagination import get_pagination_args, paginate_query

bp = Blueprint("classes", __name__)


@bp.route("", methods=["GET"])
def list_classes():
    page, size = get_pagination_args()
    query = ClassModel.query.order_by(ClassModel.id.desc())
    data = paginate_query(query, page, size)
    return success(data)


@bp.route("/<int:class_id>", methods=["GET"])
def get_class(class_id):
    clazz = ClassModel.query.get(class_id)
    if not clazz:
        return error("Class not found", 404)
    return success(clazz.to_dict())


@bp.route("", methods=["POST"])
def create_class():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return error("Class name is required", 400)
    clazz = ClassModel(name=name, grade=data.get("grade"))
    db.session.add(clazz)
    db.session.commit()
    return success(clazz.to_dict(), status_code=201)


@bp.route("/<int:class_id>", methods=["PUT"])
def update_class(class_id):
    clazz = ClassModel.query.get(class_id)
    if not clazz:
        return error("Class not found", 404)
    data = request.get_json() or {}
    clazz.name = data.get("name", clazz.name)
    clazz.grade = data.get("grade", clazz.grade)
    db.session.commit()
    return success(clazz.to_dict())


@bp.route("/<int:class_id>", methods=["DELETE"])
def delete_class(class_id):
    clazz = ClassModel.query.get(class_id)
    if not clazz:
        return error("Class not found", 404)
    db.session.delete(clazz)
    db.session.commit()
    return success({"deleted": class_id})
