---
name: create-ticket
description: Turn a rough idea into a ticket that passes the Ready gate, or split an oversized one. Inspects the repo for real context, applies the Ticket Authoring Standard, records assumptions instead of inventing facts, and calls review-ticket before declaring anything Ready. Use when saying "make a ticket for", "write this up as an issue", "file this", "/create-ticket", or "split this ticket".
license: MIT
compatibility: Any repository. Creates GitHub issues through the gh CLI by default; for another tracker it produces a markdown ticket to paste. Needs the review-ticket skill installed alongside it. Adapt via CUSTOMIZE.md.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
  argument-hint: "<rough idea> [--repo owner/repo] [--split <issue-number>]"
type: skill
scope: all
status: active
---

# create-ticket

Rough idea in, a ticket a fresh session could execute out.

The standard is [review-ticket/STANDARD.md](../review-ticket/STANDARD.md). Read
it first, every run. It lives with `review-ticket` and nowhere else, so this
skill needs that one installed beside it.

This skill writes. It doesn't grade its own work: `review-ticket` is the gate,
and nothing here is called Ready until that gate returns READY.

## Arguments

- `$1`: the rough idea, in whatever words the user used. Required unless
  `--split` is given.
- `--repo owner/repo`: the target. When not given, resolve it from the current
  checkout's `origin` remote, and say which repo you resolved to before
  writing anything.
- `--split {n}`: rebuild an existing oversized issue as several.

## Procedure

### 1. Learn what not to write

Read the target repo's README, its contributor guide or agent rules, its pull
request template, and its CI configuration.

You're reading these to know **what to leave out**. Everything they already
require (secure coding, testing, logging, least privilege, review, CI) stays out
of the ticket. Note only an exception.

Find the project-level gate: the required CI checks, or the test command your
agent runner enforces. Where it's absent or always passes, the ticket's
`## Verification` section is the only real check and becomes mandatory.

### 2. Inspect before drafting

Find what actually exists: the affected service, the current behaviour, the
API, the schema, the tests, related open issues, any spec that covers this. A
ticket written without this step is generic and describes a system that may not
be the one in front of you.

**Don't invent context.** If the idea says "add notifications" and the repo has
no email or push provider, don't name one. Record it as an unresolved decision,
or, where the choice is genuinely low-stakes and one option is already present,
record the choice under `## Assumptions`.

### 3. Decide the shape before writing

| The work is | Then |
|---|---|
| Large enough that its requirements need reviewing and tracing | Write a spec first, then one parent issue pointing at it that references requirement IDs and never copies them |
| A question, not a build | A spike. Its deliverable is a decision, never shipped behaviour |
| More than one independently deliverable outcome | Several tickets, in dependency order. See *Splitting* |
| One outcome | One ticket |

### 4. Draft

Use the required section set for the shape, plus only the conditional sections
that carry real information. Omit the rest rather than writing `N/A`. An agent
working the ticket re-reads every section on every pass, so an empty section is
a recurring cost with no return.

Acceptance criteria are the part that has to be right. Flat `- [ ]` items, one
observable outcome each, in execution order, no nesting and no prose between
them. Include the failure behaviour, not only the happy path. Never restate a
requirement as a criterion in the same words.

Where the input doesn't supply something and there's no safe default, write
`UNFILLED` in that section rather than guessing. The checker blocks on it, which
is the point.

### 5. Classify

Risk from the standard's table, with a one-line reason for High or Critical.
Priority from your priority labels. Where anything must be prepared but not
executed by an agent (a production deploy, an IAM change, a production
migration, a secrets change, anything destructive), write `## Human Approval`
and plan for the human-required label.

### 6. Gate it

Run [review-ticket](../review-ticket/SKILL.md) on the draft:

```
/review-ticket {path-or-issue}
```

Act on the findings and re-run. Where a finding is a missing decision rather
than a drafting gap, stop: the verdict is BLOCKED, and the fix is an answer from
a human, not a better sentence from you.

Cap this at three refinement passes. If it won't reach READY in three, the
remaining gaps are facts nobody in the session holds. Say what they are and who
owns them.

### 7. Hand it over

Show the finished ticket, the verdict and the score. Then ask before creating
anything:

```
Create this in {repo}? Labels: {type}, {priority}, {risk}
```

Only on an explicit yes:

```bash
gh issue create --repo {owner/repo} --title "{title}" --body-file {path} --label "{labels}"
```

**Never apply the Ready label in the same breath as creating the issue.** It's
the signal that lets an agent pick the work up, and applying it is a separate,
deliberate act by a human who has read the ticket. Say the verdict, say the
label is theirs to apply, and stop.

## Splitting

With `--split {n}`: read the issue, run `review-ticket` on it, and use its split
analysis.

Split on outcome boundaries, never to make pieces smaller. Each resulting
ticket has to stand on its own: its own objective, its own acceptance criteria,
its own reviewable PR. State the dependency order plainly and wire it with
`Depends on #N` lines, then attach each child to the parent as a sub-issue (the
command is in the standard).

```
#142 Add API-key persistence
   -> #143 Add API-key service
        -> #144 Add API endpoints
             -> #145 Add account UI
             -> #146 Add audit events
```

Prefer vertical slices. A frontend ticket plus a backend ticket plus a database
ticket for one feature is three tickets nobody can verify alone.

Leave the original issue open until its children exist, then close it with a
comment listing them. Don't delete it: it's the record of why the split
happened.

## Rules

- **Read the repo before drafting.** A ticket written from the idea alone
  describes a generic system.
- **Never invent a service, library, or vendor** the repo doesn't already use.
- **Never put a credential, token, key, or customer record into a ticket**, and
  never a working exploit path into a security ticket.
- **Never duplicate a repo standard into a ticket.** Only an exception to one
  belongs there.
- **Never grade your own output.** `review-ticket` decides.
- **Never apply the Ready label.** Recommend it; a human applies it.
- **Ask only about decisions** that change architecture, security, scope, or
  product behaviour. Anything reading the repo would resolve, resolve by
  reading the repo.

Worked examples are in [examples.md](./examples.md). See [SPEC.md](./SPEC.md)
for the reasoning, and [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for
your organization.
