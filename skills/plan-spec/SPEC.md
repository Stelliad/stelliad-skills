# Spec Planning Specification

## System Overview

A spec says what to build. It doesn't say how that fits the repository in
front of you: which runner proves it, which existing module it extends, which
pattern it follows, what it will break. This skill answers those questions by
reading the repository, then writes the answers down in two documents the
implementer can work from without the conversation that produced them.

`SPEC.md` is approved intent. `PLAN.md` is the approach. `TASKS.md` is
execution state. A later document never gets to redefine an earlier one, and
that is the rule this skill is most tempted to break: a requirement that is
awkward to plan is easiest to plan by quietly planning a smaller one.

## Where it reads and writes

```
specs/004-session-expiry/
├── SPEC.md      read, never edited
├── PLAN.md      written
└── TASKS.md     written
```

`PLAN.md` and `TASKS.md` go **beside the `SPEC.md` they plan**, because
[implement-spec](../implement-spec/CUSTOMIZE.md) reads the three from one
place. For a spec from [create-spec](../create-spec/SKILL.md) that is its
numbered folder.

A spec from [recover-spec](../recover-spec/SKILL.md) arrives two ways, and they
plan differently:

| Recovered spec | How it gets planned |
|---|---|
| Whole-system `SPEC.md` at the repository root, where the work is bringing the system into line with it (the contradictions and candidate defects its owner ruled on) | Plan it in place: `PLAN.md` and `TASKS.md` at the root beside it, and bind implement-spec's CUSTOMIZE.md section 1 (*Where they live*) to the repository root |
| Any recovered spec, where the work is a *change* to the system | Write the change with create-spec, citing the recovered spec under Dependencies as the baseline, and plan that. The recovered spec keeps describing the system; the new one describes the change |

A recovered subsystem spec (`docs/specs/{name}.md`) is never planned in place:
it isn't named `SPEC.md`, and the plan files beside it would belong to no
folder implement-spec reads. It takes the second route.

