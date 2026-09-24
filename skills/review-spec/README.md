# Spec Review

**The independent check before a spec calls itself done: every requirement
walked to its code and test, every lens delegated, every finding ranked and
written down, and the decision left to a person.**

## Running it

This is a specification an agent executes, not a binary. It reads the task list
in the shape [create-spec](../create-spec/README.md)'s templates define, and it
delegates to other skills in this collection, so copy the loop and its
reviewers:

```bash
cp -r create-spec plan-spec implement-spec review-spec \
      review-principles find-dead-code coverage-gaps verify-done secret-scan \
      /path/to/your-project/.claude/skills/
```

Then invoke it, from a fresh session:

```
/review-spec 004

or: "is SPEC-004 ready to complete", "final review of this spec"
```

**Working by hand:** read [SPEC.md](./SPEC.md) for the requirement walk and the
severity map, then fill the Review Findings table at the bottom of the spec's
`TASKS.md`.

## What it does

Starts from the spec, not from the implementer's record. For every requirement
it finds the code and the test that meet it, and treats a `PASS` with nothing
behind it as a finding. Then it runs the lenses a single implementer can't run
on their own work: correctness through your harness's code review, structure
through review-principles, dead code, test coverage, a fresh verification run,
and your own reviewers if you bind them. Everything lands in one table on one
severity scale, and the report ends with Complete or Not Complete.

## Who uses it

- **Teams running coding agents**, where the implementer and the reviewer
  shouldn't be the same conversation
- **Leads who sign off on finished work**, and want the evidence, not the
  summary
- **Teams with an existing review panel**, who want it run the same way every
  time

## Pairs with

[implement-spec](../implement-spec/SKILL.md) builds what this reviews and fixes
what it finds. [review-intake](../review-intake/SKILL.md) is how the
implementer takes the findings in without agreeing to all of them.

## What it will not do

It won't fix a finding, change a requirement, or mark the spec complete. It
can't tell you a requirement was the wrong one to build. The Limitations
section in [SPEC.md](./SPEC.md) is the full list.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
