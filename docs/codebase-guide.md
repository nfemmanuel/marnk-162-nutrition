# Codebase guide
Mirrored in Confluence: https://marnk-162.atlassian.net/wiki/spaces/SD/pages/43515905/Codebase+guide

This is the running map of the code on `main`, agreed at the Nov 10 standup. Read it to learn the code on your own time. Whoever merges a PR that adds or moves a file updates this page in the same PR.

Last checked against `main` on Nov 20.

## What the app does today

A visitor can open the home page, register, log in, see a bare account page and log out. A logged-in user gets a "Saved recipes" link in the nav. That page lists the user's saved recipes with their ingredients and a Remove button.

The database can also hold recipes downloaded from TheMealDB and USDA calories and macros for their ingredients. Code exists to add up a recipe's macros and to rank recipes by the ingredients a user has. No page uses either yet.

The route that saves a recipe exists, and so does a Save button template. No page includes the button yet, because no page lists recipes. So a user cannot save a recipe from the site today. The only other route is a temporary `/hello` page.

## Routes

| Route | Login needed | What it does | File |
| --- | --- | --- | --- |
| `GET /` | No | Home page with links to log in and register | `home.py` |
| `GET, POST /register` | No | Registration form, creates a user | `auth.py` |
| `GET, POST /login` | No | Login form, starts a session | `auth.py` |
| `POST /logout` | Yes | Ends the session | `auth.py` |
| `GET /account` | Yes | Account page | `auth.py` |
| `GET /saved` | Yes | The user's saved recipes, newest first | `saved.py` |
| `POST /saved/<recipe_id>` | Yes | Saves a recipe, then goes back to the page the user came from, or to `/saved` | `saved.py` |
| `POST /saved/<recipe_id>/remove` | Yes | Removes a saved recipe, then shows `/saved` | `saved.py` |
| `GET /hello` | No | Temporary check that the app starts | `__init__.py` |

A logged-out visitor who opens a page that needs login is sent to `/login`. A logged-in user who opens `/login` or `/register` is sent to `/account`. Saving a recipe that does not exist returns a 404.

## How a request flows

1. The server (or `flask --app nutrition`) imports the `nutrition` package and calls `create_app()` in [`__init__.py`](../app_flask/nutrition/__init__.py).
2. `create_app()` sets `SECRET_KEY` and the SQLite path, then applies any test config.
3. It connects `db`, the Flask-Login `login_manager` and the three CLI commands to the app. It registers three blueprints, `auth`, `home` and `saved`, and adds `/hello`.
4. A request such as `POST /login` matches a route in a blueprint file, here [`auth.py`](../app_flask/nutrition/auth.py).
5. The route reads the form or the URL and calls a service module. `auth.py` uses [`user_service.py`](../app_flask/nutrition/user_service.py). `saved.py` uses [`saved_service.py`](../app_flask/nutrition/saved_service.py). The services run the database queries through `db.session`.
6. The route redirects, or renders a template that extends [`base.html`](../app_flask/nutrition/templates/base.html). The base template shows flashed messages and the nav.
7. On later requests, `load_user()` in `auth.py` turns the session's user ID back into `current_user`. `@login_required` uses it to protect a route.

Routes call service modules and never write queries themselves. The home route has no database work, so it calls nothing. `saved.py` passes `current_user.id` to every service call, so a user only sees and changes their own list.

## File map

