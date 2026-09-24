# Spec Review: Customization Guide

## Before you start

The method doesn't change: walk every requirement, delegate the lenses, map
severities to one scale, write findings where the implementer will see them,
recommend and stop. What changes is who the reviewers are. Most teams already
have some: a security lead, an architect, a bot on pull requests. Bind them
here and this skill runs them instead of the shipped defaults.

Location and IDs come from [create-spec's CUSTOMIZE.md](../create-spec/CUSTOMIZE.md),
Customizations 1 and 2, shared by the whole loop.

## Customization 1: The lenses

**Where it is used:** SPEC.md, step 3.

| Lens | Shipped reviewer | Yours |
|---|---|---|
| Correctness | The harness's code review (Claude Code: `/code-review`), else [review-principles](../review-principles/SKILL.md) and a read of the diff | |
| Security | The harness's security review (Claude Code: `/security-review`), plus [secret-scan](../secret-scan/SKILL.md) | |
| Structure | [review-principles](../review-principles/SKILL.md) | |
| Dead code | [find-dead-code](../find-dead-code/SKILL.md) | |
| Test coverage | [coverage-gaps](../coverage-gaps/SKILL.md) | |
| Fresh verification | [verify-done](../verify-done/SKILL.md) | |

**If you skip it:** the shipped reviewers. Where one isn't installed, the lens
is reported as skipped for that reason, never silently dropped.

## Customization 2: Your own panel

**Where it is used:** SPEC.md, step 3, the *Your panel* row.

If your team runs separate reviewers per concern (named agents, a security
team's checklist, an architecture review), bind each one:

```
Name:          <e.g. security-reviewer>
Lens:          <security / architecture / quality / performance / accessibility>
How to invoke: <an agent name, a skill, a command, a person to request>
Runs when:     <always / when SEC- IDs exist / when the diff touches X>
Its scale:     <how it rates findings, e.g. risk 1-10, or blocker / major / minor>
```

Then map its scale onto this skill's, in Customization 3. A panel whose ratings
aren't mapped gets its findings written at the reviewer's own word, and two
scales in one table can't be sorted.

Keep each panel reviewer read-only, and give it only the spec ID and the diff,
not the implementation conversation.

**If you skip it:** no panel row; the shipped lenses only.

## Customization 3: The severity map

**Where it is used:** SPEC.md, step 5.

The five levels are fixed. Where each reviewer's output lands is yours:

```
<reviewer> <its rating>  ->  CRITICAL / HIGH / MEDIUM / LOW / INFO
e.g. security-reviewer risk 8-10       -> CRITICAL
     security-reviewer risk 4-7        -> HIGH
     architecture-reviewer "major"     -> HIGH
```

Decide also what blocks completion. The shipped rule is any open `CRITICAL` or
`HIGH`. A team in a regulated domain might add any open security finding at any
level.

**If you skip it:** the shipped map in SPEC.md, and `CRITICAL` or `HIGH`
blocks.

## Customization 4: Independence

**Where it is used:** SPEC.md, *Independence*.

```
Runs as:        <a fresh session / a subagent / a CI job / a second person>
Is given:       <the spec ID only / the ID and the PR link>
Is not given:   <the implementation conversation, the implementer's summary>
```

**If you skip it:** a subagent or new session given the spec ID only, and a
same-session run says so in the report.

## Customization 5: The diff boundary

**Where it is used:** SPEC.md, step 1.

```
Diff from:     <the commit before the first task / the spec's branch point / the PR base>
Includes:      <the files PLAN.md named / everything on the branch>
```

**If you skip it:** from the commit before the spec's first implementation
commit, over every file changed since.

## Customization 6: Where findings go

**Where it is used:** SPEC.md, step 5, and *After the review*.

```
Findings table:   <TASKS.md Review Findings / PR review comments / an issue per finding>
Who rules on a disputed finding: <a person or role>
Who marks the spec complete:      <a person or role>
```

If findings leave `TASKS.md`, keep a row there pointing at each one anyway:
[implement-spec](../implement-spec/SKILL.md) reads the task list, not your
tracker.

**If you skip it:** `TASKS.md`'s Review Findings table, and the spec's owner
rules and completes.

## Final checklist

- [ ] Each lens has a reviewer, or is knowingly skipped
- [ ] Your panel, if you have one, is bound, read-only and mapped
- [ ] The severity map is written, and what blocks completion is decided
- [ ] How independence is achieved is written down
- [ ] The diff boundary is set
- [ ] Findings have a home that implement-spec reads, and a person rules on disputes

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The trigger, the argument and the five steps |
| `SPEC.md` | The walk, the lenses, the severity map, the rules, limitations |
| `CUSTOMIZE.md` | This file: reviewers, panel, severities, independence, diff, findings |
| [create-spec/templates/TASKS.md](../create-spec/templates/TASKS.md) | The Review Findings table this writes into |
