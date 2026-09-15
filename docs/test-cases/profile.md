# Profile Test Cases

| ID | Title | Requirement | Type | Priority | Preconditions | Test Data | Steps | Expected Result |
|---|---|---|---|---|---|---|---|---|
| PROF-001 | View current profile | User can view own profile | API/UI Smoke | High | Logged in | Valid token | Open profile/get `/me` | Correct user fields returned |
| PROF-002 | Update profile | User can update allowed fields | API/UI Functional | High | Logged in | New name/department | Save profile | Updated values persist |
| PROF-003 | Reject short name | Name has minimum length | API/UI Boundary | Medium | Logged in | `A` | Save profile | Validation error |
| PROF-004 | Reject invalid type | Payload types validated | API Negative | Medium | Logged in | Numeric full name | PUT profile | 422 validation error |
| PROF-005 | Missing auth rejected | Profile is protected | API Negative | Critical | None | No token | GET `/me` | 401 authentication required |
