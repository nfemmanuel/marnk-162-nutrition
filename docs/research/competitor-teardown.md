# Competitor teardown: where nutrition apps let people down

Ticket [NUT-13](https://marnk-162.atlassian.net/browse/NUT-13), part of the Discovery epic [NUT-12](https://marnk-162.atlassian.net/browse/NUT-12). Written by Alex Korablev. Data collected on 5 October 2026.

Before we ask people how they cook and eat, I wanted to know where the apps they already use let them down. That way we don't rebuild something that already exists, and our interview questions can go straight at real problems. I read the 1 and 2 star reviews of MyFitnessPal, Cronometer and Lose It!, plus Cal AI as the newer AI-first app, and sorted them by what people were unhappy about.

## The short version

These are the five complaints that come up most in 2,000 recent 1 and 2 star Google Play reviews (500 per app):

1. **The app breaks** (31% of reviews). Crashes, getting logged out, lost entries, totals that don't add up, and syncing with step counters and watches going wrong.
2. **Paying more for less** (23%). Basics like the barcode scanner moved behind a subscription, and prices keep going up.
3. **Updates that make logging slower** (19%). Redesigns that add taps and take away shortcuts people relied on.
4. **Ads that get in the way** (15%). Full-screen video ads, often with sound, that pop up while you're typing in a food.
5. **Surprise charges** (10%). Free trials that turn into a year's payment, with no obvious way to cancel.

Paywalls, prices and surprise charges together come up in 28% of reviews, almost as often as the app breaking. Just outside the top five is **numbers you can't trust** (8%), and that's where the AI app struggles most: 84 of Cal AI's 500 reviews say its AI estimates are wrong.

What this means for us:

- Most of the anger is about anything that slows down logging: a paid barcode scanner, an extra tap, an ad in the middle of typing. Fast logging is worth protecting above almost everything else.
- Budget users get the worst version of these apps (ads, a locked scanner, trial traps), and they notice. Being free, ad-free and upfront would already set us apart for budget students.
- AI photo logging is far from solved. If we use AI, people need to see what it guessed and be able to fix it in one tap.
- Syncing with step counters and watches is a steady source of bugs in every app, so it's probably not one for MVP 1.

## The four calorie trackers at a glance

US prices from the App Store and each app's own help pages on 5 October 2026. Prices change by country (from Europe, MyFitnessPal's website showed me €9.99 a month or €49.99 a year), so treat them as a rough guide.

| App | Paid plan | What's free | What's paid only |
|---|---|---|---|
| **MyFitnessPal**<br>4.4 on Google Play, 4.7 on the App Store | Premium $19.99/month or $79.99/year. Premium+ adds meal plans and grocery lists for more | Logging food and exercise, macros as percentages, your own recipes, connecting other apps. Shows ads | Barcode scanner (paid only since October 2022), photo Meal Scan, voice logging, macros in grams, goals by day or by meal, food timestamps, fasting, data export, no ads |
| **Cronometer**<br>4.5 / 4.8 | Gold $10.99/month or $59.99/year | Logging with 84 nutrients, custom macro and vitamin targets, **barcode scanner**, syncing devices. Shows ads | Photo and voice logging, fasting, recipe importer, repeat items, printable reports, AI coach, no ads |
| **Lose It!**<br>4.6 / 4.8 | Premium $79.99/year, yearly only. Lifetime $299.99 | Calorie budget, food database, weight loss plan. Shows ads | Barcode scanner, photo and voice logging, macro and nutrient goals, syncing watches and trackers, logging meals ahead, fasting, meal plans, no ads |
| **Cal AI**<br>4.6 / 4.8. Owned by MyFitnessPal since March 2026 | Plans from $2.99 to $29.99 in the App Store. Reviewers mostly mention about $30 a year. The 3-day trial needs a card | The setup quiz and a suggested calorie plan. Reviewers say you can't log anything without a trial or subscription | Everything else, including the photo scanning the app is built around |

## The five biggest complaints about calorie trackers

How many of each app's 500 reviews mention each complaint. One review can mention several.

| Complaint | MyFitnessPal | Cronometer | Lose It! | Cal AI | All 2,000 |
|---|---:|---:|---:|---:|---:|
| 1. The app breaks | 184 | 160 | 126 | 159 | 629 (31%) |
| 2. Paying more for less | 116 | 76 | 144 | 130 | 466 (23%) |
| 3. Updates that make logging slower | 208 | 40 | 104 | 26 | 378 (19%) |
| 4. Ads that get in the way | 27 | 190 | 83 | 4 | 304 (15%) |
| 5. Surprise charges | 19 | 9 | 78 | 86 | 192 (10%) |
| Next: numbers you can't trust | 23 | 18 | 27 | 88 | 156 (8%) |

The examples under each complaint are paraphrased in my own words, with where and when each review was posted.

### 1. The app breaks

Every app has this one, and it's the biggest complaint about Cal AI. Most of it is basic but serious:

