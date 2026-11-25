# 1. FastAPI, SQLAlchemy and SQLAdmin as the application stack

- **Status:** Accepted
- **Date:** 2026-11-25

## Context

VSHMS must run offline on low-end Windows PCs, serve thin clients on a LAN, and later sync with other devices and a cloud relay (PLAN.md §5). The team chose Python. Django and FastAPI were both considered.

## Decision

- **FastAPI** for HTTP: HTML routes (Jinja2 + HTMX) for screens and JSON routes for sync and integrations.
- **SQLAlchemy 2.0** with **Alembic** for data access and migrations, on SQLite (devices) and PostgreSQL (relay).
- **SQLAdmin** for master-data screens.
- Login, sessions, CSRF and permissions are built in-house on Starlette sessions and argon2-cffi.

## Consequences

- SQLAlchemy's built-in SQLCipher dialect and session events simplify encryption and sync capture.
- Typed Pydantic APIs keep a separate front end (React, mobile) possible later.
- Auth and CSRF are our own code, so they get dedicated tests and a security review (task B3).
- Phase 0 is about two weeks longer than it would be with Django's built-ins.

# Template for new ADRs

Copy this file's headings: a title, Status, Date, Context, Decision, Consequences. Number files in order (`0002-...md`).
