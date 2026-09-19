# Spec Execution Specification

## System Overview

A spec with a task list is a plan for work someone will do later, often a
different someone, often after the conversation that produced it is gone. This
skill executes that plan and keeps the record as it goes, so the next session
can start from the files alone.

Two responsibilities, and only two:

- **Which task is next**, by dependency rather than by preference.
- **Keeping the record honest**: the checkbox, the evidence, the requirement
  status, and the conflicts that stopped a task.

Everything about *how* the change is made is delegated: the failing test first,
the minimum code to pass, and a verification gate that refuses a completion
claim with no fresh output behind it.

## The state it reads

Three documents, read in full at the start of every run:

| Document | What it carries |
|---|---|
| The spec | Requirements, each with an ID, and acceptance criteria |
| The plan | Phases, and how the work was meant to be sequenced |
| The task list | Tasks with IDs, dependencies, requirement references, and a verification command each |

Nothing else. In particular, nothing from an earlier conversation that is not
written in those three files: that is what makes the work resumable, and it is
the property people lose first.

## The loop

### 1. Select

The first unchecked task, in phase order then ID order, whose dependencies are
all checked. If a specific task was named, use it, but confirm its dependencies
first and stop if they are not met.

### 2. Understand

Read what the task and its cited requirements actually ask for, and the
relevant part of the plan. A task that seems to say something different from its
requirement is a conflict, not an ambiguity to resolve quietly: see *When the
spec is wrong*.

### 3. Implement, test first

Write the failing test, watch it fail for the stated reason, then the minimum
code that passes it. Not production code first with a test adapted afterwards;
the order is the whole point, because a test written after the code tends to
assert what the code does.

### 4. Verify

Run the task's own verification command and capture the real output. A command
that was run before the last edit is not evidence about the current state.

### 5. Record

- Check the task's box
- Add the command and its actual output to the evidence section
- Set each cited requirement's status: passing only where the evidence supports
  it, otherwise failing or blocked, with the reason
- Cite the file the change lives in

The record is the deliverable as much as the code is. A checked box with no
output under it is a claim.

## When the spec is wrong

A task can reveal that a requirement is infeasible, contradicts another
requirement, or contradicts something already true of the codebase. When that
happens: **stop.**

Do not edit the spec to match what you are about to build. Record the conflict
where the spec's review findings live, report it, and let a person rule. The
temptation to quietly narrow a requirement is strongest exactly when the
narrowing would be hardest to notice later.

## When a task is blocked

Mark it blocked with the reason, move to the next eligible task, and report
every blocker at the end. One blocked task should not stop the run; a run that
hides blockers until the end is worse than one that stops.

## Rules

1. **One task at a time.** Do not implement three and verify afterwards.
2. **No checkbox without evidence.** A green feeling is not a green checkbox.
3. **No scope creep.** A problem found outside the current task becomes a
   finding or a new task, not an inline fix.
4. **Never silently edit the spec.**
5. **A previous session's claim is not evidence.** Confirm with the repository
   state and by re-running the verification command before trusting a checked
   box you did not check yourself.

## Reporting

At the end: which tasks were completed and with what evidence, every blocker,
and how many unblocked tasks remain. If everything is checked, say so and point
at the final verification and an independent review, but do not run either
automatically. Completion is confirmed, not assumed.

## Limitations

- **It inherits the task list's quality.** A verification command that proves
  nothing produces a checked box that means nothing. The task list is where to
  spend the care.
- **It cannot tell a bad requirement from a hard one.** It can only notice a
  contradiction, and only when the contradiction is visible from the files.
- **Dependency order is only as good as the declared dependencies.** An
  undeclared one shows up as a task that cannot be finished.
- **It does not design.** Where the spec is silent, it will follow the code's
  existing pattern rather than propose a better one.
- **The record is a record, not a proof.** It captures the output a command
  produced; whether that command was the right one is the task author's call.
