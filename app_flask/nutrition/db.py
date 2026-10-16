"""The database for the app.

`db` is created here, without an app, and connected to the app inside
create_app(). Models import `db` from this file, so there's only ever one.
"""

import click
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@click.command("init-db")
def init_db_command():
    """Create any missing tables. Run once on a fresh clone: flask --app nutrition init-db"""
    # create_all() only adds tables that don't exist yet, so existing data is kept
    db.create_all()
    click.echo("Created the database tables.")