| Path | What it does | Main names | Ticket |
| --- | --- | --- | --- |
| [`app_flask/nutrition/__init__.py`](../app_flask/nutrition/__init__.py) | App factory | `create_app`, `/hello` | NUT-3, later edits for NUT-5, NUT-6, NUT-27, NUT-28, NUT-39 |
| [`app_flask/nutrition/db.py`](../app_flask/nutrition/db.py) | The shared database object and its table command | `db`, `init_db_command` | NUT-4 |
| [`app_flask/nutrition/models.py`](../app_flask/nutrition/models.py) | The tables | `User`, `Recipe`, `RecipeIngredient`, `Food`, `Ingredient`, `SavedRecipe` | NUT-4 (User), NUT-27, NUT-28, NUT-38 |
| [`app_flask/nutrition/auth.py`](../app_flask/nutrition/auth.py) | Login routes | `auth_blueprint`, `login_manager`, `register`, `login`, `logout`, `account` | NUT-5 |
| [`app_flask/nutrition/user_service.py`](../app_flask/nutrition/user_service.py) | User checks and queries | `normalize_email`, `is_valid_email`, `get_user_by_email`, `get_user_by_id`, `create_user` | NUT-5 |
| [`app_flask/nutrition/home.py`](../app_flask/nutrition/home.py) | The home page route | `home_bp`, `index` | NUT-6 |
| [`app_flask/nutrition/saved.py`](../app_flask/nutrition/saved.py) | Saved recipe routes | `saved_blueprint`, `saved_list`, `save`, `remove` | NUT-39 (list, remove), NUT-40 (save) |
| [`app_flask/nutrition/saved_service.py`](../app_flask/nutrition/saved_service.py) | Saved recipes per user | `save_recipe`, `remove_saved_recipe`, `list_saved_recipes`, `saved_recipe_ids` | NUT-38, NUT-41 (unknown user check) |
| [`app_flask/nutrition/recipe_api.py`](../app_flask/nutrition/recipe_api.py) | Downloads and validates TheMealDB recipes | `fetch_meals`, `validate_meal`, `download_recipes` | NUT-27 |
| [`app_flask/nutrition/seed.py`](../app_flask/nutrition/seed.py) | Stores the downloaded recipes | `seed_recipes_command` | NUT-27 |
| [`app_flask/nutrition/macros.py`](../app_flask/nutrition/macros.py) | Loads USDA macros and totals a recipe | `seed_ingredients_command`, `load_macros`, `to_grams`, `recipe_totals`, `names_without_macros` | NUT-28 |
| [`app_flask/nutrition/matching.py`](../app_flask/nutrition/matching.py) | Ranks recipes by what the user has | `match_recipes`, `covers`, `food_ids`, `clean`, `STAPLES`, `MAX_MISSING` | NUT-34, NUT-36 (staples, partial names, same food) |
| [`templates/base.html`](../app_flask/nutrition/templates/base.html) | The layout every page extends, with the nav and flashed messages | `title` and `content` blocks | NUT-3, NUT-5, NUT-39 (Saved recipes link) |
| [`templates/home.html`](../app_flask/nutrition/templates/home.html) | Home page | links to `/login` and `/register` | NUT-6 |
| [`templates/login.html`](../app_flask/nutrition/templates/login.html), [`register.html`](../app_flask/nutrition/templates/register.html), [`account.html`](../app_flask/nutrition/templates/account.html) | Login, registration and account pages | | NUT-5 |
| [`templates/saved.html`](../app_flask/nutrition/templates/saved.html) | The saved recipes page, each recipe opens to its ingredients | `recipes`, Remove button | NUT-39 |
| [`templates/_save_button.html`](../app_flask/nutrition/templates/_save_button.html) | A Save button for any page that lists recipes. No page includes it yet | needs `recipe` and `saved_ids` | NUT-40 |
| [`app_flask/nutrition/static/style.css`](../app_flask/nutrition/static/style.css) | Styles. Imports Pico CSS 2 from a CDN, then adds a few rules | | NUT-3, NUT-7 |
| [`app_flask/nutrition/data/`](../app_flask/nutrition/data) | USDA numbers and its own README | `foods.csv`, `ingredients.csv` | NUT-28 |
| [`app_flask/requirements.txt`](../app_flask/requirements.txt) | Python packages | Flask, Flask-Login, Flask-SQLAlchemy | |
| [`Dockerfile`](../Dockerfile), [`docker-compose.yml`](../docker-compose.yml) | One-command run | port 8000 to 5000, `instance` volume | NUT-8 |
| [`.github/workflows/tests.yml`](../.github/workflows/tests.yml) | Runs the tests on same-repo PRs and on pushes to `main`, on the self-hosted `nf-tablet` runner | job `test` | NUT-9, then PR #63 |
| [`README.md`](../README.md), [`CONTRIBUTING.md`](../CONTRIBUTING.md) | How to run, test and deploy, and how the team works. The README has the PythonAnywhere steps | | NUT-8, NUT-10, NUT-31, NUT-32 |

