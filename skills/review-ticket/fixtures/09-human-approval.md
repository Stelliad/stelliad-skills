## Objective

The `events` table stops growing without bound by dropping rows older than the
configured retention window.

## Why

The table is 400GB and adds 8GB a week. Query latency on the dashboard has
tripled in three months and the storage cost line is now the largest single
item in the bill.

## Acceptance Criteria

- [ ] Rows older than the configured retention window are removed on a schedule
- [ ] The retention window is read from configuration, not hardcoded
- [ ] The deletion runs in bounded batches and does not hold a long transaction
- [ ] The dashboard's queries return the same results for data inside the window
- [ ] The job records how many rows it removed on each run
- [ ] A dry run mode reports what would be deleted without deleting it

## Scope

**In:** retention on the `events` table.
**Out:** every other table, the retention window's value (a separate
decision, already made and recorded), and archiving deleted rows elsewhere.

## Risk

`Critical`. Irreversible deletion of production data. A wrong window or a wrong
predicate destroys rows that cannot be recovered from the application.

## Human Approval

The first production run, and any change to the retention predicate. An agent
may build the job, the dry run, and the tests, and may run the dry run against
a restored snapshot. It may not run the deletion against production.

## Verification

- The dry run against a restored snapshot reports the expected row count
- Dashboard queries return identical results for in-window data
- A single batch completes without exceeding the statement timeout
