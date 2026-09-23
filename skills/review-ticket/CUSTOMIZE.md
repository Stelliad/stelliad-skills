# Ticket Review: Customization Guide

## Before you start

This skill ships with a standard, a checker and a label vocabulary. All three
are defaults. The work below binds them to your tracker, your labels and your
risk policy. Change [STANDARD.md](./STANDARD.md) first and the checker second:
the standard is the source, and the checker mirrors it.

After any change to `scripts/review-ticket.py` or a fixture, run
`bash scripts/run-fixtures.sh` and keep it green. Update
`fixtures/expected.json` in the same change when you deliberately move a
verdict.

## Customization 1: Your labels

**Where it's used:** STANDARD.md, *Labels*, and the constants near the top of
`scripts/review-ticket.py`.

```python
PRIORITY_LABELS = {"P1-urgent", "P2-high", "P3-medium", "P4-low"}
RISK_LABELS = {"risk:low", "risk:medium", "risk:high", "risk:critical"}
READY_LABEL = "agent-ready"
HUMAN_REQUIRED_LABEL = "agent:human-required"
TOOLING_LABELS = ("agent:blocked", "agent:needs-review")
```

Rename these to whatever your queue already filters on, and change the Labels
table in STANDARD.md to match. The one decision that matters: **pick exactly one
Ready label.** Two labels meaning roughly the same thing is how a queue ends up
pulling half-finished tickets.

If your runner writes its own labels (claimed, blocked, needs review), list
them in `TOOLING_LABELS`, and the checker will flag one that looks hand-applied.

### Create the labels on the repo

GitHub rejects `gh issue create --label` for a label the repo doesn't have, so
`create-ticket` fails at its last step on a fresh repo. Create the set once per
repo, with your names if you renamed them. `--force` updates a label that
already exists instead of failing:

```bash
REPO=your-org/your-repo
while IFS='|' read -r name color desc; do
  gh label create "$name" --repo "$REPO" --color "$color" --description "$desc" --force
done <<'LABELS'
P1-urgent|b60205|Queue first
P2-high|d93f0b|Queue order: high
P3-medium|fbca04|Queue order: medium
P4-low|c2e0c6|Queue order: low
agent-ready|0e8a16|Meets the Definition of Ready; an agent may pick it up
agent:human-required|5319e7|Carries a Human Approval gate
agent:blocked|000000|Written by the agent runner, never by hand
agent:needs-review|000000|Written by the agent runner, never by hand
status:blocked|e11d21|A decision is open (Ready item 8)
status:ready-to-merge|1d76db|PR open and green, waiting on a merge
type:feature|a2eeef|Feature
type:bug|d73a4a|Bug
type:spike|d4c5f9|Spike
type:security|b60205|Security
type:infra|006b75|Infrastructure
type:tech-debt|bfdadc|Tech debt
type:docs|0075ca|Documentation
risk:low|c2e0c6|Risk: low
risk:medium|fbca04|Risk: medium
risk:high|d93f0b|Risk: high
risk:critical|b60205|Risk: critical
LABELS
```

Drop the rows you don't use. `agent:blocked` and `agent:needs-review` only
matter if an agent runner writes them.

**If you skip it:** the priority and risk checks still work if you use the
default names, and quietly never fire if you don't. `create-ticket` can't apply
a label the repo doesn't have.

## Customization 2: Your issue tracker

**Where it's used:** SKILL.md step 1, and `read_issue()` and
`check_dependencies()` in the script.

GitHub issues through the `gh` CLI is the default. For anything else:

- **Any tracker, no code change:** export or paste the ticket body to a
  markdown file and run `--file {path} --title "{title}" --label ...`. Every
  check except dependency resolution runs the same way.
