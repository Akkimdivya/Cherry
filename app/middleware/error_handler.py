from flask import current_app
from psycopg2 import DatabaseError, IntegrityError
from werkzeug.exceptions import BadRequest, HTTPException, MethodNotAllowed, NotFound

from app.helpers.response_helper import error_response


def register_error_handlers(app):
    @app.errorhandler(BadRequest)
    def bad_request(error):
        return error_response("Bad request", 400)

    @app.errorhandler(NotFound)
    def not_found(error):
        return error_response("Route not found", 404)

    @app.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return error_response("Method not allowed", 405)

    @app.errorhandler(IntegrityError)
    def integrity_error(error):
        return error_response("Duplicate value already exists", 409)

    @app.errorhandler(DatabaseError)
    def database_error(error):
        current_app.logger.exception("PostgreSQL error")
        return error_response("Database error", 500)

    @app.errorhandler(HTTPException)
    def http_error(error):
        return error_response(error.description, error.code)

    @app.errorhandler(Exception)
    def internal_error(error):
        current_app.logger.exception("Unhandled server error")
        return error_response("Internal server error", 500)
