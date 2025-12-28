# Scientific Publications API

## Overview

A FastAPI-based REST API for managing and querying scientific publications. Provides CRUD operations, flexible queries (filter, sort, group), author-publication joins, and full-text search on abstracts. Designed to run with PostgreSQL and Alembic for schema migrations.

## Quickstart

1. Prerequisites
    - Python 3.10+ and pip
    - PostgreSQL (local or hosted)

2. Clone and install
    - git clone <repo>
    - cd scientific-publications-api
    - python -m venv .venv && source .venv/bin/activate
    - pip install -r requirements.txt

3. Configure
    - Set DATABASE_URL (e.g. export DATABASE_URL="postgresql://user:pass@localhost:5432/dbname")
    - Optional: place env vars in a .env file if using python-dotenv

4. Database migrations
    - alembic revision --autogenerate -m "init tables"
    - alembic upgrade head

5. Run
    - uvicorn app.main:app --reload
    - Open API docs at http://127.0.0.1:8000/docs

## Testing & development

- Run tests: pytest
- Use /docs for interactive API exploration and example requests.

## Purpose

This README focuses on setup and quick usage. Further details (endpoints, configuration options, example queries) are documented below.
