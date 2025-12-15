import os
import uuid
from pathlib import Path

from flask import Blueprint, request, current_app

from ..extensions import db
from ..models import Material
from ..utils.responses import success, error
from ..utils.pagination import get_pagination_args, paginate_query

bp = Blueprint("materials", __name__)


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


@bp.route("", methods=["GET"])
def list_materials():
    page, size = get_pagination_args()
    query = Material.query.order_by(Material.id.desc())
    data = paginate_query(query, page, size)
    return success(data)


@bp.route("/<int:material_id>", methods=["GET"])
def get_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return error("Material not found", 404)
    return success(material.to_dict())


@bp.route("", methods=["POST"])
def create_material():
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        return error("Title is required", 400)
    material = Material(title=title, description=data.get("description"), file_path=data.get("file_path"))
    db.session.add(material)
    db.session.commit()
    return success(material.to_dict(), status_code=201)


@bp.route("/<int:material_id>", methods=["PUT"])
def update_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return error("Material not found", 404)
    data = request.get_json() or {}
    material.title = data.get("title", material.title)
    material.description = data.get("description", material.description)
    material.file_path = data.get("file_path", material.file_path)
    db.session.commit()
    return success(material.to_dict())


@bp.route("/<int:material_id>", methods=["DELETE"])
def delete_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return error("Material not found", 404)
    db.session.delete(material)
    db.session.commit()
    return success({"deleted": material_id})


@bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return error("No file part", 400)
    file = request.files["file"]
    if file.filename == "":
        return error("No selected file", 400)
    if not allowed_file(file.filename):
        return error("File type not allowed", 400)

    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = upload_folder / filename
    file.save(save_path)

    file_url = f"/uploads/{filename}"
    return success({"file_path": file_url}, status_code=201)
