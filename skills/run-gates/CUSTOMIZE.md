# Run Gates: Customization Guide

## Before you start

The sample [examples/.gates.yaml](./examples/.gates.yaml) is a shape, not a
policy. Its `make lint` and `make test` are placeholders, and a gate that runs a
command your repo doesn't have fails on day one and gets switched off on day
two. Work through the sections below once, per repository, and the gates you
end up with will be ones people actually leave on.

## Customization 1: Bind the core gates to your stack

**Where it is used:** SPEC.md, *The four core gates*.

Keep the four names and replace what they check. Write down the one command for
each, the same one CI runs:

```
Lint:        <command>
Test:        <command>
Type check:  <command, if typed>
Audit:       <command that exits non-zero on high or critical advisories>
Smoke:       <command that exercises the deployed environment>
```

Typical `build_ready` lines:

| Stack | Lint | Test |
|---|---|---|
| Python (uv) | `uv run ruff check .` | `uv run pytest` |
| Node | `npm run lint` | `npm test` |
| Rust | `cargo clippy -- -D warnings` | `cargo test` |
| Go | `go vet ./...` | `go test ./...` |

**If you skip it:** the gate either fails on a command that doesn't exist or
passes because a `||` chain found something that exits 0.

## Customization 2: Decide your floor for `repo_baseline`

**Where it is used:** SPEC.md, *The four core gates*.

Pick what every repository must have before real work starts. Common choices:
a `.gitignore`, pre-commit hooks with secret detection, a CI workflow, no
tracked `.env`, a lockfile committed. Set a lighter floor for throwaway
prototypes and write the exception as a comment in that repo's `.gates.yaml`.

**If you skip it:** "baseline" means whatever each repo happened to set up.

## Customization 3: Make `release_verified` real

**Where it is used:** SPEC.md, *Before and after a deploy are two gates*.

Name how you find the deployed URL (an environment variable your pipeline sets,
an infrastructure output, a stable domain) and what "working" means: a health
endpoint, a page that renders, a smoke or end-to-end suite pointed at the
environment. Never paste a generated hostname into the file.

**If you skip it:** you prove the artifact is sound and never prove the
environment is.

## Customization 4: Add project gates

**Where it is used:** SPEC.md, *Project gates are additive*.

List the events in your delivery that deserve their own gate: a production
deploy for a regulated service, a customer demo, a data migration, a public
launch. For each, name the core gate it composes and the extra conditions.

```yaml
  customer_demo:
    description: "Demo environment is safe to show"
    requires:
      - gate: release_verified
      - command:
          description: "Demo data is synthetic"
          run: "./scripts/check-demo-data.sh"
```

**If you skip it:** the events that most need a checkpoint run on memory.

## Customization 5: Rename the core four, once, if you must

**Where it is used:** SPEC.md, *The names are fixed; what they check is not*.

If your organization already has words for these checkpoints, rename all four
in every repository at the same time and record the mapping here. The rule
that matters is consistency across repos, not these particular words.

```
repo_baseline    -> <your name>
build_ready      -> <your name>
deploy_ready     -> <your name>
release_verified -> <your name>
```

**If you skip it:** nothing breaks. The defaults are fine.

## Customization 6: Where the gates are enforced

**Where it is used:** SPEC.md, *Why a gate blocks rather than advises*.

Decide which event runs which gate, and wire it in:

| Event | Gate | Enforced by |
|---|---|---|
| Pull request | `build_ready` | A required CI job running `check_gates.py build_ready` |
| Deploy job start | `deploy_ready` | The first step of the deploy workflow |
| Deploy job end | `release_verified` | The last step, failing the job if the environment is broken |

Make the CI job **required** in branch protection. A job that runs and can't
block a merge is a report.

**If you skip it:** the gates hold only when someone remembers to run them.

## Customization 7: Timeouts and slow conditions

**Where it is used:** SPEC.md, *Rules for conditions*.

The default per-command timeout is 300 seconds (`--timeout` changes it for a
run; `timeout:` on a condition changes it for one command). Set a budget for
each gate, and move anything slower than that budget into CI rather than a
local hook.

**If you skip it:** a hung command blocks a hook for five minutes and people
learn to bypass it.

## Customization 8: Who owns a gate

**Where it is used:** SKILL.md, *Rules*.

Name who approves a change to each repository's `.gates.yaml`. Weakening a
condition to get a release out is sometimes right, and it should be a reviewed
decision with a comment, never an edit made to get past a red run. A
`CODEOWNERS` line on `.gates.yaml` does this mechanically.

**If you skip it:** the fastest way past a failing gate is to edit it.

## Final checklist

- [ ] The four core gates run your real commands, the same ones CI runs
- [ ] `repo_baseline` states your floor, with exceptions commented
- [ ] `release_verified` reads a stable endpoint and checks real behaviour
- [ ] Project gates compose a core gate and are named for their event
- [ ] Gate names are the same in every repository
- [ ] Each gate is wired into a required job or a hook
- [ ] Timeouts fit the place each gate runs
- [ ] Someone owns changes to `.gates.yaml`

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The trigger and the procedure |
| `SPEC.md` | The core gates, composition, condition types, output, limitations |
| `CUSTOMIZE.md` | This file: the decisions that bind it to your repositories |
| `scripts/check_gates.py` | The evaluator |
| `examples/.gates.yaml` | A starting file to copy |
