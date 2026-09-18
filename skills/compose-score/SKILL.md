---
name: compose-score
description: Score a draft on seven dimensions against a stated bar, including whether its diagrams and screenshots earn their place, fix what is editorial, and route what is missing back to the author instead of generating it.
license: MIT
compatibility: Adapt the bar, dimensions, and voice profile via CUSTOMIZE.md. No external dependencies.
metadata:
  version: "1.1"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
type: skill
scope: all
status: active
---

# compose-score

Content quality gate. Score a draft on seven dimensions against a stated bar, fix what is editorial, and route what is missing back to the author instead of generating it.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the seven rubrics, the slop checklist, and the loop
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to set your bar and author your voice profile
3. Score one finished piece you already have an opinion about, and check whether the score agrees with you

## What it does

1. Score seven dimensions 1 to 10 (the seventh, Evidence Made Visible, can also score N/A), taking the lowest numeric score as the overall
2. Separate editorial fixes from gaps only the author can fill
3. Apply the editorial fixes and ask targeted questions about the rest
4. Re-score and loop, up to a stated cap

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md), and the cold-start note on
the Voice dimension. Without a voice profile that dimension measures something
narrower than its name suggests, and the report says so rather than hiding it.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
