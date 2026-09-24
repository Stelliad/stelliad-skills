# Spec Recovery

**Work backwards from a running system to the spec nobody wrote, and grade every
line by what it rests on.**

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r recover-spec /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/recover-spec <repo-path> [--as-spec|--as-reading] [--questions-only]

or: "there's no spec for this", "what does this system actually do"
```

**Working by hand:** read [SPEC.md](./SPEC.md) for the procedure and the grades,
and [references/spec-skeleton.md](./references/spec-skeleton.md) for the shape of
the document. [CUSTOMIZE.md](./CUSTOMIZE.md) binds the output routes and who
answers the questions.

## What it does

Pins the reading to a commit, draws the system boundary, inventories every
surface, traces the core data path from user action to durable write, recovers
the data model and the invariants nothing enforces, and reads the tests as the
only requirements the system states about itself.

Every statement gets one of five grades: observed, inferred, intended,
undecided, contradiction. The undecideds become a question list addressed to
whoever owns the system, and that list is the most useful thing the run
produces.

## Who uses it

- **Teams inheriting a codebase** from another team, a vendor or an acquisition
- **Anyone about to rewrite or migrate** a system, since the undecided list is
  exactly what a rewrite loses
- **Reviewers doing diligence** on a product they won't own
- **Security and compliance reviewers** who need the surface inventory and the
  data path before they can start

## Pairs with

[tech-doc-review](../tech-doc-review/SKILL.md) grades the output.
[coverage-gaps](../coverage-gaps/SKILL.md) takes the untested sections.
Once the questions are answered, [plan-spec](../plan-spec/SKILL.md) turns the
spec into tasks (or [create-spec](../create-spec/SKILL.md) writes the change
you want to make against it), and [implement-spec](../implement-spec/SKILL.md)
works them forward.

## What it will not do

It won't change the code, fix a defect, invent a reason for a constant, or
decide which behaviour was intended. It can't recover intent nobody recorded,
and it sees runtime configuration by name only. The Limitations section in
[SPEC.md](./SPEC.md) is the full list.

## The idea in one line

`MAX_RETRIES = 3` is an observed behaviour and an undecided requirement. A spec
that can't tell those apart turns every bug into a requirement.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
