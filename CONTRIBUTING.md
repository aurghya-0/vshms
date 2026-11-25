# Contributing

## Setup

1. Install Python 3.12+ and [uv](https://docs.astral.sh/uv/).
2. Clone the repository and run `uv sync`.
3. Run the checks: `uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest`.

## Workflow

- One branch per task, named `<task-id>-<short-name>` (for example `a2-hlc-clock`).
- Open a **draft pull request early**, by day 2 of a task, so reviewers can catch problems before they grow.
- Every pull request needs **one review from the mentor**, plus one from another intern when the change touches that intern's area (see the ownership table in [docs/TASKS.md](docs/TASKS.md)).
- Keep pull requests small: under about 400 changed lines where possible. Split large tasks into several pull requests.
- CI must be green before merging. Never skip or delete a failing test to get green; ask for help instead.
- Squash-merge. The pull request title becomes the commit message, so start it with the task ID: `A2: Add hybrid logical clock`.

## Module layout

Each domain module (`patients/`, `billing/`, ...) follows the same shape:

| File | Contents |
|---|---|
| `models.py` | SQLAlchemy models. Syncable models inherit the `SyncBase` mixin from `vshms.core` |
| `schemas.py` | Pydantic models for form input and JSON output |
| `services.py` | Business logic. Takes a `Session`, never a `Request`. This is where most tests point |
| `routes.py` | FastAPI routers: HTML pages and HTMX fragments, plus JSON endpoints. Thin: validate, call a service, render |
| `templates/<module>/` | Jinja2 templates for this module |

Rules:

- **Business logic lives in `services.py`**, not in routes or templates, so it can be tested without a browser.
- **Clinical and financial records are append-only.** Never update or delete a vitals row, note, payment or stock movement. Add a correcting row instead (PLAN.md §1, §5.4).
- **No bulk `update()`/`delete()` statements** on syncable tables. They bypass sync tracking (PLAN.md §5.4).
- **No CDN links.** The app must work offline, so all CSS and JS is vendored into `static/`.
- **All user-visible text goes through `_()`** so it can be translated.
- **Money is `Decimal`**, never `float`. Store paise as integers or use `Numeric(12, 2)`.
- **Never store full Aadhaar numbers** or log patient details to the console or log files.
- Every schema change comes with an Alembic migration.

## Architecture decisions

Significant design choices are recorded in `docs/adr/` as short numbered files (context, decision, consequences). Write one when you choose a library, change a data rule, or deviate from PLAN.md.
