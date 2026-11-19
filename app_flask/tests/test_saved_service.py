"""Tests for storing saved recipes per user (NUT-38).

Each test gets a throwaway in-memory database with two users and two recipes.
Run from the repo root:  python -m unittest discover -s app_flask/tests -t .
"""

import unittest
from datetime import timedelta

from sqlalchemy.exc import IntegrityError

from app_flask.nutrition import create_app
from app_flask.nutrition.db import db
from app_flask.nutrition.models import Recipe, SavedRecipe
from app_flask.nutrition.saved_service import (
    list_saved_recipes,
    remove_saved_recipe,
    save_recipe,
    saved_recipe_ids,
)
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


class SavedServiceTest(SavedRecipeTestCase):
    """The functions in saved_service.py."""

    def names(self, user_id):
        """Return the names of a user's saved recipes, in order."""
        return [recipe.name for recipe in list_saved_recipes(user_id)]

    def test_save_then_list(self):
        """A saved recipe shows up in that user's list."""
        self.assertTrue(save_recipe(self.ana, self.omelette))

        self.assertEqual(self.names(self.ana), ["Omelette"])

    def test_newest_saved_comes_first(self):
        """The list is ordered by when each recipe was saved, newest first."""
        save_recipe(self.ana, self.omelette)
        save_recipe(self.ana, self.pancakes)
        # Make the gap between the two saves clear, whatever the clock did
        first = db.session.get(SavedRecipe, (self.ana, self.omelette))
        first.created_at = first.created_at - timedelta(minutes=1)
        db.session.commit()

        self.assertEqual(self.names(self.ana), ["Pancakes", "Omelette"])

    def test_saving_twice_keeps_one_row(self):
        """Saving a recipe again succeeds and doesn't add a second row."""
        save_recipe(self.ana, self.omelette)

        self.assertTrue(save_recipe(self.ana, self.omelette))
        self.assertEqual(self.names(self.ana), ["Omelette"])

    def test_saving_an_unknown_recipe_is_refused(self):
        """A recipe ID that isn't in the database isn't saved."""
        self.assertFalse(save_recipe(self.ana, 999))

        self.assertEqual(self.names(self.ana), [])

    def test_remove(self):
        """Removing takes the recipe off the list and says it was there."""
        save_recipe(self.ana, self.omelette)

        self.assertTrue(remove_saved_recipe(self.ana, self.omelette))
        self.assertEqual(self.names(self.ana), [])

    def test_removing_what_is_not_saved_changes_nothing(self):
        """Removing a recipe the user never saved returns False."""
        self.assertFalse(remove_saved_recipe(self.ana, self.omelette))

    def test_lists_are_separate_per_user(self):
        """One user never sees, or removes, another user's saved recipes."""
        save_recipe(self.ana, self.omelette)
        save_recipe(self.ben, self.pancakes)

        self.assertEqual(self.names(self.ana), ["Omelette"])
        self.assertEqual(self.names(self.ben), ["Pancakes"])
        self.assertFalse(remove_saved_recipe(self.ben, self.omelette))
        self.assertEqual(self.names(self.ana), ["Omelette"])

    def test_two_users_can_save_the_same_recipe(self):
        """The same recipe can be on two users' lists."""
        save_recipe(self.ana, self.omelette)
        save_recipe(self.ben, self.omelette)

        self.assertEqual(self.names(self.ben), ["Omelette"])

    def test_saved_recipe_ids(self):
        """saved_recipe_ids() gives only that user's recipe IDs."""
        save_recipe(self.ana, self.omelette)
        save_recipe(self.ben, self.pancakes)

        self.assertEqual(saved_recipe_ids(self.ana), {self.omelette})


if __name__ == "__main__":
    unittest.main()
