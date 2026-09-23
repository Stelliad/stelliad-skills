---
name: recover-spec
description: Work backwards from an existing codebase to the specification nobody wrote. Fixes the system boundary, inventories every surface, traces the core data path end to end, recovers the data model and its unenforced invariants, and reads the tests as the only stated requirements the system has. Grades every statement observed, inferred, intended, undecided, or contradiction, and returns the undecided list as the questions to put to whoever owns the system. Use when saying "work backwards to a spec", "there's no spec for this", "write the spec from the code", "what does this system actually do", "document this before we change it", or before planning work on a codebase you didn't build.
license: MIT
compatibility: Any repository with code, tests and version history. Reads infrastructure-as-code where present. Read-only on the code always, and reads secret names, never values. Output location, grade markers and question format adapt via CUSTOMIZE.md.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
  argument-hint: "<repo-path> [--as-spec|--as-reading] [--subsystem <name>] [--against <ref>] [--questions-only]"
type: skill
scope: all
status: active
---

# recover-spec

Most skills that work from a spec assume the spec exists. Most inherited systems
arrive without one. This skill recovers the specification from the artifact, and
grades every statement by what it rests on, so a description of the code never
gets mistaken for a statement of what the code must do.

It **reads**. It never changes the code, never fixes what it finds, and never
decides which behaviour was intended.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the grades, the procedure and the rules
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to bind the output location, the grade markers and who answers the questions
3. Run it with `--questions-only` first if you have a conversation with the system's owner coming up

## Arguments

- `$1`: repository path (required)
- `--as-spec`: write `SPEC.md` into the repo, where it will govern future work
- `--as-reading`: write a dated reading outside the governed tree, recording what you found. **This is the default** when neither flag is given
- `--subsystem <name>`: recover one subsystem. With `--as-spec` it goes to `docs/specs/{name}.md`; as a reading it goes beside the whole-system reading (`docs/readings/{name}-spec-{YYYYMMDD}.md`). Run after a whole-system pass, never instead of one
- `--against <ref>`: pin the reading to a branch, tag or SHA. Defaults to `HEAD`, recorded either way
- `--questions-only`: skip the document and return the undecided list alone

## What it does

1. Pins the reading to a commit and records whether the tree was clean
2. Fixes the system boundary: what's in, what's out, what nobody has declared
3. Inventories every surface where work enters, leaves or persists
4. Traces the core data path end to end, one hop at a time
5. Recovers the data model and the invariants the code assumes but doesn't enforce
6. Reads the tests as the system's only stated requirements
7. Finds behaviour nobody owns, and promises nothing implements
8. Writes the spec per [references/spec-skeleton.md](./references/spec-skeleton.md), grades every statement, and hands it to a document quality review

## The grades

| Grade | Means |
|---|---|
| **Observed** | The path was read end to end, or exercised by a test |
| **Inferred** | One reading says this. Nothing exercises it |
| **Intended** | A comment, README, ticket or contract says so. The code may disagree |
| **Undecided** | The code makes a choice and nothing records whether it was a decision |
| **Contradiction** | Two parts of the system disagree, or code and docs disagree |

**A run with zero undecideds has failed.** No real system is fully specified by
its source. A clean question list means the run stopped at description.

## Downstream

The recovered spec is not yet a plan. Answer the undecideds with the owner, turn
the settled requirements into a task list with verification commands, and then
[implement-spec](../implement-spec/SKILL.md) can work it forward. No skill in
this collection writes that plan and task list: you write them, by hand or with
your own planner, in the shape [implement-spec's CUSTOMIZE.md](../implement-spec/CUSTOMIZE.md)
sections 1 and 2 describe (`PLAN.md` and `TASKS.md` beside the spec, requirement
IDs, and per task a dependency list and a verification command).

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). The grades are only as
honest as the discipline behind them, and nothing in the output will look
different if a grade was promoted to make the document read better.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
