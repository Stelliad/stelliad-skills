# Completion Verification: Customization Guide

## Before you start

This skill ships with a proof table and a set of example commands. Both are
starting points. The work below binds them to your stack, your pipeline and
your definition of done, and it is worth doing once properly: an unbound
verification gate either passes things it should not, or asks for commands your
project does not have.

Work through the numbered sections. Each one names what to decide, where it is
used, and what happens if you skip it.

## Customization 1: The command set

**Where it is used:** SPEC.md, *Procedure*, steps 1 and 2.

The skill infers commands from `package.json`, `pyproject.toml`, a `Makefile` or
CI. If your project puts them somewhere else, or names them unusually, write the
list down here and the skill will use it as given.

```
Tests:      <command>
Lint:       <command>
Types:      <command>
Build:      <command>
Migrations: <command, if a schema change needs proving>
E2E:        <command, and when it is required rather than optional>
```

**Bind this to CI, not to habit.** The list should be the jobs a pull request
must pass. If CI runs a licence check and your list does not, the gate reports
clean while that job fails.

**If you skip it:** the skill guesses from the repo, which usually works and
silently omits whatever is unusual about your setup.

## Customization 2: What counts as proof for your claims

**Where it is used:** SPEC.md, *What each claim requires*.

The shipped table covers tests, lint, types, build, bug fixes, coverage,
migrations, deploys, delegated work and requirements. Add the claims your team
actually makes, and be specific about what does **not** count:

| Claim | Proof | Not proof |
|---|---|---|
| "The feature flag is live" | The flag read back from the running service | The config committed |
| "The index is built" | Query plan showing the index used | The migration applied |
| "It works on mobile" | The device or emulator run | A responsive layout in a desktop browser |

The third column does the work. It is where you record the substitution your
team actually makes when it is in a hurry.

**If you skip it:** claims outside the shipped table get verified by analogy,
which is exactly the reasoning this skill exists to stop.

## Customization 3: Scope of a full run

**Where it is used:** SPEC.md, step 2, "full commands, not scoped ones".

On a large monorepo, "run everything" may take an hour, and a rule nobody can
afford is a rule people route around. Define the honest middle:

- What is the smallest run that covers a change in package X?
- Which changes always require the full suite (schema, auth, shared libraries)?
- What is the time budget past which a run moves to CI instead of local?

Write the rule as a sentence someone can follow at 6pm on a Friday.

**If you skip it:** either the gate is ignored under time pressure, or every
small change pays the full suite's cost.

## Customization 4: The retry cap

**Where it is used:** SPEC.md, *The retry cap*.

Three attempts is the shipped default, for loops where something fixes and this
rechecks. Set yours, and say what happens at the cap:

- Attempts before stopping: `3`
- On reaching the cap: `report and stop` / `escalate to a human` / `open a ticket`
- What must be in the report: the failure, what was tried, what is blocking

**Never raise the cap to get past a specific failure.** That is the failure
telling you something, and a higher number is how a loop spends a day on it.

**If you skip it:** an autonomous loop retries until something else stops it.

## Customization 5: Report format

**Where it is used:** SPEC.md, step 4.

Two shapes, pass and fail, are deliberate: a third invites "mostly". Adapt the
wording, the prefix, and whether reports go to a file, a PR comment or a chat
channel. Keep the property that a passing report is unreadable without its
numbers.

```
PASS  <what ran>, <counts>, <exit codes>
FAIL  <what is not done>, <the failing counts>, <what was not run and why>
```

**If you skip it:** the default shapes are fine; they are simply not in your
house voice.

## Customization 6: Delegated work

**Where it is used:** SPEC.md, *A delegated report is a claim, not evidence*.

Name what your team delegates to, and how each one's work gets checked
independently: coding agents, job runners, contractors, another team's service.
For each, the question is the same: what can you read that the reporter did not
write?

```
Agent runs:       git diff --stat, and the tests it claims to have added
Contractor PRs:   the diff, plus the suite run locally rather than their screenshot
Upstream service: a request against it, not their status page
```

**If you skip it:** a report from something that wants to look finished is
treated as evidence.

## Customization 7: Where the gate is enforced

**Where it is used:** the whole skill.

This is a specification an agent follows. If you want it to hold when nobody is
following it, wire the mechanical half into something that cannot be skipped:

- A pre-commit or pre-push hook that runs the command set
- A required CI job, so the claim cannot be merged without the evidence
- A pull-request template whose checklist names the commands

A rule in a document shapes behaviour. A required check enforces it. Use the
document for judgment and the check for the mechanical part.

**If you skip it:** the gate holds exactly as long as everyone is paying
attention.

## Customization 8: Escalation

**Where it is used:** SPEC.md, *The retry cap*.

When the cap is hit, who hears about it, and in what form? Name a person or a
channel rather than "the team", and say what a good escalation contains: the
failing command, its output, the three attempts, and the blocking question.

**If you skip it:** failures stop at the cap and stay there.

## Final checklist

- [ ] The command set matches what CI runs
- [ ] The proof table names the claims your team makes, with the substitutions
- [ ] A full run is defined for a large repo, with a time budget
- [ ] The retry cap and what happens at it are written down
- [ ] Report format matches where reports are read
- [ ] Each kind of delegated work has an independent check
- [ ] The mechanical half is wired into a hook or a required job
- [ ] Escalation names a person or a channel

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The trigger and the one-paragraph rule |
| `SPEC.md` | The gate, the proof table, the two report shapes, the limitations |
| `CUSTOMIZE.md` | This file: the decisions that bind it to your project |
