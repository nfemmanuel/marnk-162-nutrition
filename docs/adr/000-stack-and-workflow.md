# ADR-000: Tech stack and workflow

**Status:** Accepted (agreed by the team at the Oct 6, 2026 standup)

**Date:** 2026-10-02

Mirror of the [Confluence page](https://marnk-162.atlassian.net/wiki/spaces/SD/pages/9371649). Edit both together.

## Context

We are about to start the walking skeleton, and whatever it does with the stack, the folder layout and the workflow is what every feature PR after it will copy, so we want to settle those choices once and write them down before the first PR goes in.

A few things are already decided for us by the final project spec. The app has to be reachable through a web interface (mobile-only frameworks are out), it has to deploy simply on an ordinary Linux, Windows or macOS machine, it has to ship every API key it needs so nobody has to sign up for anything to run it, any LLM feature needs a fallback that works without the deployer's own key, and only work in GitHub is graded.

The course teaches a specific stack (Python, Flask with Jinja and Flask-Login, SQLAlchemy on SQLite, unittest, Docker and GitHub Actions), and Prof. Subasic mentioned that Jinja is the better choice for the group project and that anything outside the course needs everyone in the group to agree and be able to explain it. Everyone gets asked about the whole repo in the tech interview so we would rather pick things all five of us can explain than things one of us happens to know well. If anyone believes there are better alternatives and we all agree to use it for the sake of learning, then we switch.

## Decision

| Area | What we use |
| --- | --- |
| Language and framework | Python 3 with Flask, pages rendered with Jinja templates |
| Structure | An app factory (`create_app()`) with one blueprint per feature, the same shape as the flaskr tutorial |
| Login | Flask-Login |
| Database | SQLite through SQLAlchemy |
| Schema changes | Recreate the database while we only have test data, and decide on migrations (probably Flask-Migrate) before we tag MVP 1 |
| Config and secrets | Read from environment variables, with a committed `.env.example` and the real `.env` kept out of git. How we ship third-party keys safely is decided in ADR-001 along with the data source |
| Tests | `unittest`, run the same way locally and in CI |
| Running it | Docker, so the whole app starts with one command (`docker compose up`) |
| CI | GitHub Actions runs the tests on every PR |
| Branching | GitHub flow: `main` is protected (one approval and green CI to merge), every piece of work is a short-lived branch named after its ticket (e.g. `NUT-14-user-model`), and each MVP is a tag on `main` (`mvp-1`, `mvp-2`, `mvp-3`) |
| Mobile | A mobile-first web app that can be installed as a PWA (Add to Home Screen), on top of the same Jinja pages |
| Styling | A small CSS framework so every page is laid out for a phone first and stretches to a laptop (Pico or Bootstrap, the team picks one before the first frontend PR) |
| Tracking | GitHub Issues for every task that ends in a PR (that is what gets graded), Jira for epics and the roadmap, with the Jira key in issue titles, branch names and commit messages (to confirm with the team) |

Hosting is left open for now and gets its own ADR once the skeleton runs in Docker.

## Alternatives considered

- **FastAPI instead of Flask.** Prof. Subasic allows it if the whole group agrees, but the course teaches Flask, the session PCWs are all Flask, and FastAPI is built around JSON APIs, which we don't need while the pages are rendered with Jinja.
- **A JavaScript frontend (React or similar).** Allowed, but the course doesn't teach it and Prof. Subasic advised Jinja. It would split the team into a frontend half and a backend half, and the course specifically warns against an uneven split like that. We can revisit it if the interviews show we need something Jinja can't do.
- **Postgres instead of SQLite.** Better for many users at once, but it needs a separate server to install and run, and the course wants the app to deploy as simply as possible. SQLAlchemy keeps the move cheap if we ever need it.
- **pytest instead of unittest.** Nicer to write, but unittest is what the course teaches, and pytest can run unittest tests later anyway, so starting with unittest closes nothing off.
- **Gitflow (separate develop, release and hotfix branches).** Built for teams shipping versioned releases to live customers, which we don't have. Feature PRs would also merge into `develop` instead of `main`, and the course counts a PR as meaningful when it is merged into the main branch, so we didn't want to risk PRs not counting.
- **Native mobile apps (Swift, Kotlin, React Native).** Ruled out because the course requires a web interface. App stores stay a stretch goal (wrapping the PWA) and are not part of the graded product.

## Consequences

- Everything in the stack is covered in class, so everyone can build it and explain it in the tech interview, and the flaskr tutorial is a working reference for the skeleton.
- A single command runs the app on any machine, and CI catches broken code before it reaches `main`, so anyone who pulls `main` always gets something that works.
- Blueprints per feature mean people mostly work in separate files, which should cut down on merge conflicts.
- SQLite will not handle a lot of users writing at the same time, which is fine for the course project, and if it ever stops being fine, SQLAlchemy makes switching to Postgres a config change more than a rewrite.
- Recreating the database stops being acceptable once real interview users have data in it, so any migrations decisions are owed before the first MVP.
- Jinja pages are less interactive than a JavaScript frontend, so anything that needs to feel app-like (for example swiping through meal options) will need a little plain JavaScript on top, or a new ADR.
- Two follow-up ADRs are owed: ADR-001 for the nutrition data source and how we ship its key, and one for hosting once the skeleton runs.
