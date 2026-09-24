# Spec Creation Specification

## System Overview

A spec written before the code is a statement of intent: what the system must
do, for whom, and how anyone will know it does. This skill produces that
statement in a fixed shape and a fixed place, so the three skills after it can
find it and read it without being told where it is or what it means.

It produces one document, and it produces it as a **draft**. The step that
matters most is the one it refuses to take: filling in requirements nobody
gave it. A spec that reads as finished but isn't sends the planner off to plan
against gaps, and the plan inherits them as confident-looking tasks.

## Where it writes

```
specs/
└── 004-session-expiry/
    ├── SPEC.md      this skill
    ├── PLAN.md      plan-spec, later
    └── TASKS.md     plan-spec, later
```

One folder per spec, named `{NNN}-{slug}`, under `specs/` at the repository
root. That is the layout [implement-spec](../implement-spec/CUSTOMIZE.md)
reads by default, and the four skills in the loop share one binding for it
(CUSTOMIZE.md, Customization 1). Change it there and all four follow.

**A spec lives in the repository it governs.** Clone the repository and the
spec comes with it; branch the code and the spec branches too; a change to the
spec is reviewed in the same pull request as the code it changes. A spec kept
in a wiki or a different repository stops travelling with its code the first
time either moves.

State lives in `SPEC.md`'s frontmatter `status` field, and only there:

| Status | Set by | Means |
|---|---|---|
| `draft` | create-spec | Written, with open questions or empty rows |
| `ready` | a person | Every open question resolved; plan-spec may run |
| `in-progress` | a person, or your convention | Planned and being built |
| `complete` | a person | Verified, reviewed, every CRITICAL and HIGH finding resolved |

Teams that prefer to see state in the tree can move folders between
`specs/active/` and `specs/completed/` instead. That is a layout option in
CUSTOMIZE.md, off by default, and the frontmatter still carries the status
either way.

## Procedure

### 1. Check direction

Does code for this already exist and run? If yes, stop and route to
[recover-spec](../recover-spec/SKILL.md). Writing intent forwards over a
system that already behaves some way produces a spec that disagrees with the
code on day one, and nobody can tell which side was meant.

Also check the repository: a spec belongs in the repository whose code it
governs. If the feature lives in a different repository, write it there.

### 2. Assign the number

List the spec root (and `completed/`, if your layout uses it). The next number
is one past the highest `NNN` found anywhere, zero-padded to three digits.

**Numbers are never reused.** An abandoned spec keeps its number: mark it
abandoned or delete the folder, but never hand `004` to something else. A
number that meant two things is a citation that points at the wrong document.

### 3. Create the folder and copy the template

`specs/{NNN}-{slug}/SPEC.md`, copied from [templates/SPEC.md](./templates/SPEC.md).
Set `id: SPEC-{NNN}`, `created` and `updated` to today, `owner` to the person
who will rule on the open questions, and `status: draft`.

### 4. Fill what you were given, and nothing else

Write Summary, Problem, Goals and Non-Goals from what was actually said.

For User Stories, Requirements, Acceptance Criteria and the categorised
requirement sections: write a row only where the conversation gave you enough
to write it honestly. Where it didn't, leave the row open and add the gap to
Open Questions, naming who can answer it. "None identified for this spec" is
for a section that was considered and does not apply. It is not a way to empty
a section you did not think about.

Requirements are written in EARS form where they have a trigger, a state or an
undesired condition, and each one is testable. "Should be fast" goes on the
open question list as "how fast, measured where?", not into the table.

### 5. Report

The path written, the assigned ID, and what stands between this draft and
`ready`: the open questions with their owners, the empty rows, anything flagged
rather than guessed.

## Rules

1. **Never implement.** No code, no config, no dependency changes. One document.
2. **Never write `PLAN.md` or `TASKS.md`.** That is [plan-spec](../plan-spec/SKILL.md),
   and it runs after a person marks the spec `ready`.
3. **Never set `ready`.** A spec is ready when its owner says so. The skill
   always leaves it `draft`, however complete it looks.
4. **Don't pad.** An empty requirement table with the ID scheme showing is more
   honest than fabricated rows, and it is what the owner needs to see.
5. **Every open question names a person.** A question with no owner waits
   forever.
6. **Never reuse a number.**
7. **One copy.** If a spec for this already exists, report it and stop. Two
   specs for one feature drift apart, and the planner will pick one.

## Output

```
┌─────────────────────────────────────────────────────────┐
│  SPEC-{NNN}: {feature}                                  │
│  specs/{NNN}-{slug}/SPEC.md             status: draft   │
├─────────────────────────────────────────────────────────┤
│  Goals {n}   Requirements {n}   Acceptance {n}          │
│  Open questions {n}   Empty sections {n}                │
├─────────────────────────────────────────────────────────┤
│  Before ready: {the question that changes the most}     │
└─────────────────────────────────────────────────────────┘
```

## Worked example

Given: "Our notes CLI accepts a blank title. Reject blank titles and anything
over 120 characters, with a clear error." The skill writes, in part:

````markdown
---
id: SPEC-001
status: draft
owner: Dana (CLI maintainer)
---

## Requirements

| ID | Pattern | Requirement |
|---|---|---|
| REQ-001 | Unwanted Behavior | If a note title is empty or whitespace only, then the system shall reject the note with the error "title is required". |
| REQ-002 | Unwanted Behavior | If a note title is longer than 120 characters, then the system shall reject the note with the error "title is too long (max 120)". |

## Open Questions

- [ ] Q1. Is 120 counted in characters or bytes? A title in a non-Latin script differs. (ask: Dana)
- [ ] Q2. Are existing notes with blank titles migrated, left alone, or rejected on edit? (ask: Dana)
````

Q2 is the kind of question this skill exists to surface: nobody mentioned
existing data, and a plan written without the answer would pick one silently.

## Integration

| Skill | Relationship |
|---|---|
| [recover-spec](../recover-spec/SKILL.md) | The backwards direction: code exists, spec does not. Route there when that is the real situation |
| [tech-doc-review](../tech-doc-review/SKILL.md) | Scores the draft as a technical document once the open questions are answered |
| [stress-test-plan](../stress-test-plan/SKILL.md) | Attacks the idea before the spec is marked ready, when the cost of being wrong is high |
| [plan-spec](../plan-spec/SKILL.md) | The next step, after a person sets `ready`. Reads the templates shipped here |
| [implement-spec](../implement-spec/SKILL.md), [review-spec](../review-spec/SKILL.md) | Later in the loop. Both read this skill's templates by shape |

## When to run

| Trigger | Note |
|---|---|
| A new feature with no code yet | The reason this skill exists |
| Someone says "spec out X" | If X already runs, use recover-spec |
| A ticket is too big to be one ticket | A spec with tasks is the next size up |

## Limitations

- **It writes down what it is told.** A confident, wrong answer in the
  conversation becomes a confident, wrong requirement. The open question list
  only catches what nobody said, not what somebody said badly.
- **It cannot tell a goal from a solution.** "Add a Redis cache" as a goal is a
  plan in disguise. It flags obvious cases; subtle ones get through.
- **EARS makes a requirement testable, not correct.** A well-formed requirement
  can still ask for the wrong thing.
- **Numbering assumes one writer at a time.** Two branches creating specs in
  parallel can both take `005`. Resolve it at merge, and renumber the newer one
  before anything cites it.
