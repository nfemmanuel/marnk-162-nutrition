"""Tests for matching recipes to the user's ingredients (NUT-34, NUT-36).

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
        add_recipe("Chicken Curry", ["Chicken Breast", "Eggplant", "Curry Paste", "Coconut Milk"])
        add_recipe("Stuffed Peppers", ["Red Pepper", "Rice", "Salt", "Olive Oil", "Water"])

    def tearDown(self):
        """Throw the test database away."""
        db.session.remove()
        db.drop_all()
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

    def test_ignores_case_and_spaces(self):
        """'  eggs ' matches 'Eggs'."""
        results = match_recipes(["  eggs ", "BUTTER"])

        self.assertEqual(results[0]["missing"], [])

    def test_no_ingredients_gives_no_recipes(self):
        """An empty list, or only blank names, returns nothing."""
        self.assertEqual(match_recipes([]), [])
        self.assertEqual(match_recipes(["  "]), [])

    def test_staples_are_never_missing(self):
        """Salt, oil and water count as owned without being typed."""
        results = match_recipes(["Red Pepper", "Rice"])

        self.assertEqual(results[0]["recipe"].name, "Stuffed Peppers")
        self.assertEqual(results[0]["missing"], [])

    def test_staples_are_exact_names(self):
        """The staple "pepper" doesn't cover "red pepper"."""
        results = match_recipes(["Rice"])

        self.assertEqual(results[0]["missing"], ["red pepper"])

    def test_recipe_using_nothing_i_have_is_left_out(self):
        """A recipe that is only staples plus things I don't have isn't returned."""
        self.assertNotIn("Stuffed Peppers", self.names(match_recipes(["Eggs"])))

    def test_partial_name_matches_whole_words(self):
        """"chicken" covers "Chicken Breast", and "curry paste" still matches itself."""
        results = match_recipes(["chicken", "curry paste"])

        self.assertEqual(results[0]["recipe"].name, "Chicken Curry")
        self.assertEqual(results[0]["missing"], ["coconut milk", "eggplant"])

    def test_partial_name_needs_a_whole_word(self):
        """"egg" doesn't cover "Eggplant"."""
        results = match_recipes(["chicken", "curry paste", "coconut milk", "egg"])

        self.assertEqual(results[0]["recipe"].name, "Chicken Curry")
        self.assertEqual(results[0]["missing"], ["eggplant"])

    def test_longer_name_does_not_cover_a_shorter_one(self):
        """Having "egg yolks" doesn't count as having "Eggs"."""
        self.assertEqual(match_recipes(["egg yolks"]), [])


if __name__ == "__main__":
    unittest.main()
