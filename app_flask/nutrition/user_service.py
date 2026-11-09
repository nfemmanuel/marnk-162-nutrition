"""User validation and persistence operations used by authentication routes.

Keeping these operations here prevents the HTTP layer from depending directly
on SQLAlchemy queries and password-storage details.
"""

import re

from .db import db
from .models import User


# This practical application check requires ``name@domain.suffix`` without spaces.
BASIC_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_email(email):
    """Return one canonical form for case-insensitive registration and lookup."""
    return email.strip().lower()


def is_valid_email(email):
    """Return whether an email has the basic shape accepted by this app."""
    return BASIC_EMAIL_PATTERN.fullmatch(normalize_email(email)) is not None


def get_user_by_email(email):
    """Return the user with the normalized email, or ``None`` if none exists."""
    return db.session.execute(
        db.select(User).filter_by(email=normalize_email(email))
    ).scalar_one_or_none()


def get_user_by_id(user_id):
    """Return the user represented by a Flask-Login session ID, if valid."""
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None


def create_user(email, password):
    """Normalize the email, hash the password, and persist a new user."""
    new_user = User(email=normalize_email(email))
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return new_user