## Data model

- `users` has `id`, a unique `email`, `password_hash` (never the password) and `created_at`.
- `recipes` has `id`, `name`, `source`, `source_id` and `source_url`. The pair `source` and `source_id` is unique.
- `recipe_ingredients` has `id`, `recipe_id` (to `recipes`), `name` and `amount` as text such as "200g". Deleting a recipe deletes its ingredients.
- `foods` has `fdc_id` (USDA's ID), a `description`, and per 100 g `calories`, `protein`, `carbs` and `fat`.
- `ingredients` has `name` (lowercase, the key) and `fdc_id` (to `foods`). An empty `fdc_id` marks a spice. Totals skip spices, and matching never treats two spices as the same food.
- `saved_recipes` has `user_id` (to `users`) and `recipe_id` (to `recipes`) as a joint key, so one user cannot save a recipe twice, plus `created_at`.

`recipe_ingredients` links to `ingredients` by name only, with no foreign key. SQLite does not check foreign keys by default, so `save_recipe` checks that the user and the recipe exist before it adds a row.

## Matching rules

`match_recipes(have)` in `matching.py` takes the ingredient names a user has. A recipe qualifies when it uses at least one of them and needs at most `MAX_MISSING` (2) more. These rules decide what counts.

- Names are compared in lowercase without spaces at either end.
- Staples such as salt, pepper, water, oil and sugar (the `STAPLES` set, exact names) are never missing and never counted as used.
- A typed name covers a recipe name when every word of it is a word of the recipe's name. "egg" covers "egg yolks" and does not cover "eggplant".
- Two names that point to the same USDA food cover each other, such as "onion" and "red onions".
- Results come with the fewest missing first, then the most used, then by recipe name. An empty list returns nothing.

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
| `test_units.py` | The factory starts in testing mode and `/` answers |
| `test_home.py` | The home page loads with its text and its login and register links |
| `test_models.py` | Saving a `User`, unique email, `init-db` |
| `test_auth.py` | Register (bad password, bad email, duplicate email), login, logout |
| `test_recipes.py` | Meal validation, the download loop, `seed-recipes` repeat and failure |
| `test_macros.py` | `seed-ingredients`, `to_grams` and `recipe_totals` |
| `test_matching.py` | `match_recipes` ranking, ties, case, empty input, staples, partial names and same-food names |
| `test_saved_service.py` | The `saved_recipes` table and the four service functions, including refusing an unknown user or recipe |
| `test_saved.py` | The `/saved` pages through the test client (list, remove, save, login needed, another user's list) and the Save button template |

## The docs folder

[`docs/`](.) holds the team's written decisions and research, apart from the code.

- [`docs/adr/`](adr) has the Architecture Decision Records. `000-stack-and-workflow.md` is the stack and workflow decision. `002-styling.md` is the styling decision (Pico CSS 2). It used to be `docs/ADR-000-styling.md` and was renumbered and moved here. Number 001 is kept for the data source ADR in open PR #57.
- [`docs/research/competitor-teardown.md`](research/competitor-teardown.md) is the competitor teardown (NUT-13).
- [`docs/research/interviews/README.md`](research/interviews/README.md) is the round 1 interview grid, and `raw/` next to it holds the raw notes and transcripts with names removed.
- [`docs/research/interviews/synthesis.md`](research/interviews/synthesis.md) is the round 1 synthesis (NUT-15).
- [`docs/standups/`](standups) has one note per weekly standup, with a `README.md` table that lists them.
- This guide is [`docs/codebase-guide.md`](codebase-guide.md).

## In flight

Open PRs on Nov 20, not yet in the map above.

- #57 Added ADR-001 (the data source ADR, number 001 in `docs/adr/`)

## Keeping this guide current

Whoever merges a PR that adds, renames or moves a file updates its row in the file map, and the routes, data model, commands and tests sections if the PR changes them. Move finished items out of "In flight". Edit the Confluence copy at the same time.
