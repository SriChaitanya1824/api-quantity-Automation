# Contributing

Use a normal pull-request workflow for application and test-code changes.

```text
Feature branch
  ↓
Implementation
  ↓
Tests
  ↓
Commit
  ↓
Pull Request
  ↓
CI
  ↓
Code Review
  ↓
Address feedback
  ↓
Merge
```

## Branch Names

- `feature/api-request-tests`
- `feature/playwright-login-tests`
- `fix/flaky-request-test`
- `test/add-performance-suite`

## Local Checks

```bash
python3 -m ruff check .
python3 -m black --check .
python3 -m pytest -m api
cd frontend && npm ci && npm run build
```

For UI work, start the full app and run:

```bash
python3 -m pytest -m ui --browser chromium --tracing retain-on-failure --screenshot only-on-failure
```

## Review Expectations

- Test changes receive the same review as application changes.
- Do not weaken assertions to make failures disappear.
- Attach logs, screenshots, traces, or report snippets when discussing failures.
- Keep test data repeatable and avoid real secrets.
