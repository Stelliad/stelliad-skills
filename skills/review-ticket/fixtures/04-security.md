## Objective

The password reset endpoint stops accepting unlimited attempts from a single
source, so an address cannot be enumerated or a reset link brute-forced.

## Why

The endpoint has no rate limit. It returns a different response for a known and
an unknown address, which makes it an account enumeration oracle, and the reset
token can be tried without bound. This is the finding a vendor security review
raises first, and it is cheap to fix now.

## Acceptance Criteria

- [ ] The endpoint returns an identical response and timing for a known and an unknown address
- [ ] Requests beyond the configured per-source threshold receive 429
- [ ] Requests beyond the configured per-address threshold receive 429
- [ ] A rejected request is logged with the source, without the address in plaintext
- [ ] A legitimate reset within the threshold still succeeds end to end

## Scope

**In:** the password reset request and confirm endpoints.
**Out:** login rate limiting, the reset email's content, and the token format.

## Risk

`High`. Touches authentication and the account recovery path, so a defect
either locks real users out of recovery or leaves the enumeration open.

## Verification

- A known and an unknown address produce byte-identical responses
- The threshold is reached and 429 is returned
- A normal reset still completes

## References

`docs/security/security-model.md`
