"""Desktop launcher: starts the local server and opens it in a native window.

Placeholder. Task C1 in docs/TASKS.md implements it:
  1. pick a free port and start Uvicorn (vshms.main:create_app) in a background thread,
  2. wait until /health answers,
  3. open a pywebview window on http://127.0.0.1:<port>/,
  4. shut the server down cleanly when the window closes.
"""


def main() -> None:
    raise NotImplementedError("See task C1 in docs/TASKS.md")


if __name__ == "__main__":
    main()
