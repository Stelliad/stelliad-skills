---
name: review-intake
description: Process code review feedback as a technical exchange: read the whole set, clarify before touching a file, verify each item against the codebase, disposition every one, and push back with evidence where the reviewer is wrong.
license: MIT
compatibility: Any repository and any reviewer, human or automated. Thread replies assume a hosted review tool with a CLI; CUSTOMIZE.md binds yours.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
  adapted-from: "obra/superpowers, receiving-code-review (MIT). Rewritten, not vendored."
type: skill
scope: all
status: active
---

# review-intake

Code review is a technical exchange, not a social one. Every item gets checked
against the codebase before anything becomes a diff, and a wrong item gets
argued with.

The failure mode this prevents is the agreeable one: implementing a suggestion
because a reviewer made it. That ships regressions under a polite covering note,
and it gets worse as more of the review comes from tools that have no context at
all.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the sequence, the disposition table and when to push back
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to bind your review tool, reply command and escalation path
3. Run it on one review round and read the disposition table before any code moves

## When to use it

- A human left comments on a pull request
- An automated reviewer produced findings: a linter, a scanner, a review bot, or
  `review-principles`, `find-dead-code` and `coverage-gaps` from this collection
- Anyone hands over a list of things to change in code

## What it does

Reads the entire set before reacting to any of it, restates each item, clarifies
what is ambiguous **before** implementing anything, verifies each item against
the actual codebase, gives every item one of four dispositions, then implements
one at a time with a test each.

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). It sits downstream of
whatever produced the findings, and it will not tell you about the bug nobody
reviewed.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
