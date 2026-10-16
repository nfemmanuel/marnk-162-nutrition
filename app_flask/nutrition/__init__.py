from flask import Flask

from .db import db


def create_app(test_config=None):
    """Build and return a fresh copy of the app (one for the server, one per test)."""
    app = Flask(__name__)

    # The database is a SQLite file. A relative path like this one is saved in
    # the app's instance/ folder, which is kept out of git
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI="sqlite:///nutrition.sqlite")

    if test_config is not None:
        # Tests can pass their own config, e.g. {"TESTING": True}
        app.config.from_mapping(test_config)

    # Connect the database to this app
    db.init_app(app)

    # Temporary route so we can check the app starts (home page story replaces this)
    @app.route("/hello")
    def hello():
        return "Hello, Nutrition App!"

    return app