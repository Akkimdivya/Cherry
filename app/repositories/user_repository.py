from pymongo import ASCENDING, DESCENDING

from app.extensions import mongo
from app.helpers.mongo_helper import object_id, serialize_document


def _collection():
    return mongo.db.users


def create_user_indexes():
    _collection().create_index([("email", ASCENDING)], unique=True)


def build_user_filters(search=None):
    if not search:
        return {}

    return {
        "$or": [
            {"name": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
        ]
    }


def create_user(data):
    result = _collection().insert_one(data)
    return get_user_by_id(str(result.inserted_id))


def get_all_users(filters=None, skip=0, limit=20):
    cursor = (
        _collection()
        .find(filters or {})
        .sort("created_at", DESCENDING)
        .skip(skip)
        .limit(limit)
    )
    return [serialize_document(user) for user in cursor]


def count_users(filters=None):
    return _collection().count_documents(filters or {})


def get_user_by_id(user_id):
    user = _collection().find_one({"_id": object_id(user_id)})
    return serialize_document(user)


def get_user_by_email(email):
    user = _collection().find_one({"email": email})
    return serialize_document(user)


def update_user(user_id, data):
    _collection().update_one({"_id": object_id(user_id)}, {"$set": data})
    return get_user_by_id(user_id)


def delete_user(user_id):
    result = _collection().delete_one({"_id": object_id(user_id)})
    return result.deleted_count

