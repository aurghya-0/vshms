# VSHMS

An offline-first hospital management system for small Indian hospitals (5–50 beds).
It runs on a single PC with no internet and can optionally sync across devices on a LAN or through a cloud relay.

- **Product and architecture plan:** [PLAN.md](PLAN.md)
- **Intern tasks and schedule:** [docs/TASKS.md](docs/TASKS.md)
- **How we work (setup, branches, reviews, code conventions):** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Standing rules, including testing rules:** [CLAUDE.md](CLAUDE.md)

## Quick start

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

```bash
uv run uvicorn vshms.main:create_app --factory --reload --port 8710
```

Open http://127.0.0.1:8710/. The health check is at `/health`.

## Checks (all must pass before a pull request is merged)

```bash
uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest --cov
```

## Layout

```
src/vshms/
  main.py  config.py  db.py   App factory, settings, database engine and session
  core/                       SyncBase mixin, HLC, IDs, audit log, auth, permissions
  admin/                      SQLAdmin master-data screens
  sync/                       Multi-device sync (Phase 3)
  patients/ opd/ prescriptions/ billing/ pharmacy/      Phase 1 modules
  ipd/ nursing/ lab/ insurance/ registers/              Phase 2 modules
  fhir/                       FHIR / ABDM mappings (Phase 4)
  printing/                   Print templates, thermal receipts, PDF
  masters/                    Seed data loaders
  templates/ static/ locale/  Shared layouts, CSS/JS, translations
desktop/                      pywebview desktop launcher
packaging/                    PyInstaller and Inno Setup installer
migrations/                   Alembic migrations
tests/unit/ tests/integration/ tests/sync_sim/   Unit, integration and sync simulation tests
docs/adr/                     Architecture decision records
```
