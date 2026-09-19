# Completion Verification Specification

## System Overview

A completion claim is a statement about the world: the tests pass, the bug is
fixed, the build is green, the milestone is done. This skill makes one demand of
every such statement, and it is narrow enough to be checkable:

> The command that proves the claim must have been run, in full, since the last
> change, and its output must have been read.

Not "should pass". Not "looks right". Not "the agent said it finished". The
output, freshly produced, or no claim.

It is a **checker**. It reports status and fixes nothing. Whatever does the work
is a separate thing, which matters most when the two get run in a loop: see
*The retry cap* below.

## When it runs

Before any of these:

- Committing, pushing, or opening a pull request
- Saying a bug is fixed
- Saying tests, lint, types, or the build pass
- Advancing a phase, a gate, or a milestone
- Accepting a delegated agent's report
- Handing anything to someone outside the team
- Any sentence that implies the work is finished

And before any expression of satisfaction. "Great, that's working" is a
completion claim wearing a friendlier hat.

## The gate

```
1. NAME     which exact command proves this claim?
2. RUN      execute it in full, fresh, from a clean state
3. READ     the whole output: exit code, counts, new warnings
4. COMPARE  does the output actually support the claim?
5. STATE    the claim with its evidence, or the real status with its evidence
```

Skipping step 2 or step 3 is not a shortcut. It is asserting something you do
not know.

## What each claim requires

| Claim | Proof | Not proof |
|---|---|---|
| Tests pass | Full runner output, 0 failures, exit 0 | A run from before the last edit; one file when the change was broad |
| Lint clean | Linter output, 0 errors | The formatter passing; a partial path |
| Types check | `tsc --noEmit`, `mypy`, `go vet` exit 0 | Lint passing: different tool, different question |
| Build succeeds | The build command, exit 0 | Types checking; "no errors scrolled past" |
| Bug fixed | The original symptom, reproduced, now passing | The code changed and looks correct |
| Regression test works | Revert the fix, test **fails**, restore, test passes | The test is green once |
| Coverage adequate | A coverage report naming the uncovered paths | The test count going up |
| Migration applied | The schema read back from the target database | The migration command exiting 0 |
| Deployed | The deployed endpoint answering correctly | A successful infrastructure apply |
| Delegated task finished | `git diff` and `git status` showing the actual change | The agent's own success report |
| Requirements met | A line-by-line walk of the plan or the ticket | Tests passing |

The pattern in that last column is the whole framework: **each proof is one
layer more concrete than the thing people substitute for it.** Lint is not
types, types are not a build, a build is not a deploy, and a deploy is not a
working endpoint.

## A delegated report is a claim, not evidence

An agent, a job runner or a teammate reporting completion is an assertion made
by something with the same incentive to round up that you have. Check the world
instead:

```bash
git status --short
git diff --stat
```

No diff means no work, whatever the report said. A process exiting 0 says the
process exited; it says nothing about whether the change is correct.

## Procedure

### Step 1: Infer the command set from the repo

Read what the project actually uses rather than guessing:

```bash
cat package.json          # scripts: test, lint, typecheck, build
cat pyproject.toml        # tool config, test dependencies
cat Makefile justfile 2>/dev/null
ls .github/workflows/     # what CI runs is what "done" means here
```

**CI is the authority.** If a pipeline runs four jobs on a pull request, those
four are the checklist, whatever the local habit is.

### Step 2: Run everything the claim touches

Full commands, not scoped ones. A scoped run proves something about one file and
nothing about the change.

```bash
npm test            # or: pytest, cargo test, go test ./..., mvn verify
npm run lint
npx tsc --noEmit
npm run build
```

### Step 3: Read the output, including the boring parts

Three things beyond pass or fail:

- **The exit code.** A runner can print reassuring text and exit non-zero.
- **The counts.** "34 passed" means nothing without how many exist. 34 of 51 is
  a failure wearing a green tick.
- **New warnings.** A warning that appeared with this change is part of this
  change.

### Step 4: Report in one of two shapes

```
PASS  Tests 51/51, exit 0. Lint clean. Types clean. Build exit 0.
```

```
FAIL  Not done. 48/51 pass; 3 failures in auth.test.ts, expired-token path.
      Lint clean. Build not run, blocked on the test failures.
```

There is no third shape. "Mostly done" is not a status.

## The retry cap

When this runs inside a loop that fixes and rechecks, the loop is bounded:

- **Three fix-and-recheck attempts.** No more.
- If the same check fails a third time, **stop.** Report the failure, the three
  things tried, and what is actually blocking.
- Never widen scope to reach green. Never delete or skip a failing test to reach
  green. Both turn a visible failure into a hidden one.

An unbounded retry loop spends money on a fix that was never going to land. The
cap is the abandon path, and it is the reason a checker must not also be a
fixer: something that can edit the code can always make the check agree with it.

## Language that signals the gate was skipped

Catch these in your own draft before sending it:

- "should work now", "should be fine", "probably passes"
- "looks correct", "seems to be working"
- "I've fixed it", with no output attached
- "the agent completed it"
- "all set", "done", "perfect", leading a message with no evidence in it

Also the tired version: *it is late, this obviously works, one check does not
matter.* Exhaustion is when unverified claims get made, which is when the rule
earns its keep.

## Limitations

What this structurally cannot see:

- **Whether the tests test the right thing.** A green suite that asserts nothing
  passes this gate. Coverage analysis and review are different jobs.
- **Whether the claim was worth making.** It checks the evidence for the stated
  claim, not whether the stated claim is the one that mattered.
- **Flakes.** One green run is evidence about one run. A suite that fails one
  time in ten will pass this gate nine times.
- **Anything outside the command.** A passing integration suite against a
  seeded database says nothing about production data.
- **Its own command set.** If the repo's CI runs a job your command list omits,
  this reports clean while that job fails. Bind the list to CI, and re-bind it
  when CI changes.

It also cannot make anyone read the output. The gate is only as good as step 3,
and step 3 is where tired people stop.
