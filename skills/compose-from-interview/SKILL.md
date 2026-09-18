---
name: compose-from-interview
description: Interview the author for the stories, numbers, and opinions a draft needs, then write from their answers rather than inventing the substance.
license: MIT
compatibility: Adapt the interview lenses, formats, and voice profile via CUSTOMIZE.md. Stage 2 uses a search tool where one is available, and degrades to an interview-only session where none is.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
type: skill
scope: all
status: active
---

# compose-from-interview

Content extraction. Interview the author for the stories, numbers, and opinions a draft needs, then write from their answers rather than inventing the substance.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the interview procedure and the source-file contract
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to set your formats, lenses, and voice profile
3. Run it on one short piece first. The interview is the product, and it takes practice to sit through

## What it does

1. Research the topic so the questions are targeted rather than generic
2. Interview the author, one question at a time, pushing back on vague answers
3. Structure the answers into a source file of stories, quotes, and numbers
4. Draft only from that file, never from the topic in the abstract

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). The hard rule is that the
machine never fills a gap in the author's experience with generated content, and
the section says what that costs you.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
