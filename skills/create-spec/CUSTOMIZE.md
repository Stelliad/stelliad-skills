# Spec Creation: Customization Guide

## Before you start

create-spec, [plan-spec](../plan-spec/SKILL.md),
[implement-spec](../implement-spec/SKILL.md) and
[review-spec](../review-spec/SKILL.md) are one loop. The first two
customizations below are shared: the location and the ID scheme you bind here
are the ones the other three read, and implement-spec's own CUSTOMIZE.md
sections 1 and 2 bind the same things. Keep them in agreement, or the planner
writes where the implementer never looks.

## Customization 1: Spec location and lifecycle (shared)

**Where it is used:** SPEC.md, *Where it writes*, and step 2.

```
Spec root:        <e.g. specs/, docs/specs/, .specs/>
Folder name:      <e.g. {NNN}-{slug}, {ticket}-{slug}>
Lifecycle:        <status field only / active and completed folders>
Documents:        <SPEC.md, PLAN.md, TASKS.md, or your names for them>
```

With the folder lifecycle, new specs go to `{root}/active/{NNN}-{slug}/` and a
person moves the folder to `{root}/completed/` when the spec is complete. The
number is still assigned across both folders, so a completed spec never loses
its number to a new one.

**If you skip it:** `specs/{NNN}-{slug}/` at the repository root, status in the
frontmatter only, and the three shipped file names. That matches
implement-spec's default.

## Customization 2: ID scheme and requirement prefixes (shared)

**Where it is used:** SPEC.md, steps 2 and 4, and every template.

```
Spec IDs:          <e.g. SPEC-001>
Requirement IDs:   <e.g. REQ-001, scoped to the spec>
Prefixes in use:   <which of US, REQ, AC, SEC, PRIV, INFRA, OBS, DATA, EVAL-REQ, NFR>
Task IDs:          <e.g. T001, sequential across the whole spec>
```

The shipped template carries ten prefixes. Most teams need four or five. Delete
the sections you never use from [templates/SPEC.md](./templates/SPEC.md) and
the matching sections from the plan template, rather than filling them with
"None identified" forever: a section that is always empty stops being read, and
the one time it matters nobody looks.

IDs are unique within a spec. Anywhere an ID is cited outside its own folder
(another spec's Dependencies, a commit message, a ticket), qualify it with the
spec number: `SPEC-004/REQ-001`. Spec numbers are never reused, so the
qualified form is unique across the repository with no allocator to keep in
sync.

If your organization allocates requirement IDs globally rather than per spec,
say so here, and write the allocator's name where step 4 fills an ID.

**If you also run a tool that reads EARS IDs** (the agentic plugin's
decomposition, for one, only recognises `REQ-{letter}-{digits}`), put the
pattern's letter in the ID: `REQ-U-001`, `REQ-E-001`, `REQ-S-001`, `REQ-O-001`,
`REQ-W-001` for ubiquitous, event, state, optional and unwanted behaviour. The
Pattern column already records the type; this carries it into the ID so both
tools trace the same requirement. A complex requirement takes the letter of its
leading clause.

**If you skip it:** every prefix above, three digits, reset per spec.

## Customization 3: Who owns a spec

**Where it is used:** SPEC.md, step 3 and rule 5.

```
Default owner:      <a person or role, e.g. the product owner for the area>
Who sets ready:     <the owner / a tech lead / a review meeting>
Who sets complete:  <usually the same person>
```

**Name a person.** "The team" doesn't answer questions.

**If you skip it:** the owner is whoever asked for the spec, and they are named
on every open question.

## Customization 4: The templates

**Where it is used:** SPEC.md, step 3.

The three files in [templates/](./templates/) are the shape the whole loop
reads. Edit them freely: add sections your reviews need, remove prefixes you
never use, add a line your compliance process wants on every spec. Two things
to keep:

- **The frontmatter `status` field**, because plan-spec gates on it.
- **In TASKS.md, the three lines on every task** (requirements, depends on,
  verification), the Requirement Traceability table, the Verification Evidence
  section and the Review Findings table, because implement-spec and review-spec
  write into those by name.

If your templates live somewhere else (a shared project scaffold, say), point
all three skills there instead of keeping a second copy. Two copies of a
template drift, and the stale one reads as authoritative.

**If you skip it:** the shipped templates, read from this skill's folder.

## Customization 5: Spec scope

**Where it is used:** SPEC.md, step 1.

What deserves a spec in your team, and what is a ticket? Write the line:

```
Needs a spec:     <e.g. more than one ticket's work, a new data model, any SEC- or PRIV- requirement>
A ticket is enough: <e.g. a single change with one acceptance criterion>
Not here:         <e.g. customer engagement scope, which lives in its own process>
```

**If you skip it:** anything someone asks to spec gets a spec.

## Customization 6: An optional decision log

**Where it is used:** nowhere by default.

Some teams keep an append-only `audit.md` beside the spec: one short entry per
decision (the spec marked ready, an open question answered, a finding waived),
with who made it and when, never edited after it is written. It records *why*
something changed, which the diff alone doesn't.

If you want it, add it to the folder layout here and tell each of the four
skills to append an entry when it runs. It is off by default because the other
three documents already carry *what* happened, and a fourth file nobody reads is
worse than none.

## Final checklist

- [ ] Spec root, folder name and lifecycle are bound, and match implement-spec's CUSTOMIZE.md
- [ ] The ID scheme and the prefixes you actually use are set, and unused sections are deleted from the templates
- [ ] A default owner is named, and who sets ready and complete
- [ ] The templates are where all four skills read them, in one copy
- [ ] The line between a spec and a ticket is written down
- [ ] You've decided whether to keep a decision log

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The trigger, the argument and the loop |
| `SPEC.md` | The layout, the procedure, the rules, a worked example, limitations |
| `CUSTOMIZE.md` | This file: location, IDs, owners, templates, scope |
| `templates/SPEC.md`, `PLAN.md`, `TASKS.md` | The shapes the whole loop reads |
