---
name: review-spec
description: Independent final review of a spec's implementation against SPEC.md, PLAN.md, TASKS.md, the diff and the tests. Walks every requirement to the code and test that meet it, delegates the lenses to reviewers that already exist (your harness's code review, review-principles, find-dead-code, coverage-gaps, verify-done, and your own panel if you have one), and writes severity-ranked findings, CRITICAL through INFO, into TASKS.md. Never changes requirements or code, and never marks the spec complete. Use when saying "review-spec", "independent review of SPEC-X", "is this ready to complete", "final review", or "/review-spec <id>".
license: MIT
compatibility: Any repository with git history. Reads the spec, plan and task list in the shape create-spec's templates define. The reviewers it delegates to, and where their severities land, adapt via CUSTOMIZE.md.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
  argument-hint: "<spec-id | path-to-SPEC.md>"
type: skill
scope: all
status: active
---

# review-spec

The last step of the spec loop, and the check before a spec is allowed to call
itself done. **Independent** is doing real work in that sentence: run it from a
fresh session or a subagent that hasn't seen the implementation conversation,
so it reads the diff instead of trusting the implementer's account of it.

It doesn't invent its own review methods. It walks the requirements itself,
hands each lens to a reviewer that already does that job, and maps what comes
back onto one severity scale.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the requirement walk, the lenses and the severity map
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to bind your reviewers, including your own panel if you run one
3. Run it on one finished spec from a fresh session and read the findings before anyone fixes them

## Arguments

- `$1`: a spec ID or a path to a `SPEC.md`, as [plan-spec](../plan-spec/SKILL.md) takes it.

## What it does

1. Loads the spec, the plan, the task list, the diff since the spec's first commit, and the tests
2. Walks every requirement ID to the code and the test that meet it, not to the traceability table's say-so
3. Delegates the lenses: correctness, structure, dead code, test coverage, fresh verification, and any panel you bind
4. Writes findings into `TASKS.md`'s Review Findings table, most severe first
5. Recommends Complete or Not Complete, and leaves the decision to a person

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). A review that ran in the
same session as the implementation is not independent, and nothing in its
output will say so.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
