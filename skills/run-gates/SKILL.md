---
name: run-gates
description: Check a repository's gates before a merge, a deploy or a phase change by running the conditions in its .gates.yaml (files that must exist, patterns files must contain, commands that must exit clean, and other gates) and reporting pass or blocked with the fix for each failure.
license: MIT
compatibility: Any repository. The evaluator is standard-library Python 3.9+ and uses PyYAML when it is installed. Gate names and conditions are yours to set via CUSTOMIZE.md.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
  argument-hint: "<gate_name> [--project <path>] | --list"
type: skill
scope: all
status: active
---

# run-gates

A gate is a list of conditions a repository has to meet before something
irreversible happens. This skill runs them and reports the result. It never
decides a gate passed by reading files itself.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the four core gates, how they compose, and why they block rather than advise
2. Copy [examples/.gates.yaml](./examples/.gates.yaml) to your repo root and [follow CUSTOMIZE.md](./CUSTOMIZE.md) to bind each condition to your stack
3. Run `--list`, then run one gate, then wire it into CI

## Procedure

1. **Resolve the project.** A path you're given, or the current directory. If
   it's ambiguous, ask which repository.
2. **No gate named?** List them and ask which one:
   `python3 scripts/check_gates.py --list --project <path>`
3. **Run the gate:**
   `python3 scripts/check_gates.py <gate> --project <path>`
   Add `--json` when another tool will read the result.
4. **Report by exit code.** `0` passed. `1` blocked: show each failed
   condition with its fix line. `2` the gate couldn't be evaluated (no gates
   file, unknown gate, bad YAML): say so, and offer to help write one.
5. **Remediate.** For each failure, say what's missing, whether you can fix it
   now (create a file, add a config line) or it needs a person, then re-run
   the gate. The re-run is the evidence, not your edit.

## Rules

- Always run the script. Never evaluate a gate by reading files and judging.
- Never edit `.gates.yaml` to make a failing gate pass. Weakening a condition
  is a decision for whoever owns the gate, made in review.
- A `command` condition runs with your shell and credentials. Read an
  unfamiliar repository's `.gates.yaml` before running it.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
