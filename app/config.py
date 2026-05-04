import os

from dotenv import load_dotenv

load_dotenv()


def _int_env(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/flask_mongo_crud")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "flask_mongo_crud")
    JSON_SORT_KEYS = False
    USERS_DEFAULT_PAGE_SIZE = _int_env("USERS_DEFAULT_PAGE_SIZE", 20)
    USERS_MAX_PAGE_SIZE = _int_env("USERS_MAX_PAGE_SIZE", 100)
