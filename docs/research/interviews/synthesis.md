# Interview synthesis, round 1

Ticket NUT-15. Evidence is in the [summaries and grid](README.md) and the [raw notes](raw/). Participants appear as P1 to P7 only.

**Main finding:** people cook from what they have and repeat a few known recipes, but none of them keeps a tracker updated, and time or effort drives eating out more than cost.
**What we change:** build around the ingredients people already have, with no logging and calories hidden by default, and add saved recipes after "Cook from what you already have".

## The five guesses

**1. Cost comes before protein or calories: mixed.**
Cost came first for P3 ("I obviously look at the price first") and P5. Time or effort came first for P6 and P7. P4 chose food that "looks more or less healthy". Calories and protein were never first. P6 only wants a high-protein result, after time. P1 and P2 did not cover it.

**2. People quit batch cooking because it gets boring: not supported.**
Only P6 said boredom ("eating the same food became boring"). P4 runs out: "by day four or five I usually run out of food". P3 finds old food less appealing, which is freshness. P5 has a fridge that is too small. P2 preps 12 portions a week and does not get bored. P7 never tried it.

**3. People know what's in their fridge: mixed.**
P1 and P6 check before cooking, which does not show they know what is there. P3 knows her fridge, yet "herbs, unfortunately, often die faster than I can eat them". P4 listed about ten items and forgot one. P2 lacked one ingredient. P7: "I often discover food after it has gone bad."

**4. People would keep an app updated after cooking: not supported.**
All five who were asked said no (P1 to P5). P4: "too big of a commitment". P2: "I'm lazy, so I don't stick to it." P3 found Notes "too time consuming". P6 and P7 never used a tracking app, so they tell us little. The only logging that lasted took no effort: a smart scale (P2) and a photo to ChatGPT (P4).

**5. Planning happens on a phone: confirmed, thin evidence.**
P3 ("Holding my phone, of course") and P6 used a phone. P4 had a laptop and a phone at the office. P7 answered "Nothing", which gives no other device. P1, P2 and P5 did not cover it. Four answers is few.

## Patterns we didn't expect

- **People repeat known recipes.** P1: they "go to the recipes they know". P4: "a standard set of recipes that I repeat week after week". P3 cooks something she has "cooked before and liked", or saves recipes from Instagram and TikTok. Finding new recipes was not the problem for these three.
- **Time and effort beat cost for eating out.** P6 and P7 gave time or effort as the main factor. P4 has "almost no time to cook" and orders about five times a week. P2 skips cooking about twice a week.
- **One missing ingredient starts a chain.** P3 describes buying more to use up a vegetable: "It's like this snowball starts." P2's missing ingredient turned a 20-minute dish into a long walk. P5 hates leftover ingredients.
- **Waste can come from appetite.** P4 binned a whole meal prep because she did not want to eat it.
- **A chatbot is the rival.** P4 replaced two paid apps with ChatGPT. P5 would not pay for the same reason.

## What we'll change

| Decision | Evidence | In the app today |
|---|---|---|
| Rank recipes by what the user has, up to 2 missing | P3: "only need to buy a couple of ingredients". P5: "buy rice once and use it in five different dishes". P1, P2 | In review, not in main yet. Check it lists which ingredients are missing (P2, P3). |
| No logging after cooking | P1 to P5 | Nothing to build. Keep it out of scope. |
| Keep ingredient entry quick and per visit, not a standing inventory | P3 (Notes list too slow), P4, P2 (onboarding must be fast) | Open. The matching feature decides this. |
| Calories and macros hidden by default, one tap to show | P3, P4. P6 wants high protein, so keep them available | USDA macros exist per recipe in the backend. There is no screen yet, so we can set the default. |
| Phone-first layout | P3, P6, P4 | Not checked. Only login, register and account pages exist. |
| No pantry inventory or expiry reminders for now | P7 loses food to spoilage but never asked for reminders | Not built. Cook-from-what-you-have covers the waste. |

The app today has register, login, recipe import from TheMealDB and USDA macros per recipe. It has no recipe screens, saved recipes or shopping list.

**Next epic: saved recipes.** P3 already saves recipes by sending them to herself, and P1, P3 and P4 return to known recipes. Accounts exist, so this builds on what we have.

A shopping list comes second. Only P3 builds a list and checks its cost. P4 never keeps one and orders groceries online. The "2 missing" ranking already covers the part P2 and P3 asked for.

Time and effort is the biggest signal (P2, P4, P6, P7). Our recipes carry no cooking time, so we cannot act on it yet. Add a time question to round 2 and decide then.

## Gaps

- Ransith's two interviews (NUT-19) and Karolina's second (NUT-16) are not in. Verdicts could change.
- Seven interviews is a small sample. Most guesses have four to six answers.
- Evidence differs in depth. P3 and P4 are transcripts. P1, P2 and P5 are the interviewer's notes. P6 and P7 are short forms.
- P1, P2 and P5 are not scored on several guesses, and P2's budget label is a guess.
