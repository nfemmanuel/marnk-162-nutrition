"""Find the recipes a user can cook from the ingredients they already have (NUT-34).

Matching compares names only, ignoring case and spaces at either end. A recipe
qualifies when it needs at most MAX_MISSING ingredients the user doesn't have.
"""

from .db import db
from .models import Recipe

MAX_MISSING = 2


def match_recipes(have):
    """Return the recipes the user can make from `have`, a list of ingredient names.

    Each result is a dictionary with the recipe and the names of the
    ingredients it still needs: {"recipe": Recipe, "missing": [names]}.
    Recipes missing the fewest ingredients come first; among those, the one
    that uses more of the user's ingredients comes first, then by name.
    """
    have = {name.strip().lower() for name in have if name.strip()}
    if not have:
        return []

    matches = []
    for recipe in db.session.execute(db.select(Recipe)).scalars():
        needed = {item.name.strip().lower() for item in recipe.ingredients}
        missing = sorted(needed - have)
        if len(missing) <= MAX_MISSING:
            used = len(needed & have)
            matches.append((len(missing), -used, recipe.name, recipe, missing))

    matches.sort(key=lambda match: match[:3])
    return [{"recipe": recipe, "missing": missing} for *_, recipe, missing in matches]
