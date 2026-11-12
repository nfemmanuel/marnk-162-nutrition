"""Tests for the saved recipes pages (NUT-39).

Each test uses an in-memory database and Flask's test client, so it goes
through the real routes. Ana is logged in; Ben is a second user.
Run from the repo root:  python -m unittest discover -s app_flask/tests -t .
"""

import unittest

from app_flask.nutrition import create_app
from app_flask.nutrition.db import db
from app_flask.nutrition.models import Recipe, RecipeIngredient
from app_flask.nutrition.saved_service import list_saved_recipes, save_recipe
from app_flask.nutrition.user_service import create_user


def add_recipe(name, ingredient):
    """Store a recipe with this name and one ingredient, and return its ID."""
    recipe = Recipe(name=name, source="test", source_id=name, source_url="")
    recipe.ingredients.append(RecipeIngredient(name=ingredient, amount="2"))
    db.session.add(recipe)
    db.session.commit()
    return recipe.id


class SavedPagesTestCase(unittest.TestCase):
    """Shared setup: two users, two recipes, and Ana logged in."""

    def setUp(self):
        """Make a test app with an in-memory database and log Ana in."""
        self.app = create_app(
            {"TESTING": True, "SECRET_KEY": "test", "SQLALCHEMY_DATABASE_URI": "sqlite://"}
        )
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        self.ana = create_user("ana@example.com", "secret123").id
        self.ben = create_user("ben@example.com", "secret123").id
        self.omelette = add_recipe("Omelette", "Eggs")
        self.pancakes = add_recipe("Pancakes", "Flour")
        self.client = self.app.test_client()
        self.client.post("/login", data={"email": "ana@example.com", "password": "secret123"})

    def tearDown(self):
        """Throw the test database away."""
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.context.pop()

    def saved_names(self, user_id):
        """Return the names of the recipes a user has saved."""
        return [recipe.name for recipe in list_saved_recipes(user_id)]


class SavedListTest(SavedPagesTestCase):
    """The /saved page and its Remove button."""

    def test_page_lists_my_saved_recipes(self):
        """The page shows what I saved, with each recipe's ingredients."""
        save_recipe(self.ana, self.omelette)

        page = self.client.get("/saved")

        self.assertEqual(page.status_code, 200)
        self.assertIn(b"Omelette", page.data)
        self.assertIn(b"2 Eggs", page.data)
        self.assertNotIn(b"Pancakes", page.data)

    def test_page_does_not_show_another_users_recipes(self):
        """What Ben saved never appears on Ana's page."""
        save_recipe(self.ben, self.pancakes)

        page = self.client.get("/saved")

        self.assertNotIn(b"Pancakes", page.data)

    def test_empty_list_says_so(self):
        """With nothing saved, the page explains that."""
        page = self.client.get("/saved")

        self.assertIn(b"No saved recipes yet.", page.data)

    def test_page_needs_login(self):
        """A logged-out visitor is sent to the login page."""
        self.client.post("/logout")

        response = self.client.get("/saved")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/login?next=%2Fsaved")

    def test_remove(self):
        """Remove takes the recipe off my list and returns to the page."""
        save_recipe(self.ana, self.omelette)

        response = self.client.post(f"/saved/{self.omelette}/remove")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/saved")
        self.assertEqual(self.saved_names(self.ana), [])

    def test_remove_does_not_touch_another_users_list(self):
        """Ana removing a recipe leaves Ben's saved copy alone."""
        save_recipe(self.ben, self.omelette)

        self.client.post(f"/saved/{self.omelette}/remove")

        self.assertEqual(self.saved_names(self.ben), ["Omelette"])

    def test_remove_is_post_only(self):
        """Opening the remove address as a link changes nothing."""
        save_recipe(self.ana, self.omelette)

        response = self.client.get(f"/saved/{self.omelette}/remove")

        self.assertEqual(response.status_code, 405)
        self.assertEqual(self.saved_names(self.ana), ["Omelette"])

    def test_navigation_links_to_the_page_when_logged_in(self):
        """The Saved recipes link shows only for a logged-in user."""
        self.assertIn(b'href="/saved"', self.client.get("/account").data)

        self.client.post("/logout")

        self.assertNotIn(b'href="/saved"', self.client.get("/login").data)


if __name__ == "__main__":
    unittest.main()
