# Spec Execution: Customization Guide

## Before you start

This skill is shaped around a spec that carries three things: requirements with
IDs, tasks with dependencies, and a verification command per task. If your specs
carry those under different names, bind them below and everything else follows.
If they carry none of them, fix the specs first; this cannot verify what a task
never said it would prove.

## Customization 1: File names and layout

**Where it is used:** SPEC.md, *The state it reads*.

```
Spec document:      <e.g. SPEC.md, requirements.md, the ticket itself>
Plan document:      <e.g. PLAN.md, or "none: tasks carry their own order">
Task list:          <e.g. TASKS.md, a project board, a checklist in the ticket>
Where they live:    <e.g. specs/{id}-{slug}/>
```

**If you skip it:** the skill looks for the shipped names, `SPEC.md`,
`PLAN.md` and `TASKS.md` in one spec folder, and stops if they are not there.
`TASKS.md` is a checklist, one task per line, each carrying its ID, the
requirement IDs it serves, the task IDs it depends on, and its verification
command:

```
- [ ] T003 Reject expired tokens (REQ-004; depends: T001, T002)
      verify: uv run pytest tests/test_auth.py -k expired
```

A spec recovered from existing code with
[recover-spec](../recover-spec/SKILL.md) arrives as a `SPEC.md` only: write the
plan and the task list before running this.

## Customization 2: The ID scheme

**Where it is used:** SPEC.md, steps 1, 2 and 5.

```
Requirement IDs:  <e.g. REQ-001, or "GitHub issue numbers">
Task IDs:         <e.g. T001>
Other prefixes:   <security, privacy, infrastructure, whatever you use>
Traceability:     <a table in the task list / a column on the board / none>
```

**If you skip it:** requirement status is recorded in prose, which is harder to
audit later.

## Customization 3: Evidence format

**Where it is used:** SPEC.md, step 5.

Decide what "the evidence" looks like in your repository, because this is what
makes the record worth keeping:

```
Where:      <a section in the task list / a file per task / the PR body>
Contains:   <the command, its output, the date>
How much:   <full output / the summary line / the failing lines only>
```

**If you skip it:** evidence goes into the task list under the task, verbatim.

## Customization 4: The test-first and verification steps

**Where it is used:** SPEC.md, steps 3 and 4.

This skill delegates both. Name what it delegates to:

```
Test-first cycle:   <the test-first skill, your own TDD guide, or a house rule>
Verification gate:  <the verify-done skill, a CI job, a checklist>
Retry cap:          <how many fix-and-recheck attempts before stopping>
```

The two companion skills in this repository are built for this: `test-first`
produces the evidence and `verify-done` refuses the claim without it.

**If you skip it:** the cycle is followed inline, without the cap.

## Customization 5: What to do when the spec is wrong

**Where it is used:** SPEC.md, *When the spec is wrong*.

```
Findings go:     <a section in the task list / a comment on the ticket / an issue>
Who rules:       <a person or a role, not "the team">
While waiting:   <continue with other tasks / stop the run>
```

**Name a person.** A conflict recorded with no owner is a conflict that waits.

**If you skip it:** findings are written into the task list and reported, and
the run continues with other tasks.

## Customization 6: Scope discipline

**Where it is used:** SPEC.md, rule 3.

Teams differ on what a task may touch. Write yours:

```
In scope:    <the files the task names / the package it lives in>
Out:         <formatting, unrelated refactors, dependency bumps>
Where a discovered problem goes: <a new task / an issue / a TODO with an owner>
```

**If you skip it:** anything outside the current task becomes a finding, which
is the conservative reading.

## Customization 7: Commits and review

**Where it is used:** the whole loop.

- One commit per task, or one per phase?
- Does the record update ride in the same commit as the code?
- Is a pull request opened per task, per phase, or per spec?

**If you skip it:** the work lands however your repository's habit dictates,
which is usually fine and occasionally produces an unreviewable diff.

## Final checklist

- [ ] Document names and location are bound
- [ ] ID scheme and where traceability lives are set
- [ ] Evidence format and location are decided
- [ ] The test-first cycle and verification gate are named, with a retry cap
- [ ] Findings have a home and a named person who rules on them
- [ ] Scope discipline is written down
- [ ] Commit and review granularity is agreed

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The trigger and the two responsibilities |
| `SPEC.md` | The loop, the record, the stop conditions, limitations |
| `CUSTOMIZE.md` | This file: names, IDs, evidence, delegation, scope |
