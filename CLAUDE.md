# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) and to any developer or
AI assistant working with code in this repository. Please read it in full before
making changes. It is intended to be the single source of truth for how this project
is structured, how to run it, how to test it, how to deploy it, and what conventions
the team follows. Keep it up to date as the project evolves.

## Table of contents

1. Introduction and project background
2. Repository layout
3. Prerequisites and environment setup
4. Running the backend (without Docker)
5. Running the full stack (with Docker)
6. Running the frontend
7. Running the test suite
8. Architecture and module-by-module walkthrough
9. Data model and seed data
10. Environment variables
11. Dependencies
12. Deployment to Railway
13. Example skills and hooks
14. Coding conventions and style
15. Git workflow and pull requests
16. Troubleshooting and FAQ
17. Summary

## 1. Introduction and project background

This repository, `quantit-reports-demo`, is a small but realistic example application
that was put together as the hands-on codebase for the "AI-Assisted Coding" workshop
delivered by Humai for the Quantit team. It is deliberately **not** a production
system. Instead, it is a minimal viable product (an MVP) that mirrors the kind of
project a small startup team might build in its first few weeks: a monthly reports
API written in Python with FastAPI and SQLAlchemy, backed by a relational database,
with a small React single-page application on top of it that renders the numbers in a
table. The domain is intentionally simple — aggregating transactions into monthly
totals — so that participants can focus on the *workflow* of working alongside an AI
coding assistant rather than on understanding a complex business domain.

Because this is a teaching repository, it intentionally contains some technical debt
and rough edges. Please do not "tidy up" or refactor these proactively: each of them
is the subject of a specific exercise during the workshop, and removing them ahead of
time would spoil those exercises. Only change something when the user explicitly asks
you to.

The project has been kept deliberately small so that it can be cloned, installed, and
run end to end in just a few minutes on a typical laptop, with or without Docker
installed.

## 2. Repository layout

The full directory tree of the repository is as follows:

```
quantit-reports-demo/
├── README.md
├── CLAUDE.md                      # this file
├── requirements.txt               # Python dependencies
├── Dockerfile                     # builds the API image
├── docker-compose.yml             # API + Postgres for local full-stack runs
├── railway.json                   # Railway deployment configuration
├── .env.example                   # example environment variables
├── .gitignore
├── app/                           # the FastAPI backend
│   ├── __init__.py
│   ├── main.py                    # FastAPI application and routes
│   ├── models.py                  # SQLAlchemy models
│   ├── db.py                      # database engine and session setup
│   ├── reports.py                 # report-building logic
│   ├── legacy_aggregator.py       # older aggregation module
│   └── seed.py                    # inserts sample data on startup
├── tests/                         # the pytest test suite
│   ├── __init__.py
│   ├── conftest.py                # fixtures (temp DB, TestClient)
│   ├── test_reports.py            # unit-ish tests
│   └── test_integration.py        # integration test against the API
├── frontend/                      # the React + Vite single-page app
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       └── App.jsx
├── .github/
│   ├── CODEOWNERS
│   └── pull_request_template.md
├── hooks-ejemplo/                 # example Claude Code hook (inert)
│   ├── guard.sh
│   └── settings.snippet.json
└── skills-ejemplo/                # example Claude Code skills (inert)
    ├── README.md
    ├── ops/SKILL.md
    ├── cli-wrapper/SKILL.md
    ├── read-logs/SKILL.md
    ├── db-explorer/SKILL.md
    └── knowledge-base/SKILL.md
```

## 3. Prerequisites and environment setup

To work on this project you will want the following installed on your machine:

- Python 3.11 or newer (the Docker image uses Python 3.11-slim).
- pip (comes with Python).
- Node.js 18 or newer, and npm, for the frontend.
- Docker Desktop, if you want to run the full stack with Postgres (optional).
- Git, for version control.

It is strongly recommended that you create and activate a Python virtual environment
before installing the Python dependencies, so that they do not pollute your global
Python installation. You can do this with the built-in `venv` module:

