---
name: verify-done
description: Gate every completion claim behind fresh evidence: name the command that proves it, run it, read the output, then state the claim with the result attached.
license: MIT
compatibility: Any project. The command set is read from the repo's own test runner, linter, type checker and build; adapt the proof table and the retry cap via CUSTOMIZE.md.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
  adapted-from: "obra/superpowers, verification-before-completion (MIT). Rewritten, not vendored."
type: skill
scope: all
status: active
---

# verify-done

Evidence before the claim, every time. If the command that proves a claim has
not been run in this message, the claim cannot be made.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the gate, the proof table and the two report shapes
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to bind it to your runners, your definition of done, and your retry cap
3. Run it against one change first, then put it in front of your commits and PRs

## What it does

1. Names the exact command that would prove the claim
2. Runs it fresh and in full, rather than reusing an earlier run
3. Reads the exit code, the counts and the new warnings, not just the colour
4. States the claim with its evidence, or the real status with its evidence

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). It reports; it does not
fix, and it cannot tell you that a passing suite tests the right thing.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
