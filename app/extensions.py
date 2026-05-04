from contextlib import contextmanager
from urllib.parse import urlparse, urlunparse

import psycopg2
from flask import current_app
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


def ensure_database_exists(database_url):
    parsed_url = urlparse(database_url)
    database_name = parsed_url.path.lstrip("/")

    if not database_name:
        raise ValueError("DATABASE_URL must include a database name")

    maintenance_url = urlunparse(parsed_url._replace(path="/postgres"))

    connection = psycopg2.connect(maintenance_url)
    connection.autocommit = True

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (database_name,),
            )

            if cursor.fetchone():
                return

            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name))
            )
    finally:
        connection.close()


def get_db_connection():
    return psycopg2.connect(
        current_app.config["DATABASE_URL"],
        cursor_factory=RealDictCursor,
    )


@contextmanager
def get_db_cursor():
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                yield cursor
    finally:
        connection.close()
