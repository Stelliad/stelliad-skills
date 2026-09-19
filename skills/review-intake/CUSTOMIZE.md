# Review Intake: Customization Guide

## Before you start

This skill is mostly procedure, so there is less to bind than usual. What it
does need is your review tool's commands, your escalation path, and a house
answer to the question it cannot answer for you: what counts as enough evidence
to push back.

## Customization 1: The review tool and its reply command

**Where it is used:** SPEC.md, *Replying in threads* and the sequence's step 7.

Replies go inside the thread that raised the finding. Bind the two commands:

```
List open threads:   <the command that prints id, file, line and body>
Reply to thread:     <the command that posts under a given thread id>
Resolve thread:      <if your tool separates replying from resolving>
```

For a hosted service this is usually its CLI or API. Write the commands out
here, with the placeholders your repository actually uses, so nobody has to
reconstruct them under time pressure.

**If you skip it:** replies land as top-level comments, findings stay
unresolved, and the count at the end of the report means nothing.

## Customization 2: Which reviewers feed this

**Where it is used:** SPEC.md, *Verify before implementing*, and rule 6.

```
Human reviewers:     <roles, and whether any of them is final>
Automated:           <the bots, linters and scanners whose output arrives here>
Known-noisy sources: <the ones whose findings are usually wrong, and how>
```

Rule 6 says automated findings get more scrutiny, not less. If one of your tools
has earned the opposite treatment, write that down with the reason rather than
letting it happen quietly.

**If you skip it:** every source is treated as having no context, which is
conservative and occasionally insulting to a good reviewer.

## Customization 3: What "out of scope" costs

**Where it is used:** SPEC.md, the disposition table.

```
Ticket goes to:   <tracker, and which queue>
Who files it:     <the implementer, same session>
Linked where:     <in the thread reply, so it is checkable>
Reviewed by:      <who confirms it was really out of scope>
```

**Name the check.** The disposition works only if the ticket exists, and the
only reliable way to keep that true is for someone other than the person who
wanted to move on to look.

**If you skip it:** the ticket gets filed most of the time, which is the same as
saying the disposition is unreliable.

## Customization 4: The evidence bar for pushing back

**Where it is used:** SPEC.md, *When to push back*, and rule 4.

Teams differ on this, and the difference is usually unspoken until it costs
someone a bad exchange. Write yours:

```
Enough to push back:    <e.g. a failing test, a search with zero hits,
                         a linked decision record, a version constraint>
Not enough:             <e.g. "it works", preference, "we have always done it this way">
Where the reasoning goes: <the thread, always>
```

**If you skip it:** the examples in SPEC.md set the bar, which is roughly "a fact
someone else can check in under a minute".

## Customization 5: Escalation

**Where it is used:** SPEC.md, rule 9.

A finding that contradicts an architectural decision already made is a decision
to reopen, not a fix to apply:

```
Escalates to:       <a person or a role, not "the team">
Goes where:         <a decision record, a channel, a meeting>
While waiting:      <the item is parked; the rest of the set continues>
```

**If you skip it:** the item gets absorbed into the branch, which is how an
architectural decision gets reversed by a comment nobody read as a reversal.

## Customization 6: The test and verification gate

**Where it is used:** SPEC.md, *Implementation order*.

```
Test per item:    <the test-first skill, or your own convention>
Suite command:    <what runs between items>
Final gate:       <the verify-done skill, a CI job, a checklist>
```

`test-first` and `verify-done` in this collection are built for this: one
produces the evidence per item, the other refuses the "review addressed" claim
without it.

**If you skip it:** a test per item and a suite run between items, with no named
command.

## Customization 7: The report

**Where it is used:** SPEC.md, *Output*.

```
Posted where:   <the pull request description / a comment / nowhere, it is for you>
Kept:           <in the repo / in the tracker / not kept>
Audience:       <yourself / the reviewer / a lead>
```

The table is most useful posted, because it makes the pushed-back items visible
to the person who raised them rather than leaving them to notice.

**If you skip it:** it is produced and shown to whoever ran the skill.

## Final checklist

- [ ] Thread list, reply and resolve commands written out
- [ ] Reviewers and known-noisy sources named
- [ ] Out-of-scope ticket path bound, with someone checking it
- [ ] Evidence bar for pushing back agreed
- [ ] Escalation target named as a person or role
- [ ] Test-per-item and final gate named
- [ ] Report destination decided

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The triggers and what it is for |
| `SPEC.md` | The sequence, verification, dispositions, push-back, rules, limitations |
| `CUSTOMIZE.md` | This file: tool commands, reviewers, escalation, evidence bar |
