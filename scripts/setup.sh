#!/usr/bin/env bash
# One-command development setup for VSHMS (Linux, macOS, WSL, Git Bash).
#
#   ./scripts/setup.sh              set everything up and run the checks
#   ./scripts/setup.sh --run        ...then start the app at http://127.0.0.1:8710
#   ./scripts/setup.sh --yes        install uv without asking if it is missing
#   ./scripts/setup.sh --skip-checks   skip lint, type check and tests (faster)
#
# Safe to run again at any time: it only installs what is missing.
# On Windows use scripts\setup.ps1 instead. Full guide: docs/SETUP.md
set -euo pipefail

RUN=0
YES=0
CHECKS=1
for arg in "$@"; do
  case "$arg" in
    --run) RUN=1 ;;
    --yes | -y) YES=1 ;;
    --skip-checks) CHECKS=0 ;;
    -h | --help)
      sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown option: $arg (try --help)" >&2
      exit 2
      ;;
  esac
done

cd "$(dirname "${BASH_SOURCE[0]}")/.."

step() { printf '\n==> %s\n' "$*"; }
fail() {
  printf '\nERROR: %s\n' "$*" >&2
  exit 1
}

step "Checking git"
command -v git > /dev/null 2>&1 || fail "git is not installed. Install it (https://git-scm.com/downloads), then run this script again."
git --version

step "Checking uv (installs Python and all packages for us)"
# uv's installer puts it in ~/.local/bin, which may not be on PATH yet.
export PATH="$HOME/.local/bin:$PATH"
if ! command -v uv > /dev/null 2>&1; then
  echo "uv is not installed."
  command -v curl > /dev/null 2>&1 || fail "curl is needed to install uv. Install curl, or install uv yourself: https://docs.astral.sh/uv/getting-started/installation/"
  answer="n"
  if [ "$YES" = 1 ]; then
    answer="y"
  elif [ -t 0 ]; then
    read -r -p "Install uv now from https://astral.sh/uv/install.sh? [Y/n] " answer
    answer="${answer:-y}"
  fi
  case "$answer" in
    [Yy]*) curl -LsSf https://astral.sh/uv/install.sh | sh ;;
    *) fail "uv is required. Install it from https://docs.astral.sh/uv/getting-started/installation/ or run: ./scripts/setup.sh --yes" ;;
  esac
  export PATH="$HOME/.local/bin:$PATH"
  command -v uv > /dev/null 2>&1 || fail "uv was installed but is not on PATH. Open a new terminal and run this script again."
fi
uv --version

step "Installing Python 3.12+ and all project packages (locked versions)"
uv sync --locked

step "Creating the local development database"
uv run alembic upgrade head

if [ "$CHECKS" = 1 ]; then
  step "Running the full check: lint, format, types, tests"
  if ! { uv run ruff check . \
    && uv run ruff format --check . \
    && uv run mypy \
    && uv run pytest --cov; }; then
    fail "Setup finished, but the checks failed. Fix that before you start (see docs/SETUP.md, Troubleshooting) or ask your mentor."
  fi
else
  step "Skipping checks (--skip-checks)"
fi

printf '\nAll set. Useful commands (always prefix with "uv run"):\n'
printf '  uv run uvicorn vshms.main:create_app --factory --reload --port 8710   start the app\n'
printf '  uv run pytest -m "not integration and not slow"                       quick tests\n'
printf '  uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest --cov   full check\n'
printf 'Next: read docs/SETUP.md and CONTRIBUTING.md, then pick up your starter task.\n'

if [ "$RUN" = 1 ]; then
  step "Starting the app at http://127.0.0.1:8710 (Ctrl+C to stop)"
  exec uv run uvicorn vshms.main:create_app --factory --reload --port 8710
fi
