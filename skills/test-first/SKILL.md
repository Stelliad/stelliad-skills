---
name: test-first
description: Enforce the red-green-refactor cycle: require a failing test before the code that satisfies it, and halt when coverage falls.
license: MIT
compatibility: Adapt to your own stack and thresholds via CUSTOMIZE.md. No external dependencies.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
type: skill
scope: all
status: active
---

# test-first

TDD enforcement. Enforce the red-green-refactor cycle: require a failing test before the code that satisfies it, and halt when coverage falls.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the framework and the output contract
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to adapt it to your stack, thresholds, and policies
3. Run it against a single module first, then widen once the output matches your expectations

## What it does

1. Require a failing test first, and verify it fails for the stated reason
2. Write only enough code to pass it
3. Refactor against a green suite
4. Halt on the defined stop signals rather than pushing through them

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). It states what this
structurally cannot see, which matters more than what it can.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
