from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import mongo
from app.helpers.response_helper import success_response
from app.middleware.error_handler import register_error_handlers
from app.routes.user_routes import user_bp


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)

    CORS(app)
    mongo.init_app(app)

    app.register_blueprint(user_bp, url_prefix="/api/v1/users")
    register_error_handlers(app)

    @app.get("/health")
    def health_check():
        return success_response("API is running", {"service": "flask-mongo-crud"})

    return app
