"""Tests for storing saved recipes per user (NUT-38).

Each test gets a throwaway in-memory database with two users and two recipes.
Run from the repo root:  python -m unittest discover -s app_flask/tests -t .
"""

import unittest

from sqlalchemy.exc import IntegrityError

from app_flask.nutrition import create_app
from app_flask.nutrition.db import db
from app_flask.nutrition.models import Recipe, SavedRecipe
from app_flask.nutrition.user_service import create_user


def add_recipe(name):
    """Store a recipe with this name and return its ID."""
    recipe = Recipe(name=name, source="test", source_id=name, source_url="")
    db.session.add(recipe)
    db.session.commit()
    return recipe.id


class SavedRecipeTestCase(unittest.TestCase):
    """Shared setup: a test app, and the IDs of two users and two recipes."""

    def setUp(self):
        """Make a test app with an in-memory database."""
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        self.ana = create_user("ana@example.com", "secret123").id
        self.ben = create_user("ben@example.com", "secret123").id
        self.omelette = add_recipe("Omelette")
        self.pancakes = add_recipe("Pancakes")

    def tearDown(self):
        """Throw the test database away."""
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.context.pop()


class SavedRecipeModelTest(SavedRecipeTestCase):
    """The saved_recipes table."""

    def test_row_is_saved_with_a_time(self):
        """A saved recipe is stored and gets its created_at filled in."""
        db.session.add(SavedRecipe(user_id=self.ana, recipe_id=self.omelette))
        db.session.commit()

        row = db.session.get(SavedRecipe, (self.ana, self.omelette))
        self.assertIsNotNone(row.created_at)

    def test_same_user_and_recipe_twice_is_refused(self):
        """The primary key stops a second row for the same user and recipe."""
        db.session.add(SavedRecipe(user_id=self.ana, recipe_id=self.omelette))
        db.session.commit()
        # Forget the first object, so the second one reaches the database
        db.session.expunge_all()

        db.session.add(SavedRecipe(user_id=self.ana, recipe_id=self.omelette))
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_init_db_command_creates_the_table(self):
        """`flask init-db` on an empty database creates saved_recipes."""
        db.drop_all()

        result = self.app.test_cli_runner().invoke(args=["init-db"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertTrue(db.inspect(db.engine).has_table("saved_recipes"))


if __name__ == "__main__":
    unittest.main()
