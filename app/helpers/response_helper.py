from flask import jsonify


def success_response(message, data=None, status_code=200, meta=None):
    response = {
        "success": True,
        "message": message,
        "data": data,
    }

    if meta is not None:
        response["meta"] = meta

    return jsonify(response), status_code


def error_response(message, status_code=400, errors=None):
    response = {
        "success": False,
        "message": message,
    }

    if errors is not None:
        response["errors"] = errors

    return jsonify(response), status_code

