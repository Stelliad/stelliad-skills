# Run Gates

**A gate blocks. A report advises. This skill runs the conditions in your
`.gates.yaml` and exits non-zero when any of them fail.**

## Running it

Copy this folder into your project's skills directory:

```bash
cp -r run-gates /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/run-gates deploy_ready

or: "can we deploy?", "check the gates", "is this ready for production?"
```

The agent runs the evaluator and reports what's blocking. You can run it
yourself too. It needs Python 3.9+ and nothing else:

```bash
cp run-gates/examples/.gates.yaml .      # then edit it
python3 run-gates/scripts/check_gates.py --list
python3 run-gates/scripts/check_gates.py build_ready
python3 run-gates/scripts/check_gates.py deploy_ready --json
```

Exit `0` passed, `1` blocked, `2` couldn't evaluate.

## What it does

You define gates in `.gates.yaml` at the repo root. Each gate is a list of
conditions: a file exists, a file matches a pattern, a command exits with the
expected code, or another gate passes. The evaluator runs them and prints a
tree:

```
Gate:    deploy_ready

|-- PASS gate: build_ready
|   |-- PASS gate: repo_baseline
|   |   |-- PASS File exists: .gitignore
|   |   `-- PASS Secret detection configured in pre-commit
|   |-- PASS Linter passes
|   `-- PASS Tests pass
|-- PASS No high or critical dependency advisories
`-- FAIL CI green on the current commit (exit 1, expected 0: ...)

BLOCKED: 1/3 conditions failed
```

## The idea in one table

Four gate names, the same in every repository, each requiring the one before:

| Gate | When it runs |
|---|---|
| `repo_baseline` | Before serious development |
| `build_ready` | Before build work, and before calling a task done |
| `deploy_ready` | Before a deploy |
| `release_verified` | After a deploy: is the environment actually working? |

The names are fixed so two repos can be compared and so anything above them
can say "needs `build_ready`" without knowing how each repo defines it. What
each gate checks is up to the project. Project-specific gates like
`prod_deploy` compose a core gate with `- gate:` and add what's specific.

## Who uses it

- **Teams running coding agents**, who want "done" to mean a command exited 0
  rather than an agent saying so
- **Engineering leads** standardizing readiness across many repositories
- **Anyone deploying from CI** who wants the pipeline to stop on a broken
  environment, not just a broken build

## What it will not do

It can't tell you a condition is the wrong one, and a `command` condition runs
with your shell and credentials, so read an unfamiliar repo's `.gates.yaml`
before running it. The Limitations section in [SPEC.md](./SPEC.md) has the
full list.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
