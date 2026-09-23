# Recovered spec skeleton

The structure `recover-spec` writes. A spec recovered from an existing system is
shaped the same as one written before the code, so a quality review grades both
against the same bar.

Two rules before any of the sections:

**Every statement carries a grade.** Inline, as `[observed]`, `[inferred]`,
`[intended: README §3]`, `[undecided]`, `[contradiction]`. A section with no
grades hasn't been recovered, it's been described.

**Sections aren't optional, but they can be empty.** A section that says "no
scheduled work exists in this system `[observed]`" is doing its job. A missing
section leaves the reader unable to tell whether it was checked.

---

## Frontmatter

```yaml
---
doc: spec              # or reading, when written with --as-reading
skill: recover-spec
subject: <system name>
read_at:
  repo: <path or org/repo>
  sha: <short SHA>
  branch: <branch>
  tree: clean          # or dirty
  date: YYYY-MM-DD
verdict: <Recovered | Partial>
---
```

`Partial` whenever a surface was identified and not traced. A spec that silently
omits a subsystem reads as complete.

---

## 1. What this system is

Three to five sentences. What it does, for whom, and the unit of work it exists
to perform. No architecture here.

Then **how this document was produced**: one paragraph saying it was recovered
from the code at the pinned SHA, that the grades mean what the grade table says,
and that nobody has answered the undecided items yet. A reader who skips this
reads the rest as settled.

## 2. Boundary

The three-column table: in, out, undeclared. The undeclared column is a finding,
not a note.

## 3. Surfaces

Every entry point, scheduled job, queue, stream, data store and outbound call.

| Surface | Kind | Authenticated as | Trusts | On bad input |
|---|---|---|---|---|

The last two columns are where the questions come from. Fill them from the code
or mark them undecided. Never leave a cell blank.

## 4. The core data path

**The spine.** One end-to-end walk of the primary unit of work, from the entry
point to the durable write and back to the caller.

Numbered hops. Each hop: what's passed, what's stored, what leaves the trust
boundary, and what the caller sees when it fails. Where the system handles
sensitive or regulated data, record the data category at each hop, so the trace
doubles as a data-flow inventory.

This is the section a new engineer reads first, and the one most likely to be
wrong if it was assembled from file names rather than traced.

## 5. Data model

Entities, keys, relationships, access patterns, retention.

Then, under its own heading: **invariants the code assumes and doesn't
enforce.** Each one with what depends on it and what breaks if it stops holding.
These are the requirements a rewrite loses, and they exist nowhere else.

## 6. Trust boundaries and account topology

Where authority changes hands. Which account or environment each component runs
in, what crosses between them, and what enforces the crossing. If your
organisation has a standard layout, compare against it and name the gaps rather
than redrawing it. If it doesn't, describe what's there.

## 7. Recovered requirements

The numbered list, each graded, each citing the code or document it came from.

| # | Requirement | Grade | Source | Test |
|---|---|---|---|---|

The `Test` column is the coverage answer. An empty cell is a coverage gap.

## 8. Subsystems

One row per subsystem, with a one-line description and a link into `docs/specs/`
where a subsystem spec exists. **Never inline a subsystem spec here.** The master
carries the system and the subsystem specs carry the parts. A master holding
subsystem content stops being a master.

## 9. Known defects and unowned behaviour

Candidate defects found while tracing, and reachable code satisfying no named
requirement. Findings, not requirements, and marked so nobody preserves them by
accident.

---

## The question list

Written as a separate file, because it travels to a person and the spec travels
to a repo.

Each entry:

```
Q{n}. {The question, in one sentence.}
   Found:    {file}:{line}
   Behavior: {what the code does today, graded}
   Depends:  {what changes based on the answer}
   Ask:      {who can answer it}
```

Ordered by what the answer changes, not where it was found. The first three go
on the agenda for the next conversation with the owner; the rest is the backlog.
