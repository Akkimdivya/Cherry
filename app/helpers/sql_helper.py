from datetime import date, datetime
from decimal import Decimal


def parse_user_id(value):
    try:
        user_id = int(value)
    except (TypeError, ValueError):
        return None

    if user_id < 1:
        return None

    return user_id


def serialize_value(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()

    if isinstance(value, Decimal):
        return float(value)

    return value


def serialize_row(row):
    if row is None:
        return None

    return {key: serialize_value(value) for key, value in dict(row).items()}
