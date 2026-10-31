"""Flask command to import recipes from TheMealDB into SQLite."""

import click
from flask.cli import with_appcontext

from .db import db
from .models import Recipe, RecipeIngredient
from .recipe_api import download_recipes


@click.command("seed-recipes")
@click.option("--count", default=40, type=click.IntRange(30, 50), show_default=True)
@with_appcontext
def seed_recipes_command(count):
    """Fetch, validate and store recipes. Requires network access."""
    try:
        recipes, rejected = download_recipes(target=count)
    except (OSError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    db.create_all()
    added = 0
    for entry in recipes:
        existing = db.session.execute(
            db.select(Recipe).filter_by(
                source=entry["source"], source_id=entry["source_id"]
            )
        ).scalar_one_or_none()
        if existing is not None:
            continue
        recipe = Recipe(
            name=entry["name"], source=entry["source"],
            source_id=entry["source_id"], source_url=entry["source_url"],
        )
        for ingredient in entry["ingredients"]:
            recipe.ingredients.append(RecipeIngredient(**ingredient))
        db.session.add(recipe)
        added += 1
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    click.echo(
        f"Validated {len(recipes)} recipes; rejected {rejected} incomplete records; "
        f"added {added} recipes."
    )
