"""FastAPI application factory.

Run during development with:
    uv run uvicorn vshms.main:create_app --factory --reload --port 8710
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from vshms import __version__
from vshms.config import Settings, get_settings
from vshms.db import make_engine, make_session_factory

PACKAGE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=PACKAGE_DIR / "templates")


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(
        title="VSHMS",
        version=__version__,
        docs_url="/api/docs" if settings.debug else None,
        redoc_url=None,
    )
    app.state.settings = settings
    app.state.engine = make_engine(settings)
    app.state.session_factory = make_session_factory(app.state.engine)
    app.mount("/static", StaticFiles(directory=PACKAGE_DIR / "static"), name="static")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__, "mode": settings.mode.value}

    @app.get("/", response_class=HTMLResponse)
    def home(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(request, "home.html", {"mode": settings.mode.value})

    # Routers and middleware are registered here as modules are built, e.g.:
    # app.include_router(patients.routes.router, prefix="/patients")
    return app
