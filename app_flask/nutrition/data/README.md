# Ingredient macros (NUT-28)

Calories, protein, carbs and fat per 100 g for every ingredient in the starter recipe dataset: the 239 ingredient names in the 50 recipes `seed-recipes --count 50` imports (NUT-27). A smaller `--count` takes the first of the same recipes. `ingredients.csv` has 318 names, because it also keeps the ones from NUT-27's first recipe list.

| File | One row per | Columns |
| --- | --- | --- |
| `foods.csv` | USDA food | `fdc_id`, USDA's `description`, then `calories` (kcal), `protein`, `carbs` and `fat` (g) per 100 g |
| `ingredients.csv` | ingredient name, in lowercase, as recipes use it | `name`, the `fdc_id` of the USDA food it means, and a `note` on choices (not loaded) |

Several names share one food (`onion`, `onions`, `red onions`), so its numbers are stored once.

Load both files from the repo root, after `seed-recipes` (no internet needed):

```
flask --app app_flask.nutrition seed-ingredients
```

A second run replaces the rows with whatever the files hold now. If a row has a bad number, or an `fdc_id` in `ingredients.csv` isn't in `foods.csv`, the command stops and changes nothing. It also lists any recipe ingredient name that isn't in `ingredients.csv` yet. TheMealDB adds recipes over time, so a later import can bring new names to add here.

## Source

USDA FoodData Central, SR Legacy (April 2018), public domain. The four values are USDA nutrients 1008 (Energy, kcal), 1003 (Protein), 1005 (Carbohydrate, by difference) and 1004 (Total lipid, fat). Any row can be checked at `https://fdc.nal.usda.gov/food-details/<fdc_id>/nutrients`.

## Skipped on purpose (empty `fdc_id`)

- **Spices and herbs:** anything USDA lists under "Spices and Herbs": salt, pepper, dried spices, most herbs (fresh dill and rosemary too), vanilla extract, prepared mustard and vinegar. They're used by the pinch or the teaspoon and add almost nothing, as agreed at the Oct 15 stand-up.
- **Spice blends USDA doesn't list:** garam masala, Chinese five spice, harissa spice, all-purpose seasoning, celery salt and onion salt, plus curry pastes (madras, Thai green and Thai red), which recipes add by the spoonful.
- **Banana leaves:** used for wrapping, not eaten.

## Choices worth checking

- **No exact USDA food:** the closest one is used, and the `note` says so. Examples: mirin uses sake, crème fraîche uses heavy cream, the frozen seafood mix uses prawns, cassava flour and farine use tapioca (cassava starch), hot-smoked salmon uses cooked salmon, and roasted vegetables use frozen mixed vegetables.
- **Ambiguous names:** the choice follows how the recipes use them.
  - Lemon and lime mean their juice.
  - Kidney beans are canned with their liquid ("400g", "1 can").
  - "Tomato puree" is US-style purée, because Beef Asado uses 8 oz of it. The recipes that add a spoonful mean UK purée (tomato paste), which changes their totals by only a few calories. "Tomato purée" with the accent (1 tbsp in Lamb Rogan josh) is tomato paste.
  - The lamb tagine's apricots are dried. The 250 g pack of lentils is ready to eat (cooked), while brown and French lentils are dry.
- **A slip in TheMealDB's data:** Salmon noodle wraps lists 85 g each of chilli, coriander and lime but no butter, although the method uses butter. The 85 g is most likely the butter they flavour, so that recipe's total is too low.

## Recipe totals

`recipe_totals()` in `macros.py` adds up a whole recipe from these values.

- **Units it reads:** weights (g, kg, oz, lb), volumes (ml, l) and spoons and cups. Volumes are weighed as water (1 ml = 1 g), which is close enough for a rough total.
- **Spices** are skipped.
- **Amounts it can't weigh** come back in a list of ingredients left out, so a page can say the total is partial. These are pieces ("2 sliced", "8" chicken thighs), cans and packets, and words ("To taste").

Across the 50 starter recipes, 238 ingredient rows are counted, 122 spices are skipped and 167 rows are left out because their amounts can't be weighed. So far only 4 recipes have a complete total.
