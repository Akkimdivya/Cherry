from datetime import datetime

from bson import ObjectId
from bson.errors import InvalidId


def is_valid_object_id(value):
    try:
        ObjectId(value)
        return True
    except (InvalidId, TypeError):
        return False


def object_id(value):
    return ObjectId(value)


def serialize_value(value):
    if isinstance(value, ObjectId):
        return str(value)

    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, list):
        return [serialize_value(item) for item in value]

    if isinstance(value, dict):
        return {key: serialize_value(item) for key, item in value.items()}

    return value


def serialize_document(document):
    if not document:
        return None

    serialized = serialize_value(dict(document))
    serialized["id"] = serialized.pop("_id")
    return serialized

