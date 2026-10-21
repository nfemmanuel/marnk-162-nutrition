"""Behavior tests for the complete browser-facing authentication flow.

Each test uses an in-memory SQLite database and Flask's test client, so it
exercises the real routes without touching the development database.
"""

import unittest

from app_flask.nutrition import create_app
from app_flask.nutrition.db import db
from app_flask.nutrition.models import User
from app_flask.nutrition.user_service import create_user


class AuthTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test",
                "SQLALCHEMY_DATABASE_URI": "sqlite://",
            }
        )
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        registration_response = self.client.post(
            "/register",
            data={"email": "  ANA@EXAMPLE.COM ", "password": "secret123"},
            follow_redirects=True,
        )

        saved_user = db.session.execute(
            db.select(User).filter_by(email="ana@example.com")
        ).scalar_one()
        self.assertEqual(registration_response.status_code, 200)
        self.assertIn(
            b"Account created. Please log in.", registration_response.data
        )
        self.assertNotEqual(saved_user.password_hash, "secret123")

    def test_register_rejects_invalid_email(self):
        registration_response = self.client.post(
            "/register",
            data={"email": "123@1", "password": "secret123"},
            follow_redirects=True,
        )

        self.assertEqual(registration_response.status_code, 200)
        self.assertIn(
            b"Enter a valid email address.", registration_response.data
        )
        self.assertIsNone(db.session.execute(db.select(User)).scalar_one_or_none())

    def test_register_rejects_existing_email_regardless_of_case(self):
        create_user("ana@example.com", "original-password")

        registration_response = self.client.post(
            "/register",
            data={"email": "  ANA@EXAMPLE.COM ", "password": "new-password"},
            follow_redirects=True,
        )

        saved_users = db.session.execute(db.select(User)).scalars().all()
        self.assertEqual(registration_response.status_code, 200)
        self.assertIn(
            b"An account with that email already exists.",
            registration_response.data,
        )
        self.assertEqual(len(saved_users), 1)
        self.assertTrue(saved_users[0].check_password("original-password"))

    def test_login_with_correct_password(self):
        create_user("ana@example.com", "secret123")

        login_response = self.client.post(
            "/login",
            data={"email": "ANA@EXAMPLE.COM", "password": "secret123"},
            follow_redirects=True,
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertIn(
            b"You are logged in as ana@example.com.", login_response.data
        )

    def test_login_with_incorrect_password(self):
        create_user("ana@example.com", "secret123")

        login_response = self.client.post(
            "/login",
            data={"email": "ana@example.com", "password": "wrong"},
            follow_redirects=True,
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertIn(b"Incorrect email or password.", login_response.data)
        self.assertEqual(self.client.get("/account").status_code, 302)

    def test_logout(self):
        create_user("ana@example.com", "secret123")
        self.client.post(
            "/login",
            data={"email": "ana@example.com", "password": "secret123"},
        )

        logout_response = self.client.post("/logout", follow_redirects=True)

        self.assertEqual(logout_response.status_code, 200)
        self.assertIn(b"You have been logged out.", logout_response.data)
        self.assertEqual(self.client.get("/account").status_code, 302)


if __name__ == "__main__":
    unittest.main()
