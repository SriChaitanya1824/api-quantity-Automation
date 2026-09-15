# Authentication Test Cases

| ID | Title | Requirement | Type | Priority | Preconditions | Test Data | Steps | Expected Result |
|---|---|---|---|---|---|---|---|---|
| AUTH-001 | Register valid user | Users can create accounts | API/UI Functional | High | App running | Unique valid user | Submit registration | 201/API success message; no password returned |
| AUTH-002 | Duplicate registration | Emails must be unique | API/UI Negative | High | User exists | Existing email | Register same email | 409 or visible duplicate error |
| AUTH-003 | Invalid email rejected | Email format validated | API/UI Negative | High | App running | `not-an-email` | Submit registration | Validation error |
| AUTH-004 | Short password rejected | Password minimum enforced | API/UI Boundary | High | App running | `short` | Submit registration | Validation error |
| AUTH-005 | Login valid user | Users can authenticate | API/UI Smoke | Critical | Seeded user exists | Valid credentials | Submit login | Token returned / dashboard visible |
| AUTH-006 | Incorrect password rejected | Auth must reject bad secrets | API/UI Negative | Critical | User exists | Wrong password | Submit login | 401 or visible login error |
| AUTH-007 | Unknown user rejected | Auth must not reveal accounts | API Negative | High | App running | Unknown email | Submit login | 401 generic error |
| AUTH-008 | Missing credentials rejected | Required fields enforced | API/UI Negative | High | App running | Missing password | Submit login | Validation error |
| AUTH-009 | Invalid JWT rejected | Protected routes require valid token | API Negative | Critical | App running | Bad bearer token | Call profile | 401 invalid token |
| AUTH-010 | Logout clears session | Users can end session | UI Functional | Medium | Logged in | N/A | Click logout | Login form visible |
