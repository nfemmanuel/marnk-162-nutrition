# Nutrition and recipe data sources: comparison (spike)

- Ticket: NUT-22 (epic NUT-21). Unblocks ADR-001.
- Script: `spikes/compare_food_apis.py`
- Run: 2026-10-08. All APIs once, then both Open Food Facts endpoints a second time after the legacy endpoint returned 503. One machine, one network. Timings are indicative only.
- Keys used: USDA `DEMO_KEY`, Open Food Facts none (custom User-Agent), TheMealDB test key `1`.
- The saved raw JSON of every call was inspected for nutrient fields and result lists. It is not committed to the repo.

TLDR:
Bottom line: none of the three covers both recipes and macros. In our tests USDA was the strongest source for nutrition, Open Food Facts adds packaged products, and TheMealDB only supplies recipe text. This rests on four searches and one run, and the decision belongs in ADR-001.

| Use it for            | Don't use it for                                                                                                                                            | Watch out for                                                                    |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| USDA FoodData Central | Macros for ingredients and generic foods (chicken breast, lasagna). Best coverage and best typo behaviour. Per 100 g, plus gram weights for common portions | Recipes, or anything needing a spelling-tolerant UI on its own                   | Key must stay on our backend. Limit is per IP (1,000/hour with a registered key, DEMO_KEY is far smaller). SR Legacy lists energy twice (kcal and kJ) |
| Open Food Facts       | Branded and packaged products, barcodes, per 100 g macros. Use Search-a-licious                                                                             | The legacy search endpoint: 503 on half our calls, French-first results, slowest | Some hits lack macros (7 of 10 for nutella). ODbL licence has conditions. Search-a-licious rate limits aren't documented                              |
| TheMealDB             | Recipe text, ingredient lists and photos, if we want outside recipes                                                                                        | Nutrition, or broad coverage (2 lasagna recipes, 0 for chicken breast)           | No nutrition fields. Measures are free text ("1 cups", "sprinking"). Free key is for development and educational use                                  |

This document records facts and observations. The decision belongs in ADR-001.

## Method

The same four searches were sent to each API, with no page size set:

| Category      | Query            |
| ------------- | ---------------- |
| Whole food    | `chicken breast` |
| Packaged food | `nutella`        |
| Mixed dish    | `lasagna`        |
| Misspelling   | `chiken breast`  |

Endpoints used:

- USDA FoodData Central: `GET https://api.nal.usda.gov/fdc/v1/foods/search?query=...`
- Open Food Facts, legacy search: `GET https://world.openfoodfacts.org/cgi/search.pl?search_terms=...&search_simple=1&action=process&json=1`. API v2 and v3 have no full-text search, and the docs say this endpoint is not recommended for new integrations.
- Open Food Facts, Search-a-licious: `GET https://search.openfoodfacts.org/search?q=...`. This is the full-text search service Open Food Facts points to.
- TheMealDB: `GET https://www.themealdb.com/api/json/v1/1/search.php?s=...` (search by meal name)

Page sizes were left at each API's default (USDA 50, legacy Open Food Facts 50, Search-a-licious 10), so "returned" counts are not comparable across columns. "Total" is the match count the API reports.

## Results of the real calls

| Search           | USDA                                                                                                                                    | Open Food Facts, legacy (2 runs)                                                                                                                                               | Open Food Facts, Search-a-licious                                                                                                                    | TheMealDB                                                 |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| `chicken breast` | 50 returned, total 21,661, 2.27 s. "CHICKEN BREAST" x3                                                                                  | Run 1: 503. Run 2: 50 returned, total 16,143, 4.63 s. "Blanc de Poulet", "Blanc de Poulet Nature Sans Nitrite", "HERTA Blanc Poulet Broche conservation sans nitrite x4 -140g" | 10 returned, total 10,000 (not exact), 2.04 s. "Chicken breast hot&spicy", "Chicken Breast Fillets", "Chicken breast tempura bites bouchées tempura" | 0 returned, 1.36 s                                        |
| `nutella`        | 37 returned, total 37, 1.69 s. "Nutella sandwich on wheat bread", "Nutella sandwich on white bread", "NUTELLA FERRERO WITH BREADSTICKS" | Run 1: 48 returned, total 1,080, 4.08 s. "Nutella" x3. Run 2: 503                                                                                                              | 10 returned, total 631 (exact), 1.96 s. "Nutella & go! hazelnut spread + breadsticks", "Nutella", "nutella"                                          | 0 returned, 1.19 s                                        |
| `lasagna`        | 50 returned, total 631, 1.78 s. "LASAGNA" x3                                                                                            | Run 1: 50 returned, 3.67 s. Run 2: 50 returned, total 2,250, 3.41 s. Both runs: "Lasagnes de bœuf à la crème de mozzarella", "Lasagnes à la bolognaise", "Lasagne"             | 10 returned, total 2,713 (exact), 2.36 s. "beef lasagna", "Lasagna", "High Protein Chicken Lasagna Chicken Bolognese Sauce"                          | 2 returned, 1.22 s. "Vegan Lasagna", "Lasagna Sandwiches" |
| `chiken breast`  | 50 returned, total 7,734, 1.89 s. "SESAME CHIKEN", "Lunchmeat, chicken breast, sliced", "Turkey breast, sliced, prepackaged"            | 503 in both runs                                                                                                                                                               | 10 returned, total 10,000 (not exact), 2.22 s. "Chiken breast", "Chiken breasts", "Chiken breast"                                                    | 0 returned, 1.36 s                                        |

