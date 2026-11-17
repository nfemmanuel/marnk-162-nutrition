# Codebase guide
nMirrored in Confluence: https://marnk-162.atlassian.net/wiki/spaces/SD/pages/43515905/Codebase+guide

This is the running map of the code on `main`, agreed at the Nov 10 standup. Read it to learn the code on your own time. Whoever merges a PR that adds or moves a file updates this page in the same PR.

## What the app does today

A visitor can register, log in, see a bare account page and log out. The database can hold recipes downloaded from TheMealDB, USDA calories and macros for their ingredients, and the recipes each user saved. Code exists to add up a recipe's macros, to rank recipes by the ingredients a user has, and to save, remove and list a user's recipes. None of that has a page yet, so no visitor can reach it. The only other route is a temporary `/hello` page. Some of the open PRs below add pages for them.

## How a request flows

1. The server (or `flask --app nutrition`) imports the `nutrition` package and calls `create_app()` in [`__init__.py`](../app_flask/nutrition/__init__.py).
2. `create_app()` sets `SECRET_KEY` and the SQLite path, then applies any test config.
3. It connects `db`, the Flask-Login `login_manager` and the three CLI commands to the app, and registers the `auth` blueprint.
4. A request such as `POST /login` matches a route in [`auth.py`](../app_flask/nutrition/auth.py).
5. The route reads the form and calls functions in [`user_service.py`](../app_flask/nutrition/user_service.py), which run the database queries through `db.session`.
6. The route redirects, or renders a template that extends [`base.html`](../app_flask/nutrition/templates/base.html). The base template shows flashed messages and the nav.
7. On later requests, `load_user()` in `auth.py` turns the session's user ID back into `current_user`.

Routes call service modules and never write queries themselves. `saved_service.py` follows the same rule for the pages still to come.

## File map

| Path | What it does | Main names | Ticket |
| --- | --- | --- | --- |
| [`app_flask/nutrition/__init__.py`](../app_flask/nutrition/__init__.py) | App factory | `create_app`, `/hello` | NUT-3 |
| [`app_flask/nutrition/db.py`](../app_flask/nutrition/db.py) | The shared database object and its table command | `db`, `init_db_command` | NUT-4 |
| [`app_flask/nutrition/models.py`](../app_flask/nutrition/models.py) | The tables | `User`, `Recipe`, `RecipeIngredient`, `Food`, `Ingredient`, `SavedRecipe` | NUT-4 (User), NUT-27, NUT-28, NUT-38 |
| [`app_flask/nutrition/auth.py`](../app_flask/nutrition/auth.py) | Login routes | `auth_blueprint`, `login_manager`, `register`, `login`, `logout`, `account` | NUT-5 |
| [`app_flask/nutrition/user_service.py`](../app_flask/nutrition/user_service.py) | User checks and queries | `normalize_email`, `is_valid_email`, `get_user_by_email`, `get_user_by_id`, `create_user` | NUT-5 |
| [`app_flask/nutrition/recipe_api.py`](../app_flask/nutrition/recipe_api.py) | Downloads and validates TheMealDB recipes | `fetch_meals`, `validate_meal`, `download_recipes` | NUT-27 |
| [`app_flask/nutrition/seed.py`](../app_flask/nutrition/seed.py) | Stores the downloaded recipes | `seed_recipes_command` | NUT-27 |
| [`app_flask/nutrition/macros.py`](../app_flask/nutrition/macros.py) | Loads USDA macros and totals a recipe | `seed_ingredients_command`, `load_macros`, `to_grams`, `recipe_totals`, `names_without_macros` | NUT-28 |
| [`app_flask/nutrition/matching.py`](../app_flask/nutrition/matching.py) | Ranks recipes by what the user has | `match_recipes`, `MAX_MISSING` | NUT-34 |
| [`app_flask/nutrition/saved_service.py`](../app_flask/nutrition/saved_service.py) | Saved recipes per user | `save_recipe`, `remove_saved_recipe`, `list_saved_recipes`, `saved_recipe_ids` | NUT-38 |
| [`app_flask/nutrition/templates/`](../app_flask/nutrition/templates) | Jinja pages | `base.html`, `login.html`, `register.html`, `account.html` | NUT-3 (base), NUT-5 |
| [`app_flask/nutrition/static/style.css`](../app_flask/nutrition/static/style.css) | Styles | | NUT-3 |
| [`app_flask/nutrition/data/`](../app_flask/nutrition/data) | USDA numbers and its own README | `foods.csv`, `ingredients.csv` | NUT-28 |
| [`Dockerfile`](../Dockerfile), [`docker-compose.yml`](../docker-compose.yml) | One-command run | port 8000 to 5000, `instance` volume | NUT-8 |
| [`.github/workflows/tests.yml`](../.github/workflows/tests.yml) | Runs the tests on every PR | job `test` | NUT-9 |

