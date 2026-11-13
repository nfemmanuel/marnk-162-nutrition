"""Tests for matching recipes to the user's ingredients (NUT-34).

Run from the repo root:  python -m unittest discover -s app_flask/tests -t .
"""

import unittest

from app_flask.nutrition import create_app
from app_flask.nutrition.db import db
from app_flask.nutrition.matching import match_recipes
from app_flask.nutrition.models import Recipe, RecipeIngredient


def add_recipe(name, ingredients):
    """Store a recipe with these ingredient names."""
    recipe = Recipe(name=name, source="test", source_id=name, source_url="")
    for ingredient in ingredients:
        recipe.ingredients.append(RecipeIngredient(name=ingredient, amount="1"))
    db.session.add(recipe)
    db.session.commit()


class MatchRecipesTest(unittest.TestCase):
    """match_recipes() against a small set of recipes."""

    def setUp(self):
        """Make a test app with an in-memory database and three recipes."""
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        add_recipe("Omelette", ["Eggs", "Butter"])
        add_recipe("Pancakes", ["Eggs", "Milk", "Flour"])
        add_recipe("Lasagne", ["Pasta", "Beef", "Tomato", "Cheese"])

    def tearDown(self):
        """Throw the test database away."""
        db.session.remove()
        db.drop_all()
        db.engine.dispose()  # Closes the SQLite connection the pool keeps open
        self.context.pop()

    def names(self, results):
        """Return the recipe names in the results, in order."""
        return [result["recipe"].name for result in results]

    def test_exact_match_has_nothing_missing(self):
        """A recipe the user has everything for comes back with an empty missing list."""
        results = match_recipes(["Eggs", "Butter"])

        self.assertEqual(results[0]["recipe"].name, "Omelette")
        self.assertEqual(results[0]["missing"], [])

    def test_names_what_is_missing(self):
        """A recipe one or two ingredients short lists those ingredients."""
        results = match_recipes(["Eggs"])

        missing = {r["recipe"].name: r["missing"] for r in results}
        self.assertEqual(missing["Omelette"], ["butter"])
        self.assertEqual(missing["Pancakes"], ["flour", "milk"])

    def test_three_or_more_missing_is_left_out(self):
        """A recipe needing three or more extra ingredients isn't returned."""
        self.assertNotIn("Lasagne", self.names(match_recipes(["Pasta"])))

    def test_fewest_missing_comes_first(self):
        """Recipes are ordered by how many ingredients they still need."""
        self.assertEqual(
            self.names(match_recipes(["Eggs", "Butter", "Milk"])), ["Omelette", "Pancakes"]
        )

    def test_tie_goes_to_the_recipe_using_more_of_what_i_have(self):
        """With the same number missing, the recipe using more of my ingredients comes first."""
        self.assertEqual(self.names(match_recipes(["Eggs", "Milk"])), ["Pancakes", "Omelette"])

    def test_full_tie_goes_in_alphabetical_order(self):
        """Same number missing and used: alphabetical, whatever order they were stored in."""
        add_recipe("Zucchini Toast", ["Bread", "Zucchini"])
        add_recipe("Apple Toast", ["Bread", "Apple"])

        results = self.names(match_recipes(["Bread"]))

        self.assertEqual(results[:2], ["Apple Toast", "Zucchini Toast"])

    def test_ignores_case_and_spaces(self):
        """'  eggs ' matches 'Eggs'."""
        results = match_recipes(["  eggs ", "BUTTER"])

        self.assertEqual(results[0]["missing"], [])

    def test_no_ingredients_gives_no_recipes(self):
        """An empty list, or only blank names, returns nothing."""
        self.assertEqual(match_recipes([]), [])
        self.assertEqual(match_recipes(["  "]), [])


if __name__ == "__main__":
    unittest.main()
