from flask import Flask

from .home import home_bp


def create_app(test_config=None):
    # Build and return a fresh app (new copy for the server and every test)
    app = Flask(__name__)

    # Empty config for now (the tutorial sets defaults here)
    app.config.from_mapping()

    if test_config is not None:
        # Tests can pass their own config, e.g. {"TESTING": True}
        app.config.from_mapping(test_config)

    app.register_blueprint(home_bp)

    return app