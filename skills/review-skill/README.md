# Outside Skill Review

**Don't install someone else's skill. Review it, and adopt only what fills a gap
in yours.**

## Running it

This is a specification an agent executes, plus one optional script. Install it
by copying this folder into your project's skills directory:

```bash
cp -r review-skill /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/review-skill https://github.com/<owner>/<repo>/tree/main/<skill>

or: "review this skill before we install it", "can we use this plugin?"
```

The agent reads [SPEC.md](./SPEC.md) and does the work. The mechanical sweep is
a standard-library Python script you can run on its own:

```bash
python3 scripts/scan-skill.py incoming/<skill-name>
```

**Working by hand:** follow [SPEC.md](./SPEC.md) step by step.
[CUSTOMIZE.md](./CUSTOMIZE.md) binds the quarantine folder, your rules file and
your agent tool's skill paths.

## What it does

Copies the outside skill into a quarantine folder your agent never loads from.
Records the source, the commit and the licence. Reads every file, scripts
included, and flags anything that reaches for credentials, downloads and runs
code, writes outside your repo, hides text, or tells the agent to skip your
rules. Then compares each thing the skill does with what your harness already
does, and sorts it: **covered**, **gap** or **conflict**.

Only the gaps get drafted, in your conventions, with provenance at the top.
Nothing gets applied without a human.

## Why it exists

A skill is instructions your agent follows with your permissions, and the
public registries have no review. In February 2026, Snyk's
[ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
study scanned 3,984 public skills and found 13.4% with at least one critical
issue, including confirmed malware and prompt injection.

## Who uses it

- **Anyone running coding agents** who's been handed a link to "a great skill"
- **Teams maintaining a shared harness**, who need every outside idea to arrive
  with a source and a licence
- **Security-minded leads** who want a written reason every time a flag is
  cleared
- **Solo builders**, where nobody else will read the skill before the agent does

## Pairs with

`secret-scan` for anything the review turns up that looks like a real
credential, and `verify-done` before claiming a drafted change works.

## What it will not do

It won't catch a skill written to evade its patterns, review what a URL serves
after the review, or review the dependency tree of anything the skill installs.
A clean scan is not a safe skill. The Limitations section in
[SPEC.md](./SPEC.md) is the full list.

## The idea in one table

| Class | Means | What happens |
|---|---|---|
| Covered | You already do this | Nothing. Name the file that covers it |
| Gap | Nothing you have does this | Draft the smallest change, with provenance |
| Conflict | It contradicts your rules | Never adopted |

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
