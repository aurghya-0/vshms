# Development environment setup

Everything you need to go from a fresh laptop to a running app with passing tests. Allow about 15 minutes, mostly downloads.

## Quick start

You only need **Git**. The setup script installs everything else: [uv](https://docs.astral.sh/uv/) (our package manager), the right Python version and every project package, at the exact versions the team uses.

**1. Install Git** if you don't have it: https://git-scm.com/downloads (on Windows, install Git for Windows and keep the defaults).

**2. Clone the repository** and go into it:

```bash
git clone https://github.com/aurghya-0/vshms.git
cd vshms
```

**3. Run the setup script for your system.**

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

Linux, macOS, WSL or Git Bash:

```bash
./scripts/setup.sh
```

If uv is missing, the script asks before installing it (press Enter to say yes). When it ends with **"All set"**, your environment works: the lint, type check and all tests passed.

**4. Start the app:**

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1 -Run
```

Linux, macOS, WSL or Git Bash:

```bash
./scripts/setup.sh --run
```

Open http://127.0.0.1:8710. You should see "VSHMS is running". Stop the app with `Ctrl+C`.

The script is safe to run again whenever you like. Run it after pulling changes if something odd happens: it only installs what is missing.

### Script options

| What you want | Windows | Linux / macOS |
|---|---|---|
| Skip the checks (faster) | `-SkipChecks` | `--skip-checks` |
| Start the app afterwards | `-Run` | `--run` |
| Install uv without asking | `-Yes` | `--yes` |
| Show help | `Get-Help .\scripts\setup.ps1` | `./scripts/setup.sh --help` |

### What the script does

1. Checks that Git is installed.
2. Checks for uv and installs it if missing (from the official installer at astral.sh, after asking you).
3. Runs `uv sync --locked`: downloads Python 3.12 or newer if you don't have it, creates a private `.venv` folder in the project, and installs every package at the versions pinned in `uv.lock`. Nothing is installed system-wide.
4. Runs `alembic upgrade head` to create your local development database (in `~/.vshms` on Linux and macOS, `C:\Users\<you>\.vshms` on Windows).
5. Runs the full check: lint, format check, type check and the tests with coverage. This is the same check CI runs.
6. With `--run` / `-Run`, starts the app.

The scripts are plain text in the `scripts/` folder. Read them once so you know what runs on your machine.

## Check that it worked

- The script printed **"All set"** with no errors.
- http://127.0.0.1:8710/health shows `{"status":"ok", ...}` while the app is running.
- `uv run python --version` shows Python 3.12 or newer.

## Everyday commands

Always put `uv run` in front. It uses the project's private environment, so you never need to activate anything.

| Task | Command |
|---|---|
| Start the app (reloads when you save a file) | `uv run uvicorn vshms.main:create_app --factory --reload --port 8710` |
| Quick tests while coding | `uv run pytest -m "not integration and not slow"` |
| All tests with coverage | `uv run pytest --cov` |
| Lint | `uv run ruff check .` |
| Fix lint and formatting automatically | `uv run ruff check . --fix` then `uv run ruff format .` |
| Type check | `uv run mypy` |
| New database migration | `uv run alembic revision --autogenerate -m "what changed"` |
| Apply migrations | `uv run alembic upgrade head` |
| Install packages after a `git pull` | `uv sync --locked` (or run the setup script again) |

**Before every commit**, run the full check and see it pass:

```bash
uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest --cov
```

Windows PowerShell 5.1 (the one built into Windows) doesn't understand `&&`. Either use `;` between the commands, or run the checks from Git Bash. Note that `;` keeps going after a failure, so read the output of every step.

**Adding a package:** ask your mentor first (see [CLAUDE.md](../CLAUDE.md)). If approved, `uv add <package>` updates `pyproject.toml` and `uv.lock`; commit both.

## Settings for local development

The app reads settings from environment variables that start with `VSHMS_`, or from a `.env` file in the project folder (it is git-ignored, so it never gets committed).

| Setting | Effect |
|---|---|
| `VSHMS_DATA_DIR` | Where the database and other local files live. Default: `.vshms` in your home folder |
| `VSHMS_DEBUG=true` | Turns on the API docs page at http://127.0.0.1:8710/api/docs |
| `VSHMS_MODE` | `solo` (default), `hub` or `relay` |

Example `.env`:

```
VSHMS_DEBUG=true
VSHMS_DATA_DIR=C:\work\vshms-data
```

**Starting fresh:** stop the app, delete your data folder (`~/.vshms`, or `VSHMS_DATA_DIR` if you set it) and run `uv run alembic upgrade head`. The tests never touch this folder; each test uses its own temporary one.

## Editor setup

Any editor works. These settings make the project easy to work in with **VS Code**:

1. Open the `vshms` folder (File → Open Folder).
2. Install the extensions *Python*, *Pylance* and *Ruff* (by Astral).
3. Press `Ctrl+Shift+P`, choose *Python: Select Interpreter* and pick the one inside `.venv` in the project folder. Import errors in the editor almost always mean this step was skipped.
4. In settings, set *Python › Testing › Pytest Enabled* so tests show up in the Testing sidebar.

If you use PyCharm, set the project interpreter to `.venv` the same way.

## If the script fails: manual setup

Run these one at a time from the `vshms` folder. They are what the script does.

1. Install uv: https://docs.astral.sh/uv/getting-started/installation/ (then open a new terminal).
2. `uv sync --locked`
3. `uv run alembic upgrade head`
4. `uv run pytest --cov`

Tell your mentor which step failed and paste the full error. Don't retype it from memory.

## Troubleshooting

| What you see | What to do |
|---|---|
| Windows: *"running scripts is disabled on this system"* | Start the script with `powershell -ExecutionPolicy Bypass -File scripts\setup.ps1`, as in the Quick start. This applies to that one command only and changes no settings |
| *"git is not installed"* | Install Git, **close and reopen** your terminal, run the script again |
| *"uv was installed but is not on PATH"* | Close and reopen your terminal, then run the script again. The installer updates PATH for new windows only |
| Download errors, certificate errors or timeouts on a college, office or VPN network | Set your proxy first (`HTTPS_PROXY`). If you see certificate errors, also set `UV_SYSTEM_CERTS=1` so uv trusts your system certificates. If it still fails, try a different network (a phone hotspot works) |
| *"The lockfile ... needs to be updated"* | Run `git pull`, then try again. If it persists, `pyproject.toml` and `uv.lock` are out of step on `main`: tell your mentor, and don't run `uv lock` yourself |
| *"Address already in use"* or port 8710 is busy | Another copy of the app is still running. Stop it, or start this one on another port with `--port 8711` |
| *"database is locked"* | Two copies of the app share one database folder. Give each its own `VSHMS_DATA_DIR` |
| Tests fail on a clean clone | Run `uv run python --version` (must be 3.12 or newer). Then run `uv run pytest -x` and send your mentor the first failure. A clean clone should always pass; this is worth reporting |
| Windows: file path too long during `git clone` | Run `git config --global core.longpaths true`, then clone again, and avoid cloning into a deeply nested folder |
| Editor shows red import errors but the app runs | Select the `.venv` interpreter (see Editor setup) |
| *"ruff format --check"* fails | Run `uv run ruff format .` and commit the changes |
| Script says `./scripts/setup.sh: bad interpreter` or `\r` errors | The file got Windows line endings. Run `git config core.autocrlf input`, delete the repository folder and clone again |

## Notes for each track

- **Track A (data and sync):** nothing extra. Everything you need is installed. SQLite comes with Python.
- **Track B (access and UI):** nothing extra for now. htmx and Alpine.js are vendored into the repository by task S2, so you don't need Node.js or npm.
- **Track C (platform and print):** use a **Windows 10 or 11** machine or VM, because the desktop window and installer are Windows-first. pywebview, PyInstaller and the SQLCipher driver are not installed yet; they are added by tasks C1, C2 and C3 once your mentor has agreed to each. Inno Setup (the installer builder) is a separate Windows program that you install yourself when you reach C3. Linux needs some extra system libraries for pywebview; the pull request for C1 lists them.

## Getting help

Stuck for two hours: ask in the team channel with the exact command you ran and the full output. Stuck for a day: raise it at stand-up. Found a mistake in this guide: fix it in a pull request. It's a good first contribution.

Next: read [CONTRIBUTING.md](../CONTRIBUTING.md) and [CLAUDE.md](../CLAUDE.md), then start your [first-week plan](TRAINING.md).
