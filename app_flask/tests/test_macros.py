"""Tests for the ingredient macros (NUT-28): loading them, reading amounts and
adding up recipes.

The database tests load the real CSV files into a throwaway in-memory database.
Run from the repo root:  python -m unittest discover -s app_flask/tests -t .
"""

import unittest

from app_flask.nutrition import create_app
from app_flask.nutrition.db import db
from app_flask.nutrition.macros import load_macros, read_csv, recipe_totals, to_grams
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


class ToGramsTest(unittest.TestCase):
    """to_grams() reads the amounts TheMealDB recipes use."""

    def test_weights(self):
        """Grams, kilos, ounces and pounds, with or without a space."""
        self.assertEqual(to_grams("200g"), 200)
        self.assertEqual(to_grams("250 g"), 250)
        self.assertEqual(to_grams("1.5kg"), 1500)
        self.assertEqual(to_grams("450 grams Boneless skin"), 450)
        self.assertAlmostEqual(to_grams("8 ounces"), 226.8)
        self.assertAlmostEqual(to_grams("2 Lbs"), 907.2)

    def test_volumes_count_as_water(self):
        """Spoons, cups and litres are weighed as water: 1 ml = 1 g."""
        self.assertEqual(to_grams("2 tbs"), 30)
        self.assertEqual(to_grams("1/2 tsp"), 2.5)
        self.assertEqual(to_grams("1 1/2 cups"), 360)
        self.assertEqual(to_grams("½ tbsp"), 7.5)
        self.assertEqual(to_grams("1 L"), 1000)

    def test_amounts_we_cannot_weigh(self):
        """Pieces, ranges and words give None."""
        for amount in ["2 sliced", "1 large", "4", "To taste", "Pinch", "1-2tbsp", "1 Can"]:
            self.assertIsNone(to_grams(amount), amount)


class RecipeTotalsTest(unittest.TestCase):
    """recipe_totals() with the real USDA data loaded."""

    def setUp(self):
        """Make a test app with an in-memory database holding the USDA data."""
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        load_macros(read_csv("foods.csv"), read_csv("ingredients.csv"))

    def tearDown(self):
        """Throw the test database away."""
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def add_recipe(self, ingredients):
        """Save a recipe with these (name, amount) pairs and return it."""
        recipe = Recipe(name="Test recipe", source="test", source_id="1", source_url="-")
        for name, amount in ingredients:
            recipe.ingredients.append(RecipeIngredient(name=name, amount=amount))
        db.session.add(recipe)
        db.session.commit()
        return recipe

    def test_mediterranean_pasta_salad(self):
        """A starter dataset recipe, as TheMealDB lists it, matches a total done by hand."""
        recipe = self.add_recipe([
            ("mozzarella balls", "200 g"),
            ("baby plum tomatoes", "250 g"),
            ("fresh basil", "1  bunch"),
            ("farfalle", "350 g"),
            ("extra virgin olive oil", "3  tablespoons"),
            ("Green Olives", "40 g"),
            ("tuna", "200 g"),
            ("salt", "to taste"),
            ("pepper", "to taste"),
        ])

        totals, left_out = recipe_totals(recipe)

        # grams / 100 x USDA values per 100 g (calories, protein, carbs, fat):
        #   mozzarella  200 g x (299, 22.17,  2.4,  22.14)
        #   tomatoes    250 g x ( 18,  0.88,  3.89,  0.2)
        #   farfalle    350 g x (371, 13.04, 74.67,  1.51)
        #   olive oil    45 g x (884,  0,     0,   100)     3 tablespoons
        #   olives       40 g x (145,  1.03,  3.84, 15.32)
        #   tuna        200 g x (116, 25.51,  0,     0.82)
        self.assertAlmostEqual(totals["calories"], 2629.3)
        self.assertAlmostEqual(totals["protein"], 143.612)
        self.assertAlmostEqual(totals["carbs"], 277.406)
        self.assertAlmostEqual(totals["fat"], 102.833)
        # Basil, salt and pepper are spices, so they are skipped, not left out
        self.assertEqual(left_out, [])

    def test_left_out_ingredients_are_listed(self):
        """Pieces and unknown names are listed, and spices are skipped quietly."""
        recipe = self.add_recipe([
            ("Rice", "100g"),
            ("Onion", "1 sliced"),
            ("Dragon Fruit", "100g"),
            ("Salt", "1 tsp"),
        ])

        totals, left_out = recipe_totals(recipe)

        self.assertEqual(totals["calories"], 365)  # only the rice counts
        self.assertEqual(left_out, ["Onion", "Dragon Fruit"])


if __name__ == "__main__":
    unittest.main()
