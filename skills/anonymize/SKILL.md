---
name: anonymize
description: Produce a shareable copy of a file, folder or repository with client names, people, account IDs, domains and secrets consistently replaced, then check the copy for anything the pass missed.
license: MIT
compatibility: Any text-based project. Binary metadata (images, PDFs, office documents) needs a separate tool; see the Limitations in SPEC.md. Bind your identifier list and replacement scheme via CUSTOMIZE.md.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
  argument-hint: "<file_or_directory> [--mode review|map|apply] [--map replacements.yaml]"
type: skill
scope: all
status: active
---

# anonymize

Anonymization is a consistency problem, not find-and-replace. One real name
gets one replacement, everywhere it appears: prose, filenames, paths, URLs,
code identifiers and comments. A replacement map is the source of truth, a human
reviews it, and a machine applies it to a copy. The original is never touched.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the four detection layers, the procedure and the consistency rules
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to seed your identifier list and choose your replacement scheme
3. Run it in `review` mode on one file first, then widen to a folder once the map reads right

## What it does

1. Scans the target for identifiers across identity, infrastructure, secrets and business content
2. Groups every finding by concept and proposes one replacement per concept in a map
3. Stops for a human to review and edit the map
4. Applies the approved map to a copy under `_anonymized/`, filenames and paths included
5. Re-scans the copy for residue: every original value, every pattern, every near miss

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). A name nobody told the
scan about stays in, and a document with every name stripped can still point at
one client through the facts it keeps.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
