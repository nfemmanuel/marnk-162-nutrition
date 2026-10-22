"""The database for the app.

`db` is created here without an app and connected to it in create_app(), so
models can import it without importing the app. `flask --app nutrition init-db`
creates any missing tables and keeps existing data.
"""

import click
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@click.command("init-db")
def init_db_command():
    """Create any missing tables."""
    db.create_all()
    click.echo("Created the database tables.")
