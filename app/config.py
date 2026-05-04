import os

from dotenv import load_dotenv

load_dotenv()


def _bool_env(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


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
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/flask_pg_crud",
    )
    AUTO_INIT_DB = _bool_env("AUTO_INIT_DB", True)
    JSON_SORT_KEYS = False
    USERS_DEFAULT_PAGE_SIZE = _int_env("USERS_DEFAULT_PAGE_SIZE", 20)
    USERS_MAX_PAGE_SIZE = _int_env("USERS_MAX_PAGE_SIZE", 100)
