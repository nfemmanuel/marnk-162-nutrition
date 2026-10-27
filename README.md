# marnk-162-nutrition
CS162 Group 4 nutrition app (internal placeholder name)


## Recipe Dataset (NUT-27)

The app uses [TheMealDB API](https://www.themealdb.com/api.php) to fetch recipes and store them locally in SQLite using SQLAlchemy. Each recipe includes its name, ingredients, and quantities.

### Setup and Seeding

From the repository root, with your Python virtual environment activated:

```powershell
py -m pip install -r app_flask/requirements.txt
py -m flask --app app_flask.nutrition init-db
py -m flask --app app_flask.nutrition seed-recipes --count 50
```

- `init-db` creates missing database tables without deleting existing data.
- `seed-recipes` fetches, validates, and stores recipes, skipping duplicates.
- `--count 50` requests 50 recipes; fewer may be saved if some are duplicates or invalid.
- Internet access is required for importing recipes. No API key is needed.

### Tests

Run all tests from the repository root:

```powershell
py -m unittest discover -s app_flask/tests -t .
```

Recipe data is sourced from TheMealDB. The importer and database models are implemented in `app_flask/nutrition/`.