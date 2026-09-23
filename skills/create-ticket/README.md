# Ticket Creation

**Turn a rough idea into a ticket a fresh engineer or an unattended agent could
execute without the conversation that produced it.**

## Running it

This is a specification an agent executes. It needs
[review-ticket](../review-ticket/README.md) installed beside it, because that's
where the standard and the gate live. Copy both folders:

```bash
cp -r create-ticket review-ticket /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/create-ticket admins stay logged in forever, sessions should expire
/create-ticket --split 87

or: "write that up as an issue", "file this", "split this ticket"
```

**Working by hand:** write the ticket to
[STANDARD.md](../review-ticket/STANDARD.md), then run `review-ticket` on it.
[examples.md](./examples.md) shows good and bad versions side by side.

## What it does

Reads the target repo first, so the ticket describes the system that actually
exists rather than a generic one, and leaves out everything the repo's own
rules already require. Picks the shape (one ticket, several, a spike, or a spec
with one parent). Drafts to the standard, records assumptions where a safe
default exists and unresolved decisions where one doesn't, then hands the draft
to `review-ticket` and refines until it returns READY.

It also splits an oversized issue into several that each stand alone, with the
dependency order stated and each child attached to the parent.

## Output

A finished ticket, the verdict and score from `review-ticket`, and a question
before anything is created. Nothing reaches the tracker without an explicit
yes, and the skill never applies the Ready label: recommending it is the most
it does.

## Who uses it

- **Teams running coding agents off an issue tracker**, where the ticket is the
  whole prompt
- **Founders and leads** turning a Slack message or a call note into real work
- **Anyone splitting an epic** that's quietly three projects

## What it will not do

Invent a vendor, a service or a requirement to fill a gap. A missing decision
comes back as BLOCKED with the question named and the owner identified. A
ticket built on a guess fails later and more expensively than one that stalls
now. The Limitations section in [SPEC.md](./SPEC.md) has the rest.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
