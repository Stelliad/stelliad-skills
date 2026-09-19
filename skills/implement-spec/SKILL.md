---
name: implement-spec
description: Work a spec's task list forward one task at a time, test first and verified, updating the checkbox, the evidence and the requirement traceability as it goes, and stopping when the spec turns out to be wrong.
license: MIT
compatibility: Any spec that carries a task list with dependencies and verification commands. File names, ID scheme and evidence format adapt via CUSTOMIZE.md.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
type: skill
scope: all
status: active
---

# implement-spec

Takes a written spec and works its tasks forward. It owns **which task is next**
and **keeping the record honest**. It does not own how a change is written and
proven: that is the test-first cycle and the completion gate, called per task.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the loop, the stop conditions and the record it keeps
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to bind it to your file names, ID scheme and evidence format
3. Run it on one task and read what it wrote down before letting it run on

## What it does

1. Reads the spec, the plan and the task list, and nothing from memory
2. Picks the first unchecked task whose dependencies are all met
3. Implements it test first, then verifies against the task's own command
4. Records the evidence and the requirement status, or records the blocker

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). Its honesty rests on the
verification commands the task list carries; a task whose command proves nothing
gets a checkbox anyway.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