The shapes come from [create-spec's templates](../create-spec/templates/), one
copy for the whole loop.

## Procedure

### 1. Locate and gate

Find the spec: by ID under the spec root (default `specs/{NNN}-*/SPEC.md`), or
by the path given. Then apply the Ready gate.

| The spec came from | Ready means |
|---|---|
| create-spec, or any spec with a `status` field | Frontmatter `status: ready` (or `in-progress`, on a re-plan) |
| recover-spec | Every requirement being planned is graded observed, intended or answered, with no `[undecided]` or `[contradiction]` left on it, and its question list has an answer for each of those. A person has said the recovered requirements now govern |

Also check, in either case: no Open Questions item is still open, every
requirement has an ID, and every requirement has at least one acceptance
criterion or verification line.

Where CUSTOMIZE.md binds a panel review of the spec, it runs here, before any
plan exists: domain reviewers read the spec alone for gaps, conflicts and
requirements nobody could test. Their findings go to the spec's owner as open
questions, and the spec isn't ready until each is answered. This is the
cheapest point to catch a wrong requirement, since nothing has been built on
it yet. The panel reviews the spec; it never edits it.

**If the spec is not ready, stop.** Report which questions are open, which
sections are empty, which requirements lack an ID or a criterion, and who owns
each. Do not inspect, and do not write a partial plan "to get ahead". A plan
against a draft turns the draft's gaps into tasks, and a task looks settled.

### 2. Inspect the repository

For real, with file reads, searches and commands, against the code this spec
touches. Start from the spec's Affected Areas, so you read the parts that
matter rather than the whole tree.

- **Stack.** Language, framework and package manager, read from the manifest
  nearest the target, not the repository root, which may not match.
- **Runners.** Which test runner, linter, type checker and build command
  actually exist for the target. Run the existing suite once, to confirm the
  runner works and to learn how it narrows to one test. If none is
  configured, note that plainly.
- **Patterns.** Naming, module layout, error handling, and how the closest
  similar feature was built. Cite the file.
- **Standards.** For each requirement prefix in the spec, read the standards
  file CUSTOMIZE.md binds to it (a security policy for `SEC-`, a database
  standard for `DATA-`, and so on) if the repository has one.
- **Infrastructure.** Where `INFRA-` requirements exist, the real
  infrastructure code for the stack they touch.

Record every file read and command run. That record becomes the plan's
Repository Analysis section.

### 3. Write PLAN.md

From [templates/PLAN.md](../create-spec/templates/PLAN.md). Repository Analysis
and Existing Patterns cite what step 2 actually found, by path. Where no
equivalent pattern exists, say so and justify the new approach, rather than
filling the section with something that sounds right.

Every category section carries forward every ID of its prefix from the spec
(`SEC-` and `PRIV-` under Security Considerations, `DATA-` under Data Model
Changes, and so on) and says how each is addressed. Every implementation phase
names the IDs it covers, and its verification line is a command confirmed in
step 2, in the form step 4 describes.

Prefer what the repository already does. A new framework, library, service or
pattern needs a stated reason the existing ones can't meet, in Existing
Patterns. A new dependency is justified the same way.

### 4. Write TASKS.md

From [templates/TASKS.md](../create-spec/templates/TASKS.md). Break each phase
into atomic tasks, each small enough that one failing test can drive it:

````markdown
- [ ] T004 Reject titles over 120 characters
  - Requirements: REQ-002, AC-002
  - Depends on: T001
  - Verification: `python3 -m unittest tests.test_titles -k too_long`
````

- IDs run `T001` upwards across the whole spec, never reset per phase.
- **Requirements** lists every spec ID the task serves, any prefix.
- **Depends on** lists task IDs, or `None`. A dependency you can see and don't
  declare shows up later as a task nobody can finish.
- **Verification** is one runnable command that proves this task, narrowed to
  it where the runner allows. "Tests pass" is not a command. It uses a runner
  confirmed in step 2, and usually names the test the task itself will write,
  so it **fails today and passes once the task is done**. That red run is what
  [test-first](../test-first/SKILL.md) starts from. A command that already
  passes before the task proves nothing about the task.

Then fill the Requirement Traceability table: **one row per ID in the spec,
every prefix**, status `NOT STARTED`, pointing at the task that will satisfy
it. An ID with no row is a requirement this plan has silently dropped. An ID
the plan deliberately does not cover gets a row with status `N/A` and a
reason, and goes on the report.

Delete the Final Verification rows that do not apply to this target. Leave
Verification Evidence and Review Findings as the template has them: the example
block shows implement-spec the evidence format, and both sections are filled
later, by implement-spec and review-spec.

### 5. Self-check, then report

Before reporting, check the output against the shape
[implement-spec](../implement-spec/CUSTOMIZE.md) reads:

- [ ] `SPEC.md`, `PLAN.md` and `TASKS.md` sit together
- [ ] Every task has an ID, requirement IDs, a dependency list and a verification command
- [ ] Every dependency names a task that exists, and none is circular
- [ ] Every spec ID appears in the traceability table
- [ ] Every verification command uses a runner confirmed in step 2, and none passes today for a task not yet done

Then report: what was inspected, the phase and task counts, any spec ID marked
`N/A` and why, and anything the spec asks for that the repository has no
pattern for.

## Rules

1. **The Ready gate holds.** Not ready means stop and report. No partial plans.
2. **Inspection is mandatory and evidenced.** A plan with no citations to files
   actually read didn't happen.
3. **Never invent a command.** If the target has no test runner, the plan says
   so, the first task is setting one up, and every later task depends on it.
4. **Never touch application code, config or dependencies.** Two documents.
5. **Never narrow or reinterpret a requirement to make it easier to plan.** If
   one looks infeasible against the repository, say so under Open
   Implementation Questions and report it to the spec's owner. Don't plan
   around a quieter version of it.
6. **Never edit `SPEC.md`.** A gap in the spec found while planning is a
   finding for its owner, and may send the spec back to `draft`.
7. **Prefer existing patterns.** New ones need a written reason.
8. **Re-plan rather than hand-patch.** When the repository has moved under a
   plan, re-run this skill to refresh the analysis. Hand-edited citations go
   stale without anyone noticing.

## Output

```
┌─────────────────────────────────────────────────────────┐
│  PLANNED: SPEC-{NNN} {feature}                          │
│  {n} files read · {n} commands run                      │
├─────────────────────────────────────────────────────────┤
│  Phases {n}   Tasks {n}   Spec IDs traced {n} of {n}    │
│  Test runner: {command, or "none configured"}           │
├─────────────────────────────────────────────────────────┤
│  No existing pattern for: {list, or none}               │
│  Open implementation questions: {n}                     │
└─────────────────────────────────────────────────────────┘
```

If the gate failed, the output is the gap list instead, and nothing is written.

## Integration

| Skill | Relationship |
|---|---|
| [create-spec](../create-spec/SKILL.md) | Writes the spec this reads, and ships the templates this writes from |
| [recover-spec](../recover-spec/SKILL.md) | The other source of a spec. Its undecided and contradiction grades are what this skill's Ready gate checks |
| [stress-test-plan](../stress-test-plan/SKILL.md) | Attacks the plan before anyone builds it, when being wrong is expensive |
| [implement-spec](../implement-spec/SKILL.md) | Consumes `PLAN.md` and `TASKS.md` next |
| [test-first](../test-first/SKILL.md), [verify-done](../verify-done/SKILL.md) | What each task's verification command will be held to. Write commands those two can use |

## When to run

| Trigger | Note |
|---|---|
| A spec is marked ready | The normal path |
| A recovered spec's questions are answered | Plan the requirements that now govern |
| The repository has moved under a ready spec's plan | Re-run to refresh the analysis |
| implement-spec stopped because a task was wrong | After the spec's owner rules, re-plan the affected phase |

## Limitations

- **It inherits the spec's quality.** A clear, wrong requirement gets a clear,
  wrong plan.
- **A verification command can pass and prove nothing.** The skill confirms a
  command exists and runs; it cannot confirm the test behind it asserts the
  right thing. Read a sample.
- **Inspection is bounded by Affected Areas.** A spec that under-declares what
  it touches gets a plan that misses the rest, and the miss surfaces as a
  regression in review.
- **Dependencies are only as good as what is visible.** Coupling through a
  shared database or a runtime flag often isn't.
- **It doesn't estimate.** Task counts aren't effort, and a phase with two
  tasks can be the long one.
