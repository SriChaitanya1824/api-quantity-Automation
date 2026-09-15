# Test Execution Report

## Latest Verified Run

- Date: 2026-09-15
- Environment: Local shell, Python 3.9.6, FastAPI TestClient, SQLite test override.
- Command: `python3 -m pytest -m api --junitxml=reports/api-junit.xml --html=reports/api-report.html --self-contained-html`
- Result: 40 passed, 0 failed, 0 skipped; 19 UI tests deselected by marker.
- Duration: 13.09 seconds.
- Reports: `reports/api-junit.xml`, `reports/api-report.html`.

## Not Verified In This Environment

- Docker Compose runtime: Docker command unavailable.
- UI tests: 19 tests collected successfully with `python3 -m pytest -m ui --collect-only`; full execution requires running frontend/backend and Playwright browser binaries.
- Locust performance smoke: implemented, not executed against a running backend.
