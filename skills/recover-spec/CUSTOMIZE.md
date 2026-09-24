# Spec Recovery: Customization Guide

## Before you start

The method doesn't change: pin, bound, inventory, trace, grade, ask. What
changes is where the output lands, how grades are written, and who answers the
questions. Bind those once and the run produces documents your team can file
without reformatting.

## Customization 1: The output routes

**Where it is used:** SPEC.md, *Where the output goes*.

```
Spec route:        <e.g. SPEC.md at repo root, or docs/SPEC.md>
Subsystem specs:   <e.g. docs/specs/{name}.md>
Reading route:     <e.g. docs/readings/system-spec-{YYYYMMDD}.md, or a
                    folder outside the repo for systems you don't hold>
Subsystem reading: <e.g. docs/readings/{name}-spec-{YYYYMMDD}.md, beside the
                    reading, never in the subsystem spec folder>
Question list:     <e.g. beside the spec as QUESTIONS.md, or an issue per question>
```

Keep the split between a spec (defines what gets built, lives in the repo it
governs) and a reading (records what you found, lives wherever your team keeps
analysis). If your team does diligence on systems it never gets write access
to, the reading route has to be outside the target repo.

**If you skip it:** a run with no mode flag writes a reading. Specs go to
`SPEC.md` at the root with subsystems in `docs/specs/`, and readings, subsystem
readings included, go to `docs/readings/`. Both assume you can write to the
repo.

## Customization 2: Grade markers

**Where it is used:** SPEC.md, *The grade*, and the skeleton.

The five grades are the method. The spelling is yours:

```
Observed:       <[observed] / ✓ / O>
Inferred:       <[inferred] / ~ / I>
Intended:       <[intended: source] / quote the source inline>
Undecided:      <[undecided] / ? / a link to the question entry>
Contradiction:  <[contradiction] / ! / a link to both sides>
```

**Don't merge grades.** Collapsing intended into inferred, or undecided into
inferred, loses exactly the distinction the skill exists to keep.

**If you skip it:** grades are written inline in square brackets.

## Customization 3: Requirement IDs

**Where it is used:** the skeleton, section 7.

If your specs number requirements (`REQ-001`, `FR-12`), bind the scheme here so
a recovered spec slots into the same traceability as a written one, and so
[plan-spec](../plan-spec/SKILL.md) and [implement-spec](../implement-spec/SKILL.md)
can cite the IDs later. Use the scheme bound in
[create-spec's CUSTOMIZE.md](../create-spec/CUSTOMIZE.md), Customization 2.

```
Requirement IDs:  <e.g. REQ-001>
Question IDs:     <e.g. Q1, or the issue number once filed>
```

**If you skip it:** requirements are numbered in a table and questions as `Q{n}`.

## Customization 4: Who answers the questions

**Where it is used:** SPEC.md, *Undecided is the deliverable*, and the question
list's `Ask` field.

A question with no named person waits forever. Bind the roles:

```
Product behaviour:      <a person or role, e.g. the product owner>
Infrastructure:         <e.g. the platform lead>
Data and retention:     <e.g. the data owner, or whoever signs off privacy>
When nobody is left:    <who rules on an undecided whose author has gone>
```

**If you skip it:** each question names the most recent committer on the file,
which is a guess about who remembers, not about who decides.

## Customization 5: Sensitive data on the spine

**Where it is used:** SPEC.md, step 4.

If your systems handle regulated data, name the categories you tag at each hop
so the trace serves your privacy or compliance review directly:

```
Categories:   <e.g. personal data, payment data, health data, credentials>
Tag format:   <e.g. a column in the hop table>
Review that consumes it: <the skill, checklist or team>
```

**If you skip it:** the hop table records what's passed and stored, without a
category column.

## Customization 6: Which skills the steps hand off to

**Where it is used:** SPEC.md, steps 6, 7 and 8, and rule 7.

| Step | Shipped hand-off | Yours |
|---|---|---|
| Untested behaviour | [coverage-gaps](../coverage-gaps/SKILL.md) | |
| Unreachable code | [find-dead-code](../find-dead-code/SKILL.md) | |
| Found a secret | [secret-scan](../secret-scan/SKILL.md) | |
| Quality bar on the output | [tech-doc-review](../tech-doc-review/SKILL.md) | |

**If you skip it:** the shipped skills are named, and if they aren't installed
the finding is reported for a person to route.

## Customization 7: The quality bar

**Where it is used:** SPEC.md, step 8.

Decide what a recovered spec has to clear before anyone relies on it: a review
score, a second reader, a walkthrough with the owner. Also decide the grade mix
you'll accept. A team might say no section of a spec that governs production may
be more than half inferred.

**If you skip it:** the document goes to `tech-doc-review` and is reported with
its grade split, and the decision to rely on it is yours.

## Final checklist

- [ ] Spec, subsystem, reading and question routes are bound
- [ ] Grade markers are chosen, and all five grades are kept distinct
- [ ] Requirement and question IDs match the rest of your specs
- [ ] Every kind of question has a named person or role to answer it
- [ ] Sensitive data categories are named, if your systems carry any
- [ ] Hand-offs for coverage, dead code, secrets and quality are bound
- [ ] The bar a recovered spec must clear is written down

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The trigger, the arguments and the five grades |
| `SPEC.md` | The procedure, the rules, the output, the limitations |
| `CUSTOMIZE.md` | This file: routes, markers, IDs, owners, hand-offs |
| `references/spec-skeleton.md` | The section structure and the question entry format |
