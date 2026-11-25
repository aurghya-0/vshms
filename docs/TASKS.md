# Intern task plan: Phase 0 foundations and first Phase 1 features

Three interns, 12 weeks, one mentor. Weeks 1–8 build the Phase 0 foundations from [PLAN.md](../PLAN.md) §9. Weeks 9–12 start the first Phase 1 features so the internship ends with a working demo.

If the internship is shorter, drop the week 9–12 feature tasks (A7, B6, C6) first; the foundations matter more.

## Tracks and ownership

Each intern owns one track, so they rarely edit the same files. Each intern is also the **second reviewer** for one other track, so knowledge spreads.

| Track | Intern | Owns (in `src/vshms/`) | Reviews |
|---|---|---|---|
| **A: Data and sync core** | Intern A | `db.py`, `core/ids.py`, `core/hlc.py`, `core/sync_base.py`, `core/audit.py`, `core/backup.py`, `pharmacy/` | Track C |
| **B: Access and UI** | Intern B | `main.py` (middleware, routers), `core/auth.py`, `core/permissions.py`, `admin/`, `templates/`, `static/`, `locale/`, `patients/` | Track A |
| **C: Platform and print** | Intern C | `desktop/`, `packaging/`, `printing/`, `masters/`, `billing/`, `__main__.py` (CLI), `.github/workflows/` | Track B |

The mentor reviews every pull request and gives a **deep review** to the two security- and data-critical tasks: **A3** (sync capture) and **B3** (login and sessions).

## Milestones

| End of week | Milestone | What the demo shows |
|---|---|---|
| 1 | **Everyone has shipped** | Each intern has merged a starter task and knows the workflow |
| 4 | **Walking skeleton** | The desktop window opens the app; records get UUIDv7 IDs and HLC timestamps; a user can log in |
| 8 | **Phase 0 complete** | PLAN.md Phase 0 exit criteria: the Windows installer works, backup/restore round-trips, the power-cut test passes, cold start is under 5 s, auth passes review |
| 12 | **First patient journey** | Register a patient → bill an OPD consultation → print a thermal receipt; pharmacy stock services pass their tests |

## Interface contracts (agree these early)

Parallel work depends on a few shared interfaces. Each is **published as a stub by its owner on the date shown**, even before the real behaviour exists, so others can build against it.

| Contract | Owner | Stub by | Used by |
|---|---|---|---|
| `SyncBase` mixin: column names and types (`id`, `site_id`, `device_id`, `created_at`, `updated_hlc`, `deleted`) | A | Week 2, Wed | B2, B6, C6, A7 |
| `audit.record(session, actor_id, action, entity, entity_id, details)` | A | Week 3 | B3, B6, C6 |
| `require("permission.code")` FastAPI dependency and `current_user` | B | Week 3 | All routes, B4, C4 |
| `Patient` model with `id`, `uhid`, `name`, `mobile` | B | Week 9, Mon | C6 |
| Print API: `render_print(request, template, context, paper="a5")` | C | Week 6 | B6, C6 |

Changing a contract after its date needs a short note in the team channel and the mentor's agreement.

---

## Week 1: onboarding (all interns)

Everyone:

