---
name: repo-audit
description: Audit a repository against a security and quality baseline, and report which gaps block the delivery phase it is in.
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

# repo-audit

Repository baseline audit. Audit a repository against a security and quality baseline, and report which gaps block the delivery phase it is in.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the framework and the output contract
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to adapt it to your stack, thresholds, and policies
3. Run it against a single module first, then widen once the output matches your expectations

## What it does

1. Check secrets, tests, linting, dependencies, CI, and documentation
2. Score against the threshold set for the phase you map it to
3. Separate what the audit can auto-fix from what it cannot
4. Exit with a code your pipeline can gate on

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). It states what this
structurally cannot see, which matters more than what it can.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
