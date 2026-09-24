# Spec Planning: Customization Guide

## Before you start

This skill writes the two documents [implement-spec](../implement-spec/SKILL.md)
reads, so the location and ID scheme are not yours to set here alone: they are
bound once in [create-spec's CUSTOMIZE.md](../create-spec/CUSTOMIZE.md),
Customizations 1 and 2, and must match implement-spec's own CUSTOMIZE.md
sections 1 and 2. What this file binds is what only a planner needs: the
standards a plan must respect, and how fine to cut a task.

## Customization 1: Where specs are found

**Where it is used:** SPEC.md, *Where it reads and writes*, and step 1.

Take the spec root and folder name from create-spec's Customization 1. Add only
what differs for planning:

```
Recovered whole-system spec:  <e.g. SPEC.md at repo root, or docs/SPEC.md>
Planned in place:             <yes, plan files beside it / no, always via a create-spec change spec>
```

**If you skip it:** specs by ID under `specs/{NNN}-{slug}/`, a root `SPEC.md`
by path with its plan files beside it, and every other recovered spec through a
create-spec change spec.

## Customization 2: Standards files your plan must respect

**Where it is used:** SPEC.md, step 2 (*Standards*) and step 3.

List the documents your repositories keep that a plan has to follow, and the
requirement prefix each one governs. The planner reads the bound file whenever
the spec carries that prefix, and cites it in the matching plan section.

| Prefix | Standards file | Plan section it governs |
|---|---|---|
| `SEC-` | <e.g. docs/standards/security.md> | Security Considerations |
| `PRIV-` | <e.g. your data-handling policy> | Security Considerations |
| `INFRA-` | <e.g. infrastructure/README.md> | Infrastructure Changes |
| `OBS-` | <e.g. docs/standards/observability.md> | Observability |
| `DATA-` | <e.g. docs/standards/database.md> | Data Model Changes, Migration Strategy |
| `EVAL-REQ-` | <e.g. docs/standards/ai-evaluations.md> | Evaluation Strategy |
| (any) | <e.g. your architecture decision records> | Existing Patterns |

A standards file the planner can't find is reported, not guessed at. A plan
that cites a standard nobody wrote is worse than one that says there isn't one.

**If you skip it:** the planner looks for obvious candidates (a `SECURITY.md`,
a `docs/` folder, agent rule files) and cites what it finds, and says so where
it finds nothing.

## Customization 3: Task granularity

**Where it is used:** SPEC.md, step 4.

```
A task is:         <e.g. one failing test's worth of work / at most half a day>
Tests and code:    <same task / a test task then an implementation task>
Infrastructure:    <its own task per stack / folded into the feature task>
Documentation:     <its own task / part of each task>
```

**If you skip it:** one task per behaviour a single failing test can drive,
with the test and the code in the same task, because that is how
[test-first](../test-first/SKILL.md) works.

## Customization 4: The Ready gate

**Where it is used:** SPEC.md, step 1.

The gate is the method; what counts as evidence of readiness is yours:

```
Ready is set by:          <the status field / a label / an approval on the PR that adds the spec>
Recovered specs need:     <e.g. owner sign-off recorded in the question list>
Also required before planning: <e.g. a tech-doc-review score, a security reviewer's sign-off,
                                a panel review of the spec itself such as the agentic plugin's design-review>
```

**Don't soften the gate itself.** Teams that let the planner "plan what it can"
against a draft get plans that encode the draft's gaps as tasks.

**If you skip it:** the status field, and for a recovered spec, no undecided or
contradiction grade left on a requirement being planned.

## Customization 5: The verification command

**Where it is used:** SPEC.md, step 4.

```
Test command form:     <e.g. uv run pytest {file} -k {name} / npm test -- {pattern} / go test ./pkg/... -run {name}>
Other checks per task: <e.g. the type checker on touched files>
Commands never to use: <e.g. anything that deploys, anything that needs production credentials>
```

**If you skip it:** the runner found in step 2, narrowed to the task where it
allows, and nothing that reaches outside the repository.

## Final checklist

- [ ] Spec root and IDs match create-spec's and implement-spec's CUSTOMIZE.md
- [ ] Where recovered specs live, and where their plan files go, is bound
- [ ] Every requirement prefix you use has a standards file, or a written "none"
- [ ] Task granularity is agreed
- [ ] What counts as ready is written down, and the gate is not softened
- [ ] The verification command form, and what it must never do, are set

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The trigger, the argument and the five steps |
| `SPEC.md` | The gate, the inspection, the task shape, the rules, limitations |
| `CUSTOMIZE.md` | This file: location, standards, granularity, the gate, commands |
| [create-spec/templates/](../create-spec/templates/) | The `PLAN.md` and `TASKS.md` shapes, one copy for the loop |
