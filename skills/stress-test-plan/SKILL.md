---
name: stress-test-plan
description: Interrogate a plan or decision one round of questions at a time, working a design tree from the questions that can be answered now, until the weakest assumption is named.
license: MIT
compatibility: Any plan, decision or design. Round size, format and stopping rule adapt via CUSTOMIZE.md. No external dependencies.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
type: skill
scope: all
status: active
---

# stress-test-plan

Hold a plan still and ask it the questions it has been avoiding, in rounds.
Produces no document and edits nothing: the output is what you conclude.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the design tree, the frontier rule and the round format
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to set round size, tone and the stopping rule
3. Bring a decision that is hard to undo; this is wasted on a reversible one

## What it does

1. Maps the plan as a tree of decisions, each hanging off the one above it
2. Asks the whole frontier, every question whose prerequisites are already settled, in one round
3. Carries a recommended answer with each question, so you are reacting rather than composing
4. Recomputes the frontier from your answers and asks the next round, until nothing is left assumed

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). It interrogates the plan
you brought; it cannot tell you that you brought the wrong plan.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
