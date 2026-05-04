from flask import request

from app.helpers.response_helper import error_response, success_response
from app.services import user_service


def _get_json_body():
    if not request.data:
        return {}, None

    data = request.get_json(silent=True)
    if data is None:
        return None, error_response(
            "Invalid JSON body",
            400,
            {"body": "Request body must be valid JSON"},
        )

    return data, None


def _send_service_result(result):
    data, message, status_code, errors, meta = result

    if status_code >= 400:
        return error_response(message, status_code, errors)

    return success_response(message, data, status_code, meta)


def create_user():
    data, error = _get_json_body()
    if error:
        return error

    return _send_service_result(user_service.create_user(data))


def get_all_users():
    return _send_service_result(user_service.get_all_users(request.args))


def get_user_by_id(user_id):
    return _send_service_result(user_service.get_user_by_id(user_id))


def update_user(user_id):
    data, error = _get_json_body()
    if error:
        return error

    return _send_service_result(user_service.update_user(user_id, data))


def delete_user(user_id):
    return _send_service_result(user_service.delete_user(user_id))
