"""Bee Cycles repair-request API application factory.

Coursework prototype. The organisation's actual systems are not accessed.
"""

from pathlib import Path
import os

from flask import Flask, jsonify

from .db import initialise_database
from .routes import api


def create_app(test_config=None):
    """Create a Flask application with a configurable SQLite database."""
    app = Flask(__name__)
    default_database = Path(__file__).resolve().parent.parent / "data" / "repairs.db"

    app.config.from_mapping(
        DATABASE_PATH=os.getenv("DATABASE_PATH", str(default_database)),
        STAFF_API_KEY=os.getenv("STAFF_API_KEY", ""),
        MAX_CONTENT_LENGTH=64 * 1024,
        JSON_SORT_KEYS=False,
    )
    if test_config:
        app.config.update(test_config)

    initialise_database(app.config["DATABASE_PATH"])
    app.register_blueprint(api)

    @app.errorhandler(413)
    def payload_too_large(_error):
        return jsonify({"error": "Request body exceeds the 64 KB limit"}), 413

    @app.after_request
    def prevent_caching_personal_data(response):
        if response.mimetype == "application/json" and response.status_code != 404:
            response.headers["Cache-Control"] = "no-store"
        return response

    return app
