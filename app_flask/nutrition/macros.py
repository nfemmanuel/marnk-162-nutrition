"""Calories and macros for recipe ingredients, from USDA values per 100 g.

`flask --app nutrition seed-ingredients` loads data/foods.csv and
data/ingredients.csv into the database, and recipe_totals() adds up a recipe
from them. data/README.md says where the numbers come from and which
ingredients are skipped.
"""

import csv
import string
from pathlib import Path

import click

from .db import db
from .models import Food, Ingredient, RecipeIngredient

DATA_FOLDER = Path(__file__).resolve().parent / "data"

# Grams in one unit. Spoons and cups are weighed as water (1 ml = 1 g), which is
# close enough for a rough total.
GRAMS_PER_UNIT = {
    "g": 1, "gram": 1, "grams": 1, "kg": 1000,
    "ml": 1, "l": 1000,
    "oz": 28.35, "ounce": 28.35, "ounces": 28.35, "lb": 453.6, "lbs": 453.6,
    "tsp": 5, "teaspoon": 5, "teaspoons": 5,
    "tbs": 15, "tbls": 15, "tblsp": 15, "tbsp": 15, "tablespoon": 15, "tablespoons": 15,
    "cup": 240, "cups": 240,
}


def read_csv(filename):
    """Return the rows of a CSV file in data/ as a list of dictionaries."""
    with open(DATA_FOLDER / filename, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def load_macros(food_rows, ingredient_rows):
    """Replace the foods and ingredients tables with these rows.

    It all happens in one transaction, so a bad row leaves the tables as they were.
    """
    try:
        # Ingredients first: they point to foods
        db.session.execute(db.delete(Ingredient))
        db.session.execute(db.delete(Food))
        for row in food_rows:
            food = Food(
                fdc_id=int(row["fdc_id"]),
                description=row["description"],
                calories=float(row["calories"]),
                protein=float(row["protein"]),
                carbs=float(row["carbs"]),
                fat=float(row["fat"]),
            )
            db.session.add(food)
        for row in ingredient_rows:
            # Spices have an empty fdc_id: they have no food
            fdc_id = int(row["fdc_id"]) if row["fdc_id"] else None
            db.session.add(Ingredient(name=row["name"].lower(), fdc_id=fdc_id))
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise


def names_without_macros():
    """Return the recipe ingredient names that have no row in the ingredients table."""
    missing = set()
    for item in db.session.execute(db.select(RecipeIngredient)).scalars():
        if db.session.get(Ingredient, item.name.lower()) is None:
            missing.add(item.name.lower())
    return sorted(missing)


@click.command("seed-ingredients")
def seed_ingredients_command():
    """Load the USDA calories and macros in data/ into the database."""
    db.create_all()
    foods = read_csv("foods.csv")
    ingredients = read_csv("ingredients.csv")
    load_macros(foods, ingredients)
    click.echo(f"Loaded {len(foods)} USDA foods and {len(ingredients)} ingredient names.")

    missing = names_without_macros()
    if missing:
        click.echo("Recipe ingredients not in ingredients.csv yet: " + ", ".join(missing))


def read_number(text):
    """Read "2", "1.5" or "1/2" as a number. Raises ValueError for anything else."""
    if "/" in text:
        top, bottom = text.split("/")
        return float(top) / float(bottom)
    return float(text)


def to_grams(amount):
    """Turn an amount like "200g", "1 1/2 cups" or "2 tbs" into grams.

    Returns None for amounts we can't weigh, like "2 sliced", "1 large" or "To taste".
    """
    text = amount.lower().replace("½", " 1/2").replace("¼", " 1/4").replace("¾", " 3/4")
    number = 0
    for word in text.split():
        digits = word.rstrip(string.ascii_lowercase)  # "100g" -> "100"
        unit = word[len(digits):]  # "100g" -> "g"
        if digits:
            try:
                number += read_number(digits)
            except (ValueError, ZeroDivisionError):  # a range like "1-2", or "1/0"
                return None
        if unit:
            if number == 0 or unit not in GRAMS_PER_UNIT:
                return None
            return number * GRAMS_PER_UNIT[unit]
    return None


def recipe_totals(recipe):
    """Add up the calories, protein, carbs and fat of a recipe's ingredients.

    Spices are skipped. Returns the totals and a list of the ingredients left
    out: names with no macros yet, and amounts we can't weigh, like "2 sliced".
    """
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    left_out = []
    for item in recipe.ingredients:
        ingredient = db.session.get(Ingredient, item.name.lower())
        if ingredient is not None and ingredient.fdc_id is None:
            continue  # a spice
        grams = to_grams(item.amount)
        if ingredient is None or grams is None:
            left_out.append(item.name)
            continue
        food = db.session.get(Food, ingredient.fdc_id)
        share = grams / 100  # USDA values are per 100 g
        totals["calories"] += food.calories * share
        totals["protein"] += food.protein * share
        totals["carbs"] += food.carbs * share
        totals["fat"] += food.fat * share
    return totals, left_out
