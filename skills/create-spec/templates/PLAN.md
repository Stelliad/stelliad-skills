---
spec: SPEC-[NNN]
status: draft
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
---

# Implementation Plan: SPEC-[NNN]

## Specification

Link: `./SPEC.md`. Its status when this plan was written: `ready` as of
[YYYY-MM-DD], at commit [short SHA]. If the spec changes after this plan is
written, this line is how a later reader knows the plan may be stale.

## Repository Analysis

What was actually inspected before writing this plan: files read, commands
run, existing patterns found. This is evidence, not a summary. If it names a
pattern this plan reuses, that pattern must have been found in the repository,
not assumed to exist because it is common elsewhere.

| Inspected | What it showed |
|---|---|
| [path or command] | [finding] |

## Existing Patterns

Architectural, naming and tooling patterns already in this repository that
this plan reuses, cited by file path. If no equivalent pattern exists and a new
one is needed, say so and justify it here rather than introducing one
silently. A new dependency is justified here too, including why nothing already
in the repository covers the need.

## Architecture Impact

What structurally changes, and everything it touches: modules, data flow, the
deploy path if one exists for this target.

## Files Expected to Change

| File | Change |
|---|---|

## New Files Expected

| File | Purpose |
|---|---|

## Data Model Changes

Carry forward every `DATA-` ID from the spec and state how each is addressed:
the table or entity it touches, the constraint or scoping it adds. An ID with
no line here is an ID this plan has not accounted for. Write "None identified"
if the spec has no `DATA-` requirements.

## API and Interface Changes

None, or describe.

## Infrastructure Changes

Carry forward every `INFRA-` ID from the spec and state how each is addressed:
which stack or module it touches, and whether it is a new resource, a changed
one, or a new stack. Infrastructure changes go into code and deploy through the
pipeline, never as a manual change to make something take effect. Write "None
identified" if the spec has no `INFRA-` requirements.

## Security Considerations

Carry forward every `SEC-` and `PRIV-` ID from the spec and state how each is
addressed by this plan. An ID with no line here is an ID this plan has not
accounted for.

## Observability

Carry forward every `OBS-` ID from the spec and state how each is addressed:
which log fields, metric, trace, or alert condition it maps to. Write "None
identified" if the spec has no `OBS-` requirements.

## Evaluation Strategy

Carry forward every `EVAL-REQ-` ID from the spec and state how each is
addressed. Write "None identified" if the spec has no `EVAL-REQ-` requirements
or no AI behaviour, and delete the prompts below.

- **Dataset:** which golden, regression, edge-case, adversarial or holdout
  cases this feature needs, and where they live.
- **Dimensions:** which apply (correctness, groundedness, task completion,
  safety, schema validity), not every dimension by default.
- **Graders:** which checks are deterministic, and which need a model judge or
  a human.
- **Baseline:** the model, prompt, retriever and tool configuration this change
  compares against.
- **Release gates:** which regressions block outright, which need review, and
  which dimensions are hard gates regardless of the average.
- **Cost:** expected tokens and cost per task, and the threshold that triggers
  review.

## Implementation Phases

Every phase names the spec IDs it covers, so a reader can tell what a phase is
for without re-reading the spec.

### Phase 1: [name]

Covers: REQ-xxx, SEC-xxx

Expected changes: ...

Verification: `[the actual command, on a runner confirmed in this repository]`

### Phase 2: [name]

## Testing Strategy

What test types apply here (unit, integration, end-to-end) and the actual
runner this repository uses for each, confirmed by reading the manifest nearest
the target (`package.json`, `pyproject.toml`, `go.mod`, a `Makefile`). If no
runner is configured for the target, say so plainly.

## Migration Strategy

None, or describe: the migration, backward compatibility, backfill, deployment
sequence, and rollback or forward-fix approach for any schema-changing `DATA-`
requirement. Don't hide migration behaviour inside a phase note.

## Rollback Strategy

None, or describe.

## Risks

## Open Implementation Questions

Anything the spec asks for that the repository makes hard, ambiguous or
infeasible, stated rather than planned around. A question here that changes a
requirement goes back to the spec's owner; the plan does not answer it.
