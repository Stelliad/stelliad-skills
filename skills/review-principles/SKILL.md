---
name: review-principles
description: Review a codebase against SOLID, DRY, and KISS, and report findings tied to a consequence rather than to taste.
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

# review-principles

Code review. Review a codebase against SOLID, DRY, and KISS, and report findings tied to a consequence rather than to taste.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the framework and the output contract
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to adapt it to your stack, thresholds, and policies
3. Run it against a single module first, then widen once the output matches your expectations

## What it does

1. Sample entry points, largest files, and most-imported modules
2. Assess against the principle set you configure
3. Rate severity by consequence, not by style preference
4. Return findings with file, line, and the change each one implies

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). It states what this
structurally cannot see, which matters more than what it can.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
