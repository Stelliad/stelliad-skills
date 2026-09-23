# Ticket Creation Specification

## System Overview

Most bad tickets aren't lazy. They're written by someone who knows exactly what
they mean, for a reader who'll have the same conversation in their head. Once
the reader is an agent picking work off a queue, or an engineer who joins next
month, that conversation is gone, and the ticket is all there is.

This skill turns a rough idea into a ticket that survives that reader. It
applies the Ticket Authoring Standard, which lives in one place:
[review-ticket/STANDARD.md](../review-ticket/STANDARD.md). This folder doesn't
carry a copy, because two copies of a standard drift and the stale one still
reads as authoritative.

It's the **author**. [review-ticket](../review-ticket/SKILL.md) is the
**checker**, and this skill calls it before declaring anything Ready. Neither
does the other's job: the author never grades its own output, and the checker
never edits.

## The sequence

```
1. LEARN     what the repo already requires, so the ticket leaves it out
2. INSPECT   what actually exists: service, behaviour, API, schema, tests, specs
3. SHAPE     spec plus parent, spike, several tickets, or one ticket
4. DRAFT     required sections for the shape, conditional ones only when they carry information
5. CLASSIFY  risk, priority, and any human approval gate
6. GATE      review-ticket, up to three refinement passes
7. HAND OVER show it, ask, create only on a yes, never apply the Ready label
```

## Why the steps are in that order

**Learning what the repo requires comes first** because the most common way a
ticket bloats is restating standards that already bind the work: testing,
logging, review, CI. An agent re-reads the ticket on every pass, so each
restated line is a recurring cost that buys nothing. Reading the rules first is
how you know what to leave out.

**Inspection comes before drafting** because a ticket written from the idea
alone describes a generic system. Inspection is also where invented context
gets caught: if the repo has no email provider, the ticket can't name one.

**Shape comes before drafting** because a spike written as an implementation
ticket skips the decision it exists to produce, and a three-outcome ticket
written as one gets built as one tangled PR.

**The gate comes last and is external.** A skill that checks its own work finds
what it was already looking for.

## Assumptions against decisions

The line this skill walks most often: a fact is missing. What happens next
depends on what the fact changes.

| The missing answer | Do |
|---|---|
| Is resolvable by reading the repo | Read the repo. Don't ask |
| Has a safe default, and one option is already present | Pick it, and state it under `## Assumptions` so it can be challenged |
| Changes architecture, security, scope or product behaviour | Don't pick. The ticket is BLOCKED; name the decision and who owns it |
| Is simply unknown and the section needs it | Write `UNFILLED` in the section. The checker blocks on it |

The failure this prevents is the plausible guess. A ticket that names a vendor
nobody chose passes review, gets built, and fails later and more expensively
than one that stalls now.

## Splitting

A ticket splits on outcome boundaries, never to make pieces smaller. Each piece
has its own objective, its own acceptance criteria and its own reviewable PR.
Vertical slices beat horizontal ones: one ticket carrying the minimal data, API
and UI change for one outcome is verifiable; a frontend ticket, a backend ticket
and a database ticket for the same outcome aren't, alone.

The children are wired with `Depends on #N` and attached to the parent as
sub-issues. The original stays open until the children exist, then closes with
a comment listing them.

Work big enough that its requirements need reviewing and tracing gets a spec
and one parent issue instead. Minting an issue per requirement puts execution
state in two places.

## The Ready label is a human act

The skill never applies the label that makes a ticket eligible for an agent to
pick up. It reports the verdict and says the label is the human's to apply.
Applying it is the moment someone takes responsibility for the ticket being
right, and an automated step can't take that responsibility for them.

## Worked examples

[examples.md](./examples.md) walks through fourteen synthetic tickets, including
the vague request that fails on six defects, the same request written properly,
and the mechanically clean ticket that's still BLOCKED.

## Limitations

- **It's only as good as the inspection.** In a repo it can't read, or a
  monorepo too big to survey, it falls back to what the user said, and
  generic tickets follow.
- **It can't supply facts nobody has.** Three refinement passes that don't reach
  READY usually mean a missing answer, and the skill's job then is to name it,
  not to fill it.
- **It doesn't know your priorities.** Priority comes from what the user says or
  your triage policy; the skill doesn't infer business urgency.
- **It creates GitHub issues only.** For other trackers it produces the markdown
  ticket and stops. CUSTOMIZE.md covers wiring in a different create command.
- **The split is a proposal.** Whether two outcomes are "tightly coupled" is a
  judgement, and the person who knows the codebase gets the last word.
