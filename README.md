# marnk-162-nutrition

CS162 Group 4's nutrition app (working name). It helps people work out what they can cook from what they already have, plus one or two extra ingredients. It's a Flask app with Jinja pages and a SQLite database.

## Run it locally

You need Python 3. From the repo root:

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r app_flask\requirements.txt
cd app_flask
flask --app nutrition init-db
flask --app nutrition seed-recipes
flask --app nutrition seed-ingredients
flask --app nutrition run
```

**macOS or Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r app_flask/requirements.txt
cd app_flask
flask --app nutrition init-db
flask --app nutrition seed-recipes
flask --app nutrition seed-ingredients
flask --app nutrition run
```

Then open http://127.0.0.1:5000. `init-db` creates the database in `app_flask/instance/` (git ignores it) and only adds missing tables, so it's safe to run again. `seed-recipes` downloads the 40 starter recipes from TheMealDB (internet needed, no API key) and skips ones already stored; `seed-ingredients` loads their calories and macros from `nutrition/data/`. Both are safe to run again.

## Run the tests

From the repo root, with the virtual environment active:

```
python -m unittest discover -s app_flask/tests -t . -v
```

Test files go in `app_flask/tests/` and must be named `test_*.py`, or they won't be found.

## Run it with Docker

You need Docker running (on Windows and macOS, open Docker Desktop first). From the repo root:

```
docker compose up --build
```

Then open http://localhost:8000. The container listens on 5000, and Compose maps it to 8000 on your machine, because macOS uses port 5000 for AirPlay. On every start the container creates any missing tables, downloads the 40 starter recipes from TheMealDB (skipping ones it already has) and loads their calories and macros. The database lives in a Docker volume, so your data stays between restarts. Without internet the recipe download is skipped and the app starts with the recipes it already stored. Press Ctrl+C to stop it.

## Deploy

The testing deployment is hosted on PythonAnywhere's free tier. Until the home
page is merged, open the registration page directly:

https://muya123.pythonanywhere.com/register

The live deployment has been verified with all 40 starter recipes and their
ingredient data loaded.

To redeploy the latest `main`, open a PythonAnywhere Bash console and run:

```bash
cd /home/muya123/marnk-162-nutrition
git pull --ff-only origin main
source .venv/bin/activate
python -m pip install -r app_flask/requirements.txt
python -m unittest discover -s app_flask/tests -t . -v
cd app_flask
flask --app nutrition init-db
flask --app nutrition seed-recipes
flask --app nutrition seed-ingredients
```

Then reload `muya123.pythonanywhere.com` from the PythonAnywhere **Web** page.
The deployment costs $0 on the free tier. Its SQLite database persists across
application reloads and code redeployments, and the free web app must be
renewed monthly from the PythonAnywhere dashboard.

The production `SECRET_KEY` is stored on PythonAnywhere outside the repository
and must never be committed.

## Repo layout

| Path | What's there |
| --- | --- |
| `app_flask/nutrition/` | The app: `create_app()` in `__init__.py`, the database in `db.py`, tables in `models.py`, `templates/` and `static/` |
| `app_flask/tests/` | `unittest` tests |
| `docs/` | Research and decisions, mirrored from our Confluence space |
| `spikes/` | Throwaway experiments, not app code (for example the nutrition API comparison) |

## How we work

Branching, tickets, PRs and reviews are in [CONTRIBUTING.md](CONTRIBUTING.md), and the stack choices are in [ADR-000](docs/adr/000-stack-and-workflow.md). Tickets live on the [Jira board](https://marnk-162.atlassian.net/jira/software/projects/NUT/boards).
