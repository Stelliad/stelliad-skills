---
name: plan-spec
description: Read a ready SPEC.md, inspect the repository it governs, and write PLAN.md and TASKS.md beside it, every task carrying its requirement IDs, its dependencies and a verification command that actually exists in the repo. Never modifies application code. Halts and reports the gap if the spec is not ready. Use when saying "plan-spec", "plan out SPEC-X", "write the implementation plan for X", "break this spec into tasks", or "/plan-spec <id-or-path>".
license: MIT
compatibility: Any repository. Reads specs from create-spec or recover-spec, and writes the plan and task list in the shape implement-spec reads, from create-spec's templates. Spec location, requirement prefixes and the standards a plan must respect adapt via CUSTOMIZE.md.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
  argument-hint: "<spec-id | path-to-SPEC.md>"
type: skill
scope: all
status: active
---

# plan-spec

The second step of the spec loop. Turns an approved `SPEC.md` into a plan
grounded in the actual repository, and a task list a fresh session can resume
cold. The repository inspection is the point: a plan written from memory of how
these things usually look is a guess with headers.

It writes two documents and **touches no application code.** It won't plan
against a spec that isn't ready.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the Ready gate, the inspection and the task shape
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to bind the spec location and the standards files your plan must respect
3. Run it on one ready spec and check every verification command it wrote by running it yourself

## Arguments

- `$1`: a spec ID (`004`, `SPEC-004`, `004-session-expiry`) or a path to a
  `SPEC.md`. A path is how a whole-system spec from
  [recover-spec](../recover-spec/SKILL.md) gets planned in place at the
  repository root. A change to a recovered system goes through
  [create-spec](../create-spec/SKILL.md) first.

## What it does

1. Finds the spec and gates on it: not ready means stop and report why
2. Inspects the code the spec touches: stack, runners, patterns, prior art
3. Writes `PLAN.md` from [create-spec's template](../create-spec/templates/PLAN.md), citing what it read
4. Writes `TASKS.md` from [the task template](../create-spec/templates/TASKS.md): atomic tasks, each with requirement IDs, dependencies and a real command
5. Fills the traceability table with one row per spec ID, and reports anything the repo has no pattern for

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). A plan is only as good as
its verification commands, and a command that runs green while proving nothing
looks exactly like one that proves something.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
