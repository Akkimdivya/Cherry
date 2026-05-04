import re

ALLOWED_USER_FIELDS = {"name", "email", "age"}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _unknown_field_errors(data):
    unknown_fields = sorted(set(data) - ALLOWED_USER_FIELDS)
    if not unknown_fields:
        return None
    return f"Unknown fields are not allowed: {', '.join(unknown_fields)}"


def clean_user_payload(data):
    payload = {}

    if "name" in data:
        payload["name"] = data["name"].strip()

    if "email" in data:
        payload["email"] = data["email"].strip().lower()

    if "age" in data:
        payload["age"] = data["age"]

    return payload


def validate_create_user(data):
    if not isinstance(data, dict):
        return {"body": "JSON body must be an object"}

    errors = {}
    unknown_error = _unknown_field_errors(data)
    if unknown_error:
        errors["fields"] = unknown_error

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        errors["name"] = "Name is required"

    email = data.get("email")
    if not isinstance(email, str) or not email.strip():
        errors["email"] = "Email is required"
    elif not EMAIL_PATTERN.match(email.strip()):
        errors["email"] = "Email must be valid"

    if "age" in data:
        age = data["age"]
        if not isinstance(age, int) or isinstance(age, bool):
            errors["age"] = "Age must be an integer"
        elif age < 0:
            errors["age"] = "Age must be greater than or equal to 0"

    return errors


def validate_update_user(data):
    if not isinstance(data, dict):
        return {"body": "JSON body must be an object"}

    errors = {}
    if not data:
        errors["body"] = "At least one field is required"

    unknown_error = _unknown_field_errors(data)
    if unknown_error:
        errors["fields"] = unknown_error

    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            errors["name"] = "Name cannot be empty"

    if "email" in data:
        email = data["email"]
        if not isinstance(email, str) or not email.strip():
            errors["email"] = "Email cannot be empty"
        elif not EMAIL_PATTERN.match(email.strip()):
            errors["email"] = "Email must be valid"

    if "age" in data:
        age = data["age"]
        if not isinstance(age, int) or isinstance(age, bool):
            errors["age"] = "Age must be an integer"
        elif age < 0:
            errors["age"] = "Age must be greater than or equal to 0"

    return errors

