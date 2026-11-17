"""Save, remove and list the recipes a user wants to keep (NUT-38).

The routes call these functions, so the HTTP layer never builds queries itself.
Every function takes the user's ID, and every query filters by it, so one
user's saved recipes are never read or changed for another.
"""

from sqlalchemy.exc import IntegrityError

from .db import db
from .models import Recipe, SavedRecipe


def save_recipe(user_id, recipe_id):
    """Save a recipe for a user. Return False when the recipe doesn't exist.

    Saving a recipe that is already saved changes nothing and returns True.
    """
    if db.session.get(Recipe, recipe_id) is None:
        return False
    if db.session.get(SavedRecipe, (user_id, recipe_id)) is not None:
        return True

    db.session.add(SavedRecipe(user_id=user_id, recipe_id=recipe_id))
    try:
        db.session.commit()
    except IntegrityError:
        # Two requests saved it at the same moment; the other one's row is enough
        db.session.rollback()
    return True


def remove_saved_recipe(user_id, recipe_id):
    """Remove a recipe from a user's saved list. Return whether it was there."""
    saved = db.session.get(SavedRecipe, (user_id, recipe_id))
    if saved is None:
        return False
    db.session.delete(saved)
    db.session.commit()
    return True


def list_saved_recipes(user_id):
    """Return the recipes a user saved, the most recently saved first."""
    query = (
        db.select(Recipe)
        .join(SavedRecipe, SavedRecipe.recipe_id == Recipe.id)
        .where(SavedRecipe.user_id == user_id)
        .order_by(SavedRecipe.created_at.desc(), Recipe.name)
    )
    return db.session.execute(query).scalars().all()


def saved_recipe_ids(user_id):
    """Return the IDs of the recipes a user saved, as a set."""
    query = db.select(SavedRecipe.recipe_id).where(SavedRecipe.user_id == user_id)
    return set(db.session.execute(query).scalars())
