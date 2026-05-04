from flask import Blueprint

from app.controllers import user_controller

user_bp = Blueprint("users", __name__)


@user_bp.post("")
def create_user():
    return user_controller.create_user()


@user_bp.get("")
def get_all_users():
    return user_controller.get_all_users()


@user_bp.get("/<user_id>")
def get_user_by_id(user_id):
    return user_controller.get_user_by_id(user_id)


@user_bp.put("/<user_id>")
def update_user(user_id):
    return user_controller.update_user(user_id)


@user_bp.delete("/<user_id>")
def delete_user(user_id):
    return user_controller.delete_user(user_id)

