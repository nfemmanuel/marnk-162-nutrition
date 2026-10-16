"""The database for the app.

`db` is created here, without an app, and connected to the app inside
create_app(). Models import `db` from this file, so there's only ever one.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
