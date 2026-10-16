"""Tests for the database and the User model.

Each test gets a throwaway in-memory database, so nothing touches the real file.
Run from the repo root:  python -m unittest discover -s app_flask/tests -t .
"""

import unittest

from sqlalchemy.exc import IntegrityError

from app_flask.nutrition import create_app
from app_flask.nutrition.db import db
from app_flask.nutrition.models import User


class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_user_is_saved_and_read_back(self):
        user = User(email="ana@example.com")
        user.set_password("secret123")
        db.session.add(user)
        db.session.commit()

        saved = db.session.execute(
            db.select(User).filter_by(email="ana@example.com")
        ).scalar_one()
        self.assertIsNotNone(saved.id)
        self.assertIsNotNone(saved.created_at)

        self.assertNotEqual(saved.password_hash, "secret123")
        self.assertTrue(saved.check_password("secret123"))
        self.assertFalse(saved.check_password("wrong"))

    def test_email_must_be_unique(self):
        db.session.add(User(email="ana@example.com", password_hash="x"))
        db.session.add(User(email="ana@example.com", password_hash="y"))
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_init_db_command_creates_the_tables(self):
        # Start with no tables, like a fresh clone
        db.drop_all()

        result = self.app.test_cli_runner().invoke(args=["init-db"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("Created the database tables", result.output)
        self.assertTrue(db.inspect(db.engine).has_table("users"))


if __name__ == "__main__":
    unittest.main()
