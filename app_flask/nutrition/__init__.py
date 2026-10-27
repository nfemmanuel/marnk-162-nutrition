"""Build and configure independent Nutrition App instances.

The application factory connects extensions and blueprints in one place. The
server receives one app instance, while each test can create an isolated one.
"""

import os

from flask import Flask

from .auth import auth_blueprint, login_manager
from .db import db, init_db_command
from . import models  # noqa: F401  (loads the tables so the database knows about them)


def create_app(test_config=None):
    """Create an application, optionally overriding configuration for tests."""
    app = Flask(__name__)

    # A relative SQLite path is saved in the app's instance/ folder, which git ignores
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI="sqlite:///nutrition.sqlite",
    )

    if test_config is not None:
        # Tests can pass their own config, e.g. {"TESTING": True}
        app.config.from_mapping(test_config)

    db.init_app(app)
    app.cli.add_command(init_db_command)

    login_manager.init_app(app)
    # ``login_required`` redirects unauthenticated requests to this endpoint.
    login_manager.login_view = "auth.login"
    app.register_blueprint(auth_blueprint)

    # Temporary route so we can check the app starts (home page story replaces this)
    @app.route("/hello")
    def hello():
        return "Hello, Nutrition App!"

    return app
