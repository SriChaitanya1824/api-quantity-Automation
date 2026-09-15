# Services Test Cases

| ID | Title | Requirement | Type | Priority | Preconditions | Test Data | Steps | Expected Result |
|---|---|---|---|---|---|---|---|---|
| SVC-001 | Retrieve service catalog | Employees can view services | API/UI Smoke | High | Logged in | Valid token | GET/open services | Active services shown |
| SVC-002 | Validate service schema | Service data is structured | API Functional | High | Logged in | N/A | GET services | id/name/category/description/active present |
| SVC-003 | Retrieve one service | Service details available | API Functional | Medium | Logged in | Valid ID | GET service by ID | Matching service returned |
| SVC-004 | Invalid service ID | Bad IDs handled | API Negative | Medium | Logged in | `99999` | GET service by ID | 404 service not found |
| SVC-005 | Auth required | Catalog is protected | API Negative | High | None | No token | GET services | 401 authentication required |
