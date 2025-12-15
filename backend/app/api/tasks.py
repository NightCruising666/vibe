from datetime import datetime

from flask import Blueprint, request

from ..extensions import db
from ..models import Task
from ..utils.responses import success, error
from ..utils.pagination import get_pagination_args, paginate_query

bp = Blueprint("tasks", __name__)


@bp.route("", methods=["GET"])
def list_tasks():
    page, size = get_pagination_args()
    query = Task.query.order_by(Task.id.desc())
    data = paginate_query(query, page, size)
    return success(data)


@bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return error("Task not found", 404)
    return success(task.to_dict())


@bp.route("", methods=["POST"])
def create_task():
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        return error("Task title is required", 400)
    due_date = None
    if data.get("due_date"):
        try:
            due_date = datetime.fromisoformat(data["due_date"]).date()
        except ValueError:
            return error("Invalid due_date format", 400)
    task = Task(title=title, description=data.get("description"), due_date=due_date)
    db.session.add(task)
    db.session.commit()
    return success(task.to_dict(), status_code=201)


@bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return error("Task not found", 404)
    data = request.get_json() or {}
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    if data.get("due_date"):
        try:
            task.due_date = datetime.fromisoformat(data["due_date"]).date()
        except ValueError:
            return error("Invalid due_date format", 400)
    db.session.commit()
    return success(task.to_dict())


@bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return error("Task not found", 404)
    db.session.delete(task)
    db.session.commit()
    return success({"deleted": task_id})
