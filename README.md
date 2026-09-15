# Brivo QA Automation Platform

Production-style QA automation portfolio project for an internal Employee Access & Service Management Portal. The application is intentionally small; the main focus is the automated quality engineering framework around it.

## Architecture

```text
Browser
  |
  v
React + TypeScript + Vite
  |
  v
FastAPI REST API
  |
  v
PostgreSQL
```

```text
Developer
  |
  v
GitHub Pull Request
  |
  v
GitHub Actions
  |
  +-- Static Checks
  +-- API Tests
  +-- UI Tests
  +-- Performance Smoke Import Check
  |
  v
Reports / Screenshots / Traces / JUnit XML
```

## Stack

- Backend: Python, FastAPI, SQLModel, JWT auth
- Frontend: React, TypeScript, Vite
- Database: PostgreSQL for app runtime, SQLite override for API tests
- API automation: PyTest + reusable HTTP client
- UI automation: Playwright Python + Page Object Model
- Performance: Locust
- CI/CD: GitHub Actions
- Quality: Ruff, Black, PyTest reports

## Features Under Test

- Register/login/logout
- Protected profile read/update
- Service catalog browsing
- Service request create/list/filter/update/cancel
- Negative validation for invalid credentials, invalid IDs, missing fields, invalid auth, and invalid state transitions

## Repository Structure

```text
backend/                  FastAPI app
frontend/                 React/Vite app
tests/api/                API regression tests
tests/ui/                 Playwright UI tests
tests/performance/        Locust smoke scenario
tests/utils/              API client, assertions, data generation
pages/                    Playwright Page Objects
docs/test-cases/          Manual/automated test case design
docs/defects/             Representative defect records
.github/workflows/        CI pipelines
reports/                  Local generated reports, git-ignored
```

## Run The App

```bash
docker compose up --build
docker compose --profile tools run --rm seed
```

- UI: http://localhost:5173
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

Seeded login:

- Email: `qa.user@example.com`
- Password: `Password123!`

Docker was not available in this local shell, so the integrated Docker runtime was not verified here.

## Run API Tests

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -m api --junitxml=reports/api-junit.xml --html=reports/api-report.html --self-contained-html
```

Latest verified local result: 40 passed, 0 failed, 0 skipped, 12.12 seconds.

## Run UI Tests

Start and seed the app first, then:

```bash
python3 -m playwright install chromium
python3 -m pytest -m ui --browser chromium --tracing retain-on-failure --screenshot only-on-failure
```

UI tests use Page Objects in `pages/` and stable `data-testid` selectors.

## Run Performance Smoke

```bash
locust -f tests/performance/locustfile.py --headless -u 5 -r 1 -t 1m --host http://localhost:8000
```

Do not treat local Locust numbers as production capacity.

## Useful Test Filters

```bash
pytest -m smoke
pytest -m regression
pytest -m api
pytest -m ui
pytest -m performance
```

## Reports And Artifacts

- JUnit XML: `reports/api-junit.xml`
- HTML report: `reports/api-report.html`
- Playwright screenshots/traces: `test-results/`
- CI uploads reports and failure artifacts with `actions/upload-artifact`.

## Documentation

- [Test Strategy](docs/test-strategy.md)
- [Exploratory Testing](docs/exploratory-testing.md)
- [CI Failure Triage](docs/ci-failure-triage.md)
- [Performance Testing](docs/performance-testing.md)
- [Test Execution Report](docs/test-execution-report.md)
- [Defects](docs/defects/BUG-001.md)

## Future Improvements

- Add migrations with Alembic.
- Add admin role workflows for approving/completing requests.
- Split frontend components as the UI grows.
- Run browser tests across Chromium, Firefox, and WebKit in scheduled CI.
# api-quantity-Automation
