"""Tests for the ingredient macros (NUT-28).

Each test loads the real CSV files into a throwaway in-memory database.
Run from the repo root:  python -m unittest discover -s app_flask/tests -t .
"""

import unittest

from app_flask.nutrition import create_app
from app_flask.nutrition.db import db
from app_flask.nutrition.macros import load_macros, read_csv
from app_flask.nutrition.models import Food, Ingredient, Recipe, RecipeIngredient


class SeedIngredientsTest(unittest.TestCase):
    """The seed-ingredients command and the data it loads."""

    def setUp(self):
        """Make a test app with an in-memory database and run seed-ingredients."""
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
        self.context = self.app.app_context()
        self.context.push()
        self.runner = self.app.test_cli_runner()
        self.result = self.runner.invoke(args=["seed-ingredients"])

    def tearDown(self):
        """Throw the test database away."""
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_loads_every_row_of_both_files(self):
        """Every row of foods.csv and ingredients.csv ends up in the database."""
        self.assertEqual(self.result.exit_code, 0, self.result.output)
        self.assertEqual(db.session.query(Food).count(), len(read_csv("foods.csv")))
        self.assertEqual(
            db.session.query(Ingredient).count(), len(read_csv("ingredients.csv"))
        )

    def test_running_it_again_keeps_one_copy(self):
        """A second run replaces the rows instead of adding them twice."""
        foods = db.session.query(Food).count()

        result = self.runner.invoke(args=["seed-ingredients"])

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(db.session.query(Food).count(), foods)

    def test_every_food_an_ingredient_points_to_exists(self):
        """SQLite doesn't check foreign keys by default, so the test does."""
        for ingredient in db.session.query(Ingredient):
            if ingredient.fdc_id is not None:
                food = db.session.get(Food, ingredient.fdc_id)
                self.assertIsNotNone(food, ingredient.name)

    def test_spices_have_no_food_and_staples_do(self):
        """Salt is skipped, and rice has USDA's values for raw white rice."""
        self.assertIsNone(db.session.get(Ingredient, "salt").fdc_id)

        rice = db.session.get(Food, db.session.get(Ingredient, "rice").fdc_id)
        self.assertEqual(rice.calories, 365)
        self.assertEqual(rice.protein, 7.13)

    def test_a_bad_row_changes_nothing(self):
        """The delete and the inserts are one transaction, so a bad number undoes both."""
        foods = db.session.query(Food).count()
        bad_food = {
            "fdc_id": "1", "description": "Bad row", "calories": "lots",
            "protein": "0", "carbs": "0", "fat": "0",
        }

        with self.assertRaises(ValueError):
            load_macros([bad_food], [])

        self.assertEqual(db.session.query(Food).count(), foods)

    def test_reports_recipe_ingredients_without_an_entry(self):
        """Names in the recipes that ingredients.csv doesn't cover are listed."""
        recipe = Recipe(name="Fruit salad", source="test", source_id="1", source_url="-")
        recipe.ingredients.append(RecipeIngredient(name="Dragon Fruit", amount="1"))
        recipe.ingredients.append(RecipeIngredient(name="Lime", amount="1"))
        db.session.add(recipe)
        db.session.commit()

        result = self.runner.invoke(args=["seed-ingredients"])

        self.assertIn("not in ingredients.csv yet: dragon fruit", result.output)


if __name__ == "__main__":
    unittest.main()
