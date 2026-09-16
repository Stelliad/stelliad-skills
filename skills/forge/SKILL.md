---
name: forge
description: Score a technical document on claim clarity, structural completeness, precision, defensibility, novelty, and slop detection. Loops revision until it hits a 9/10 bar. Distinguishes between editorial fixes (the machine handles) and knowledge gaps (routes back to the author).
license: MIT
compatibility: Run against any patent disclosure, ADR, design doc, whitepaper, or spec. No external dependencies.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
type: skill
scope: all
status: active
---

# forge

Score a technical document against a quality bar. Fix what the machine can fix. Route knowledge gaps back to the author. Loop until it hits 9/10 or the author says ship.

## Quick start

1. [Read SPEC.md](./SPEC.md) to understand the six scoring dimensions and the editorial-vs-knowledge-gap split
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to set your own bar and document types
3. Identify the document type (patent, ADR, design doc, whitepaper, spec)
4. Score it using the rubrics in SPEC.md
5. Apply editorial fixes directly; route knowledge gaps back to the author as specific questions
6. Re-score, loop up to 3 editorial passes, stop at the bar or when the author says ship

## Scoring dimensions

- **Claim clarity**: can someone act on this without a follow-up?
- **Structural completeness**: are all required sections present and substantive?
- **Precision**: is every statement load-bearing and verifiable?
- **Defensibility**: would this survive review by a hostile reader?
- **Novelty / value**: does it say something that isn't already obvious?
- **Slop detection**: is any of this AI-generated filler?

Overall score is the lowest dimension. One weak link means not ready.

## Time required

- First pass on a real document: 20–40 minutes, most of it in the editorial fix loop
- Author follow-up on knowledge gaps: varies, this is the part that can't be brute-forced

## Who runs this

- **Author**: answers the knowledge-gap questions, makes the ship/no-ship call
- **Reviewer / tech lead**: can run it standalone as a second opinion before a design review

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your document types and bar.
