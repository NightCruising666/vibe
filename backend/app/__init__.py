from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import db, migrate
from .api import register_blueprints
from .utils.responses import register_error_handlers
from flask import send_from_directory, current_app


def create_app(config_object: str | type[Config] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object or Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register routes and error handlers
    register_blueprints(app)
    register_error_handlers(app)

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

    return app