1. Reads PLAN.md (§1, §5 and §6 closely), README.md and CONTRIBUTING.md.
2. Sets up the project and gets all checks passing locally.
3. Works through the relevant tutorials (see [Learning resources](#learning-resources)).
4. Ships one small starter task through the full workflow: branch → draft PR → review → green CI → merge.

| ID | Owner | Starter task | Done when |
|---|---|---|---|
| **S1** | A | Extend `/health` to report whether the database answers (`SELECT 1` through `get_session`) and the SQLite journal mode | `/health` returns `"database": "ok"` and `"journal_mode": "wal"`; a test covers it |
| **S2** | B | Download **htmx** and **Alpine.js** into `static/vendor/` (pinned versions, no CDN), load them in `base.html`, and add a button on the home page that loads the server time as an HTMX fragment | The button works with the network disconnected; versions are noted in `static/vendor/README.md` |
| **S3** | C | Add a `vshms` command (`src/vshms/__main__.py` plus a `[project.scripts]` entry) with a `serve` subcommand that starts Uvicorn using `Settings.host` and `Settings.port` | `uv run vshms serve` starts the app; `uv run vshms --help` lists commands |

---

## Track A: Data and sync core

The data rules in PLAN.md §5.4 must hold from the very first table, even though multi-device sync only ships in Phase 3.

### A1. IDs, device identity and the `SyncBase` mixin (weeks 2–3)
- Generate **UUIDv7** primary keys (`uuid6` package; the standard library has `uuid.uuid7()` from Python 3.14).
- Give each install a **device identity** created on first run and stored in `data_dir/device.json`: device ID, site code and short device code (used later in UHIDs and invoice series).
- Write the `SyncBase` mixin with `id`, `site_id`, `device_id`, `created_at`, `updated_hlc`, `deleted`. **Publish the stub by week 2, Wednesday.**
- Add a soft-delete helper (`mark_deleted(obj)`). Syncable rows are never hard-deleted.
- **Done when:** a demo model using `SyncBase` gets every field filled automatically on insert; IDs sort by creation time; tests cover all of it; an Alembic migration creates the demo table.

### A2. Hybrid logical clock (weeks 2–3)
- Implement an HLC (wall-clock milliseconds + counter + device ID) encoded as a fixed-width string that sorts correctly as text.
- It must stay **monotonic when the system clock jumps backwards** (common on PCs with a dead CMOS battery) and must merge correctly with timestamps received from other devices.
- **Done when:** Hypothesis property tests show that timestamps are strictly increasing on one device, that receiving a remote timestamp never makes the clock go backwards, and that string ordering matches logical ordering.

### A3. Outbox capture (weeks 3–5) · mentor deep review
- Add a `before_flush` session event that, for every new, changed or soft-deleted `SyncBase` row, stamps `updated_hlc` and writes an `Outbox` row (table, row ID, operation, HLC, JSON snapshot of the row).
- Add a `do_orm_execute` event that **rejects** bulk `update()`/`delete()` statements on syncable tables, with a clear error message.
- **Done when:** tests prove that a row and its outbox entry commit together and roll back together; that bulk statements are rejected; and that non-syncable tables are unaffected. Write an ADR describing the outbox format.

### A4. Hash-chained audit log (weeks 4–5)
- `AuditEvent` table, append-only. Each event stores the SHA-256 of the previous event's hash plus its own canonical JSON.
- `audit.record(...)` helper (**publish the stub in week 3**), and a `verify_chain()` function exposed as `vshms audit verify`.
- **Done when:** tests show that changing, deleting or reordering any past event is detected; recording an event is fast enough to call on every page view (measure it).

### A5. Backup and restore (weeks 5–7)
- Snapshots taken with SQLite's **online backup API** (safe while the app is running in WAL mode), saved to `data_dir/backups/` with a checksum manifest.
- Rotation: keep the last 24 hourly and 30 daily snapshots (configurable).
- `vshms backup`, `vshms backup --to <folder>` (for USB drives) and `vshms restore <file>`, which checks integrity (`PRAGMA integrity_check` and the checksum) before replacing anything and keeps the old database aside.
- **Done when:** a backup → wipe → restore round-trip in a test gives an identical database; restoring a corrupted file is refused with a clear message.

### A6. Power-cut durability test (weeks 7–8)
- A script in `tests/durability/` that repeatedly starts a writer process (inserting records with outbox and audit entries), kills it at a random moment, and checks the database afterwards.
- **Done when:** 500 kill cycles show no corruption, no half-written transactions (every row has its outbox and audit entries) and an intact audit chain. Results are recorded in an ADR.

### A7. Pharmacy stock ledger services (weeks 9–12, Phase 1)
- Models: `Item` (with HSN code, GST rate, schedule H/H1/X flag), `Batch` (batch number, expiry, MRP, purchase rate), `StockMovement` (append-only: receipt, sale, return, adjustment, expiry write-off).
- Services: stock on hand as a sum of movements; **FEFO** (first-expiry-first-out) batch picking; near-expiry and reorder-level queries.
- **Done when:** services have full test coverage including concurrent sales on two sessions; no UI yet (it follows in Phase 1).

---

## Track B: Access and UI

### B1. UI shell (weeks 2–3)
- Base layout: top bar with the current user and role, a role-specific home page, flash messages, and a printable area.
- Jinja2 macros that render form fields and **Pydantic validation errors**, so every form looks and behaves the same.
- Keyboard shortcut layer (PLAN.md §6): `F2` new registration, `F3` search, `Esc` back, `?` shows a shortcut help overlay.
- Large touch targets, and a layout that works on a 10-inch tablet.
- **Done when:** a demo form validates with Pydantic and shows errors inline; shortcuts work; it looks right at 1366×768 (common on cheap laptops) and on a tablet.

### B2. Users, roles and permissions (weeks 3–4)
- Models: `User`, `Role`, and permission codes such as `billing.refund` (built on `SyncBase` from A1).
- Default roles seeded: reception, doctor, nurse, pharmacist, lab, billing, admin. A user can hold several roles.
- `require("code")` FastAPI dependency and `current_user`; **publish the stub in week 3**.
- **Done when:** tests cover allowed and denied access for every default role on a sample route.

### B3. Login, sessions, CSRF and PIN switching (weeks 4–6) · mentor deep review
- **argon2-cffi** password hashing; login and logout pages.
- Starlette `SessionMiddleware` with a secret generated on first run and stored in `data_dir`.
- Auto-lock after an idle period (configurable, default 10 minutes).
- **CSRF protection:** a token stored in the session and sent by HTMX in a header on every unsafe request; requests without it are rejected.
- Quick user switching with a **4-digit PIN** on shared PCs, locked after 5 wrong attempts.
- Login, logout, failed login and lockout are recorded with `audit.record` (A4).
- **Done when:** tests cover each case, including CSRF rejection and lockout; the mentor's security review is passed before merging.

### B4. SQLAdmin master-data screens (weeks 6–7)
- Mount SQLAdmin at `/admin`, with an authentication backend that reuses B3's session and requires the `admin.masters` permission.
- First screens: users and roles, departments, and practitioners (including their medical council registration number).
- **Done when:** a non-admin user cannot reach `/admin`; an admin can create a doctor and a department; changes are audited.

### B5. Translations and Indian formats (weeks 7–8)
- Babel extraction config, the Jinja2 i18n extension, `_()` in templates and Python, and a per-user language setting.
- Hindi translation of the UI shell and login.
- Formatting helpers: **₹ with lakh/crore grouping** (₹1,23,456.00), DD-MM-YYYY dates, and the financial year (April–March) for a date.
- **Done when:** switching a user to Hindi translates the shell; formatter tests pass, including edge cases (negative amounts, 31 March vs 1 April).

### B6. Patient registration and search (weeks 9–12, Phase 1)
- `Patient` model on `SyncBase`: UHID, name, sex, date of birth **or approximate age** (years, months or days), mobile, C/o (S/o, D/o, W/o) and guardian, address with PIN code, state and district, category (General/BPL/Staff/PM-JAY/TPA), ABHA field. **Publish the model by week 9, Monday.**
- UHID format `<site code><device code>-<sequence>` using the device identity from A1.
- Registration form (B1 macros) and **live search** by mobile number, name or UHID with HTMX; warn about a likely duplicate before saving.
- Registration printout of the patient card using C4's print API.
- **Done when:** a receptionist can register and print in **under 30 seconds** using only the keyboard (time it with someone outside the team).

---

## Track C: Platform and print

### C1. Desktop launcher (weeks 2–3)
- Implement `desktop/launcher.py`: pick a free port, start Uvicorn in a background thread, wait until `/health` answers, open a **pywebview** window, and shut down cleanly when the window closes.
- Allow only one running instance; starting it a second time brings the existing window forward.
- **Done when:** it works on Windows 10/11 and Ubuntu; closing the window leaves no process running.

### C2. SQLCipher spike (weeks 3–4)
- Get the `sqlcipher3` driver working with SQLAlchemy's `sqlite+pysqlcipher` dialect on **Windows and Linux**. If no ready-made Windows wheel exists, build one in CI.
- Propose how the encryption key is kept (for example the OS keyring or Windows DPAPI) and how the printed recovery key restores access (PLAN.md §7).
- **Done when:** an ADR records what worked, what failed and the recommendation; if it works, `db.py` supports an encrypted database behind a setting.

### C3. Windows installer (weeks 4–6)
- PyInstaller **one-folder** build and an **Inno Setup** installer with a Start-menu shortcut; uninstalling keeps the hospital's data.
- A CI job on `windows-latest` builds the installer and uploads it as a build artifact.
- **Measure on a 4 GB RAM PC:** installer size, cold start time (target under 5 s) and memory use. Note any antivirus warnings.
- **Done when:** a clean Windows 10 machine installs and runs the app from the CI artifact; measurements are recorded in an ADR.

### C4. Print engine (weeks 6–8)
- `render_print(...)` API (**publish the stub in week 6**) with CSS page sizes for **A4, A5 and 80 mm** and adjustable margins for pre-printed letterheads.
- Printing through the WebView2 print dialog (spike: check it works and what can be preset).
- Silent **thermal receipt printing** with python-escpos, plus a "test print" button.
- **Done when:** a sample prescription prints correctly on A5 and on a letterhead, and a sample receipt prints on a thermal printer.

### C5. Master seed data (weeks 8–9)
- Idempotent loaders (`vshms masters load <name>`) for: the PIN code directory (data.gov.in), the National List of Essential Medicines as a starter generic drug list, and a starter lab-test list with reference ranges (reviewed by a doctor before use). ICD-10 is added once its licence terms are confirmed.
- **Check and record each dataset's licence** in `masters/README.md` before committing data.
- **Done when:** loading twice does not create duplicates; PIN code lookup returns district and state offline.

### C6. OPD billing and receipts (weeks 9–12, Phase 1)
- Models: `ServiceRate` (tariff), `Invoice`, `InvoiceLine`, `Payment` (append-only; corrections are void-and-reissue).
- **Invoice numbers per device per financial year**, at most 16 characters (for example `R1/26-27/00123`), using A1's device code and B5's financial-year helper.
- OPD consultation bill for a patient (uses B6's `Patient` model; mock it until week 9).
- Receipt with a **UPI QR code** generated offline (`qrcode` package), printed through C4.
- **Done when:** a consultation can be billed and the receipt printed; invoice numbers never repeat, even across a financial-year boundary (tested).

---

## Definition of done (every task)

- [ ] Code follows [CONTRIBUTING.md](../CONTRIBUTING.md) (module layout, append-only records, no CDN, `_()` for text, `Decimal` for money).
- [ ] Unit tests cover the logic and edge cases named in the task; integration tests cover each new route or screen (see the testing rules in [CLAUDE.md](../CLAUDE.md)).
- [ ] UI and print changes were also checked by hand (keyboard-only, 1366×768, tablet, offline, real paper sizes).
- [ ] `ruff`, `mypy` and `pytest --cov` (80% minimum) pass in CI on Ubuntu and Windows.
- [ ] Schema changes come with an Alembic migration.
- [ ] Decisions and spike results are recorded in `docs/adr/`.
- [ ] The intern has shown it working at the Friday demo.

## Team rhythm

- **Daily:** a 15-minute stand-up (what I finished, what I'm doing, what's blocking me).
- **Monday:** 30-minute planning with the mentor; confirm the week's tasks and any contract changes.
- **Wednesday:** a 1-hour pairing slot, rotating between intern pairs.
- **Friday:** demo of merged work, then a short retro.
- Stuck for more than 2 hours? Ask in the team channel. Stuck for a day? Raise it at stand-up.

## Learning resources

| Topic | Who | Resource |
|---|---|---|
| FastAPI | All | Tutorial – User Guide: https://fastapi.tiangolo.com/tutorial/ |
| SQLAlchemy 2.0 | All, A in depth | Unified tutorial: https://docs.sqlalchemy.org/en/20/tutorial/ and ORM events: https://docs.sqlalchemy.org/en/20/orm/events.html |
| Alembic | A, B | Tutorial: https://alembic.sqlalchemy.org/en/latest/tutorial.html |
| Pydantic | All | https://docs.pydantic.dev/latest/ |
| htmx / Alpine.js | B | https://htmx.org/docs/ and https://alpinejs.dev/start-here |
| Hypothesis | A | https://hypothesis.readthedocs.io/ |
| SQLAdmin | B | https://aminalaee.github.io/sqladmin/ |
| pywebview / PyInstaller | C | https://pywebview.flowrl.com/ and https://pyinstaller.org/en/stable/ |
| Hybrid logical clocks | A | Kulkarni et al., "Logical Physical Clocks and Consistent Snapshots in Globally Distributed Databases" (2014) |
| OWASP sessions and CSRF | B | OWASP Cheat Sheet Series: Session Management, CSRF Prevention |
| Domain | All | PLAN.md §2–§4; spend a morning watching the front desk of a small hospital if possible |
