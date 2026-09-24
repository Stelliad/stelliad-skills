---
name: coverage-gaps
description: Find the code paths no test reaches, ranked by the risk of the code that is uncovered, and the tests that run code without asserting anything about it.
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

# coverage-gaps

Coverage gap analysis. Find the code paths no test reaches, ranked by the risk of the code that is uncovered, and the tests that run code without asserting anything about it.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the framework and the output contract
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to adapt it to your stack, thresholds, and policies
3. Run it against a single module first, then widen once the output matches your expectations

## What it does

1. Map exported functions and routes against the tests that touch them
2. Rank gaps by the risk tier of the module they sit in
3. Flag false-confidence gaps: tests that execute code and assert nothing, or only a mock's call count
4. Report what the analysis structurally cannot see

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). It states what this
structurally cannot see, which matters more than what it can.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
