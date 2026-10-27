"""Fetch and validate recipe ingredients and measures from TheMealDB."""

import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://www.themealdb.com/api/json/v1/1/search.php"
SEARCH_TERMS = (
    "chicken", "rice", "pasta", "beef", "fish", "salmon", "egg", "soup",
    "potato", "curry", "vegetarian", "lentil", "pork", "noodle", "bean",
    "cake", "salad", "bread", "lamb", "pie", "shrimp", "tofu",
)


def validate_meal(meal):
    """Normalize a TheMealDB recipe, or return None if mandatory data is missing."""
    if not isinstance(meal, dict):
        return None
    meal_id = str(meal.get("idMeal") or "").strip()
    name = str(meal.get("strMeal") or "").strip()
    if not meal_id.isdigit() or not name or len(name) > 120:
        return None

    ingredients = []
    seen = set()
    for index in range(1, 21):
        ingredient = str(meal.get(f"strIngredient{index}") or "").strip()
        amount = str(meal.get(f"strMeasure{index}") or "").strip()
        if not ingredient:
            if amount:
                return None  # Amount without an ingredient: inconsistent API record.
            continue
        if not amount or len(ingredient) > 120 or len(amount) > 100:
            return None
        if ingredient.casefold() in seen:
            return None
        seen.add(ingredient.casefold())
        ingredients.append({"name": ingredient, "amount": amount})

    if len(ingredients) < 2:
        return None

    return {
        "name": name,
        "source": "TheMealDB",
        "source_id": meal_id,
        # An API lookup URL, not an unverified website permalink.
        "source_url": f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}",
        "ingredients": ingredients,
    }


def fetch_meals(term):
    """Call the free educational API using Python's standard library."""
    request = Request(
        BASE_URL + "?" + urlencode({"s": term}),
        headers={"User-Agent": "NUT-CS162-recipe-import/1.0"},
    )
    with urlopen(request, timeout=20) as response:
        data = json.load(response)
    if not isinstance(data, dict):
        raise ValueError(f"Unexpected response for {term}")
    if data.get("meals") is None:
        return []
    if not isinstance(data["meals"], list):
        raise ValueError(f"Unexpected response for {term}")
    return data["meals"]


def download_recipes(target=40, fetch=None):
    """Collect a specified number of distinct, validated recipes."""
    if fetch is None:
        fetch = fetch_meals
    recipes = []
    seen_ids = set()
    seen_names = set()
    rejected = 0
    for term in SEARCH_TERMS:
        for meal in fetch(term):
            recipe = validate_meal(meal)
            if recipe is None:
                rejected += 1
                continue
            normalized_name = recipe["name"].casefold()
            if recipe["source_id"] in seen_ids or normalized_name in seen_names:
                continue
            recipes.append(recipe)
            seen_ids.add(recipe["source_id"])
            seen_names.add(normalized_name)
            if len(recipes) == target:
                return recipes, rejected
    raise ValueError(
        f"Only {len(recipes)} distinct valid recipes found (target {target}); "
        f"{rejected} invalid"
    )
