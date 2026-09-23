### Type

Security

### Objective

An inactive administrator session ends on its own instead of staying valid
indefinitely, so an unattended admin browser stops being a standing route in.

### Why

Admin sessions currently never expire. A logged-in admin tab left open on a
shared machine keeps full administrative access with no time bound.

### Acceptance criteria

- [ ] An admin session idle past the configured window is invalidated server-side
- [ ] A request on an invalidated session returns 401
- [ ] The web client redirects a 401 on an admin route to the login screen
- [ ] Activity within the window extends the session without re-authentication

### Scope

**In:** admin session expiry and the client redirect.

**Out:** the login screen design and the refresh-token format.

### Risk

High

### Why this risk level

Touches authentication for the highest-privilege role, so a defect either locks admins out or leaves the gap open.

### Context, constraints, and dependencies

Must use the existing identity provider.

### Verification

- An admin session idle past the window returns 401 on the next request

### Human approval required

_No response_
