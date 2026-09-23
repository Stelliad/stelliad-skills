## Objective

An inactive administrator session ends on its own instead of staying valid
indefinitely, so an unattended admin browser stops being a standing route into
the account.

## Why

Admin sessions currently never expire. A logged-in admin tab left open on a
shared or lost machine keeps full administrative access with no time bound,
which is the finding a vendor security review will raise first.

## Context

Admin auth runs through the existing identity provider. Refresh-token issue and
rotation already work and are not the problem; the gap is that nothing ever
invalidates an idle session.

## Acceptance Criteria

- [ ] An admin session with no request for the configured idle window is invalidated server-side
- [ ] A request on an invalidated session returns 401
- [ ] The web client redirects a 401 on an admin route to the login screen with the return path preserved
- [ ] Activity within the idle window extends the session without forcing re-authentication
- [ ] A standard (non-admin) user session is unaffected
- [ ] The idle window is read from configuration, not hardcoded

## Scope

**In:** admin session expiry, the API behaviour on an expired session, and the
web client's redirect.

**Out:** the login screen's design, the refresh-token format, and session policy
for non-admin users.

## Constraints

Must use the existing identity provider. Must not change the refresh-token
format, which other clients depend on.

## Risk

`High`. Touches authentication for the highest-privilege role, so a defect
either locks admins out or leaves the gap open.

## Verification

- An admin session idle past the window returns 401 on the next request
- An admin session kept active past the window is still valid
- Existing non-admin login is unchanged

## References

`docs/security/security-model.md`
