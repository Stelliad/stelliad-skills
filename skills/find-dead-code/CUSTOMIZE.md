# Dead Code Sweep: Customization Guide

## Before you start

The sweep's accuracy rests almost entirely on two things: whether it knows your
entry points, and whether it knows what your framework reaches without an
import. Both are project-specific, and neither can be guessed reliably. Spend
the twenty minutes once.

## Customization 1: Entry points

**Where it is used:** SPEC.md, *Procedure*, step 1.

List every root of the import tree. A missed entry point makes everything below
it look orphaned, which is the failure that makes people stop trusting the
report.

```
Application:   <e.g. src/main.tsx>
Workers/jobs:  <every handler, including ones only infrastructure names>
CLI:           <bin entries>
Library API:   <what the manifest exports>
Migrations:    <often run by a tool, never imported>
Seeds/fixtures:<same>
```

**If you skip it:** the sweep reads the manifest and finds the obvious ones,
which on a service with scheduled jobs is usually incomplete.

## Customization 2: What your framework reaches by string

**Where it is used:** SPEC.md, *Language notes* and the confidence levels.

Name the places code is reached without an import, so those files are never
reported 🟢:

```
Route/view resolution by string:   <e.g. "app.routes" modules>
Plugin or registry directories:    <e.g. src/plugins/*>
Template or component name lookup: <e.g. dynamic import('./pages/' + name)>
Dependency injection by name:      <container registrations>
Reflection or decorators:          <ORM models discovered at import time>
```

**If you skip it:** live code appears in the report at high confidence, and the
first wrong deletion ends the practice.

## Customization 3: Exclusions

**Where it is used:** SPEC.md, step 3.

The defaults exclude config, tests with live subjects, type declarations and
entry points. Add what your repo has that the defaults do not know:

```
Generated code:     <paths>
Vendored code:      <paths>
Public API surface: <exports that must never be called unused>
Docs and examples:  <often import from src to stay honest>
```

**If you skip it:** generated and vendored directories dominate the report.

## Customization 4: Dependency checking

**Where it is used:** SPEC.md, step 5.

Decide how dependencies are judged, because the naive comparison is wrong in
both directions:

- Are development dependencies in scope? A tool used only in CI is not dead.
- Which packages are imported for their side effects and never by name?
- Which are peer dependencies, required by contract rather than by import?

**If you skip it:** build tooling gets reported as dead.

## Customization 5: Confidence thresholds and what to do with each level

**Where it is used:** SPEC.md, *Report*.

Agree what each level means in practice, so the report drives action:

```
🟢  Remove after a reviewer glance
🟡  Needs the person who knows the framework; never removed in bulk
🔴  Fix the sweep's configuration rather than the code
```

**If you skip it:** every row gets the same amount of attention, which is either
too much or too little.

## Customization 6: Scope and cadence

**Where it is used:** the whole skill.

- Which parts of the repo are swept, and which are left alone
- How often: before releases, quarterly, on a schedule
- Whether the report is a file, an issue, or a pull-request comment
- Who owns acting on it

A sweep nobody owns produces a report nobody reads.

**If you skip it:** it runs when someone remembers, which is after the bundle
grew.

## Customization 7: The deletion policy

**Where it is used:** SPEC.md, *System Overview*.

This skill never deletes. Write down what happens after the report, because that
is where the risk actually lives:

- Who approves a removal
- Whether removals go in their own commit, separate from behaviour changes
- How a removal is reverted if something breaks in staging
- Whether anything is archived rather than deleted

**If you skip it:** removals ride along with feature commits and are hard to
revert.

## Final checklist

- [ ] Every entry point is listed, including jobs and migrations
- [ ] Framework string-resolution paths are named and never reported 🟢
- [ ] Exclusions cover generated, vendored and public-API code
- [ ] Dependency rules cover dev, side-effect and peer dependencies
- [ ] Each confidence level has an agreed action
- [ ] Scope, cadence, output location and an owner are set
- [ ] The deletion policy says who approves and how a removal is reverted

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The trigger and what the sweep is |
| `SPEC.md` | Categories, procedure, report format, confidence levels, limitations |
| `CUSTOMIZE.md` | This file: entry points, exclusions, policy |
