# Regression Suite

Regression coverage maps to automated markers:

- `pytest -m smoke`: critical login, service retrieval, request creation, and profile basics.
- `pytest -m api`: full API regression suite.
- `pytest -m ui`: browser workflow regression suite against a running app.
- `locust --headless`: local performance smoke traffic.

Representative regression scenarios:

| ID | Scenario | Automation |
|---|---|---|
| REG-001 | Duplicate email stays blocked | API/UI |
| REG-002 | Invalid JWT cannot access profile | API |
| REG-003 | Request cancellation preserves status | API/UI |
| REG-004 | Cancelled requests cannot be edited | API |
| REG-005 | Service catalog fields remain stable | API/UI |
