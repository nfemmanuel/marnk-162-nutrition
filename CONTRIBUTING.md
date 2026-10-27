# How we work

Mirror of the [Confluence SOP](https://marnk-162.atlassian.net/wiki/spaces/SD/pages/13467658). Edit both together.

This is how we take a piece of work from an idea to merged code. It's short on purpose, and it changes whenever we find something better, so if anything here gets in your way, bring it up at the Tuesday standup and we change it.

## Where things live

- **Jira** has our epics, stories and tasks, and the timeline ([NUT board](https://marnk-162.atlassian.net/jira/software/projects/NUT/boards))
- **GitHub** has the code and an issue for every ticket that ends in a PR, and this is the part that gets graded ([repo](https://github.com/nfemmanuel/marnk-162-nutrition))
- **Confluence** has drafts, research and decisions (Software Development space), and anything finished also goes into the repo's `docs/` folder through a PR, since Confluence isn't graded
- **Telegram** is for quick questions and updates, and anything we decide there gets written up in Confluence so it doesn't get lost

## Ticket types

- **Epic** is an outcome that takes a week or more (for example the [walking skeleton](https://marnk-162.atlassian.net/browse/NUT-2)). It has one person accountable for it, and the tickets under it are split across the team.
- **Story** is something a user can see, and it's always written as "As a [user], I want to (or I need to) ... so that ...". The "so that" is what tells whoever builds it why it matters.
- **Task** is work users never see (setting up CI, a database table, a doc).
- **Bug** is something that used to work or should work and doesn't.
- **Sub-task** is a step inside a story or task. It doesn't get its own branch, you just use its key in the commit.

Every ticket has the same blocks, so anyone can pick one up and understand it without asking. Those are **Why**, **Done when** (a check someone else could run), **Steps**, **Waits on** and **Unblocks**, and **Links** (real links to everything it mentions, not just names). It also has one assignee, a start and due date, a label (frontend, backend, devops, docs or research) and a priority.

For priority we use **Highest** when it's blocking someone right now, **High** when other tickets are waiting on it this week, **Medium** for normal work, and **Low** for nice-to-haves. If you're stuck, tick the Impediment flag on the ticket so it comes up at standup.

## Starting a piece of work

1. Move the ticket to In Progress.
2. If it's going to end in a PR, open a GitHub issue with the Jira key at the start of the title (for example `NUT-3 Set up the app factory and the base page layout`) and assign yourself.
3. Branch off the latest `main`, with the key and a couple of words in the name (for example `NUT-3-app-factory`). One branch per story or task, never one per sub-task.

## Commits

Start every commit message with the ticket key, and use the sub-task's key when the commit finishes a sub-task (for example `NUT-7 add User model`). That's what links the commit to the ticket in Jira. Small commits often are better than one big commit at the end, because the course looks at how evenly everyone's work is spread over the semester.

## Pull requests

Every story or task ends in one PR into `main`. The course only counts a PR when it's meaningful, so each one should

- do one small, complete thing
- have a title starting with the ticket key, and a description that explains what it does and why, so someone can understand it from the PR alone
- say `Closes #<issue number>` so the GitHub issue closes when it merges
- include docstrings and tests where they make sense
- be reviewed and approved by a teammate, and merged into `main`

## Reviews

Every PR needs one approval before it can merge, and GitHub won't let it through without one. Reviews have to be in your own words (the course allows AI almost everywhere, but not for reviews), and a good review has specific things the author can act on, not just "looks good". Every comment gets resolved before merging, either by making the change or by replying with why not, and that goes for comments from bots too. Try to review within a day of being asked, since someone is usually waiting on it.

## Merging

The author merges once the PR is approved and the tests pass. We use merge commits (squash is turned off) so everyone's individual commits stay in the history, and the branch deletes itself after the merge. Then move the ticket to Done.

## MVPs

We ship at least three MVPs, spread across the semester, and each one is a tag on `main` (`mvp-1`, `mvp-2`, `mvp-3`). Before tagging, the PRD is updated with what changed and why, the app runs from a fresh clone with one command, and we write short release notes. Each MVP should change based on what we heard in user interviews.

## Decisions

Anything that changes how we build (the stack, the data source, hosting) gets an ADR in the [Architecture Decision Records](https://marnk-162.atlassian.net/wiki/spaces/SD/folder/4194305) folder, starting with [ADR-000](docs/adr/000-stack-and-workflow.md). Once the team agrees, it goes into `docs/adr/` in the repo through a PR. We don't edit old ADRs, we write a new one that replaces them.

## Meetings

We have a weekly standup on Tuesdays at 11:30 AM Pacific, where everyone says what they finished, what they're on next and whether anything is blocking them. In between, updates go in Telegram.