- Getting logged out every time you open the app, or not being able to log back in. That's about 70 of MyFitnessPal's 161 bug reviews.
- The day's total not matching the foods logged (MyFitnessPal and Cal AI).
- Entries, streaks or whole histories disappearing.
- Syncing with other apps going wrong: steps counted twice or not at all, and workouts duplicated or lost. Health Connect (Android's shared health data) is the partner named most often.

What reviewers said:

- A MyFitnessPal user of 13 years woke up to find their whole history gone, and support never replied. (Google Play, 1★, 24 Sep 2026)
- Cal AI said one user had eaten 1,368 calories, but their logged foods added up to 1,133. (Google Play, 2★, 11 Mar 2026)
- Lose It! showed about 17,500 steps for a day when the user's phone counted about 10,000, even after reconnecting the sync. (Google Play, 1★, 28 Jun 2026)

For us: hardly anyone complains about missing features (70 of 2,000 reviews), but almost a third complain about broken basics. A small app that never loses an entry and always adds up correctly is already better than what these people have now.

### 2. Paying more for less

The anger is less about paying at all and more about losing things that used to be free.

- **MyFitnessPal:** 43 of its 93 paywall complaints mention the barcode scanner, four years after it went Premium-only. The newest wave, starting 1 October 2026, is about macros per meal, which the free diary no longer shows.
- **Lose It!:** reviewers lost carb and macro tracking, and some can't even set their own calorie budget without Premium. Premium is now $79.99 a year with no monthly option, and people who paid much less before say they won't renew.
- **Cronometer** keeps the barcode scanner free, which reviewers notice and like, but it has been moving things into Gold too: the full nutrient view (one reviewer dates this to 26 July 2026), meal timestamps and photo logging.
- **Cal AI** has no free version at all. After the setup quiz you have to start a trial with a card before you can log anything.

What reviewers said:

- A MyFitnessPal user of over ten years could live with the redesign, but not with losing the barcode scanner they'd always used, and is now looking for another app. (Google Play, 1★, 22 Sep 2026)
- A Lose It! user says setting their own calorie budget, something they'd done for years, suddenly needs Premium. (Google Play, 1★, 2 May 2026)
- A Cronometer reviewer calls it a rip-off to pay about £8 a month just to record what time they ate. (Google Play, 1★, 5 Jun 2026)

For us: budget users notice exactly which basics are locked, and the barcode scanner is the one they miss most. Barcode lookups can be free for us, since Open Food Facts has a free barcode API (Ransith is already comparing it in [NUT-22](https://marnk-162.atlassian.net/browse/NUT-22)).

### 3. Updates that make logging slower

This is mostly MyFitnessPal and Lose It!. Both changed their main screens in the last year, and long-time users really dislike it.

- MyFitnessPal launched a new "Today" screen in April 2026 ([news coverage](https://piunikaweb.com/2026/04/24/myfitnesspal-new-update-complaints/)). Complaints have come in waves after each update since then. The latest wave started on 1 October 2026, after the diary stopped showing carbs and macros for each meal, which matters to people with diabetes who count carbs per meal.
- What people miss: swiping between days, copying several foods at once, and seeing everything on one screen. A new shortcut that re-logs yesterday's meal is easy to tap by accident.
- Lose It!'s updates in November 2025 and January 2026 cut the nutrients shown at the top to three and removed the quick-add button.
- The App Store shows the same thing: 18 of 32 recent 1 and 2 star MyFitnessPal reviews there are about the redesign.

What reviewers said:

- A Lose It! lifetime member says every "improvement" over two months added three or four taps per meal, and asks for the old version back. (Google Play, 2★, 1 Feb 2026)
- A MyFitnessPal user who lost about 70 lb says the new design makes them click through so many screens that it's putting them off tracking. (Google Play, 1★, 7 Sep 2026)
- A type 1 diabetic says the latest MyFitnessPal update made it useless for counting carbs meal by meal, because it now only shows carbs for the whole day. (Google Play, 2★, 3 Oct 2026)

For us: count the taps for whatever people will do every day, and try changes on real users before shipping them. This is exactly where our guess that people will keep an app updated after they cook (guess 4 in the [interview guide](https://marnk-162.atlassian.net/wiki/spaces/SD/pages/9699331)) could go wrong. Any friction there and people stop.

### 4. Ads that get in the way

This is almost all Cronometer (190 of its 500 reviews, or 38%) and Lose It!.

- The ads are full-screen videos, often with sound, that appear in the middle of typing a food or right after scanning one. Some have fake or hidden close buttons, and some freeze the app.
- Several Cronometer reviewers noticed the ads are mild for the first few days and then ramp up, which feels like a bait and switch.
- Paying doesn't always help. Lose It! members still see upsells and partner promotions, including ones for GLP-1 weight loss drugs.
- The App Store shows the same thing: 10 of 18 recent 1 and 2 star Cronometer reviews there are about ads.

What reviewers said:

- A Cronometer user of over a decade says unskippable video ads after every ingredient finally drove them away. They'd pay a little just to remove ads, but not the full Gold price. (Google Play, 2★, 9 Feb 2026)
- Another Cronometer user saw only banner ads at first, then from day four got full-screen timed ads several times a day. (Google Play, 2★, 5 Jun 2026)
- A paying Lose It! user objects to being shown promotions for weight loss drugs at all. (Google Play, 2★, 23 Jun 2026)

For us: many of these reviewers say they'd accept a banner. What they won't accept is something that interrupts logging. We won't have ads, but the lesson is wider than ads. MyFitnessPal and Cal AI reviewers complain about streak and badge pop-ups for the same reason.

### 5. Surprise charges

This is mostly Cal AI and Lose It!, which both ask for a card at the end of a long setup quiz.

- The price only shows up after you've answered all the setup questions.
- The free trial turns into a full year's payment, sometimes even after people cancelled in time. Neither app lets you cancel from inside it: Cal AI's FAQ sends you to your phone's subscription settings, and Lose It! reviewers say it only works on the website or in Google Play.
- Double charges and refused refunds.
- Apple briefly pulled Cal AI from the App Store in April 2026 over its paywall, which showed a weekly price more prominently than the real charge, hid the auto-renewal behind a free trial toggle, and pushed a second offer at people who said no ([TechCrunch](https://techcrunch.com/2026/04/21/apples-cal-ai-crackdown-signals-its-still-policing-the-app-store/)).

What reviewers said:

- A Cal AI user cancelled inside the three-day trial and was still charged twice. (Google Play, 2★, 28 Mar 2025)
- A Lose It! user says nothing told them the trial could only be stopped on the website, so they paid for a subscription they didn't want yet, and were charged twice. (Google Play, 2★, 4 Oct 2026)
- A MyFitnessPal user went through the whole account setup before being asked to pick between $20 a month and $80 a year. (Google Play, 1★, 5 Sep 2026)

For us: being upfront costs nothing and earns trust. Let people try the app before asking them for anything.

### Next: numbers you can't trust

This is where Cal AI stands out, with 88 of its 500 reviews (84 of them about the AI itself).

- The AI names the wrong dish, gets the amount wrong even when it recognises the food, or says no food was found in a clear photo.
- The same meal can get very different numbers each time it's scanned.
- Home-cooked and mixed dishes do worst. Packaged food is easier, but even barcode and label scans go wrong.
- Fixing a bad estimate is often harder than typing the food in, and several people say they end up doing the AI's job for it.
- In the other three apps it's mostly wrong or duplicate entries in the food database.

What reviewers said:

- A Cal AI user tested it next to another tracker during the trial, and a 65 calorie side salad kept coming out at over 500. (Google Play, 2★, 13 Apr 2025)
- Another says logging the same meal several times gave calorie counts up to 400 apart, and the app couldn't tell pork from a bread roll. (Google Play, 2★, 18 Sep 2026)
- A third gets "no food detected" on about nine in ten photos. (Google Play, 2★, 29 Jul 2025)

Cal AI's own FAQ says its scans are about 80% accurate. For us: if we estimate food with AI, we should show what it guessed (the dish and the amount), call it an estimate, and make fixing it one tap. Verified data like USDA's is also more trustworthy than entries other users typed in, which matters for the data source decision in [NUT-21](https://marnk-162.atlassian.net/browse/NUT-21).

## Smaller things worth knowing

- **Long setup before you can do anything** (104 reviews, mostly Lose It! and Cal AI). Quizzes that take 15 minutes or 40 questions, some of them personal, then an email or a card before you see the app.
- **Can't find foods** (119 reviews). Search misses basic items, and local foods are missing outside the US. For example, Cronometer's French and Swiss coverage is thin. Worth checking for our city.
- **Unhealthy goals** (51 reviews). Cal AI gave one user a target of 736 calories a day for six months. Lose It! gave another macro goals that added up to over 400 calories more than their calorie budget.
- **Support doesn't answer** (90 reviews). Chatbots, ticket numbers and silence.

## Eleven more apps: shopping lists, pantry trackers and meal planners

In a second round I added 11 apps, to see whether keeping track of food at home is a real pain point and how the apps that plan meals and shopping hold up. I picked the biggest shared shopping list apps, two pantry trackers, five meal planning and recipe apps (including mise, a new app that is very close to our idea), and YAZIO, the calorie tracker most people use in Germany. I read their newest 1 and 2 star Google Play reviews the same way as in the first round, 3,870 reviews in total. For Bring! I used the German store, where most of its users are.

| App | What it does | Made by | Google Play installs | Rating (Play / App Store) |
|---|---|---|---:|---|
| **Bring!** | Shared shopping lists, recipes, supermarket offers | Bring! Labs, Switzerland | 10M+ | 4.1 / 4.8 |
| **Listonic** | Shared shopping lists | Listonic, Poland | 10M+ | 4.6 / 4.7 |
| **AnyList** | Shopping lists, recipes, meal planning calendar | Purple Cover, US | 1M+ | 4.8 / 4.9 |
| **KitchenPal** | Pantry with expiry dates and barcode scanning, lists, recipes | iCuisto, Singapore | 100k+ | 4.5 / 4.5 |
| **NoWaste** | Fridge, freezer and pantry lists with expiry reminders | KH Creations, Denmark | 50k+ | 2.8 / 4.2 |
| **Mealime** | Weekly meal plan that turns into a shopping list | Mealime, owned by the US supermarket group Albertsons | 1M+ | 4.6 / 4.8 |
| **Samsung Food** | Saved recipes, AI meal plans, shopping lists, a list of what's in your fridge | Samsung (formerly Whisk) | 1M+ | 4.5 / 4.8 |
| **Paprika** | Recipe manager with meal plans, pantry and lists, paid once | Hindsight Labs, US | 500k+ | 4.9 / 4.9 |
| **SuperCook** | Recipes from the ingredients you already have | SuperCook, US | 1M+ | 4.6 / 4.8 |
| **mise** | Weekly meal plans from your diet, budget, supermarket and what's at home | TEGS Labs, UK (launched June 2026) | 100k+ | 4.7 / 4.7 |
| **YAZIO** | Calorie and fasting tracker | YAZIO, Germany | 50M+ | 4.4 / 4.7 |

How many of each app's reviews mention each complaint, grouped the same way as for the calorie trackers. The biggest complaint for each app is in bold. The smaller apps get fewer bad reviews, so their samples reach further back (to 2017 for KitchenPal) and mix old and new problems.

| Complaint | Bring! | Listonic | AnyList | KitchenPal | NoWaste | Mealime | Samsung Food | Paprika | SuperCook | YAZIO | mise |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Reviews read | 500 | 500 | 360 | 271 | 29 | 500 | 475 | 296 | 304 | 500 | 135 |
| The app breaks | **39%** | 26% | 18% | **46%** | **52%** | 23% | **40%** | **37%** | **39%** | 18% | 7% |
| Paying more for less | 3% | 7% | 24% | 21% | 10% | 28% | 8% | 35% | 0% | 16% | **53%** |
| Updates that make it slower | 26% | 10% | 11% | 12% | 0% | 6% | 25% | 11% | 2% | **23%** | 0% |
| Ads and upsell | 11% | **36%** | 2% | 0% | 3% | 2% | 13% | 1% | 5% | **23%** | 1% |
| Surprise charges | 0% | 2% | 2% | 4% | 3% | 13% | 1% | 17% | 0% | 10% | 28% |
| Hard to start | 4% | 1% | **38%** | 2% | 14% | 1% | 5% | 0% | 1% | **23%** | 11% |
| Plans and recipes don't fit | 1% | 0% | 0% | 9% | 0% | **31%** | 6% | 0% | 30% | 1% | 27% |
| Sharing breaks | 5% | 8% | 2% | 3% | 0% | 2% | 4% | 9% | 0% | 1% | 1% |
| Keeping the pantry up to date | 0% | 0% | 0% | 7% | 14% | 0% | 0% | 1% | 3% | 0% | 0% |

### Shopping lists: Bring!, Listonic and AnyList

- **Sharing is why people use them, and it hurts when it breaks.** People share a list with a partner, family or housemates. The angry reviews are about invites that do nothing, edits that vanish or overwrite each other, and both people buying the same thing.
- **The business model ends up inside the list.** Ads are Listonic's biggest complaint, in over a third of its reviews. In both Listonic and Bring!, reviewers say sponsored brand products landed on their shared list or replaced what they typed, and some only noticed at home. Bring! users who pay for Premium still see "offers". Listonic also added an AI feature in March 2026 that can't be turned off (50 reviews object to it being there at all) and a consent screen listing hundreds of data partners.
- **Supermarket offers matter.** The biggest wave of Bring! complaints in our sample came in late 2024, when the Aldi, Lidl, REWE and EDEKA brochures disappeared from the app. People use it to plan their shop around deals.
- **AnyList's biggest complaint is having to make an account before trying it** (38% of its reviews), often together with worries about what happens to their email address.
- **Amounts don't add up.** One Bring! reviewer put two egg recipes on the list and got two separate amounts in a note instead of one total. For batch cooking, that total is the whole point.
- **Hardly anyone asks these apps to track what's at home.** A few want a permanent list of staples, quantities or expiry dates.

What reviewers said:

- A Listonic user says the app put about 20 brand-name products on the list they share with their partner, more than once. (Google Play, 1★, 20 Feb 2025)
- A Bring! user paid almost €5 for a lotion they thought their partner had added. At home they spotted a small ad marker next to it. (Google Play, German store, 1★, 29 Nov 2025)
- A Bring! user says the Aldi, Lidl and REWE offers vanished without explanation, and without them the app is much less useful. (Google Play, German store, 1★, 18 Oct 2024)

### Pantry trackers: is keeping track of food a pain point?

- **Dedicated pantry apps are small.** KitchenPal has over 100,000 Android installs and NoWaste over 50,000, against over 10 million each for Bring! and Listonic. NoWaste is rated 2.8 on Google Play.
- **The inventory usually dies at the start, not later.** Getting a kitchen into the app takes hours of scanning. Barcodes often aren't recognised, free versions cap how many items you can add, and some people lost everything they'd entered.
- **Nothing updates by itself.** Food isn't taken off when you cook, and in KitchenPal, subtracting what you've used or moving bought items from the shopping list into the pantry are paid features.
- **SuperCook, the "what can I make with what I have" app, shows the same thing from the other side.** People don't want to enter their whole pantry and would rather start from two or three ingredients, and a common complaint is that its recipes still need things you don't have.

What reviewers said:

- A KitchenPal user says almost everything is now paid, including adding items by hand and moving them from the shopping cart into the pantry, which makes the app useless to them. (Google Play, 2★, 29 Aug 2026)
- A NoWaste user chose the UK database and found it recognised one of the 29 items in their fridge. (Google Play, 1★, 8 Aug 2021)
- A SuperCook user hoped to enter two or three main ingredients, but the app wanted everything in the pantry, staples included, which took longer than it was worth. (Google Play, 2★, 11 Jun 2024)

For us: the reviews show that keeping an inventory is a chore people drop, but they can't tell us whether not knowing what's at home stops people from cooking. That's guess 3 in the [interview guide](https://marnk-162.atlassian.net/wiki/spaces/SD/pages/9699331), so it's worth asking. If we track what's at home, it should come out of things people already do, like ticking off the shopping list or cooking a recipe, and never be a setup step.

### Meal planners and recipe apps: Mealime, Samsung Food, Paprika, SuperCook and mise

- **Plans don't fit how people actually cook.** It's the biggest complaint about Mealime (31%) and close to the top for SuperCook (30%) and mise (27%). People can't cook for one, diet and allergy settings get ignored (mise and Samsung Food's AI planner), and recipes repeat after a week or two (mise). Reviewers say mise plans about four dinners no matter how many days they ask for.
- **The shopping list from the plan goes wrong.** Mealime's lists have left out ingredients or not updated when the plan changed. mise's price estimates can be off by up to double, and its lists include things the chosen supermarket doesn't sell.
- **Recipe import is the big time saver, and it breaks.** In Samsung Food, saving a recipe from a website often fails or leaves out the steps, and import problems are one of the most common complaints about Paprika.
- **These apps change under their users.** Mealime closes on 21 October 2026 and moves into the apps of a US supermarket chain, and all personal data will be deleted ([Mealime's announcement](https://www.mealime.com/closing)). Samsung Food switched sign-in to Samsung accounts in 2026, and some people lost access to their saved recipes. Paprika charges again for each device and each new major version.
- **mise, the newest app and the closest to our idea, has a hard paywall straight after a long setup quiz.** Paying is its biggest complaint (53%), then surprise charges (28%), and reviewers mostly quit before they get to try planning around what's at home.

What reviewers said:

- A mise user asked for a seven-day plan and got four dinners. (Google Play, 1★, 10 Aug 2026)
- Another says mise estimated a week's shop at about 66, and the same list at the same store came to about 127. (Google Play, 2★, 2 Sep 2026)
- A Samsung Food user says its planner keeps suggesting breakfasts that take an hour on workdays and ignores their weekly budget. (Google Play, 1★, 20 Jul 2026)
- A long-time Mealime user says the replacement app needs a supermarket that doesn't serve their area, so they can't use it. (Google Play, 1★, 6 Sep 2026)

### YAZIO, the calorie tracker most people use in Germany

- **It has MyFitnessPal's problems plus a few of its own.** Its biggest complaints are a setup quiz of 20 to 40 minutes that comes back after a few days away (23% of reviews), unskippable video ads in the free version plus constant pushing of PRO (23%), and updates that took away things people used (23%). In July 2026, Quick Add was replaced by AI text entry.
- **AI estimates are often off** (10% of reviews), and 8% object to the AI being there at all.
- **A few reviewers say logging food for the next day now needs PRO**, which gets in the way of meal prep.

What reviewers said:

- A YAZIO user checked their screen time afterwards: setup took 40 minutes. (Google Play, 2★, 6 Aug 2026)
- Another says each entry in the free version meant two video ads and then four screens pushing PRO. (Google Play, 1★, 17 Jun 2026)
- Another says the July update took away the quick way to log a meal with your own name and nutrients. (Google Play, 1★, 30 Jul 2026)

## Pain points by persona

How the competitors try to help our two personas, and where it goes wrong according to their reviews.

### Time-constrained users

Most of these apps promise to save time. The reviews say the time actually goes on setup and entering things, not on cooking.

| What saves time | Who has it | What goes wrong |
|---|---|---|
| Fast logging: barcode scanner, photo and voice AI, quick add, repeating yesterday's meal | MyFitnessPal, Lose It!, Cronometer, YAZIO, Cal AI | The scanner is often paid (MyFitnessPal, Lose It!). AI estimates are often wrong (Cal AI, YAZIO). Updates removed shortcuts (Lose It!'s quick add in January 2026, YAZIO's Quick Add in July 2026) or added taps (MyFitnessPal's redesign) |
| A weekly plan that turns into a shopping list | Mealime, mise, Samsung Food, AnyList (paid), MyFitnessPal Premium+ | Plans don't fit real life: no cooking for one, diets ignored, the same recipes again. Lists miss ingredients, mise's budget estimates are far off, and the best parts are paid |
| Saving recipes from websites straight into a plan or list | AnyList, Paprika, Samsung Food, Bring! | Imports fail or come out garbled, the steps go missing, and AnyList and Mealime limit free imports |
| Adding to the list by voice | Bring!, AnyList | Google Assistant support ended in 2023 and an Alexa change broke adding by voice in 2024 |
| Getting started quickly | Almost none | Long quizzes (YAZIO, Lose It!, mise), an account before you can try anything (AnyList), or a paywall before you can try anything (Cal AI, mise) |

For us: the time to beat is setup and entry. A first plan and shopping list within a minute or two, without an account wall or a long quiz, would already be faster than most of these apps. Once people rely on a shortcut, keep it.

### Batch cooks and inventory managers

| What they need | Who has it | What goes wrong |
|---|---|---|
| A shared shopping list | Bring!, Listonic, AnyList, KitchenPal | Edits get lost or overwritten between partners, sponsored items turn up in shared lists (Listonic, Bring!), and in Paprika each person has to buy the app |
| Cooking several portions and planning a week at a time | Paprika (menus, monthly calendar), AnyList (calendar), Mealime, mise | Servings come in fixed sizes, plans come out shorter than asked for (mise), there's no planning for leftovers or cooking ahead, amounts from several recipes aren't added up (Bring!), and a few YAZIO reviewers say logging food ahead now needs PRO |
| Knowing what's at home, with expiry dates | KitchenPal, NoWaste, Paprika, Samsung Food (paid) | Getting everything in takes hours and barcodes often fail, nothing comes off when you cook, and there are caps and paywalls on the basics |
| Recipes from what you already have | SuperCook, KitchenPal, mise, Samsung Food (paid) | Suggestions still need ingredients you don't have, people won't enter a whole pantry, and food bought for one meal isn't used up in later ones (mise) |
| Keeping track of a batch you've cooked | Not really: pantry apps track ingredients, not cooked portions | KitchenPal reviewers ask to track frozen ready meals and how much is left |

For us: nobody handles "cook once, eat four times" well. That means adding up amounts, scaling a recipe up, and keeping track of the portions left, which is exactly what the batch cooking persona needs. Knowing what's at home should come for free from the shopping list and the recipes people cook, not from typing in a pantry.

## Questions this suggests for the interviews

These ask about what people have done, not what they would do, and don't pitch anything (the same rules as the interview guide):

- "Have you ever used an app to track food or plan meals? Tell me about the last time. What made you stop?" (tests guess 4, keeping an app updated)
- "The last time you logged or planned a meal on your phone, what slowed you down?"
- "Have you ever paid for a food or fitness app? What made you pay, or not?" (tests guess 1, cost first)
- "Tell me about the last meal you cooked at home. If you had to log it, how would you work out what was in it?"
- "Has an app ever surprised you with a charge, an ad or a change you didn't ask for? What did you do?"

## How I did it

- **Apps.** MyFitnessPal, Cronometer and Lose It! from the ticket, plus Cal AI as the AI-first app. Cal AI is the best-known app built around photo logging (about 370,000 App Store ratings), and MyFitnessPal bought it in [March 2026](https://news.myfitnesspal.com/myfitnesspal-expands-its-position-as-the-leading-player-in-digital-nutrition-tracking-with-cal-ai-acquisition/).
- **Google Play.** The 500 newest 1 and 2 star reviews for each app (250 of each rating) from the US store, collected on 5 October 2026. They cover different stretches of time because some apps get far more bad reviews than others. MyFitnessPal's 500 all came from the last three and a half months, while Cronometer's and Cal AI's go back about eighteen months.
- **App Store.** Apple's public review feed mostly came back empty, so I only got 52 recent 1 and 2 star reviews (32 for MyFitnessPal from Canada, 18 for Cronometer from Australia and 2 for Cal AI from its US page). I used them as a cross-check, and they point the same way as Google Play.
- **Sorting.** I wrote a list of 19 complaint types (in the appendix) and gave every review one or more of them. I used an AI assistant to read and tag all 2,000 reviews against that list. A second, separate tagging pass on a random 40 reviews agreed with it: at least one shared tag on all 40, and exactly the same tags on 36.
- **Prices and paywalls.** From each app's US App Store listing and its own help pages, checked on 5 October 2026.

Limits to keep in mind:

- These are the unhappiest users on purpose. All four apps average 4.4 to 4.8 stars, and 1 and 2 star ratings are only 5 to 10% of each app's ratings on Google Play.
- It's mostly Android users in the US writing in English.
- Reddit isn't included.
- 112 of Cal AI's reviews don't name a specific problem (many just say "nice" under a 1 or 2 star rating), so its other numbers are a bit lower than they would be otherwise.

## Sources

- Google Play: [MyFitnessPal](https://play.google.com/store/apps/details?id=com.myfitnesspal.android), [Cronometer](https://play.google.com/store/apps/details?id=com.cronometer.android.gold), [Lose It!](https://play.google.com/store/apps/details?id=com.fitnow.loseit), [Cal AI](https://play.google.com/store/apps/details?id=com.viraldevelopment.calai)
- App Store: [MyFitnessPal](https://apps.apple.com/us/app/id341232718), [Cronometer](https://apps.apple.com/us/app/id1145935738), [Lose It!](https://apps.apple.com/us/app/id297368629), [Cal AI](https://apps.apple.com/us/app/id6480417616)
- MyFitnessPal Help Center, [The difference between Free, Premium, and Premium+](https://support.myfitnesspal.com/hc/en-us/articles/34889191368077-The-difference-between-Free-Premium-and-Premium)
- Lose It! Help Center, [Membership Tiers & Pricing](https://loseit.zendesk.com/hc/en-us/articles/51906523474708-Lose-It-Membership-Tiers-Pricing)
- Cronometer, [Gold plans](https://cronometer.com/gold/)
- Cal AI, [website and FAQ](https://www.calai.app/)
- Droid Life, [MyFitnessPal puts barcode scanner behind Premium paywall](https://www.droid-life.com/2022/08/24/myfitnesspal-puts-barcode-scanner-behind-premium-paywall/) (24 Aug 2022)
- MyFitnessPal, [Cal AI acquisition announcement](https://news.myfitnesspal.com/myfitnesspal-expands-its-position-as-the-leading-player-in-digital-nutrition-tracking-with-cal-ai-acquisition/) (2 Mar 2026)
- TechCrunch, [Apple's Cal AI crackdown signals it's still policing the App Store](https://techcrunch.com/2026/04/21/apples-cal-ai-crackdown-signals-its-still-policing-the-app-store/) (21 Apr 2026)
- PiunikaWeb, [MyFitnessPal users complain new Today tab update makes the app harder to use](https://piunikaweb.com/2026/04/24/myfitnesspal-new-update-complaints/) (24 Apr 2026)
- Google Play, second round: [Bring!](https://play.google.com/store/apps/details?id=ch.publisheria.bring), [Listonic](https://play.google.com/store/apps/details?id=com.l), [AnyList](https://play.google.com/store/apps/details?id=com.purplecover.anylist), [KitchenPal](https://play.google.com/store/apps/details?id=fr.icuisto.icuisto), [NoWaste](https://play.google.com/store/apps/details?id=com.khcreations.nowaste), [Mealime](https://play.google.com/store/apps/details?id=com.mealime), [Samsung Food](https://play.google.com/store/apps/details?id=com.foodient.whisk), [Paprika](https://play.google.com/store/apps/details?id=com.hindsightlabs.paprika.android.v3), [SuperCook](https://play.google.com/store/apps/details?id=com.supercook.app), [mise](https://play.google.com/store/apps/details?id=com.gregorytaylor.shopping), [YAZIO](https://play.google.com/store/apps/details?id=com.yazio.android)
- App Store, second round: [Bring!](https://apps.apple.com/us/app/id580669177), [Listonic](https://apps.apple.com/us/app/id331302745), [AnyList](https://apps.apple.com/us/app/id522167641), [KitchenPal](https://apps.apple.com/us/app/id1084982489), [NoWaste](https://apps.apple.com/us/app/id926211004), [Mealime](https://apps.apple.com/us/app/id1079999103), [Samsung Food](https://apps.apple.com/us/app/id1133637674), [Paprika](https://apps.apple.com/us/app/id1303222868), [SuperCook](https://apps.apple.com/us/app/id1477747816), [mise](https://apps.apple.com/us/app/id6777471316), [YAZIO](https://apps.apple.com/us/app/id946099227)
- Mealime, [Mealime is closing](https://www.mealime.com/closing)

## Appendix: complaint types and counts

### First round: calorie trackers

Google Play reviews per app (out of 500 each). The five complaints above group these: "the app breaks" is bugs plus syncing, "paying more for less" is paywall plus price, "updates that make logging slower" is redesign plus logging effort, "ads that get in the way" is ads plus upsell, and "numbers you can't trust" is food data plus AI accuracy.

| Complaint type | What it covers | MyFitnessPal | Cronometer | Lose It! | Cal AI | Total |
|---|---|---:|---:|---:|---:|---:|
| Bugs | Crashes, freezing, logouts, lost data, wrong totals | 161 | 140 | 102 | 152 | 555 |
| Paywall | Basics locked, free version too limited, no free version | 93 | 41 | 112 | 116 | 362 |
| Redesign | An update made the app worse or removed something | 191 | 19 | 93 | 4 | 307 |
| Ads | Intrusive third-party ads | 16 | 187 | 64 | 1 | 268 |
| Billing | Unexpected charges, trial traps, can't cancel, no refund | 19 | 9 | 78 | 86 | 192 |
| Other | No specific reason given, or nothing else fits | 14 | 31 | 18 | 112 | 175 |
| Logging effort | Logging is slow, fiddly or takes too many taps | 67 | 22 | 25 | 22 | 136 |
| Price | Too expensive, price went up, no cheaper option | 29 | 42 | 37 | 18 | 126 |
| Search | Can't find foods, local foods missing | 31 | 59 | 15 | 14 | 119 |
| Onboarding | Long setup quiz or forced sign-up | 6 | 11 | 65 | 22 | 104 |
| AI accuracy | Photo, voice or label AI gets it wrong | 4 | 3 | 8 | 84 | 99 |
| Sync | Problems with Health Connect, Fitbit, Garmin and others | 29 | 29 | 25 | 8 | 91 |
| Support | Support doesn't answer or doesn't help | 23 | 14 | 16 | 37 | 90 |
| Missing feature | Wants something the app never had | 18 | 20 | 15 | 17 | 70 |
| Food data | Wrong or duplicate database entries | 19 | 15 | 20 | 11 | 65 |
| Goals | Calorie or macro targets wrong or unhealthy | 10 | 8 | 14 | 19 | 51 |
| Upsell | Constant pushing of the app's own premium | 11 | 6 | 19 | 3 | 39 |
| Privacy | Data sharing, spam, breaches | 12 | 6 | 12 | 5 | 35 |
| Unwanted AI | Doesn't want AI in the app at all | 4 | 3 | 1 | 0 | 8 |

### Second round: lists, pantry trackers and meal planners

Google Play reviews per app, with the same complaint types plus three new ones for these apps: sharing (shared lists or plans don't sync between people), upkeep (keeping track of what's at home takes too much work) and content (recipes or meal plans don't suit people). Bring! reviews are from the German store.

| Complaint type | Bring! | Listonic | AnyList | KitchenPal | NoWaste | Mealime | Samsung Food | Paprika | SuperCook | YAZIO | mise | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Reviews read | 500 | 500 | 360 | 271 | 29 | 500 | 475 | 296 | 304 | 500 | 135 | 3,870 |
| Bugs | 138 | 126 | 33 | 124 | 15 | 104 | 175 | 87 | 116 | 74 | 10 | 1,002 |
| Paywall | 3 | 24 | 70 | 53 | 3 | 114 | 31 | 32 | 0 | 65 | 57 | 452 |
| Redesign | 76 | 42 | 22 | 2 | 0 | 17 | 98 | 15 | 2 | 70 | 0 | 344 |
| Ads | 55 | 174 | 1 | 1 | 0 | 4 | 56 | 2 | 14 | 71 | 0 | 378 |
| Billing | 0 | 10 | 6 | 11 | 1 | 65 | 5 | 50 | 0 | 51 | 38 | 237 |
| Other | 32 | 23 | 20 | 12 | 4 | 12 | 37 | 20 | 28 | 21 | 5 | 214 |
| Logging effort | 61 | 14 | 17 | 30 | 0 | 13 | 26 | 21 | 5 | 67 | 0 | 254 |
| Price | 11 | 13 | 28 | 6 | 1 | 48 | 12 | 78 | 0 | 19 | 21 | 237 |
| Search | 4 | 9 | 1 | 46 | 1 | 14 | 39 | 3 | 52 | 25 | 0 | 194 |
| Onboarding | 20 | 3 | 136 | 5 | 4 | 6 | 25 | 0 | 2 | 115 | 15 | 331 |
| AI accuracy | 1 | 1 | 0 | 4 | 0 | 0 | 14 | 0 | 9 | 52 | 2 | 83 |
| Sync | 61 | 8 | 32 | 0 | 0 | 12 | 18 | 26 | 2 | 19 | 0 | 178 |
| Support | 17 | 23 | 12 | 7 | 0 | 14 | 10 | 53 | 3 | 17 | 2 | 158 |
| Missing feature | 114 | 29 | 31 | 29 | 4 | 79 | 81 | 37 | 34 | 72 | 21 | 531 |
| Food data | 2 | 2 | 1 | 38 | 4 | 2 | 7 | 0 | 6 | 5 | 10 | 77 |
| Goals | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 0 | 0 | 10 | 0 | 20 |
| Upsell | 1 | 10 | 7 | 0 | 1 | 6 | 5 | 0 | 0 | 74 | 1 | 105 |
| Privacy | 26 | 58 | 22 | 14 | 0 | 18 | 9 | 0 | 5 | 7 | 1 | 160 |
| Unwanted AI | 0 | 50 | 0 | 0 | 0 | 0 | 3 | 1 | 0 | 39 | 9 | 102 |
| Sharing (new) | 23 | 39 | 8 | 8 | 0 | 8 | 20 | 26 | 1 | 4 | 1 | 138 |
| Upkeep (new) | 0 | 0 | 0 | 20 | 4 | 0 | 0 | 4 | 8 | 0 | 0 | 36 |
| Content (new) | 3 | 0 | 0 | 24 | 0 | 153 | 30 | 0 | 92 | 3 | 36 | 341 |
