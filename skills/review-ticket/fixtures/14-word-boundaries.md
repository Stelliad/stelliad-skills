## Objective

A webhook delivered to the wrong tenant's endpoint is rejected before any
handler runs, instead of being processed under the receiving tenant.

## Why

Signature verification checks that a webhook is signed, not that it is signed
for this tenant, so the service does not reject a misrouted delivery correctly.
One misconfigured integration has already written events into another tenant.

## Acceptance Criteria

- [ ] A webhook signed with another tenant's secret receives 401 and no handler runs
- [ ] An incorrectly routed delivery is logged with both tenant identifiers
- [ ] A webhook signed with the receiving tenant's secret is processed as before

## Scope

**In:** webhook signature verification and the rejection path.
**Out:** the signing scheme, secret rotation, and the handlers themselves.

## Risk

`High`. Touches the tenant isolation boundary, so a defect either drops valid
webhooks or keeps the leak open.
