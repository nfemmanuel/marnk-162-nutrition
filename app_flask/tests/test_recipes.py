"""Offline recipe API-validation, CLI and database tests."""

import unittest
from unittest.mock import patch

from app_flask.nutrition import create_app
from app_flask.nutrition.db import db
from app_flask.nutrition.models import Recipe, RecipeIngredient
from app_flask.nutrition.recipe_api import download_recipes, validate_meal


def sample_meal(number, name=None):
    return {
        "idMeal": str(number), "strMeal": name or f"Recipe {number}",
        "strIngredient1": "Rice", "strMeasure1": "1 cup",
        "strIngredient2": "Water", "strMeasure2": "2 cups",
    }


class APIValidationTest(unittest.TestCase):
    def test_valid_record(self):
        record = validate_meal(sample_meal(52795, "Chicken Handi"))
        self.assertEqual(record["source_id"], "52795")
        self.assertEqual(record["ingredients"][0]["amount"], "1 cup")
        self.assertEqual(record["source"], "TheMealDB")
        self.assertIn("lookup.php?i=52795", record["source_url"])

    def test_missing_amount_is_rejected(self):
        item = sample_meal(1)
        item["strMeasure2"] = ""
        self.assertIsNone(validate_meal(item))

    def test_orphan_amount_is_rejected(self):
        item = sample_meal(1)
        item["strMeasure3"] = "2 tsp"
        self.assertIsNone(validate_meal(item))

    def test_duplicates_and_invalid_records_excluded(self):
        def fake_fetch(term):
            if term == "chicken":
                return [sample_meal(i) for i in range(1, 31)] + [
                    sample_meal(1), {"idMeal": "bad"}
                ]
            return [sample_meal(i) for i in range(31, 41)]

        records, rejected = download_recipes(40, fake_fetch)
        self.assertEqual(len(records), 40)
        self.assertEqual(rejected, 1)
        self.assertEqual(len({r["source_id"] for r in records}), 40)

    def test_insufficient_records_is_error(self):
        with self.assertRaises(ValueError):
            download_recipes(40, lambda term: [])


class RecipeSeedTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_import_and_repeat_are_idempotent(self):
        entries = [validate_meal(sample_meal(i)) for i in range(1, 41)]
        with patch("app_flask.nutrition.seed.download_recipes", return_value=(entries, 2)):
            runner = self.app.test_cli_runner()
            first = runner.invoke(args=["seed-recipes"])
            second = runner.invoke(args=["seed-recipes"])
        self.assertEqual(first.exit_code, 0, first.output)
        self.assertIn("added 40", first.output)
        self.assertEqual(second.exit_code, 0, second.output)
        self.assertIn("added 0", second.output)
        self.assertEqual(db.session.query(Recipe).count(), 40)
        self.assertEqual(db.session.query(RecipeIngredient).count(), 80)

    def test_download_failure_does_not_change_tables(self):
        with patch("app_flask.nutrition.seed.download_recipes", side_effect=ValueError("offline")):
            result = self.app.test_cli_runner().invoke(args=["seed-recipes"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertEqual(db.session.query(Recipe).count(), 0)


class CommandContextTest(unittest.TestCase):
    def test_seed_cli_runs_without_manual_app_context(self):
        app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
        records = [validate_meal(sample_meal(i)) for i in range(1, 31)]
        with patch("app_flask.nutrition.seed.download_recipes", return_value=(records, 0)):
            result = app.test_cli_runner().invoke(args=["seed-recipes", "--count", "30"])
        self.assertEqual(result.exit_code, 0, result.output)
        with app.app_context():
            self.assertEqual(db.session.query(Recipe).count(), 30)
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
