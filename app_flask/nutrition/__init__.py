"""The nutrition app. create_app() builds a fresh app: one for the server, one per test."""

from flask import Flask

from .db import db, init_db_command
from . import models  # noqa: F401  (loads the tables so the database knows about them)


def create_app(test_config=None):
    app = Flask(__name__)

    # A relative SQLite path is saved in the app's instance/ folder, which git ignores
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI="sqlite:///nutrition.sqlite")

    if test_config is not None:
        # Tests can pass their own config, e.g. {"TESTING": True}
        app.config.from_mapping(test_config)

    db.init_app(app)
    app.cli.add_command(init_db_command)

    # Temporary route so we can check the app starts (home page story replaces this)
    @app.route("/hello")
    def hello():
        return "Hello, Nutrition App!"

    return app