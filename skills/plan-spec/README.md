# Spec Planning

**Read the repository before planning against it, then write a task list an
implementer can resume cold, every task carrying the command that proves it.**

## Running it

This is a specification an agent executes, not a binary. It needs
[create-spec](../create-spec/README.md) installed beside it, because that's
where the `PLAN.md` and `TASKS.md` templates live. Copy the loop:

```bash
cp -r create-spec plan-spec implement-spec review-spec /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/plan-spec 004
/plan-spec SPEC.md

or: "plan out SPEC-004", "break this spec into tasks"
```

**Working by hand:** check the spec is ready, read the code it touches, then
fill [the plan template](../create-spec/templates/PLAN.md) and
[the task template](../create-spec/templates/TASKS.md).
[SPEC.md](./SPEC.md) has the gate and the task shape.

## What it does

Stops unless the spec is ready. Then reads the code the spec touches: the
stack, the runners that actually exist, the patterns the nearest similar
feature follows, and the standards files your team binds to each kind of
requirement. Writes a plan that cites what it read, and a task list where every
task names the requirements it serves, what it depends on, and a command that
proves it. Every spec ID gets a row in the traceability table, so nothing is
dropped without someone seeing it.

## Who uses it

- **Teams running coding agents against specs**, where the task list is the
  agent's whole brief
- **Leads who review plans before work starts**, since every claim cites a file
- **Anyone who inherited a codebase**, planning from a recovered spec rather
  than a written one

## Pairs with

[create-spec](../create-spec/SKILL.md) and [recover-spec](../recover-spec/SKILL.md)
produce the spec. [stress-test-plan](../stress-test-plan/SKILL.md) can attack
the plan before it's built. [implement-spec](../implement-spec/SKILL.md) works
the tasks forward, and [review-spec](../review-spec/SKILL.md) checks the result.

## What it will not do

It won't plan a draft, touch code, edit the spec, or narrow a requirement that
is hard to plan. It can't tell whether a test that runs green asserts the right
thing. The Limitations section in [SPEC.md](./SPEC.md) is the full list.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