```bash
python3 -m venv .venv
source .venv/bin/activate     # on macOS/Linux
# .venv\Scripts\activate      # on Windows
```

Once the virtual environment is activated, install the dependencies (see section 4).

## 4. Running the backend (without Docker)

The fastest way to get the API running is to run it directly with uvicorn, using
SQLite as the database. SQLite requires no separate database server and stores its
data in a local file called `reports.db`, which is created automatically.

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The `--reload` flag makes uvicorn restart automatically whenever you change a source
file, which is convenient during development. The API will be available at
`http://localhost:8000`. There are two endpoints:

- `GET /health` returns a small JSON object indicating that the service is up.
- `GET /reports/monthly` returns the monthly totals as a JSON object keyed by month.

You can test them with curl:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/reports/monthly
```

## 5. Running the full stack (with Docker)

If you want to run the application the way it runs in production — that is, against a
real PostgreSQL database rather than SQLite — you can use Docker Compose. This will
build the API image from the `Dockerfile` and start two containers: one for the API
and one for Postgres.

```bash
docker compose up -d --build       # start in the background
docker compose ps                  # see container status
docker compose logs api            # view the API logs
docker compose logs api | tail -n 100   # view the last 100 log lines
docker compose down                # stop and remove the containers
```

Note that the first build can take a few minutes because it has to download the base
images and install the Python dependencies inside the container. After the first
build, subsequent runs are much faster because the layers are cached.

## 6. Running the frontend

The frontend is a small React application built with Vite. To run it:

```bash
cd frontend
npm install
npm run dev
```

This starts the Vite development server on `http://localhost:5173`. The page fetches
the monthly report from the backend and renders it in a table. The backend URL can be
configured through the `VITE_API_URL` environment variable; if it is not set, it
defaults to `http://localhost:8000`. You can also build a production bundle with
`npm run build`, and preview it with `npm run preview`.

## 7. Running the test suite

The tests are written with pytest. To run the whole suite:

```bash
python3 -m pytest -q
```

You can also run a single test file, or a single test, by passing its path:

```bash
python3 -m pytest tests/test_reports.py -q
python3 -m pytest tests/test_reports.py::test_health -q
```

Note that one test in the suite currently fails. This is expected and intentional —
it is part of the workshop exercises — and does not mean your environment is broken.
If `pytest` cannot import `fastapi` or other packages, make sure you have installed
the dependencies from `requirements.txt` into your active environment.

## 8. Architecture and module-by-module walkthrough

The backend lives in the `app/` package. A request to `GET /reports/monthly` flows
through the following modules:

- `app/main.py` defines the FastAPI application, configures logging and CORS, seeds
  the database on startup, and declares the two routes (`/health` and
  `/reports/monthly`). It wires the report endpoint to the report-building function.
- `app/reports.py` contains `monthly_report`, which queries all `Transaction` rows
  from the database, maps each row into a plain dictionary, and passes the list to the
  aggregation function.
- `app/legacy_aggregator.py` contains `aggregate_monthly`, an older function that
  sums the amounts per month and returns a dictionary keyed by month. It also contains
  some accumulated cruft from earlier versions of the project.
- `app/models.py` defines the single SQLAlchemy model, `Transaction`.
- `app/db.py` sets up the SQLAlchemy engine and session factory. It reads the database
  URL from the `DATABASE_URL` environment variable and falls back to a local SQLite
  database when that variable is not set.
- `app/seed.py` inserts a small set of sample transactions into the database. It is
  idempotent, meaning it can be run multiple times without inserting duplicates.

The frontend lives in `frontend/`. `src/main.jsx` mounts the React application, and
`src/App.jsx` contains the component that fetches the report and renders the table.

## 9. Data model and seed data

There is a single table, `transactions`, represented by the `Transaction` model in
`app/models.py`. It has the following columns:

- `id` — integer primary key.
- `month` — a string in the format `YYYY-MM`, for example `2026-01`.
- `category` — a free-text string describing the transaction category.
- `value` — a floating point number representing the amount of the transaction.

