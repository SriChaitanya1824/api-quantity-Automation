# Exploratory Testing Sessions

## Session 1: Authentication

- Testing Charter: Explore account creation, login, logout, and auth error messaging.
- Environment: Local Docker Compose target, seeded database.
- Feature: Authentication.
- Areas Explored: Duplicate emails, malformed emails, short passwords, wrong password, session persistence.
- Test Ideas: Refresh after login, use expired/bad token, register with edge-length names.
- Observations: Generic login error is good for security; registration needs clear duplicate feedback.
- Risks: Weak client validation could create confusing form states.
- Potential Defects: Duplicate registration error not displayed in UI.
- Automation Candidates: Duplicate registration UI test, invalid JWT API test.

## Session 2: Profile

- Testing Charter: Explore profile display and editable fields.
- Environment: Local app with seeded user.
- Feature: Profile.
- Areas Explored: Minimum length, maximum length, persistence after refresh, unauthorized access.
- Test Ideas: Submit one-character name, update department to long value, call API without token.
- Observations: API correctly restricts profile access to authenticated users.
- Risks: UI may not display backend validation if client-side validation is incomplete.
- Potential Defects: Validation message could be missed by screen readers if not tied to fields.
- Automation Candidates: Profile update API/UI tests and boundary API tests.

## Session 3: Service Requests

- Testing Charter: Explore request lifecycle from creation to cancellation.
- Environment: Local app with seeded services.
- Feature: Service Requests.
- Areas Explored: Create, list, filter, cancel, invalid IDs, cross-user isolation.
- Test Ideas: Cancel same request twice, update cancelled request, access another user's request.
- Observations: Returning 404 for another user's request avoids leaking object existence.
- Risks: Shared seeded UI user can accumulate old requests during manual testing.
- Potential Defects: Request list could become noisy without a test-data reset.
- Automation Candidates: Cross-user API test, cancelled-update regression test.
