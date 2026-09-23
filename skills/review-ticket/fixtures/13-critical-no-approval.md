## Objective

Customer records deleted more than thirty days ago are purged from the primary
database and its read replicas, not only soft-deleted.

## Why

Deleted customers stay in the database indefinitely behind a `deleted_at`
flag. The privacy notice promises removal within thirty days, and today that
promise is not kept anywhere.

## Acceptance Criteria

- [ ] A customer soft-deleted more than thirty days ago has no row in the primary database
- [ ] The same customer has no row on any read replica after replication catches up
- [ ] A customer soft-deleted less than thirty days ago is untouched
- [ ] Each purge run records how many customers it removed

## Scope

**In:** purging soft-deleted customer rows and their dependent rows.
**Out:** backups, the analytics warehouse, and the soft-delete flow itself.

## Risk

`Critical`. Irreversible deletion of customer data in production. A wrong
predicate removes live customers.

## Human Approval

None
