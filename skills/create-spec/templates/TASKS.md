---
spec: SPEC-[NNN]
status: draft
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
---

# Tasks: SPEC-[NNN]

Execution state for this spec. A fresh session resumes work by reading this
file's checkbox state and the Requirement Traceability table below, nothing
else. Task IDs (`T001`, `T002`, ...) are sequential across the whole spec, not
reset per phase, so a task is never ambiguous when cited elsewhere.

Every task carries the same three lines: the spec IDs it serves (any prefix),
the task IDs it depends on, and the command that proves it.

## Phase 1: [name]

- [ ] T001 [task description]
  - Requirements: REQ-xxx, AC-xxx
  - Depends on: None
  - Verification: `[actual command]`

## Phase 2: [name]

## Final Verification

Run each applicable check fresh, read the exit code and the full output, and
record passing-with-evidence or failing-with-evidence under Verification
Evidence, never "probably passes". The `verify-done` skill does exactly this.
Delete the rows that do not apply to this spec's target rather than leaving an
unchecked box for something that was never applicable.

- [ ] Acceptance criteria pass
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] End-to-end tests pass
- [ ] Security requirements verified
- [ ] AI evaluation suite passes (golden, regression, safety)
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Build passes
- [ ] Infrastructure validation passes
- [ ] Documentation updated
- [ ] Independent review completed (`review-spec`)

## Verification Evidence

Never fabricate a result. A check with no fresh output behind it is not
checked.

### [T001 or check name]

Command:

```
[actual command]
```

Result:

```
[actual output, or a PASS/FAIL summary with the count, e.g. "PASS, 12/12"]
```

## Requirement Traceability

One row per ID in the spec, every prefix. An ID with no row is a requirement
the plan has silently dropped. Cite an ID from another spec as
`SPEC-{NNN}/{ID}`.

| Requirement | Task | Implementation | Verification | Status |
|---|---|---|---|---|
| REQ-001 | T001 | [path/file] | [test or command] | NOT STARTED |

Status values, and only these: `NOT STARTED`, `IN PROGRESS`, `PASS`, `FAIL`,
`BLOCKED`, `N/A`. A row reads `PASS` only when a matching entry exists under
Verification Evidence above; a status changed without evidence is a claim, not
a result.

## Review Findings

Where a conflict with the spec is recorded during implementation, and where
`review-spec` writes its findings, most severe first. Severity: `CRITICAL`,
`HIGH`, `MEDIUM`, `LOW`, `INFO`.

| Severity | Finding | File | Source | Status |
|---|---|---|---|---|