The seed data in `app/seed.py` inserts several transactions spread across three
months. The expected monthly totals, once everything is working correctly, are:
`2026-01` totals to 300, `2026-02` totals to 200, and `2026-03` totals to 300.

## 10. Environment variables

The application reads the following environment variables:

- `DATABASE_URL` — the SQLAlchemy connection string for the database. When it is not
  set, the application uses a local SQLite database stored in `reports.db`. When
  running under Docker Compose or on Railway, it is set to a PostgreSQL URL.
- `VITE_API_URL` — used by the frontend to know where the backend is. Defaults to
  `http://localhost:8000`.

An example file, `.env.example`, is provided. Copy it to `.env` and fill in any values
you need. The `.env` file is listed in `.gitignore` and must never be committed.

## 11. Dependencies

The Python dependencies are pinned in `requirements.txt`:

- `fastapi` — the web framework.
- `uvicorn[standard]` — the ASGI server used to run the application.
- `SQLAlchemy` — the ORM used to talk to the database.
- `psycopg2-binary` — the PostgreSQL driver, used when running against Postgres.
- `httpx` — used by the test client.
- `pytest` — the test runner.

The frontend dependencies are declared in `frontend/package.json`: `react`,
`react-dom`, `vite`, and `@vitejs/plugin-react`.

## 12. Deployment to Railway

The repository includes a `railway.json` configuration and a `Dockerfile`, so it can
be deployed to Railway. A typical first deployment looks like:

```bash
railway init                       # create a project
railway add --database postgres    # provision a Postgres database
railway up -d                      # deploy in the background
railway logs                       # watch the logs
```

## 13. Example skills and hooks

The `skills-ejemplo/` and `hooks-ejemplo/` directories contain example Claude Code
skills and an example hook. They are **inert** by default — that is, they are not
active just by being in the repository. They are there to be read and adapted. To
activate a skill, copy it into `.claude/skills/`. To activate the hook, copy the
relevant block from `hooks-ejemplo/settings.snippet.json` into `.claude/settings.json`
and make the script executable with `chmod +x hooks-ejemplo/guard.sh`.

## 14. Coding conventions and style

- Write clear, readable Python. Prefer explicit names over clever abbreviations.
- Keep functions small and focused on a single responsibility.
- Use type hints where they add clarity.
- Do not commit secrets. Anything sensitive goes in `.env`, which is gitignored.
- Match the style of the surrounding code when editing existing files.
- Keep the frontend simple; this is a demo, not a design showcase.
- Document non-obvious decisions with a short comment.

## 15. Git workflow and pull requests

- Create a feature branch for your work rather than committing to the main branch.
- Run the test suite before opening a pull request.
- Open pull requests using the template in `.github/pull_request_template.md` and fill
  in its checklist. The checklist is designed for AI-assisted pull requests: it asks
  you to confirm that imports actually exist, that no test was commented out, skipped,
  or marked `xfail` just to make the suite pass, and that the description matches the
  actual diff.
- The `CODEOWNERS` file requires review on certain sensitive files, including
  `app/legacy_aggregator.py`, `.env.example`, and `railway.json`.

## 16. Troubleshooting and FAQ

- **`uvicorn: command not found`** — your virtual environment is probably not
  activated, or the dependencies are not installed. Activate it and run
  `pip install -r requirements.txt`.
- **Tests cannot import `fastapi`** — same cause as above; install the dependencies.
- **Port already in use** — something else is already listening on port 8000 or 5173.
  Stop it, or run the server on a different port.
- **Docker build is slow** — the first build downloads images and installs packages
  inside the container; subsequent builds are cached and much faster.
- **One test always fails** — this is intentional and part of the exercises; it does
  not indicate a broken environment.

## 17. Summary

This repository is a small FastAPI + SQLAlchemy + React MVP used as the hands-on
codebase for the AI-Assisted Coding workshop. Run the backend with uvicorn (SQLite)
or with Docker Compose (Postgres), run the frontend with Vite, and run the tests with
pytest. It intentionally contains some technical debt that is the subject of the
workshop exercises, so please do not refactor it proactively. See the README for a
shorter overview.
