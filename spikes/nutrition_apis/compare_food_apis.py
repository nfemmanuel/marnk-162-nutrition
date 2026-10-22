"""Spike: run the same searches against USDA FoodData Central, Open Food Facts
and TheMealDB, and save every raw response for inspection.

Throwaway code, not part of the app.

    USDA_API_KEY=... OFF_CONTACT_EMAIL=you@example.com python compare_food_apis.py

USDA_API_KEY is optional (falls back to the rate-limited DEMO_KEY).
OFF_CONTACT_EMAIL is required: Open Food Facts asks for a User-Agent with a contact.

Pass API names to run only those (default: all), e.g. to retry Open Food Facts:

    python compare_food_apis.py off off_sal
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import NamedTuple

import requests

QUERIES = {
    "whole food": "chicken breast",
    "packaged food": "nutella",
    "mixed dish": "lasagna",
    "misspelling": "chiken breast",
}
TIMEOUT_SECONDS = 30
OUT_DIR = Path(__file__).parent / "responses"


class Api(NamedTuple):
    url: str
    query_param: str
    extra_params: dict
    headers: dict
    items_key: str  # JSON key holding the list of results
    name_key: str  # JSON key holding a result's display name


OFF_HEADERS = {"User-Agent": f"NutSpike/0.1 ({os.environ['OFF_CONTACT_EMAIL']})"}

APIS = {
    "usda": Api(
        "https://api.nal.usda.gov/fdc/v1/foods/search",
        "query",
        {"api_key": os.environ.get("USDA_API_KEY", "DEMO_KEY")},
        {},
        "foods",
        "description",
    ),
    "off": Api(
        "https://world.openfoodfacts.org/cgi/search.pl",
        "search_terms",
        {"search_simple": 1, "action": "process", "json": 1},
        OFF_HEADERS,
        "products",
        "product_name",
    ),
    "off_sal": Api(  # Search-a-licious, the Open Food Facts full-text search service
        "https://search.openfoodfacts.org/search",
        "q",
        {},
        OFF_HEADERS,
        "hits",
        "product_name",
    ),
    "mealdb": Api(
        "https://www.themealdb.com/api/json/v1/1/search.php",
        "s",
        {},
        {},
        "meals",
        "strMeal",
    ),
}


def search(name, api, label, query):
    start = time.perf_counter()
    response = requests.get(
        api.url,
        params={**api.extra_params, api.query_param: query},
        headers=api.headers,
        timeout=TIMEOUT_SECONDS,
    )
    seconds = time.perf_counter() - start
    response.raise_for_status()
    body = response.json()

    path = OUT_DIR / f"{name}_{label.replace(' ', '_')}.json"
    path.write_text(json.dumps(body, indent=2, ensure_ascii=False), encoding="utf-8")

    items = body.get(api.items_key) or []
    first_names = [item.get(api.name_key) for item in items[:3]]
    limits = {
        key: value
        for key, value in response.headers.items()
        if key.lower().startswith("x-ratelimit")
    }
    print(
        f"{name:7}{label:14}{query!r:18}{seconds:5.2f}s "
        f"returned={len(items):<3} first3={first_names} {limits or ''}"
    )


def main():
    OUT_DIR.mkdir(exist_ok=True)
    selected = sys.argv[1:] or list(APIS)
    for label, query in QUERIES.items():
        for name in selected:
            try:
                search(name, APIS[name], label, query)
            except requests.RequestException as error:
                print(f"{name:7}{label:14}FAILED: {error}")


if __name__ == "__main__":
    main()
