---
name: review-ticket
description: Grade a ticket against the Ticket Authoring Standard and return READY, NEEDS_REFINEMENT, or BLOCKED with a score out of 12, naming exactly what stops safe execution. Also reports when a ticket holds more than one deliverable outcome and how it splits. Reports only, never edits the ticket. Use when saying "review this ticket", "is this issue ready", "can an agent pick this up", "should this be split", or "/review-ticket <#>".
license: MIT
compatibility: Any repository. GitHub issues by default through the gh CLI, or a local markdown draft for any tracker. The checker is Python 3.9+ standard library. Adapt labels, tracker and risk levels via CUSTOMIZE.md.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
  argument-hint: "<issue-number | file-path> [--repo owner/repo]"
type: skill
scope: all
status: active
---

# review-ticket

The gate a ticket passes before a human or an unattended agent picks it up. It
reports and never edits. [create-ticket](../create-ticket/SKILL.md) does the
writing and calls this one to confirm it's finished, because a skill that
grades its own output isn't a gate.

The standard is [STANDARD.md](./STANDARD.md), in this folder. Read it before
running this. Don't reconstruct the rules from memory, and never invent a
criterion that isn't in it.

## Arguments

- `$1`: an issue number, or a path to a markdown draft. Required.
- `--repo owner/repo`: required with an issue number. When you weren't told,
  resolve it from the current checkout's `origin` remote and say which repo you
  used.

## Procedure

Paths below are relative to this skill's folder.

### 1. Run the mechanical checks

```bash
python3 scripts/review-ticket.py --issue {n} --repo {owner/repo}
# or, for a draft or another tracker's export:
python3 scripts/review-ticket.py --file {path} --title "{title}" --label P2-high
```

Always run it. It decides everything that can be decided without judgement:
required sections for the ticket's shape, whether the acceptance criteria are a
flat checkbox list, vague verbs with no measurable target, an empty or `N/A`
section, a generic title, a missing out-of-scope half, a High or Critical risk
with no reason, an open `#N` dependency (resolved only with `--repo`; without
it the script warns and you check), a credential in the body.

A `BLOCKING` line isn't a judgement call you can overrule. Report it.

### 2. Read the repo before judging

The script can't tell an invented dependency from a real one. Before grading,
check what the ticket asserts about the codebase: does the named service
exist, does the API it references exist, is the constraint real. A ticket that
names an email provider in a repo that has never had one fails item 8, not
item 3.

Read the repo's README, its contributor or agent rules, and any spec the ticket
cites.

### 3. Grade the ten Ready items

Walk the Definition of Ready in the standard item by item, and record pass or
fail for each with the evidence. Then score:

| Dimension | Ready items | Max |
|---|---|---|
| Objective clarity | 1 | 2 |
| Context sufficiency | 2, 10 | 2 |
| Requirements clarity | 3 | 2 |
| Acceptance criteria | 4, 5 | 2 |
| Scope clarity | 6 | 2 |
| Dependencies | 7 | 1 |
| Risk and approval | 9 | 1 |

Full marks only where the dimension is genuinely complete. Half marks round
down. A dimension with a `BLOCKING` line against it can't score full.

### 4. Decide the verdict

| Verdict | When |
|---|---|
| `BLOCKED` | Ready item 8 fails: a decision that changes architecture, security, scope, or product behaviour hasn't been made. Report the score anyway |
| `NEEDS_REFINEMENT` | Any mechanical `BLOCKING` line, or a score of 9 or under |
| `READY` | No `BLOCKING` line and a score of 10 to 12 |

### 5. Check whether it's one ticket

A ticket holds more than one deliverable outcome when it spans unrelated
subsystems, needs more than one deployment, or has acceptance criteria that
would land in separate PRs. When it does, name the split: the titles, the
boundary between them, and the dependency order.

Don't split tightly coupled work to make the pieces smaller, and don't propose
a frontend, backend and database split when a vertical slice is available.
Where the requirements need reviewing and tracing, the answer is a spec and one
parent issue, not a pile of issues.

### 6. Report

```
Verdict:  READY | NEEDS_REFINEMENT | BLOCKED
Score:    X / 12

Strengths
  ...

Issues
  <what specifically stops safe execution, and why>

Missing information
  <the fact, not the section name>

Recommended changes
  <the concrete edit, not "add more detail">

Split
  <only when step 5 found more than one outcome>
```

Then a revised ticket, only when the verdict isn't READY and the fix is
editorial. Where the gap is a missing decision or a fact nobody in the session
holds, name the question and who owns it. Don't write a revised ticket that
invents the answer.

Where the verdict is READY, say so and stop. Don't rewrite a good ticket.

## Rules

- **Never edit the ticket.** Not the file, not the issue. Report the change and
  let `create-ticket` or a human apply it.
- **Never apply or remove a label**, the Ready label least of all. Applying it
  is a deliberate human act; this skill only says whether the checklist behind
  it is met.
- **"Vague" isn't a finding.** Name the sentence, say what a reader can't
  determine from it, and give the replacement.
- **Don't invent requirements** to fill a gap. A missing answer is a finding,
  not a drafting opportunity.
- **A credential in an issue body is a rotation event.** Report where it is,
  never reproduce the value, and say plainly that it needs rotating and a
  secret scan.
- This grades the ticket, not the work done against it.

See [SPEC.md](./SPEC.md) for the reasoning and limitations, and
[CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
