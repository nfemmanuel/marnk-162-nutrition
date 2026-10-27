# Ingredient macros (NUT-28)

Calories, protein, carbs and fat per 100 g for every ingredient in the starter recipe dataset (NUT-27: the 50 recipes `seed-recipes --count 50` imports, 209 ingredient names).

| File | One row per | Columns |
| --- | --- | --- |
| `foods.csv` | USDA food | `fdc_id`, USDA's `description`, then `calories` (kcal), `protein`, `carbs` and `fat` (g) per 100 g |
| `ingredients.csv` | ingredient name, in lowercase, as recipes use it | `name`, the `fdc_id` of the USDA food it means, and a `note` on choices (not loaded) |

Several names share one food (`onion`, `onions`, `red onions`), so its numbers are stored once.

Load both files with `flask --app app_flask.nutrition seed-ingredients`. A second run replaces the rows with whatever the files hold now. The command also lists any recipe ingredient name that isn't in `ingredients.csv` yet.

## Source

USDA FoodData Central, SR Legacy (April 2018), public domain. The four values are USDA nutrients 1008 (Energy, kcal), 1003 (Protein), 1005 (Carbohydrate, by difference) and 1004 (Total lipid, fat). Any row can be checked at `https://fdc.nal.usda.gov/food-details/<fdc_id>/nutrients`.

## Skipped on purpose (empty `fdc_id`)

- **Spices and herbs:** anything USDA lists under "Spices and Herbs": salt, pepper, dried spices, most herbs, prepared mustard and vinegar. They're used by the pinch or the teaspoon and add almost nothing, as agreed at the Oct 15 stand-up.
- **Spice blends USDA doesn't list:** garam masala, Chinese five spice, harissa spice, celery salt and onion salt.
- **Banana leaves:** used for wrapping, not eaten.

## Choices worth checking

- **No exact USDA food:** the closest one is used, and the `note` says so. Examples: mirin uses sake, crème fraîche uses heavy cream, and the frozen seafood mix uses prawns.
- **Ambiguous names:** the choice follows how the recipes use them.
  - Lemon and lime mean their juice ("1/3 cup").
  - Kidney beans are canned with their liquid: the recipes pour in the whole can.
  - "Tomato puree" is US-style purée: three recipes use 8 oz of it.

## Recipe totals

`recipe_totals()` in `macros.py` adds up a whole recipe from these values.

- **Units it reads:** weights (g, kg, oz, lb), volumes (ml, l) and spoons and cups. Volumes are weighed as water (1 ml = 1 g), which is close enough for a rough total.
- **Spices** are skipped.
- **Amounts it can't weigh** come back in a list of ingredients left out, so a page can say the total is partial. These are pieces ("2 sliced", "8" chicken thighs) and words ("To taste").

Across the 50 starter recipes, 269 ingredient rows are counted, 122 spices are skipped and 164 rows are left out, mostly pieces.
