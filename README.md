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
flask --app nutrition run
```

**macOS or Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r app_flask/requirements.txt
cd app_flask
flask --app nutrition init-db
flask --app nutrition run
```

Then open http://127.0.0.1:5000. `init-db` creates the database in `app_flask/instance/` (git ignores it) and only adds missing tables, so it's safe to run again.

## Run the tests

From the repo root, with the virtual environment active:

```
python -m unittest discover -s app_flask/tests -t . -v
```

Test files go in `app_flask/tests/` and must be named `test_*.py`, or they won't be found.

## Run it with Docker

Coming with NUT-8 (`docker compose up`).

## Deploy

Coming with NUT-32 (public URL and redeploy steps).

## Repo layout

| Path | What's there |
| --- | --- |
| `app_flask/nutrition/` | The app: `create_app()` in `__init__.py`, the database in `db.py`, tables in `models.py`, `templates/` and `static/` |
| `app_flask/tests/` | `unittest` tests |
| `docs/` | Research and decisions, mirrored from our Confluence space |
| `spikes/` | Throwaway experiments, not app code (for example the nutrition API comparison) |

## How we work

Branching, tickets, PRs and reviews are in [CONTRIBUTING.md](CONTRIBUTING.md), and the stack choices are in [ADR-000](docs/adr/000-stack-and-workflow.md). Tickets live on the [Jira board](https://marnk-162.atlassian.net/jira/software/projects/NUT/boards).
