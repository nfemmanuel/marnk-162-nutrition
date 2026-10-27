"""Calories and macros for recipe ingredients, from USDA values per 100 g.

`flask --app nutrition seed-ingredients` loads data/foods.csv and
data/ingredients.csv into the database. data/README.md says where the numbers
come from and which ingredients are skipped.
"""

import csv
from pathlib import Path

import click

from .db import db
from .models import Food, Ingredient, RecipeIngredient

DATA_FOLDER = Path(__file__).resolve().parent / "data"


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
