from flask import Blueprint, request

from ..extensions import db
from ..models import Feedback
from ..utils.responses import success, error
from ..utils.pagination import get_pagination_args, paginate_query

bp = Blueprint("feedback", __name__)


@bp.route("", methods=["GET"])
def list_feedback():
    page, size = get_pagination_args()
    query = Feedback.query.order_by(Feedback.id.desc())
    data = paginate_query(query, page, size)
    return success(data)


@bp.route("/<int:feedback_id>", methods=["GET"])
def get_feedback(feedback_id):
    record = Feedback.query.get(feedback_id)
    if not record:
        return error("Feedback not found", 404)
    return success(record.to_dict())


@bp.route("", methods=["POST"])
def create_feedback():
    data = request.get_json() or {}
    content = data.get("content")
    if not content:
        return error("Content is required", 400)
    record = Feedback(content=content, contact=data.get("contact"))
    db.session.add(record)
    db.session.commit()
    return success(record.to_dict(), status_code=201)


@bp.route("/<int:feedback_id>", methods=["PUT"])
def update_feedback(feedback_id):
    record = Feedback.query.get(feedback_id)
    if not record:
        return error("Feedback not found", 404)
    data = request.get_json() or {}
    record.content = data.get("content", record.content)
    record.contact = data.get("contact", record.contact)
    db.session.commit()
    return success(record.to_dict())


@bp.route("/<int:feedback_id>", methods=["DELETE"])
def delete_feedback(feedback_id):
    record = Feedback.query.get(feedback_id)
    if not record:
        return error("Feedback not found", 404)
    db.session.delete(record)
    db.session.commit()
    return success({"deleted": feedback_id})
