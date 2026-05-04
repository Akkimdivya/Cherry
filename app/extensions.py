from contextlib import contextmanager

import psycopg2
from flask import current_app
from psycopg2.extras import RealDictCursor


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
