# Spec Execution

**Work a task list forward, one task at a time, test first, and keep the record
honest enough that the next session can start from the files alone.**

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r implement-spec /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/implement-spec <spec-id>

or: "continue the spec", "work the next task"
```

**Working by hand:** read [SPEC.md](./SPEC.md) for the loop and the stop
conditions. [CUSTOMIZE.md](./CUSTOMIZE.md) binds it to your document names, ID
scheme and evidence format.

## What it does

Reads the spec, plan and task list in full, picks the first unchecked task whose
dependencies are met, implements it test first, runs the task's own verification
command, and writes down the command, its real output and the requirement
status. Then the next one.

It stops in two situations, and both matter more than the happy path: when a
task reveals the spec is wrong, in which case it records the conflict and waits
for a person rather than quietly editing the spec, and when a task is blocked,
in which case it records the blocker and moves on.

## Who uses it

- **Teams running agents against written specs**, who need the record to survive
  the session
- **Anyone resuming work they left a week ago**, since the files carry the state
- **Leads who want traceability** from a requirement to the command that proved
  it

## Pairs with

`test-first` produces the evidence, `verify-done` refuses the claim without it.
This skill calls both, once per task.

It is the third step of a loop: [create-spec](../create-spec/SKILL.md) (or
[recover-spec](../recover-spec/SKILL.md) for existing code) writes the spec,
[plan-spec](../plan-spec/SKILL.md) writes the plan and task list this reads,
and [review-spec](../review-spec/SKILL.md) is the independent review once the
last task is checked.

## What it will not do

It inherits the task list's quality: a verification command that proves nothing
produces a checked box that means nothing. It does not design, it cannot tell a
bad requirement from a hard one, and it will not reorder work around an
undeclared dependency. The Limitations section in [SPEC.md](./SPEC.md) is the
full list.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
