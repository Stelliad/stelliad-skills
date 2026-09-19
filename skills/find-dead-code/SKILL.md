---
name: find-dead-code
description: Find orphaned files, unused exports, dead dependencies and commented-out code, and report them with a confidence level rather than deleting anything.
license: MIT
compatibility: TypeScript, JavaScript, Python and Rust out of the box. Entry points, exclusions and confidence rules adapt via CUSTOMIZE.md.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
type: skill
scope: all
status: active
---

# find-dead-code

A hygiene sweep that finds what nothing reaches: orphaned files, exports nobody
imports, dependencies nobody uses, and large blocks of commented-out code. It
reports; it never deletes.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the categories, the procedure and the report format
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to declare your entry points and what must never be called dead
3. Run it on one package first, and check the 🟡 rows before trusting the 🟢 ones

## What it does

1. Reads the project's own config to find entry points
2. Traces the import graph from each one
3. Reports what the graph never reaches, by category, with a confidence level
4. Leaves every deletion decision to a person

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). Static analysis cannot see
a dynamic import, and a framework that resolves files by string will make live
code look dead.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