The result field names the script relies on all worked where a call succeeded: `foods` / `description` (USDA), `products` / `product_name` (Open Food Facts legacy), `hits` / `product_name` (Search-a-licious), `meals` / `strMeal` (TheMealDB).

Observations:

- **Open Food Facts legacy search was unreliable:** 4 of 8 requests across the two runs returned 503. The misspelled query failed both times. Chicken breast and nutella each failed once and succeeded once. The first Open Food Facts call of the first run failed, and we never sent more than 4 searches in a run, so our own request rate (limit: 10 searches/min) was not the cause. The docs say 503 is returned when global rate limits are exceeded, but this spike cannot tell whether that was the reason. When it worked it was the slowest option (3.41 to 4.63 s).
- **Search-a-licious succeeded on all 4 searches** in 1.96 to 2.36 s, with no key and the same User-Agent. It returned 10 results per search, its documented default page size.
- **Language of results:** on the legacy endpoint, 31 of the 50 `lasagna` products have `lang` = `fr`, and the top `chicken breast` results are French. Search-a-licious returned English names for the same queries. Its spec says the `langs` parameter, which defaults to English, selects the language-specific fields searched.
- **What kind of foods come back:** Open Food Facts hits are packaged products (brand and barcode fields). USDA mixes sources. The 50 `chicken breast` results on the first page were 10 Branded, 20 Survey (FNDDS), 17 SR Legacy and 3 Foundation entries, and the `lasagna` page held 29 Branded, 10 Survey (FNDDS) and 11 SR Legacy entries. The generic entries are reference foods without a brand. The first three USDA hits for `chicken breast` are branded products named "CHICKEN BREAST" (Giant Eagle, Tyson, Jennie-O Turkey Store). Of the 37 USDA results for `nutella`, 34 are Branded and 3 are Survey (FNDDS).
- **TheMealDB:** name search returned `{"meals": null}` for `chicken breast`, `nutella` and `chiken breast`. For `chicken breast` this is expected from the endpoint: it matches meal names, and the docs describe a separate ingredient filter (`filter.php?i=chicken_breast`) that this spike did not call.
- **Misspelling:**
  - USDA: the first hit is a product literally named "SESAME CHIKEN", but 35 of the 50 returned names contain both "chicken" and "breast", and the Foundation entry "Chicken, breast, boneless, skinless, raw" is 12th. USDA's echoed request criteria show `requireAllWords: false` (also false on the other three queries).
  - Search-a-licious: all 10 returned names contain the typo ("Chiken breast", "Chiken Breast Costco", ...), so it matched products whose names are spelled that way. Nothing was corrected in the top 10.
  - TheMealDB: nothing.
  - Open Food Facts legacy: failed, so not tested.

## Nutrition data in the responses

For the `lasagna` search, first hit of each API, plus how many hits on the page carry all four of energy, protein, fat and carbohydrate as numbers:

