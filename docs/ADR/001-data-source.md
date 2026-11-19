# ADR-001: Nutrition and recipe data sources

**Status:** Proposed. Awaiting team agreement and a reviewed PR.

**Date:** 2026-11-16

**Ticket:** [NUT-24](https://marnk-162.atlassian.net/browse/NUT-24), under [NUT-21](https://marnk-162.atlassian.net/browse/NUT-21). GitHub: [#13](https://github.com/nfemmanuel/marnk-162-nutrition/issues/13).

## Context

Our app needs recipes to suggest meals from ingredients people have, and nutrition data to estimate their macros. We also plan to let people add their own recipes. Those recipes may contain ingredients outside our starter dataset, so choosing a recipe API does not settle how nutrition will work for every recipe.

[ADR-000](000-stack-and-workflow.md) requires a simple local deployment and no third-party signup to run the app. Publishing a private API key in the repository would conflict with USDA's key policy. We therefore need to decide both where data originates and what data the app actually needs at runtime.

### Work already completed

The following is merged into `main`, checked at commit [`e9eae20`](https://github.com/nfemmanuel/marnk-162-nutrition/commit/e9eae204eba7a7b4d626ee9237654efcd726e962):

- **NUT-22, [PR #14](https://github.com/nfemmanuel/marnk-162-nutrition/pull/14):** real calls to USDA FoodData Central, Open Food Facts and TheMealDB. The [comparison](../../spikes/nutrition_apis/api_comparison.md) records coverage, response shapes, timings, messy search input, limits and licences. It tested four queries on October 8, 2026, on one machine/network; it is evidence for this choice, not a performance benchmark.
- **NUT-27, [PR #34](https://github.com/nfemmanuel/marnk-162-nutrition/pull/34):** TheMealDB importer and `seed-recipes`. It validates ingredients and amounts, selects across multiple search terms and avoids importing the same source record twice. It stores recipe names, ingredients, measures and source references. It does **not** store instructions, photos or servings.
- **NUT-28, [PR #36](https://github.com/nfemmanuel/marnk-162-nutrition/pull/36):** bundled CSVs containing 186 USDA SR Legacy foods (April 2018) and 318 ingredient names, plus local macro calculation. The [data notes](../../app_flask/nutrition/data/README.md) document approximations and report complete totals for only 4 of the 50 starter recipes; many piece, can and packet quantities cannot yet be converted to grams.

The nutrition seed already works from local files. The recipe seed currently makes network calls. User ownership and upload fields are not yet implemented.

## Decision

### 1. Use USDA for nutrition, TheMealDB for starter recipes, and users for their own recipes

| Source | Role | Evidence and limits |
| --- | --- | --- |
| **USDA FoodData Central** | Primary nutrition reference, stored locally | Best fit in our spike for generic ingredients and per-100 g macros. Search returns `foods` containing descriptions and nutrient lists; energy units need checking. Data is public domain under CC0. It does not supply cooking recipes. |
| **TheMealDB** | Starter recipe catalogue, imported through its official API | Returns `meals` or `null`, with numbered ingredient/measure pairs and free-text amounts. It supplies recipes but no nutrition. Keep its format inside the importer. |
| **User submissions** | Recipes beyond the starter catalogue | Store in our database, with ownership and the same ingredient/nutrition workflow. Users do not need a TheMealDB account or identifier. |
| **Open Food Facts** | Deferred; reconsider for packaged-food or barcode features | Useful packaged-product coverage, but incomplete nutrition on some results. The spike's legacy search failed on 4 of 8 calls; Search-a-licious succeeded on 4 of 4. Adding another provider is unnecessary for the initial generic-ingredient workflow. |

The detailed responses and search results remain in the spike rather than being repeated here. No tested provider gave us a dependable spelling-correction feature: USDA returned useful results for `chiken breast`, but that does not justify automatically accepting the first result. TheMealDB name search is also different from its ingredient filter.

The [USDA guide](https://fdc.nal.usda.gov/api-guide/) permits reuse of the data and requires private keys to stay private. TheMealDB's [API page](https://www.themealdb.com/api.php) permits test key `1` for development and education. Its [terms](https://www.themealdb.com/terms_of_use.php) permit copying and modification of official API output, prohibit website scraping and API resale, and require permission or another legal basis for third-party content. Preserve source attribution and notices. We will initially retain the factual fields our importer already stores; instructions and images need a separate rights check before inclusion.

### 2. Ship data so normal use needs no private API key

Keep the bundled USDA files and add a versioned snapshot of the validated starter recipes. The default setup will seed both from local files. Recipe search, matching, macro calculation and saving user recipes will read our database. Refreshing external data will be a separate maintainer operation, never a requirement for startup or each user request.

For each distributed dataset, record its source, release or retrieval date, reuse terms and any transformations. USDA values retain their `fdc_id`; imported recipes retain `(source, source_id)` and a source URL. Do not silently replace a release's recipe list with whatever the API returns that day.

| Credential | How we handle it |
| --- | --- |
| USDA registered key | **Not shipped or required.** Maintainers can use downloadable USDA data without an API key. If a future optional API refresh is added, read `USDA_API_KEY` on the backend from an ignored environment file or deployment secret; never put it in git, container images, browser responses or logs. |
| USDA `DEMO_KEY` | Spike/exploration only. Not a runtime dependency or the default source for user uploads. |
| TheMealDB test key `1` | A public educational identifier already used by the importer, not a private secret. Normal operation will use the snapshot. |
| Open Food Facts | Reads need no key, but require an identifying User-Agent. No runtime integration is selected. |

This satisfies the course requirement by requiring no private third-party key for supported app features. An environment-variable placeholder alone would not satisfy it if a user still had to register before the app worked.

Limits remain relevant to refresh tooling: USDA documents 1,000 requests/hour/IP for registered keys and 30/hour plus 50/day/IP for `DEMO_KEY`; our demo-key spike observed a lower header limit of 10. Open Food Facts documents 10 searches/minute/IP and 15 product reads/minute/IP for its listed endpoints; do not assume these also describe Search-a-licious. We found no numeric free-tier limit on the TheMealDB pages reviewed. Refreshes must use bounded requests and handle failures without discarding the last usable data.

TheMealDB's public-hosted course-app permission remains unclear in the reviewed pages; app-store release requires a supporter subscription. Before wider public distribution, confirm that the intended use and redistribution are covered, or replace the starter recipes with team-authored or otherwise licensed recipes. Local storage solves availability, not licensing.

### 3. Support user recipes without making an API call for every ingredient

Extend the existing `Recipe`, `RecipeIngredient`, `Food` and `Ingredient` models rather than creating a second recipe system. The implementation must support these rules:

| Data | Required behaviour |
| --- | --- |
| Recipe identity and ownership | Use our local recipe ID. External IDs/URLs are optional for user recipes. User recipes have an owner and are private by default; another user's search cannot expose them. Import deduplication remains based on source identity, not a globally unique recipe title. |
| Recipe content | Accept user-authored instructions and an optional positive serving count. Require users to have the rights to submitted text/images. Keep external source credit where applicable. |
| Ingredient entry | Preserve the entered name and amount. Store an optional confirmed food reference and gram amount separately, with any conversion or approximation recorded. There is no TheMealDB-style 20-ingredient limit in our own model. |
| Shared nutrition | Store each reference food's per-100 g values once. Use reviewed aliases for common names; a user's recipe-specific substitution must not silently change the shared mapping for everyone. |
| Unresolved ingredients | Let users select a suitable local food or leave it unmatched. Save the recipe either way and report what is missing. Unknown is different from an ingredient deliberately omitted under our documented approximation policy. |

The current 186-food subset covers the starter mappings, not arbitrary user recipes. When uploads are implemented, expand the bundled generic-food catalogue from USDA downloads as needed. Search locally, normalize case and whitespace, and offer candidates for ambiguous names. A raw food, a cooked food and a branded product are not interchangeable just because their names overlap.

Use the same calculation path for seeded and user recipes: multiply each mapped food's per-100 g nutrients by the ingredient's grams divided by 100, then sum. Divide by servings only when servings are known. Missing mappings or weights produce a clearly labelled partial estimate and a list of omitted ingredients, never an apparently complete total with unknowns treated as zero.

The current water-density conversion for cups/spoons and blanket spice exclusions are documented MVP approximations. They must remain visible in estimates; a complete calculation can still be approximate. Prefer food-specific portion weights or user-entered grams as these are added.

Normal traffic will therefore grow against our database rather than provider quotas. Keep SQLite and SQLAlchemy as ADR-000 specifies; use indexed lookups and paginated results as the catalogue grows. Reconsider database hosting when measured concurrent writes require it. User recipe edits or future catalogue refreshes must update records without deleting user content: the current destructive nutrition reseed is not suitable once user records reference those foods.

### 4. Treat website imports and recipe rights separately

Under the [U.S. Copyright Office's Circular 33](https://www.copyright.gov/circs/circ33.pdf), ingredient facts and simple procedures are generally outside copyright protection, while creative explanations, photographs and other original expression can be protected. This does not establish a general right to scrape a site or republish its catalogue. Giving credit alone is not a replacement for permission.

Policies reviewed on November 10, 2026:

| Site | Finding | Decision for NUT |
| --- | --- | --- |
| [Tastes Better From Scratch](https://tastesbetterfromscratch.com/privacy-policy/) | Its policy expressly requires written permission for use in developing, training or operating AI/ML systems. We found no general recipe-database import permission in that policy. | Link to the original; no automated recipe import or AI processing selected. |
| [Just One Cookbook](https://www.justonecookbook.com/content-permissions/) | Lists CC BY-NC-SA 4.0 and specific recipe-sharing conditions; photographs require permission. | Any integration needs a review of those conditions for our use. No blanket importer selected. |
| [Eatwell101](https://www.eatwell101.com/photo-and-recipe-sharing-policy) | Directs recipe sharing to links; restricts republication and systematic collection for recipe databases/apps without an applicable legal basis or permission. | Link to the original; no catalogue scraping selected. |

NUT-23 links to `betterfromscratch.com`, which could not be retrieved during this check. Tastes Better From Scratch is a separate domain, checked as a possible intended reference; its policy must not be attributed to the unavailable domain. Verify the intended site before marking that part of NUT-23 complete.

For the initial app, a pasted external recipe URL is a **bookmark/source reference**, not an instruction to scrape. A user choosing a URL does not itself grant NUT reuse rights. Likewise, [Schema.org Recipe](https://schema.org/Recipe) describes structured fields such as ingredients, instructions and yield; exposing those fields is not a content licence.

Later automated imports may be added for specific sources whose access and reuse terms cover the feature. Import only permitted fields, retain attribution and permission evidence, and keep private imports out of the shared catalogue unless redistribution is allowed. Otherwise, users can enter their own recipe or follow the original link. A general “import any recipe URL” feature is deferred.

### 5. Keep price data separate from nutrition

No tested source establishes reliable current local grocery prices for our app. Cost per serving and protein per dollar therefore remain dependent on a separate price-data feature, such as user-entered price, currency, package quantity and date. Missing prices or servings mean the relevant result is unavailable. Nutrition values must not be presented as evidence of cost.

## Alternatives considered

- **Live USDA calls for every search or upload.** Better access to new foods, but introduces private-key distribution, shared quotas and network failures into ordinary use. Prefer local data and optional maintainer refreshes.
- **Open Food Facts as the primary nutrition source.** Stronger fit for packaged-product/barcode features. Its ODbL database, Database Contents License and image share-alike terms add reuse obligations to assess before combining or redistributing datasets; its search reliability and completeness in our small spike were weaker for our immediate needs. This is deferral, not a claim that its licence prohibits our app. See its [API documentation](https://openfoodfacts.github.io/openfoodfacts-server/api/) and [licence guidance](https://openfoodfacts.github.io/openfoodfacts-server/api/tutorials/license-be-on-the-legal-side/).
- **TheMealDB as the complete data backend.** Does not provide macros and should not determine how our users' recipes are stored. Use it to populate the starter catalogue.
- **Only user-authored recipes.** Avoids dependency on a third-party starter catalogue but leaves a fresh installation empty. Keep it as the fallback if starter-data rights cannot be confirmed.
- **A paid all-in-one API or unrestricted website scraping.** Adds cost, credential or permission dependencies that we have not justified for the course project. No such source is selected.

## Consequences

- A fresh installation will have useful data without third-party signup, and ordinary use can continue through API outages. The local recipe snapshot and default setup changes still need implementation.
- We own the work of maintaining ingredient mappings, useful quantity conversions and source records. The current small catalogue and incomplete totals are real limits, especially for user recipes.
- User submissions can grow independently of TheMealDB, while sharing the existing nutrition calculation code. Ownership, schema changes and safe incremental seeding must land before real user recipes are stored.
- Public sharing, wider distribution and new external sources require the relevant reuse conditions to be checked. Our existing source selections do not grant permission to copy arbitrary recipe sites.
- Accepting this ADR records the architecture, not completion of every follow-up. Before closing NUT-24, record team agreement, change Status to Accepted with the agreement date, and merge `docs/adr/001-data-source.md` through a reviewed PR for [#13](https://github.com/nfemmanuel/marnk-162-nutrition/issues/13). The PR should say `Closes #13`.
