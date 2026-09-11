---
name: generate-readme
description: Generate a README from what a codebase actually contains, rather than from a template with placeholders left in it.
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

# generate-readme

README generation. Generate a README from what a codebase actually contains, rather than from a template with placeholders left in it.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the framework and the output contract
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to adapt it to your stack, thresholds, and policies
3. Run it against a single module first, then widen once the output matches your expectations

## What it does

1. Detect stack, entry points, scripts, and dependencies from the tree
2. Write only sections the codebase supports evidence for
3. Preserve hand-written content between custom markers on regeneration
4. Refuse to invent badges, metrics, or features that are not there

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). It states what this
structurally cannot see, which matters more than what it can.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
