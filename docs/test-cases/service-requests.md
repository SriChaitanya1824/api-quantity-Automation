# Service Request Test Cases

| ID | Title | Requirement | Type | Priority | Preconditions | Test Data | Steps | Expected Result |
|---|---|---|---|---|---|---|---|---|
| REQ-001 | Create request | User can request a service | API/UI Smoke | Critical | Logged in, service exists | Valid request | Submit request | 201/open request visible |
| REQ-002 | List requests | User can view own requests | API/UI Functional | High | Request exists | Valid token | GET/open requests | Created request listed |
| REQ-003 | Retrieve one request | User can inspect request | API Functional | High | Request exists | Request ID | GET request | Matching ID/title returned |
| REQ-004 | Update request | Editable requests can change | API Functional | Medium | Open request | New title | PUT request | Updated fields returned |
| REQ-005 | Cancel request | User can cancel eligible request | API/UI Functional | High | Open request | Request ID | DELETE/click cancel | Status becomes cancelled |
| REQ-006 | Filter by status | User can filter requests | API/UI Functional | Medium | Mixed statuses | `cancelled` | Filter requests | Only matching statuses shown |
| REQ-007 | Invalid request ID | Bad IDs handled | API Negative | High | Logged in | `99999` | GET request | 404 request not found |
| REQ-008 | Cross-user access denied | Users cannot view others' requests | API Security | Critical | Two users | Other request ID | GET request | 404 not found |
| REQ-009 | Employee cannot complete | Invalid transition blocked | API Negative | High | Open request | `completed` | PUT status | 403 forbidden |
| REQ-010 | Cancelled cannot update | Terminal-ish state protected | API Regression | High | Cancelled request | New title | PUT request | 409 conflict |
| REQ-011 | Missing required fields | Payload required fields enforced | API Negative | High | Logged in | Missing title | POST request | 422 validation error |
| REQ-012 | Boundary accepted | Max lengths supported | API Boundary | Medium | Logged in | 160 title/1000 desc | POST request | Request created |
