# Ticket Review Specification

## System Overview

A ticket is a prompt. Once an agent can pick work up from an issue tracker, the
issue body stops being a note between colleagues and becomes the instruction
set for a worker with no memory of the conversation that produced it. Most
tickets aren't written for that reader, and the failure doesn't show up when
the ticket is filed. It shows up as a wrong build three hours later.

This skill is the gate in front of that. It grades a ticket against
[STANDARD.md](./STANDARD.md) and returns one of three verdicts, a score out of
twelve, and the specific reason behind every deduction.

It's a **checker**. It never edits the ticket and never applies a label. The
writing belongs to [create-ticket](../create-ticket/SKILL.md), which calls this
skill before it declares anything Ready. Keeping the two apart is the point:
anything that can edit the ticket can make the grade agree with it.

## Two halves: mechanical and judgement

| Half | Done by | Decides |
|---|---|---|
| Mechanical | `scripts/review-ticket.py` | Required sections per shape, flat checkbox acceptance criteria, vague verbs with no measurable target, empty or `N/A` sections, generic titles, a missing out-of-scope half, a High or Critical risk with no reason, a Critical risk with no human approval section, open `#N` dependencies, credentials in the body, an `UNFILLED` marker |
| Judgement | The agent running the skill | Is the objective an outcome or a task, is the reason legible without the conversation, is the scope honest, does the ticket assert things about the repo that aren't true, is any decision still open |

The script says in its own output that it didn't attempt the judgement half.
That sentence matters: a mechanical PASS on a ticket that invents a vendor is
the division of labour working, not the script failing. Fixture `08-blocked.md`
is exactly that case.

A mechanical `BLOCKING` line can't be overruled by judgement. The reverse isn't
true: judgement routinely fails a mechanically clean ticket.

## Why the rules are the rules

**Acceptance criteria are a flat checkbox list in execution order** because an
agent works them as a queue, taking the next unfinished item on each pass. A
nested or narrated list reads as one blob and can't be iterated.

**Scope must name what's out** because "in" never stops anything. An agent
that can't finish without crossing the out line has to stop and say so, and
that only happens if the line exists.

**High and Critical risk carry a reason, and Critical carries a human approval
section**, because the reader deciding whether to run the ticket unattended
needs to know what could go wrong and what the agent must not do. The approval
section still enforces nothing by itself; see STANDARD.md.

**Item 8 is a verdict, not a deduction.** A missing decision isn't bad writing.
Scoring it would let a beautifully written ticket with an unmade architecture
choice reach READY at 11 out of 12, and the agent would make the choice for
you.

**No invented context.** A ticket that names a library, provider or service the
repo doesn't use turns an obvious stall into a non-obvious wrong build. Reading
the repo is the only way to catch it, which is why step 2 exists.

## Ticket shapes

The checker detects the shape from the headings (or a `[Bug]` or `[Spike]` title
prefix) and applies that shape's required set:

| Shape | Required sections |
|---|---|
| Task | Objective, Why, Acceptance Criteria, Scope, Risk |
| Bug | Summary, Impact, Current Behavior, Expected Behavior, Reproduction, Acceptance Criteria, Risk |
| Spike | Decision Needed, Why, Scope, Expected Deliverable, Decision Criteria, Risk |

A spike has no acceptance criteria on purpose. Its output is a decision.

GitHub issue forms render each field's label as a `###` heading, and a
readable label ("Risk of the fix", "Why we need the answer") isn't the
canonical section name. The checker normalises those through
`SECTION_ALIASES`, and treats `_No response_` (GitHub's text for a blank
optional field) as an absent section rather than an empty one. Fixtures 10 to
12 are form submissions exactly as GitHub renders them.

## Splitting

A ticket is more than one ticket when it has more than one independently
deliverable outcome: unrelated subsystems, more than one deployment, or
acceptance criteria that would land in separate PRs. The report names each
resulting title, the boundary, and the dependency order.

What it doesn't do: split tightly coupled work to make pieces smaller, or split
one feature horizontally into frontend, backend and database tickets that
can't be verified alone. Work big enough to need decomposition usually needs a
spec and one parent issue instead.

## The fixtures

`fixtures/` holds twelve synthetic tickets, one per scenario, with the expected
mechanical verdict for each in `fixtures/expected.json`. They're both the
regression suite for the checker and the worked examples `create-ticket` points
people at, so an edit to one is an edit to reference material.

```bash
bash scripts/run-fixtures.sh
```

| Fixture | Scenario | Mechanical |
|---|---|---|
| `01-vague.md` | Vague feature idea | FAIL |
| `02-well-defined.md` | The same idea, done properly | PASS |
| `03-bug.md` | Bug shape | PASS |
| `04-security.md` | Security fix, no exploit detail | PASS |
| `05-infra.md` | Irreversible infrastructure, Critical | PASS |
| `06-tech-debt.md` | End state plus what mustn't change | PASS |
| `07-spike.md` | Spike shape | PASS |
| `08-blocked.md` | Mechanically clean, BLOCKED on judgement | PASS |
| `09-human-approval.md` | What an agent may build against what it may run | PASS |
| `10-form-task.md` to `12-form-spike.md` | Issue form submissions | PASS |

## Limitations

- **It grades the ticket, not the work.** A READY ticket can still be built
  wrong.
- **The judgement half is only as good as the repo reading.** If the agent
  doesn't look, an invented dependency passes.
- **Vague-verb detection is a word list.** It catches "improve" and "properly".
  It won't catch a vague sentence built from specific-sounding words.
- **The secret check is a tripwire, not a scanner.** It catches an obvious
  paste. A real sweep needs a real secret scanner.
- **Dependencies resolve only as `#N` on GitHub.** A dependency on another
  tracker, a document or a person gets a warning at most, and needs a human to
  confirm it's satisfied.
- **The score compares tickets; it doesn't rank them.** Two tickets at 9 can be
  weak for completely different reasons, and the Issues list is where that
  shows.
