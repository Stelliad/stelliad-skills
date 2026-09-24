---
name: create-spec
description: Scaffold a new feature spec from an idea, writing SPEC.md into its own numbered folder (default specs/{NNN}-{slug}/) from the shipped template, with what was actually said filled in and what was not left open as questions. Stops there, as a draft; no plan, no tasks, no code. For a codebase that already runs with no written spec, use recover-spec instead. Use when saying "create-spec", "new spec for X", "spec out this feature", "start a spec", "scaffold a spec", or "/create-spec <name>".
license: MIT
compatibility: Any repository. Ships the SPEC.md, PLAN.md and TASKS.md templates that plan-spec, implement-spec and review-spec read. Spec location, ID scheme and requirement prefixes adapt via CUSTOMIZE.md.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
  argument-hint: "<feature-name>"
type: skill
scope: all
status: active
---

# create-spec

The first step of the spec loop. Turns an idea into a `SPEC.md` in its own
folder, and nothing else. The spec leaves as a `draft`, with every gap it could
not honestly fill listed as an open question for a named person.

If the idea already has running code behind it, this is the wrong skill:
[recover-spec](../recover-spec/SKILL.md) reads the code backwards instead of
writing intent forwards.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the procedure, the rules and why the draft stays a draft
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to bind the spec location, the ID scheme and the requirement prefixes
3. Run it on one small feature and read the Open Questions it wrote before trusting the rest

## Arguments

- `$1`: feature name, lowercase and hyphenated (required). Becomes the folder
  slug, as in `specs/004-session-expiry/`.

## What it does

1. Assigns the next spec number, never reusing one
2. Creates the spec folder and copies [templates/SPEC.md](./templates/SPEC.md) into it
3. Fills Summary, Problem, Goals and Non-Goals from what was actually said
4. Leaves requirements it has no basis for as open rows, and lists what is missing under Open Questions
5. Reports what stands between the draft and `ready`

## The loop

| Step | Skill | Writes |
|---|---|---|
| Intent | create-spec, or [recover-spec](../recover-spec/SKILL.md) for existing code | `SPEC.md` |
| Ready | a person | `status: ready` |
| Plan | [plan-spec](../plan-spec/SKILL.md) | `PLAN.md`, `TASKS.md` |
| Build | [implement-spec](../implement-spec/SKILL.md) | code, tests, the task record |
| Review | [review-spec](../review-spec/SKILL.md) | findings in `TASKS.md` |
| Complete | a person | `status: complete` |

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). A draft that reads as
finished is the failure it guards against, and it can only guard against it if
you don't pad the answers you give it.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
