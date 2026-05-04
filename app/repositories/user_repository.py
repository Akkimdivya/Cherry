from app.extensions import get_db_cursor
from app.helpers.sql_helper import serialize_row

USER_COLUMNS = "id, name, email, age, created_at, updated_at"


def init_db():
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                age INTEGER,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )


def create_user(data):
    with get_db_cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO users (name, email, age, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING {USER_COLUMNS}
            """,
            (
                data["name"],
                data["email"],
                data.get("age"),
                data["created_at"],
                data["updated_at"],
            ),
        )
        return serialize_row(cursor.fetchone())


def get_all_users(search=None, skip=0, limit=20):
    where_clause, params = _search_clause(search)
    params.extend([limit, skip])

    with get_db_cursor() as cursor:
        cursor.execute(
            f"""
            SELECT {USER_COLUMNS}
            FROM users
            {where_clause}
            ORDER BY created_at DESC, id DESC
            LIMIT %s OFFSET %s
            """,
            params,
        )
        return [serialize_row(row) for row in cursor.fetchall()]


def count_users(search=None):
    where_clause, params = _search_clause(search)

    with get_db_cursor() as cursor:
        cursor.execute(
            f"""
            SELECT COUNT(*) AS total
            FROM users
            {where_clause}
            """,
            params,
        )
        return cursor.fetchone()["total"]


def get_user_by_id(user_id):
    with get_db_cursor() as cursor:
        cursor.execute(
            f"SELECT {USER_COLUMNS} FROM users WHERE id = %s",
            (user_id,),
        )
        return serialize_row(cursor.fetchone())


def get_user_by_email(email):
    with get_db_cursor() as cursor:
        cursor.execute(
            f"SELECT {USER_COLUMNS} FROM users WHERE email = %s",
            (email,),
        )
        return serialize_row(cursor.fetchone())


def update_user(user_id, data):
    allowed_fields = ["name", "email", "age", "updated_at"]
    fields = [field for field in allowed_fields if field in data]
    set_clause = ", ".join(f"{field} = %s" for field in fields)
    values = [data[field] for field in fields]
    values.append(user_id)

    with get_db_cursor() as cursor:
        cursor.execute(
            f"""
            UPDATE users
            SET {set_clause}
            WHERE id = %s
            RETURNING {USER_COLUMNS}
            """,
            values,
        )
        return serialize_row(cursor.fetchone())


def delete_user(user_id):
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        return cursor.rowcount


def _search_clause(search):
    if not search:
        return "", []

    search_value = f"%{search}%"
    return "WHERE name ILIKE %s OR email ILIKE %s", [search_value, search_value]
