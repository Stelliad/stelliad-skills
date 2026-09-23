# Ticket Review

**Grade a ticket before anyone picks it up, and name exactly what would stop a
fresh engineer or an unattended agent from building the right thing.**

## Running it

This is a specification an agent executes, plus a small standard-library Python
checker. Install it by copying this folder into your project's skills
directory:

```bash
cp -r review-ticket /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/review-ticket 42 --repo your-org/your-repo
/review-ticket drafts/session-expiry.md

or: "is this issue ready for an agent", "should this ticket be split"
```

**Working by hand:** run the checker yourself, then walk the Definition of
Ready in [STANDARD.md](./STANDARD.md):

```bash
python3 scripts/review-ticket.py --file draft.md --title "Add idle expiration to admin sessions"
```

## What it does

Runs the checker for everything a script can decide, reads the repo to catch
what it can't, and returns one of three verdicts with a score out of twelve:

| Verdict | Means |
|---|---|
| `READY` | No blocking defect, score 10 to 12 |
| `NEEDS_REFINEMENT` | A blocking defect, or a score of 9 or under |
| `BLOCKED` | A decision that changes architecture, security, scope or product behaviour hasn't been made |

It also says when a ticket is really two or three, and how to split it.

```
Verdict:  NEEDS_REFINEMENT
Score:    6 / 12

Issues
  "Improve session handling" states a task, not an outcome. An agent can't
  tell from it what would be true when the work is done.
  Acceptance criteria are nested two levels, so an agent working them as a
  queue can't tell the items apart.
  Scope names what's in and not what's out, so nothing stops this becoming a
  login redesign.

Missing information
  What the idle window should be, and whether it applies to non-admin users.

Recommended changes
  Title: "Add idle expiration to admin sessions".
  Add: a request on an expired session returns 401.
```

## Who uses it

- **Teams running coding agents off an issue tracker**, where the ticket is the
  whole prompt
- **Engineering leads** triaging a backlog before a sprint
- **Anyone filing an issue for someone else**, who wants to know it'll survive
  being read without them in the room

## Pairs with

[create-ticket](../create-ticket/README.md) writes tickets to the same
standard and calls this one before declaring anything Ready. `verify-done`
checks the work once it's built.

## What it will not do

It never edits a ticket and never applies a label. It grades the ticket, not
the work, and its judgement half is only as good as its reading of the repo.
The Limitations section in [SPEC.md](./SPEC.md) is the full list.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
