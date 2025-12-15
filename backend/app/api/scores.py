from flask import Blueprint, request

from ..extensions import db
from ..models import Score
from ..utils.responses import success, error
from ..utils.pagination import get_pagination_args, paginate_query

bp = Blueprint("scores", __name__)


@bp.route("", methods=["GET"])
def list_scores():
    page, size = get_pagination_args()
    query = Score.query.order_by(Score.id.desc())
    data = paginate_query(query, page, size)
    return success(data)


@bp.route("/<int:score_id>", methods=["GET"])
def get_score(score_id):
    score = Score.query.get(score_id)
    if not score:
        return error("Score not found", 404)
    return success(score.to_dict())


@bp.route("", methods=["POST"])
def create_score():
    data = request.get_json() or {}
    student_id = data.get("student_id")
    course_id = data.get("course_id")
    if not student_id or not course_id:
        return error("student_id and course_id are required", 400)
    score = Score(student_id=student_id, course_id=course_id, score=data.get("score"))
    db.session.add(score)
    db.session.commit()
    return success(score.to_dict(), status_code=201)


@bp.route("/<int:score_id>", methods=["PUT"])
def update_score(score_id):
    score_obj = Score.query.get(score_id)
    if not score_obj:
        return error("Score not found", 404)
    data = request.get_json() or {}
    score_obj.student_id = data.get("student_id", score_obj.student_id)
    score_obj.course_id = data.get("course_id", score_obj.course_id)
    score_obj.score = data.get("score", score_obj.score)
    db.session.commit()
    return success(score_obj.to_dict())


@bp.route("/<int:score_id>", methods=["DELETE"])
def delete_score(score_id):
    score_obj = Score.query.get(score_id)
    if not score_obj:
        return error("Score not found", 404)
    db.session.delete(score_obj)
    db.session.commit()
    return success({"deleted": score_id})