|                    | USDA                               | Open Food Facts, legacy                                   | Open Food Facts, Search-a-licious | TheMealDB                    |
| ------------------ | ---------------------------------- | --------------------------------------------------------- | --------------------------------- | ---------------------------- |
| First hit          | Branded "LASAGNA" (Scardigno's)    | "Lasagnes de bœuf à la crème de mozzarella" (Maison Tino) | "beef lasagna" (Southgate)        | "Vegan Lasagna"              |
| Energy             | 101 kcal                           | 151 kcal                                                  | 93.9 kcal                         | none                         |
| Protein            | 5.53 g                             | 7.2 g                                                     | 3.29 g                            | none                         |
| Fat                | 4.15 g                             | 7.5 g                                                     | 4.23 g                            | none                         |
| Carbohydrate       | 10.1 g                             | 13 g                                                      | 9.86 g                            | none                         |
| Hits with all four | 50 of 50                           | 50 of 50                                                  | 10 of 10                          | 0 of 2 (no nutrition fields) |
| Basis              | Per 100 g (USDA docs, see sources) | Per 100 g (`_100g` keys, `nutrition_data_per` = `100g`)   | Per 100 g (`_100g` keys)          | Not applicable               |

Details that matter when using the data:

- **USDA** lists nutrients as a flat list of objects with `nutrientName`, `unitName` and `value`. Generic entries in the same `lasagna` page have the same fields, for example Survey (FNDDS) "Lasagna with meat" (139 kcal, 7.45 g protein, 4.97 g fat, 16.17 g carbohydrate) and SR Legacy "Lasagna, cheese, frozen, prepared" (130 kcal, 6.54 g, 5.33 g, 13.8 g). SR Legacy hits list Energy twice (KCAL and kJ), so energy must be picked by unit. Branded hits carry `servingSize` (in grams, present on all 29 Branded hits) and `householdServingFullText` (for example "1/3 lasagna"). Survey (FNDDS) hits carry `foodMeasures` with household portions and gram weights (for example "1 cup" = 250 g).
- **Open Food Facts** returns nutrients in a flat `nutriments` object with keys such as `energy-kcal_100g`, `proteins_100g`, `fat_100g` and `carbohydrates_100g`. Other searches were less complete: all four numeric values were present on 49 of 50 `chicken breast` hits (legacy), 47 of 48 `nutella` hits (legacy), 10 of 10 `chicken breast` hits (Search-a-licious) and 7 of 10 `nutella` hits (Search-a-licious).
- **TheMealDB** has no nutrition fields. Each meal has metadata (`strMeal`, `strCategory`, `strArea`, `strTags`, `strSource`, `strYoutube`, image fields), `strInstructions`, and up to 20 `strIngredient` / `strMeasure` pairs. The measures are free text, for example "1 cups", "sprinking", "150g", "2 tbs", "8 slices", "1/4 cup".

## Comparison

|                                              | USDA FoodData Central                                                                                                                                                         | Open Food Facts                                                                                                                                                                                                                                              | TheMealDB                                                                                                                                                           |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| What it holds                                | US government food composition data: Foundation Foods, SR Legacy, FNDDS survey foods, Branded Foods, Experimental Foods                                                       | Packaged food products submitted by volunteers. The docs state there is no assurance the data is accurate, complete or reliable                                                                                                                              | Recipes: name, category, area, instructions, image, ingredients and measures                                                                                        |
| Key needed                                   | Yes. A free data.gov key goes on every request. `DEMO_KEY` exists for exploring                                                                                               | No for reads. A custom User-Agent (`AppName/Version (ContactEmail)`) is required. Writes need an account                                                                                                                                                     | Test key `1` in the URL, for development and educational use                                                                                                        |
| Rate limits (docs)                           | Registered key: 1,000 requests/hour per IP; exceeding it blocks the key for 1 hour. `DEMO_KEY`: 30/hour and 50/day per IP                                                     | Legacy search and product reads: 10 searches/min and 15 product reads/min per IP, not for search-as-you-type. Global limits return 503. Bulk needs: download the data files. Search-a-licious: not stated in its spec                                        | None stated on the official pages read. The paid tier's terms mention a rate limit                                                                                  |
| Rate limits (observed)                       | `X-Ratelimit-Limit: 10` on all four calls (remaining 9 down to 6), using `DEMO_KEY`. This differs from the 30/hour in the guide                                               | No rate-limit headers on either endpoint. Legacy: 4 of 8 requests got 503. Search-a-licious: 4 of 4 succeeded                                                                                                                                                | No rate-limit headers seen                                                                                                                                          |
| Licence                                      | Public domain, CC0 1.0. Citation requested                                                                                                                                    | Database under ODbL, individual contents under the Database Contents License, images under CC BY-SA. These licences have conditions that this spike did not analyse                                                                                          | Terms of use: you may copy and modify content from the official endpoints, you may not resell the API, and artwork must not be passed off as yours                  |
| Can it ship with the app                     | The data can. The key must not be public (keys found in public repos are deactivated), so calls should come from our backend, and the per-IP limit then applies to the server | No key needed, but the documented limits are low and the docs push heavy users to the data downloads or a local copy. The legacy search endpoint failed half our requests                                                                                    | The free key is for development and educational use. Publishing to an app store requires a paid supporter key. The terms do not say whether a hosted web app counts |
| Response shape                               | Top level: `totalHits`, `currentPage`, `totalPages`, `foodSearchCriteria`, `foods`, `aggregations` (counts by data type). First hit had 27 keys                               | Legacy: `count`, `page`, `page_count`, `page_size`, `products`, `skip`; first product had 243 keys. Search-a-licious: `hits`, `count`, `is_count_exact`, `page`, `page_size`, `page_count`, `took`, `facets`, `aggregations` and more; first hit had 43 keys | `meals`, a list or `null`. Flat objects with numbered ingredient and measure fields                                                                                 |
| Size per result (saved JSON, pretty-printed) | About 26 KB (`lasagna`, 50 results)                                                                                                                                           | Legacy: about 81 KB (`lasagna`, 50 results). Search-a-licious: about 21 KB (`lasagna`, 10 results)                                                                                                                                                           | About 2.5 KB (`lasagna`, 2 results)                                                                                                                                 |
| Speed (successful calls)                     | 1.69 to 2.27 s                                                                                                                                                                | Legacy: 3.41 to 4.63 s. Search-a-licious: 1.96 to 2.36 s                                                                                                                                                                                                     | 1.19 to 1.36 s                                                                                                                                                      |

File sizes are inflated by indentation, and the `fields` parameter documented for Search-a-licious was not tested.

## Open Food Facts: Search-a-licious

From its OpenAPI spec:

- `GET https://search.openfoodfacts.org/search` takes `q`, `langs`, `page_size` (default 10), `page`, `fields`, `sort_by` and `facets`.
- `q` supports Lucene query syntax, and words the parser does not recognise are searched as full text.
- The `/search` endpoint has no fuzziness parameter. A `fuzziness` option exists only on `/autocomplete`, which searches taxonomies.
- The spec lists the software licence as AGPL-3.0. It does not say which licence covers the data it serves, and it does not state rate limits.

## Observations relevant to ADR-001 (not a decision)

- Only USDA returned generic reference entries (Foundation, SR Legacy, Survey) for a whole food and for a mixed dish, alongside branded products. Macros were on a per 100 g basis and present on 47 of 50 hits (`chicken breast`) and 50 of 50 hits (`lasagna`).
- Open Food Facts hits are packaged products with per 100 g macros. Search-a-licious was faster and more reliable than the legacy endpoint in this run.
- TheMealDB holds recipes without nutrition data. Computing macros for a recipe would need ingredient measures (free text) matched to another source's nutrition entries.
- No API visibly corrected the typo. USDA still returned many chicken breast entries, while Search-a-licious returned products spelled with the typo.

## Open questions

- Why the legacy Open Food Facts endpoint returned 503 for half our requests.
- Search-a-licious: rate limits, the licence on the data it serves, and reliability beyond 4 requests. Results beyond its first 10 were not read.
- Whether Lucene's fuzzy operator (`~`) in a Search-a-licious query would handle the misspelling. Not tested.
- USDA rate limit: the header showed 10 with `DEMO_KEY`, while the guide says 30/hour. A registered key was not tested.
- TheMealDB: whether the free key may be used by a publicly hosted course app. The terms do not say. This only matters if TheMealDB is chosen.

## Sources

- USDA FoodData Central API guide: https://fdc.nal.usda.gov/api-guide
- USDA Branded Foods documentation (values standardised per 100 g): https://fdc.nal.usda.gov/GBFPD_Documentation
- USDA FoodData Central data dictionary (nutrient amounts per 100 g): https://fdc.nal.usda.gov/portal-data/external/dataDictionary
- Open Food Facts API introduction: https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/
- Open Food Facts API tutorial: https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/tutorial-off-api/
- Open Food Facts API cheatsheet (search section): https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/ref-cheatsheet
- Search-a-licious API docs: https://search.openfoodfacts.org/docs
- TheMealDB API: https://www.themealdb.com/api.php
- TheMealDB terms of use: https://www.themealdb.com/terms_of_use.php
