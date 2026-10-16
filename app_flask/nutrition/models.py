"""Database tables for the app, written as SQLAlchemy models."""

from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from .db import db


class User(db.Model):
    """Someone with an account. Their meals and plans will point back to this."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    # Used to log in, so no two users can share one
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Never the real password, only a salted hash of it
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def set_password(self, password):
        """Hash the password and store the hash (werkzeug adds a random salt)."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Return True if the password matches the stored hash."""
        return check_password_hash(self.password_hash, password)
