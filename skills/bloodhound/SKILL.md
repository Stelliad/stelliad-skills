---
name: bloodhound
description: Scan a repository for exposed credentials, map the blast radius of each one, and produce rotation guidance ordered by what an attacker reaches first.
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

# bloodhound

Secrets scanner. Scan a repository for exposed credentials, map the blast radius of each one, and produce rotation guidance ordered by what an attacker reaches first.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the framework and the output contract
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to adapt it to your stack, thresholds, and policies
3. Run it against a single module first, then widen once the output matches your expectations

## What it does

1. Scan the working tree and git history for credential patterns
2. Verify whether a found credential is still live, where the scan mode allows it
3. Map blast radius: what each credential reaches, and in what order
4. Produce rotation steps ranked by exposure

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). It states what this
structurally cannot see, which matters more than what it can.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
