# Spec Review Specification

## System Overview

When the last box in `TASKS.md` is checked, the implementer believes the spec
is met. That belief rests on the traceability table and the evidence section,
both written by the implementer. This skill is the reading that doesn't share
that belief: it starts from the spec, walks each requirement to the code and
test that meet it, runs the lenses a single implementer can't run on their own
work, and writes down what it finds where the next session will see it.

Three things it never does, and each is the easy way out of a hard finding:

- **It never changes code.** A finding fixed by the reviewer is a fix nobody
  reviewed.
- **It never changes a requirement.** A spec edited to match the code is
  exactly the failure the loop exists to prevent.
- **It never completes the spec.** It recommends. A person decides.

## Independence

Run it where the implementation conversation isn't: a new session, or a
subagent given only the spec's ID. A reviewer that watched the code being
written has already accepted the implementer's framing of every tradeoff, and
reads the diff looking for what it expects to see.

If it has to run in the same session, say so at the top of the report. The
findings may still be right; the absence of findings means less.

## Procedure

### 1. Load everything

`SPEC.md`, `PLAN.md` and `TASKS.md` in full. The diff: `git diff` from the
commit before the spec's first implementation commit, or `git log` over the
files `PLAN.md` named. The tests the tasks' verification commands run.

If any task in `TASKS.md` is unchecked or blocked, say so first. Review can
still run, but the recommendation can't be Complete.

### 2. Walk every requirement

For every ID in `SPEC.md`, every prefix: **is it met by the diff, with
evidence?** Not by the traceability table saying `PASS`. Find the code, find
the test, and check the test asserts what the requirement says.

| Prefix | Met means |
|---|---|
| `REQ-`, `AC-` | Code that does it and a test that fails without it |
| `SEC-`, `PRIV-` | The control exists in the code path, not only in `PLAN.md`'s Security Considerations |
| `INFRA-` | A real change in the infrastructure code, not a line in the plan |
| `OBS-` | The log field, metric, trace or alert exists in the diff |
| `DATA-` | A real constraint, migration or scoping check in the schema or query code |
| `EVAL-REQ-` | An evaluation case exists, was run, and its result is recorded |
| `NFR-` | A measurement, with the number, against the stated threshold |

A row marked `PASS` with no matching code or test is itself a finding. So is an
ID with no row at all.

### 3. Delegate the lenses

Scope each one to the files this spec changed. Each lens is a reviewer that
already exists; this skill runs them and collects what they say.

| Lens | Reviewer | Runs |
|---|---|---|
| Correctness | Your harness's code review, where it ships one (Claude Code has `/code-review`); otherwise [review-principles](../review-principles/SKILL.md) plus a line-by-line read of the diff | Always |
| Security | Your harness's security review, where it ships one (Claude Code has `/security-review`), and [secret-scan](../secret-scan/SKILL.md) on the diff | When the spec has `SEC-` or `PRIV-` IDs, or the diff touches authentication, secrets, external input or personal data |
| Structure | [review-principles](../review-principles/SKILL.md) | When the diff is more than a few files, or `PLAN.md`'s Architecture Impact is non-trivial |
| Dead code | [find-dead-code](../find-dead-code/SKILL.md) | When the diff removes or replaces anything |
| Test coverage | [coverage-gaps](../coverage-gaps/SKILL.md) | Always. A requirement with no test is the finding most often missed |
| Fresh verification | [verify-done](../verify-done/SKILL.md), re-running Final Verification | Always. The evidence section records a past run; this is the current one |
| UI surface | Screenshots or a driven walkthrough of each screen the spec names, one image per requirement it evidences, with the requirement ID in the file name. A requirement about what a person sees isn't verified by a unit test alone | When the spec names a screen, a page or a visible state |
| Your panel | Whatever CUSTOMIZE.md binds: a security lead, an architect, a separate agent per lens | When bound |

Skip a lens only when its trigger doesn't apply, and name every skipped lens
and why in the report. A reader has to be able to tell a lens that ran clean
from one that never ran.

### 4. Look across the lenses

The lenses each see one thing. These are what sits between them:

- **Missing requirements.** An ID with no implementing code.
- **Incorrect implementation.** Code that runs, passes its test, and doesn't
  do what the requirement says, usually because the test asserts the wrong
  thing.
- **Requirement drift.** The spec says one thing and the code quietly does
  another, and no conflict was recorded while implementing.
- **Regressions.** Behaviour outside the spec's scope that changed.
- **Plan violations.** Code that departs from `PLAN.md`'s approach without a
  recorded reason.
- **Unneeded complexity.** More than the spec asked for.
- **Security at the seams.** Where this change meets the rest of the system,
  which a lens scoped to the diff doesn't see.

### 5. Write findings

Into `TASKS.md`'s Review Findings table, most severe first. One row per
finding: severity, what is wrong in one sentence, the file and line, which lens
or step found it, and `OPEN`.