- **Jira, Linear, GitLab, Azure Boards:** replace `read_issue()` with a call to
  your tracker's CLI or API that returns `title`, `body` and a list of label
  names. Replace the `gh issue view` call in `check_dependencies()` so a `#N`
  (or your tracker's key format, such as `ABC-123`) resolves to open or closed.
  Change the `#(\d+)` pattern there to match your key format.
- **Trackers with rich-text bodies:** convert to markdown first. The checker
  finds sections by `##` or `###` headings and acceptance criteria by `- [ ]`.

**If you skip it:** non-GitHub tickets work from a file, and their dependencies
come back as warnings for a human to confirm.

## Customization 3: Your risk levels

**Where it's used:** STANDARD.md, *Risk*, and `check_risk()` and
`check_human_approval()` in the script.

The four levels are Low, Medium, High and Critical. If your org uses a
different scale, change three things together:

1. The Risk table in STANDARD.md, with what each level means for you.
2. The level regex in `check_risk()`, and which levels need a stated reason.
3. Which level requires a `## Human Approval` section in
   `check_human_approval()`.

Write down what an agent may never run unattended at each level. That list is
what goes in a ticket's Human Approval section, and it's the part people most
often leave implicit.

**If you skip it:** a ticket using another scale fails with "Risk does not name
a level".

## Customization 4: Your section names and issue forms

**Where it's used:** `SHAPES`, `KNOWN_SECTIONS` and `SECTION_ALIASES` in the
script.

The shipped `SECTION_ALIASES` rows match a set of sample issue forms that
aren't included here, so treat them as examples rather than a match for your
repo. If your issue forms use labels like "Risk of the fix" or "What done looks like",
add a row to `SECTION_ALIASES` mapping the casefolded label to the canonical
section, and add a fixture that is the form's rendered output. Form labels are
the first thing to drift, and a mismatch shows up as a "missing required
section" on a ticket that has it.

To add a shape (an incident follow-up, say), add it to `SHAPES` with its
required sections and teach `detect_shape()` the heading that identifies it.

**If you skip it:** hand-written tickets using the standard's headings work;
form submissions with renamed fields fail.

## Customization 5: Vague words and generic titles

**Where it's used:** `VAGUE_VERBS`, `MEASURABLE`, `GENERIC_TITLES` and
`UNDECIDED` in the script.

Add the phrases your team actually hides behind. Two cautions: a word that's
also a legitimate noun in your domain ("refactor" in a refactoring tool) will
fire constantly, and the measurable-target rescue is a regex, so a criterion
with any digit on the line passes. Tighten `MEASURABLE` if that's too generous
for you.

**If you skip it:** the shipped list catches the common ones.

## Customization 6: Your project-level gate

**Where it's used:** STANDARD.md, *Verification, and who's authoritative*.

Name the gate that decides whether work is done in your repos: required CI
checks, or the test command your agent runner enforces. Where a repo has no
real test command, say so in that repo's docs, so a reviewer knows the ticket's
`## Verification` section is the only real check.

**If you skip it:** reviewers can't tell whether a ticket's Verification
section is extra assurance or the only assurance.

## Customization 7: Where the gate is enforced

This is a specification an agent follows. To make it hold when nobody is
following it:

- A scheduled job or webhook that runs the checker on issues about to get the
  Ready label, and comments the result
- A queue that refuses tickets whose last recorded verdict wasn't READY
- Issue forms whose required fields match the standard's required sections

**If you skip it:** the gate holds as long as someone remembers to run it.

## Final checklist

- [ ] Label names in the script and STANDARD.md match what your queue reads
- [ ] The labels exist on every repo tickets are filed into
- [ ] Exactly one Ready label
- [ ] Tracker reading and dependency resolution work, or `--file` is the path
- [ ] Risk levels and their human approval rule written down
- [ ] Issue form labels mapped in `SECTION_ALIASES`, with a fixture each
- [ ] `bash scripts/run-fixtures.sh` passes

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | Triggers and the procedure |
| `SPEC.md` | Why the rules are what they are, the fixtures, the limitations |
| `STANDARD.md` | The Ticket Authoring Standard itself, the one copy |
| `CUSTOMIZE.md` | This file |
| `scripts/review-ticket.py` | The mechanical half |
| `scripts/run-fixtures.sh` | The regression suite |
| `fixtures/` | Fourteen synthetic tickets and their expected verdicts |
