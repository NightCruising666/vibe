from flask import Blueprint, request

from ..extensions import db
from ..models import Admin
from ..utils.responses import success, error
from ..utils.pagination import get_pagination_args, paginate_query

bp = Blueprint("admins", __name__)


@bp.route("", methods=["GET"])
def list_admins():
    page, size = get_pagination_args()
    query = Admin.query.order_by(Admin.id.desc())
    data = paginate_query(query, page, size)
    return success(data)


@bp.route("/<int:admin_id>", methods=["GET"])
def get_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return error("Admin not found", 404)
    return success(admin.to_dict())


@bp.route("", methods=["POST"])
def create_admin():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return error("Username and password are required", 400)
    if Admin.query.filter_by(username=username).first():
        return error("Username already exists", 400)

    admin = Admin(
        username=username,
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone"),
    )
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    return success(admin.to_dict(), status_code=201)


@bp.route("/<int:admin_id>", methods=["PUT"])
def update_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return error("Admin not found", 404)
    data = request.get_json() or {}
    admin.name = data.get("name", admin.name)
    admin.email = data.get("email", admin.email)
    admin.phone = data.get("phone", admin.phone)
    if data.get("password"):
        admin.set_password(data["password"])
    db.session.commit()
    return success(admin.to_dict())


@bp.route("/<int:admin_id>", methods=["DELETE"])
def delete_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return error("Admin not found", 404)
    db.session.delete(admin)
    db.session.commit()
    return success({"deleted": admin_id})