| Finding | Severity |
|---|---|
| Security: an exploitable path | `CRITICAL` |
| A requirement not implemented, or implemented wrong, where users or data are affected | `CRITICAL` |
| Security: a confirmed weakness with no demonstrated exploit | `HIGH` |
| A requirement not implemented, or implemented wrong, with contained impact | `HIGH` |
| A `PASS` with no test behind it, or a test that doesn't assert the requirement | `HIGH` |
| review-principles 🔴 Critical | `HIGH` |
| Security: hardening, defence in depth | `MEDIUM` or `LOW` |
| review-principles 🟡 Significant | `MEDIUM` |
| A regression outside the spec's scope | `MEDIUM`, or higher by blast radius |
| review-principles 🟢 Minor | `LOW` |
| Dead code, unused exports left by the change | `LOW` |
| Naming, style, documentation gaps | `INFO` |

Set severity by what breaks and for whom, not by which lens noticed. Where the
spec itself looks wrong, that is a finding too, addressed to the spec's owner,
not something this skill resolves.

### 6. Recommend

One of two, stated plainly:

- **Complete**: every requirement met with evidence, every task checked, Final
  Verification green on this run, and no `CRITICAL` or `HIGH` finding open.
- **Not Complete**: name exactly which findings or requirements block it.

Then stop. Marking the spec `complete` (or moving its folder, in the
active/completed layout) is a person's decision.

## After the review

The findings go back to the implementer. Fixing them is
[implement-spec](../implement-spec/SKILL.md)'s job, on a new task per finding,
and [review-intake](../review-intake/SKILL.md) is how the implementer takes
them in: verify each against the code, disposition every one, push back with
evidence where the reviewer is wrong. A finding the implementer rejects stays
in the table with the reason, so the person who completes the spec can see it.

Then run this skill again. A second review reads only the diff since the first,
plus every finding still open.

## Rules

1. **Read-only.** No edits to code, `SPEC.md`, `PLAN.md` or the task list,
   except the Review Findings table.
2. **Never fix a finding.** Report it. Fixing is implement-spec's job.
3. **Never change a requirement** to make the implementation look compliant.
   If the spec is wrong, that is a finding for its owner.
4. **Never mark the spec complete.** Recommend, then stop.
5. **The traceability table is a claim, not evidence.** Every `PASS` is checked
   against code and a test.
6. **Fixed severity vocabulary:** `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`.
7. **Name every skipped lens** and why.
8. **Say when it wasn't independent.**

## Output

```
┌─────────────────────────────────────────────────────────┐
│  REVIEWED: SPEC-{NNN} {feature}                         │
│  {n} commits · {n} files · independent: {yes|no}        │
├─────────────────────────────────────────────────────────┤
│  Requirements met {n} of {n}                            │
│  CRITICAL {n}  HIGH {n}  MEDIUM {n}  LOW {n}  INFO {n}  │
│  Lenses run: {list}   skipped: {list, with reason}      │
├─────────────────────────────────────────────────────────┤
│  Recommendation: {Complete | Not Complete}              │
│  Blocking: {the findings, or none}                      │
└─────────────────────────────────────────────────────────┘
```

## Integration

| Skill | Relationship |
|---|---|
| [create-spec](../create-spec/SKILL.md), [plan-spec](../plan-spec/SKILL.md) | Produce the three documents this reads, in the templates' shape |
| [implement-spec](../implement-spec/SKILL.md) | Builds what this reviews, and fixes what it finds, one task per finding |
| [verify-done](../verify-done/SKILL.md) | Re-runs Final Verification fresh. It confirms the checks pass; this skill judges whether they check the right things |
| [review-principles](../review-principles/SKILL.md) | The structure lens, and the correctness fallback where the harness has no code review |
| [find-dead-code](../find-dead-code/SKILL.md), [coverage-gaps](../coverage-gaps/SKILL.md) | The dead-code and test-coverage lenses |
| [secret-scan](../secret-scan/SKILL.md) | Part of the security lens, on the diff |
| [review-intake](../review-intake/SKILL.md) | How the implementer takes the findings in |

## When to run

| Trigger | Note |
|---|---|
| Every task is checked and Final Verification has run | The normal path |
| Before anyone marks the spec complete | Required by the loop |
| After findings are fixed | Re-review the new diff and the open findings |

## Limitations

- **Independence is a practice, not a property.** Nothing in the output
  distinguishes a review from a fresh session from one in the implementer's.
- **It is as good as the reviewers it delegates to.** A lens that misses
  something misses it here too. Binding a real panel is the upgrade.
- **The diff boundary is a guess.** Work committed before the spec started, or
  mixed into unrelated commits, can fall outside it.
- **It can't prove a requirement is right**, only whether the code meets it. A
  well-met wrong requirement passes.
- **Severity is judgement.** The map makes it consistent, not correct. Read the
  `HIGH` findings yourself before acting on the recommendation.
