from datetime import datetime

from flask import Blueprint, request

from ..extensions import db
from ..models import Student
from ..utils.responses import success, error
from ..utils.pagination import get_pagination_args, paginate_query

# Blueprint serving CRUD endpoints used by StudentList.vue
bp = Blueprint("students", __name__)


@bp.route("", methods=["GET"])
def list_students():
    # StudentList.vue load() 调用此接口获取表格数据
    page, size = get_pagination_args()
    query = Student.query.order_by(Student.id.desc())
    data = paginate_query(query, page, size)
    return success(data)


@bp.route("/<int:student_id>", methods=["GET"])
def get_student(student_id):
    # 预留给详情页或其它前端查询单个学生信息
    student = Student.query.get(student_id)
    if not student:
        return error("Student not found", 404)
    return success(student.to_dict())


@bp.route("", methods=["POST"])
def create_student():
    # StudentList.vue submit() 在新增模式下提交 POST /students
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return error("Student name is required", 400)
    birthday = None
    if data.get("birthday"):
        try:
            birthday = datetime.fromisoformat(data["birthday"]).date()
        except ValueError:
            return error("Invalid birthday format", 400)
    student = Student(
        name=name,
        gender=data.get("gender"),
        birthday=birthday,
        class_id=data.get("class_id"),
    )
    db.session.add(student)
    db.session.commit()
    return success(student.to_dict(), status_code=201)


@bp.route("/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    # StudentList.vue submit() 编辑现有学生时触发 PUT /students/<id>
    student = Student.query.get(student_id)
    if not student:
        return error("Student not found", 404)
    data = request.get_json() or {}
    student.name = data.get("name", student.name)
    student.gender = data.get("gender", student.gender)
    if data.get("birthday"):
        try:
            student.birthday = datetime.fromisoformat(data["birthday"]).date()
        except ValueError:
            return error("Invalid birthday format", 400)
    student.class_id = data.get("class_id", student.class_id)
    db.session.commit()
    return success(student.to_dict())


@bp.route("/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    # StudentList.vue remove() 使用 DELETE /students/<id> 删除记录
    student = Student.query.get(student_id)
    if not student:
        return error("Student not found", 404)
    db.session.delete(student)
    db.session.commit()
    return success({"deleted": student_id})
