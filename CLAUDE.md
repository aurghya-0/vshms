# CLAUDE.md: standing rules for VSHMS

VSHMS is an offline-first hospital management system for small Indian hospitals (5–50 beds). Python 3.12+, FastAPI, SQLAlchemy 2.0 + Alembic, SQLite (PostgreSQL on the cloud relay), Jinja2 + HTMX + Alpine.js, SQLAdmin, pywebview desktop shell.

Read before working: [PLAN.md](PLAN.md) (architecture and compliance), [docs/TASKS.md](docs/TASKS.md) (who owns what), [CONTRIBUTING.md](CONTRIBUTING.md) (workflow and module layout).

These rules apply to everyone working in this repository, human or AI.

## Commands

```bash
uv sync                                    # install
uv run uvicorn vshms.main:create_app --factory --reload --port 8710   # run
uv run pytest -m "not integration and not slow"   # quick unit run while coding
uv run pytest --cov                        # full suite with coverage (what CI runs)
uv run ruff check . && uv run ruff format --check . && uv run mypy   # lint, format, types
uv run alembic revision --autogenerate -m "<what changed>"          # new migration
```

**Before every commit, run the full check and see it pass:** `uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest --cov`.

## Architecture rules (do not break these)

1. **Offline first.** No request path may depend on the internet. No CDN links: vendor all CSS/JS into `static/`. Anything that needs the internet (ABDM, SMS, cloud sync) goes through the background job queue and must tolerate being offline for days.
2. **Clinical and financial records are append-only.** Never update or delete vitals, notes, orders, prescriptions, results, payments, charges, stock movements or audit events. Correct them by adding an amending or voiding row that references the original.
3. **Syncable models inherit `SyncBase`** (UUIDv7 `id`, `site_id`, `device_id`, `created_at`, `updated_hlc`, `deleted`). Soft-delete with a tombstone, never hard-delete.
4. **No bulk `update()`/`delete()` statements on syncable tables.** They bypass the sync outbox. Load objects and change them through the ORM.
5. **Human-readable numbers never need a central server.** UHIDs and invoice numbers include the site/device code; invoice series reset per financial year (April–March), at most 16 characters.
6. **Layering:** `routes.py` stays thin (validate → call service → render). Business logic lives in `services.py`, takes a `Session`, and never touches `Request`. Models in `models.py`, Pydantic schemas in `schemas.py`.
7. **Money is `Decimal`** (or integer paise), never `float`. Dates shown as DD-MM-YYYY, amounts with lakh/crore grouping.
8. **All user-visible text goes through `_()`** for translation.
9. **Every schema change ships with an Alembic migration**, written to run on both SQLite (batch mode) and PostgreSQL.
10. **No module-level global state** for engines, sessions or settings. Use `app.state` and FastAPI dependencies so tests can isolate everything.

## Privacy and compliance

- **Never store full Aadhaar numbers.** Mask other ID numbers.
- **Never log patient-identifying data** (names, mobile numbers, diagnoses) to console or log files. Log IDs only.
- **Test data and fixtures are synthetic.** Never commit real patient data, real hospital data or secrets (`.env`, keys, recovery keys).
- **Don't invent legal values.** Retention periods, tax rates, statutory form fields and thresholds go in configuration with a comment citing the source, and anything uncertain is marked `TODO(compliance): verify` and raised with the mentor.
- Sensitive registers (MTP, PC-PNDT, HIV, psychiatric) must be excluded from general search and every access audited.

## Testing rules

Every change that alters behaviour comes with tests in the same pull request. No exceptions for "small" changes.

### Which kind of test