## Data model

- `users` has `id`, a unique `email`, `password_hash` (never the password) and `created_at`.
- `recipes` has `id`, `name`, `source`, `source_id` and `source_url`. The pair `source` and `source_id` is unique.
- `recipe_ingredients` has `id`, `recipe_id` (to `recipes`), `name` and `amount` as text such as "200g". Deleting a recipe deletes its ingredients.
- `foods` has `fdc_id` (USDA's ID) and per 100 g `calories`, `protein`, `carbs` and `fat`.
- `ingredients` has `name` (lowercase, the key) and `fdc_id` (to `foods`). An empty `fdc_id` marks a spice, which totals skip.
- `saved_recipes` has `user_id` and `recipe_id` as a joint key, so one user cannot save a recipe twice, plus `created_at`.

`recipe_ingredients` links to `ingredients` by name only, with no foreign key.

## Commands and data loading

Run these from `app_flask/` with `flask --app nutrition`.

- `init-db` creates missing tables and keeps data.
- `seed-recipes` downloads recipes from TheMealDB (internet needed), 40 by default and 30 to 50 with `--count`. It skips recipes already stored and changes nothing if the download fails.
- `seed-ingredients` replaces the `foods` and `ingredients` tables with the CSV files in `data/`. A bad row changes nothing. It lists recipe ingredients that have no row yet.

Docker runs `init-db`, then `seed-recipes` (the app still starts if it fails), then `seed-ingredients`, then `run --host 0.0.0.0`, on every start.

## Tests

The tests are in [`app_flask/tests/`](../app_flask/tests). From the repo root, with the venv active, run `python -m unittest discover -s app_flask/tests -t . -v`. Files must be named `test_*.py`. CI runs the same command.

| File | Covers |
| --- | --- |
| `test_units.py` | The factory starts in testing mode |
| `test_models.py` | Saving a `User`, unique email, `init-db` |
| `test_auth.py` | Register (bad password, bad email, duplicate email), login, logout |
| `test_recipes.py` | Meal validation, the download loop, `seed-recipes` repeat and failure |
| `test_macros.py` | `seed-ingredients`, `to_grams` and `recipe_totals` |
| `test_matching.py` | `match_recipes` ranking, ties, case and empty input |
| `test_saved_service.py` | The `saved_recipes` table and the four service functions |

## In flight

Open PRs on Nov 17, not yet in the map above.

- #37 NUT-6 Home page
- #39 NUT-15 Round 1 interview synthesis
- #44 NUT-36 Match recipes without listing staples or exact names
- #46 NUT-39 See and remove my saved recipes
- #47 NUT-40 Save a recipe from where I see it
- #55 Add standup notes to docs
- #56 NUT-32 Document PythonAnywhere deployment
- #57 Added ADR-001
- #59 NUT-41 Refuse saving a recipe for an unknown user

## Keeping this guide current

Whoever merges a PR that adds, renames or moves a file updates its row in the file map, and the data model, commands and tests sections if the PR changes them. Move finished items out of "In flight". Edit the Confluence copy at the same time.
