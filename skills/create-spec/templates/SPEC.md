---
id: SPEC-[NNN]
status: draft
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
owner: [name]
---

# SPEC-[NNN]: [Feature Name]

The `status` field in the frontmatter above is the only copy of this spec's
state. Its values, in order: `draft`, `ready`, `in-progress`, `complete`.

A spec enters `plan-spec` only once it is `ready`, and `ready` means every Open
Question below is resolved. A person sets it. No skill in this set promotes a
spec to `ready` or to `complete`.

## Summary

Two or three sentences: what this is, for whom, and why it matters now. Not a
restatement of the title.

## Problem

What is broken, missing, or slow today. The situation this spec exists to
change, described without naming the solution yet.

## Goals

What this spec must achieve. Numbered, short, each one independently
verifiable.

1. ...

## Non-Goals

What this spec explicitly does not attempt. As load-bearing as Goals: a
reviewer should be able to reject scope creep by pointing at this section.

- ...

## Affected Areas

Which applications, packages, services and infrastructure this spec touches,
so the planner knows the real scope before inspecting anything.

```
Affected:
- [app or package path]
- [infrastructure stack or module]
```

A feature spanning several applications stays one spec when it is one cohesive
capability: list every area it actually touches rather than splitting it into
disconnected per-app specs. If it is scoped to one area, list only that one.

## User Stories

| ID | Story |
|---|---|
| US-001 | As a [role], I want [capability], so that [outcome]. |

## Requirements

Written in EARS form wherever the requirement has a trigger, a state, or an
undesired condition it responds to. Classify each one:

| Pattern | Template |
|---|---|
| Ubiquitous | The system shall \<response\>. |
| Event-Driven | When \<trigger\>, the system shall \<response\>. |
| State-Driven | While \<state\>, the system shall \<response\>. |
| Optional | Where \<feature\>, the system shall \<response\>. |
| Unwanted Behavior | If \<undesired condition\>, then the system shall \<response\>. |

| ID | Pattern | Requirement |
|---|---|---|
| REQ-001 | | |

Avoid vague requirements ("the application should be secure"). Write the
measurable form instead ("the system shall reject any request without a valid
session token"). If a requirement cannot be phrased as testable, it is not
finished yet.

## Acceptance Criteria

Each row must be checkable by running something, not by reading the code and
deciding it looks right.

| ID | Requirement | Criteria | Verification |
|---|---|---|---|
| AC-001 | REQ-001 | [observable, pass/fail condition] | [command or test that proves it] |

## Security Requirements

| ID | Requirement |
|---|---|
| SEC-001 | |

If none apply, write "None identified for this spec" rather than deleting the
section, so a reviewer can tell it was considered and not skipped.

## Privacy and Compliance Requirements

| ID | Requirement |
|---|---|
| PRIV-001 | |

Personal data, regulated data categories, retention, consent, and anything a
contract or policy says may or may not reach a given system. If your team keeps
a data-handling policy, check it before filling this in. If none apply, say so
rather than deleting the section.

## Infrastructure Requirements

| ID | Requirement |
|---|---|
| INFRA-001 | |

Anything this spec needs from infrastructure-as-code: a new resource in an
existing stack, a new stack, a changed access boundary, a new environment
variable a deployed component reads. Each one gets planned against the real
infrastructure code in the repository, not invented. If none apply, write "None
identified for this spec".

## Observability Requirements

| ID | Requirement |
|---|---|
| OBS-001 | |

What this feature must emit to be diagnosable in production without
reproducing the issue locally: a log with named fields, a metric, a trace, an
alert condition. Don't add this mechanically to a trivial feature. If none
apply, write "None identified for this spec".

## Database Requirements

| ID | Requirement |
|---|---|
| DATA-001 | |

A persistence-layer requirement this feature depends on: a uniqueness or
integrity constraint, tenant scoping, a migration's backward-compatibility
need, a backfill. If there is no real persistence change, write "None
identified for this spec".

## Evaluation Requirements

| ID | Requirement |
|---|---|
| EVAL-REQ-001 | |

For a feature that calls a language model, an agent, a tool-calling workflow or
a retrieval pipeline: what evaluation its AI behaviour must pass, meaning a
dataset, a dimension, a threshold, a safety gate. If the feature has no AI
behaviour, write "None identified for this spec".

## Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-001 | |

Performance, reliability, accessibility, cost. Each one measurable, not
aspirational ("fast" is not a requirement; "responds within 300ms at the 95th
percentile" is).

## Constraints

Technical, organizational, or timeline constraints this spec has to work
within. Not requirements: things the plan cannot change even if it wanted to.

## Dependencies

Other specs, systems, libraries, or people this spec depends on.

## Out of Scope

Work that belongs to this feature conceptually but is deliberately deferred to
a later spec. Different from Non-Goals, which is work this spec rejects
outright rather than defers.

## Open Questions

Unresolved items blocking `ready`. Each one names who can answer it. When one is
answered, replace it with the answer and who gave it. An open checkbox here
keeps the spec `draft`.

- [ ] Q1. [the question] (ask: [person or role])
