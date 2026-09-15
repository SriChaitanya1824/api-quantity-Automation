# CI Failure Triage

```text
CI failure
  ↓
Inspect logs and artifacts
  ↓
Reproduce locally
  ↓
Check application/API behavior
  ↓
Check test reliability
  ↓
Check environment and infrastructure
  ↓
Classify
  ↓
Fix / Defect / Retry
```

## Classifications

- Genuine product defect: app behavior violates requirement. Example: duplicate registration returns 201 instead of 409. Action: file defect and fix app.
- Test automation defect: test expectation or setup is wrong. Example: test uses stale selector. Action: fix Page Object/test.
- Flaky test: behavior passes on retry without app changes due to timing/data race. Example: UI click before dashboard loaded. Action: add deterministic wait.
- Environment/configuration failure: wrong `DATABASE_URL`, missing `JWT_SECRET`, service unavailable. Action: fix config and rerun.
- Infrastructure failure: CI runner/network/browser install issue. Action: inspect runner logs and retry after infra recovery.

Evidence should include logs, screenshots/traces for UI, API response bodies, and local reproduction notes.
