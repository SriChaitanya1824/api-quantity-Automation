# Test Strategy

## Scope

The Brivo QA Automation Platform validates an Employee Access & Service Management Portal through API, UI, exploratory, regression, and performance smoke testing.

## Test Categories

- Functional testing: verifies registration, login, profile updates, service catalog browsing, and service request workflows.
- API testing: validates REST status codes, JSON schemas, field values, auth behavior, and business rules.
- UI testing: validates user workflows through the browser using Playwright Page Objects and stable `data-testid` selectors.
- Smoke testing: covers critical login, service retrieval, request creation, and basic navigation.
- Regression testing: protects previously validated behavior after app or test changes.
- Negative testing: covers invalid credentials, malformed payloads, missing auth, invalid IDs, and forbidden transitions.
- Boundary testing: checks minimum and maximum accepted field lengths.
- Exploratory testing: uses charters to find usability, edge-case, and workflow risks before automation.
- Performance testing: uses Locust for local smoke-level API traffic, not production capacity claims.
- CI testing: runs automated checks on pull requests and uploads reports/artifacts.

## Environments

- Local API tests use an isolated SQLite database through FastAPI dependency overrides.
- Docker Compose is the intended local integrated runtime for PostgreSQL-backed app testing.
- UI tests expect the backend, frontend, and seed data to be running.

## Reporting

PyTest generates console output, JUnit XML, and HTML reports. Playwright is configured in CI to capture traces and screenshots on failure.
