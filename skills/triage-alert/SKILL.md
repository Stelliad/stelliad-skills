---
name: triage-alert
description: Ingest a monitoring alert, trace it to the commit that introduced it, and route it to one of four outcomes: fix, file, escalate, or suppress.
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

# triage-alert

Alert triage. Ingest a monitoring alert, trace it to the commit that introduced it, and route it to one of four outcomes: fix, file, escalate, or suppress.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the framework and the output contract
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to adapt it to your stack, thresholds, and policies
3. Run it against a single module first, then widen once the output matches your expectations

## What it does

1. Normalise an alert from your monitoring system
2. Classify severity, recurrence, and data impact
3. Trace the stack to source and run git blame on the introducing commit
4. Route to fix, file, escalate, or suppress, with the reasoning recorded

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). It states what this
structurally cannot see, which matters more than what it can.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
