from datetime import datetime, timezone

from flask import current_app

from app.helpers.sql_helper import parse_user_id
from app.repositories import user_repository
from app.schemas.user_schema import (
    clean_user_payload,
    validate_create_user,
    validate_update_user,
)


def _utc_now():
    return datetime.now(timezone.utc)


def _parse_positive_int(value, default, max_value=None):
    if value is None:
        return default, None

    try:
        number = int(value)
    except (TypeError, ValueError):
        return None, "Must be a positive integer"

    if number < 1:
        return None, "Must be greater than or equal to 1"

    if max_value and number > max_value:
        return None, f"Must be less than or equal to {max_value}"

    return number, None


def create_user(data):
    errors = validate_create_user(data)
    if errors:
        return None, "Validation failed", 400, errors, None

    payload = clean_user_payload(data)
    existing_user = user_repository.get_user_by_email(payload["email"])
    if existing_user:
        return None, "Email already exists", 409, None, None

    now = _utc_now()
    payload["created_at"] = now
    payload["updated_at"] = now

    user = user_repository.create_user(payload)
    return user, "User created successfully", 201, None, None


def get_all_users(query_args):
    default_limit = current_app.config["USERS_DEFAULT_PAGE_SIZE"]
    max_limit = current_app.config["USERS_MAX_PAGE_SIZE"]

    page, page_error = _parse_positive_int(query_args.get("page"), 1)
    limit, limit_error = _parse_positive_int(query_args.get("limit"), default_limit, max_limit)

    errors = {}
    if page_error:
        errors["page"] = page_error
    if limit_error:
        errors["limit"] = limit_error
    if errors:
        return None, "Validation failed", 400, errors, None

    search = (query_args.get("search") or "").strip()
    skip = (page - 1) * limit

    users = user_repository.get_all_users(search, skip=skip, limit=limit)
    total = user_repository.count_users(search)
    meta = {
        "page": page,
        "limit": limit,
        "total": total,
        "pages": (total + limit - 1) // limit,
    }

    return users, "Users fetched successfully", 200, None, meta


def get_user_by_id(user_id):
    user_id = parse_user_id(user_id)
    if user_id is None:
        return None, "Invalid user id", 400, None, None

    user = user_repository.get_user_by_id(user_id)
    if not user:
        return None, "User not found", 404, None, None

    return user, "User fetched successfully", 200, None, None


def update_user(user_id, data):
    user_id = parse_user_id(user_id)
    if user_id is None:
        return None, "Invalid user id", 400, None, None

    errors = validate_update_user(data)
    if errors:
        return None, "Validation failed", 400, errors, None

    existing_user = user_repository.get_user_by_id(user_id)
    if not existing_user:
        return None, "User not found", 404, None, None

    payload = clean_user_payload(data)
    if "email" in payload:
        user_with_email = user_repository.get_user_by_email(payload["email"])
        if user_with_email and user_with_email["id"] != user_id:
            return None, "Email already exists", 409, None, None

    payload["updated_at"] = _utc_now()
    user = user_repository.update_user(user_id, payload)
    return user, "User updated successfully", 200, None, None


def delete_user(user_id):
    user_id = parse_user_id(user_id)
    if user_id is None:
        return None, "Invalid user id", 400, None, None

    existing_user = user_repository.get_user_by_id(user_id)
    if not existing_user:
        return None, "User not found", 404, None, None

    user_repository.delete_user(user_id)
    return None, "User deleted successfully", 200, None, None
