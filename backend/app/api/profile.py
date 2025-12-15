from flask import Blueprint, request

from ..extensions import db
from ..models import UserProfile, Admin
from ..utils.responses import success, error

bp = Blueprint("profile", __name__)


@bp.route("", methods=["GET"])
def get_profile():
    admin_id = request.args.get("admin_id", type=int, default=1)
    profile = UserProfile.query.filter_by(admin_id=admin_id).first()
    if not profile:
        profile = UserProfile(admin_id=admin_id, full_name="", email="", phone="")
        db.session.add(profile)
        db.session.commit()
    return success(profile.to_dict())


@bp.route("", methods=["PUT"])
def update_profile():
    admin_id = request.args.get("admin_id", type=int, default=1)
    data = request.get_json() or {}
    profile = UserProfile.query.filter_by(admin_id=admin_id).first()
    if not profile:
        return error("Profile not found", 404)
    profile.full_name = data.get("full_name", profile.full_name)
    profile.email = data.get("email", profile.email)
    profile.phone = data.get("phone", profile.phone)
    db.session.commit()
    return success(profile.to_dict())
