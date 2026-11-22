"""Tests for the "what can I cook" page (NUT-29).

Each test uses an in-memory database and Flask's test client, so it goes
through the real route.
Run from the repo root:  python -m unittest discover -s app_flask/tests -t .
"""

import unittest

from app_flask.nutrition import create_app
from app_flask.nutrition.db import db
from app_flask.nutrition.models import Recipe, RecipeIngredient
from app_flask.nutrition.user_service import create_user


def add_recipe(name, ingredients):
    """Store a recipe with these ingredient names."""
    recipe = Recipe(name=name, source="test", source_id=name, source_url="")
    for ingredient in ingredients:
        recipe.ingredients.append(RecipeIngredient(name=ingredient, amount="1"))
    db.session.add(recipe)
    db.session.commit()


class CookPageTest(unittest.TestCase):
    """The /cook page with a small set of recipes."""

    def setUp(self):
        """Make a test app with an in-memory database and two recipes."""
        self.app = create_app(
            {"TESTING": True, "SECRET_KEY": "test", "SQLALCHEMY_DATABASE_URI": "sqlite://"}
        )
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        add_recipe("Omelette", ["Eggs", "Butter"])
        add_recipe("Pancakes", ["Eggs", "Milk", "Flour"])
        self.client = self.app.test_client()

    def tearDown(self):
        """Throw the test database away."""
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.context.pop()

    def search(self, text):
        """Submit the form with this text and return the page as text."""
        response = self.client.post("/cook", data={"ingredients": text})
        self.assertEqual(response.status_code, 200)
        return response.get_data(as_text=True)

    def test_get_shows_form(self):
        """The page loads with a form and no results."""
        response = self.client.get("/cook")
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("<form", page)
        self.assertIn('name="ingredients"', page)
        self.assertNotIn("Omelette", page)

    def test_results_best_first_with_missing(self):
        """Recipes come back with the fewest missing first, and name what is missing."""
        page = self.search("eggs, butter")
        self.assertIn("Omelette", page)
        self.assertIn("Pancakes", page)
        self.assertLess(page.index("Omelette"), page.index("Pancakes"))
        self.assertIn("milk", page)
        self.assertIn("flour", page)

    def test_newline_separated(self):
        """Ingredients can be separated by new lines."""
        page = self.search("eggs\nbutter")
        self.assertIn("Omelette", page)

    def test_empty_submission(self):
        """An empty submission asks for an ingredient and shows no results."""
        page = self.search("  , \n ")
        self.assertIn("Enter at least one ingredient", page)
        self.assertNotIn("Omelette", page)

    def test_no_matches(self):
        """Ingredients no recipe uses give a friendly message."""
        page = self.search("dragon fruit")
        self.assertIn("No recipes yet", page)

    def test_logged_out_can_search_without_save_button(self):
        """A visitor who is not logged in gets results but no Save button."""
        page = self.search("eggs")
        self.assertIn("Omelette", page)
        self.assertNotIn(">Save<", page)

    def test_logged_in_sees_save_button(self):
        """A logged-in user gets a Save button on each result."""
        create_user("ana@example.com", "secret123")
        self.client.post("/login", data={"email": "ana@example.com", "password": "secret123"})
        page = self.search("eggs, butter")
        self.assertEqual(page.count(">Save<"), 2)


if __name__ == "__main__":
    unittest.main()