| Kind | Location | What it covers | Rules |
|---|---|---|---|
| **Unit** | `tests/unit/` mirroring `src/vshms/` (e.g. `tests/unit/billing/test_invoice_numbers.py`) | One function, class or service: HLC, formatters, GST rules, invoice numbering, stock calculations, permission checks | Fast (whole unit suite under ~10 s). No HTTP. Services are tested through the `session` fixture against a real temporary SQLite database |
| **Integration** | `tests/integration/` (automatically marked `integration`) | Several layers together: HTTP route → service → database, HTMX fragments, login and CSRF, SQLAdmin access, Alembic migrations, print rendering | Use the `client`/`app` fixtures. Assert on what a user or caller sees: status codes, rendered content, rows written, audit entries created |
| **Property-based** | Next to the unit or sync tests they cover | Anything with invariants: HLC ordering, sync merge rules, stock ledgers, number series, round-trips (backup → restore, model → FHIR → model) | Use Hypothesis. State the invariant in the test's docstring |
| **Sync simulation** | `tests/sync_sim/` | Several simulated devices with partitions, clock skew and replays | Must show convergence and no lost append-only rows |
| **Durability** | `tests/durability/` (marked `slow`) | Killing the process mid-write, then checking integrity | Run before every release and for any change to `db.py`, the outbox, audit or backup code |

### How to write tests

- **A bug fix starts with a failing test** that reproduces the bug, then the fix.
- **Use a real SQLite database, not mocks, for data access.** The fixtures in `tests/conftest.py` give each test its own throwaway database. Mock only things outside the process: ABDM and other HTTP APIs, SMS/WhatsApp, printers, the system clock.
- **Control time and randomness.** Inject a clock rather than calling `datetime.now()` inside logic, so tests can cover clock jumps, midnight, and 31 March → 1 April.
- **Tests are independent and order-free.** No shared files, no reliance on `~/.vshms`, no network access, no `sleep()`.
- **Test edge cases named in the task**, plus Indian-context ones where relevant: approximate ages, missing DOB, shared mobile numbers, financial-year boundaries, GST thresholds, regional-language text.
- **For every permission-protected route, test both allowed and denied roles.**
- **For every append-only record, test that corrections create a new row and leave the original unchanged.**
- **Name tests by behaviour:** `test_refund_requires_billing_refund_permission`, not `test_refund_2`. Arrange → act → assert, separated by blank lines.
- Keep fixtures in the nearest `conftest.py`; build test data with small factory functions, not large shared JSON files.

### Coverage and CI

- CI runs the full suite on Ubuntu and Windows with coverage. **Overall coverage must stay at or above 80%** (enforced). `core/`, `sync/` and `billing/` should stay above 90%.
- **Never skip, `xfail`, delete or weaken a test to get CI green.** If a test is wrong, fix the test in a separate, clearly explained commit. If it can't be fixed now, stop and ask.
- A flaky test is a bug: fix it or raise it, don't re-run until it passes.

### Manual testing

Automated tests aren't enough for screens and printing. For any UI or print change, also:

- Click through the flow in the running app, keyboard-only as well as with a mouse, at 1366×768 and on a tablet-sized window.
- Print to the actual paper sizes affected (A4, A5, 80 mm thermal) or to PDF, and check alignment on a pre-printed letterhead if relevant.
- Check it still works with the network disconnected.
- Note what was checked in the pull request description.

## Workflow rules

- Work on a feature branch; **never commit or push directly to `main`** unless explicitly asked.
- **Every change to `main` must pass the Main gate** (`.github/workflows/main-gate.yml`): tests on Ubuntu and Windows, migrations matching models, CodeQL, Bandit, dependency audit, dependency review and secret scanning. Fix the finding; never disable a check, lower a threshold, or add a `# noqa: S...` / `# nosec` without a comment explaining why it is safe and the mentor's agreement.
- Keep pull requests small (under about 400 changed lines) and title them with the task ID: `A2: Add hybrid logical clock`.
- **Ask before adding a new dependency.** Prefer pure-Python packages or ones with Windows wheels; record the choice in an ADR if it's significant.
- Record design decisions and spike results in `docs/adr/` (numbered, short).
- Stay within the task's track and owned files (docs/TASKS.md). If a change needs another track's code or a shared contract, say so instead of editing it silently.
- When unsure about clinical, legal or billing behaviour, ask. Don't guess.
