# Run Gates Specification

## System Overview

A gate is a named list of conditions that must all hold before a specific event:
starting build work, merging, deploying, calling a release done. Each condition
is deterministic: a file exists, a file matches a pattern, a command exits with
the expected code, or another gate passes.

The skill does one thing. It runs the conditions, prints what passed and what
didn't, and exits `0` or `1`. It doesn't grade, weigh or summarize. The exit
code is the result.

## Why a gate blocks rather than advises

A report gets read once, by whoever happens to be looking. An exit code wired
into a CI job, a pre-push hook or a deploy script can't be skimmed past. That's
the whole design, and it's why the skill always runs the script instead of
reading files and forming a view: an agent's judgment that "the tests look
fine" is a report, and a report is exactly what a gate replaces.

It also means a gate is only as strong as the place it's enforced. A
`.gates.yaml` nobody runs is documentation. Wire it into something that stops
the event.

## The four core gates

Every repository uses the same four names, and each one requires the one before
it:

| Gate | Question | When it runs |
|---|---|---|
| `repo_baseline` | Does this repo meet the security and quality floor? | Before serious development starts |
| `build_ready` | Can work happen here: manifest, lint, tests all run? | Before build work, and before calling a task done |
| `deploy_ready` | Is it safe to push to an environment? | Before a deploy |
| `release_verified` | Is the deployed environment actually working? | After a deploy |

### The names are fixed; what they check is not

Two repositories calling the same checkpoint `build_ready` and
`build_to_staging` can't be compared by a person or a tool. The four names are
the vocabulary. What each one *checks* is project-specific: a Rust service and
a static site put very different commands under `build_ready`, and both answer
the same question.

Fixed names are also what makes composition work. A higher-level process (a
release checklist, a portfolio dashboard, a phase review) can say "this needs
`build_ready`" and delegate down to every repo without knowing how each one
defines it. Rename it in one repo and that delegation silently breaks there.

If your organization prefers other words, rename all four once, everywhere.
Never per project.

### Before and after a deploy are two gates

`deploy_ready` runs before a deploy and proves the artifact is sound.
`release_verified` runs after and proves the environment is. A repo with only
the first can pass every check and still ship a broken environment: a pipeline
going green while the app is down is the exact failure `release_verified`
exists to catch. It's the gate most repos skip and most need.

## Project gates are additive

A project can add its own gates for events specific to it: `prod_deploy`,
`customer_demo`, `data_migration`. Three rules:

1. **Compose, don't copy.** A project gate starts with `- gate: <core gate>`
   and adds only what's specific. Duplicating the core checks means two copies
   that drift.
2. **Name it for the event it guards**, in lowercase snake_case, not for a
   phase or a team.
3. **Never use a project gate as a rename** of a core one.

```yaml
  prod_deploy:
    description: "Production deploy for a service handling personal data"
    requires:
      - gate: release_verified      # the whole core stack
      - file_contains:              # then what is specific
          path: "docs/runbook.md"
          pattern: "^## Rollback"
```

## Condition types

Each item under `requires:` carries exactly one condition key.

| Type | Shape | Passes when |
|---|---|---|
| `file_exists` | `file_exists: "path"` | The path is a file, relative to the project root |
| `file_contains` | `path`, `pattern`, optional `description` | The file exists and matches the regex (Python `re`, multiline) |
| `command` | `run`, optional `exit_code` (default `0`), `description`, `timeout` | The command, run through `/bin/sh` from the project root, exits with `exit_code` |
| `gate` | `gate: name` | Every condition of that gate passes |

A nested gate is evaluated in the same run, and its conditions print indented
under it. A cycle (`a` requires `b` requires `a`) fails with the cycle named
instead of recursing forever.

## Rules for conditions

These are the failure modes that actually bite:

1. **Fast and deterministic.** Once a gate runs inside a hook or a required CI
   job, a slow or flaky condition times out the automation or blocks for the
   wrong reason. A condition that fails one run in ten trains everyone to
   re-run until green.
2. **No ephemeral endpoints.** A generated load balancer or CDN hostname
   changes on redeploy, and a gate that curls a dead URL fails for the wrong
   reason. Use a stable domain, or read the endpoint from your infrastructure
   tool's output or an environment variable your pipeline sets.
3. **Run tools the way CI runs them.** Use your lockfile-aware runner
   (`uv run`, `npx`, `bundle exec`, `make`) rather than a bare interpreter, or
   the gate and CI disagree about the same code.
4. **Paths must survive a restructure.** A condition hardcoding `app/` breaks
   the day the repo becomes a monorepo. Prefer a command that discovers the
   path.
5. **A mention is not a control.** A `grep` for a feature flag matches the
   `.gates.yaml` that declares it and the README that documents it. Exclude
   those, or the condition goes green on a repo with no flag at all.
6. **Comment every exception** in `.gates.yaml`, saying why.

## Output

Text by default, a tree with `PASS` or `FAIL` per condition and a fix line on
each failure. `--json` prints one object:

```json
{"gate": "deploy_ready", "project": "api", "description": "...",
 "available": true, "passed": 2, "failed": 1, "total": 3, "pass": false,
 "checks": [{"description": "...", "pass": false, "fix": "...", "children": []}]}
```

When the gate can't be evaluated, `--json` prints
`{"gate": ..., "available": false, "reason": ..., "checks": []}`.

| Exit | Means |
|---|---|
| `0` | Every condition passed |
| `1` | At least one failed: the gate is blocked |
| `2` | Not evaluated: no gates file, unknown gate, unparseable YAML |

Treat `2` as blocked in automation. A gate that can't run hasn't passed.

## Files

```
run-gates/
├── SKILL.md
├── SPEC.md
├── CUSTOMIZE.md
├── README.md
├── scripts/check_gates.py     the evaluator
└── examples/.gates.yaml       four core gates and one project gate
```

## Limitations

- **It checks what you wrote down.** A gate with a weak condition passes weak
  work. The evaluator can't tell you a condition is the wrong one.
- **A command is trusted code.** It runs with your shell, environment and
  credentials. A gates file from an unfamiliar repository deserves the same
  read you'd give its Makefile before you run it.
- **Exit codes are the only signal from a command.** Output is discarded. If a
  tool exits `0` on findings, wrap it so it doesn't.
- **The built-in YAML parser reads a subset**: block mappings and lists, plain
  and quoted scalars, comments, and `|` / `>` block scalars. Flow collections
  (`[a, b]`, `{a: b}`), anchors and tags need PyYAML installed.
- **One run is one run.** A flaky condition that passes today says nothing
  about tomorrow.
- **It can't enforce itself.** Without a hook or a required CI job running it,
  a gate is a checklist people can skip.
