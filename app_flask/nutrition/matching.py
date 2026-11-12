"""Find the recipes a user can cook from the ingredients they already have (NUT-34).

Matching compares names, ignoring case and spaces at either end. A name the
user types also covers a longer recipe name that contains all of its words, so
"chicken" covers "chicken breast", and two names for the same USDA food cover
each other, so "egg" covers "eggs" (NUT-36). A recipe
qualifies when it uses at least one of the user's ingredients and needs at most
MAX_MISSING more. Staples are never counted as missing (NUT-36).
"""

from .db import db
from .models import Ingredient, Recipe

MAX_MISSING = 2

# Things almost every kitchen has, so nobody should have to type them. These are
# exact names on purpose: "pepper" must not cover "red pepper", and "water" must
# not cover "water chestnut".
STAPLES = {
    "salt",
    "sea salt",
    "kosher salt",
    "pepper",
    "black pepper",
    "water",
    "warm water",
    "oil",
    "vegetable oil",
    "olive oil",
    "extra virgin olive oil",
    "sugar",
}


def clean(name):
    """Return a name in lowercase, without spaces at either end."""
    return name.strip().lower()


def food_ids():
    """Return a dictionary from ingredient name to its USDA food ID.

    Names without a food (spices) are left out, so two spices never look alike.
    """
    rows = db.session.execute(db.select(Ingredient)).scalars()
    return {row.name: row.fdc_id for row in rows if row.fdc_id is not None}


def covers(mine, needed, foods):
    """Return whether an ingredient the user has counts as one a recipe needs.

    Both names are already clean, and `foods` comes from food_ids(). They match
    when they are equal, when every word the user typed is a word of the
    recipe's name ("egg" covers "egg yolks" but not "eggplant"), or when both
    names point to the same USDA food ("onion" and "red onions").
    """
    if set(mine.split()) <= set(needed.split()):
        return True
    return mine in foods and foods[mine] == foods.get(needed)


def match_recipes(have):
    """Return the recipes the user can make from `have`, a list of ingredient names.

    Each result is a dictionary with the recipe and the names of the
    ingredients it still needs: {"recipe": Recipe, "missing": [names]}.
    Recipes missing the fewest ingredients come first; among those, the one
    that uses more of the user's ingredients comes first, then by name.
    """
    have = {clean(name) for name in have if name.strip()}
    if not have:
        return []

    foods = food_ids()
    matches = []
    for recipe in db.session.execute(db.select(Recipe)).scalars():
        needed = {clean(item.name) for item in recipe.ingredients}
        missing = []
        used = 0
        for name in sorted(needed):
            if any(covers(mine, name, foods) for mine in have):
                used += 1
            elif name not in STAPLES:
                missing.append(name)
        # Without `used`, a recipe of staples plus two other things would match anyone
        if used and len(missing) <= MAX_MISSING:
            matches.append((len(missing), -used, recipe.name, recipe, missing))

    matches.sort(key=lambda match: match[:3])
    return [{"recipe": recipe, "missing": missing} for *_, recipe, missing in matches]
