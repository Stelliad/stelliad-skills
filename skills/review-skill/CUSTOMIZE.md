# Outside Skill Review: Customization Guide

## Before you start

This skill ships with generic names: `~/skill-quarantine/`, "your rules file", "your
skills directory". The work below binds them to your harness and your agent
tool. Do it once. An unbound review compares outside skills against a harness
it can't find, and every behaviour comes back as a gap.

Each section names what to decide, where it's used, and what happens if you
skip it.

## Customization 1: The quarantine folder

**Where it's used:** SPEC.md, step 1.

Pick one path and make three things true of it:

```
Quarantine:  ~/skill-quarantine/
In a repo:   no. Outside every working tree, so nothing can commit it
Loaded by:   nothing. Outside every directory your agent scans for skills or instructions
```

Outside the working tree matters as much as outside the skills directory.
Agents load `CLAUDE.md`, `AGENTS.md` and their own config folders from where
they sit, so a quarantine inside your repo can hand a skill's instructions to
the agent that's reviewing it.

Check the third line against your tool, not against memory. See Customization 3.

**If you skip it:** someone clones an outside skill into the skills directory
"just to look", and the next session loads it.

## Customization 2: What your harness is made of

**Where it's used:** SPEC.md, step 7. The comparison needs to know where to look.

Write down every place a behaviour can already be covered:

```
Rules file:      AGENTS.md           (or CLAUDE.md, or your steering folder)
Skills:          skills/             (or .claude/skills/, .agents/skills/)
Gates:           gates/, CI workflows
Hooks:           .githooks/, your agent's hook config
Templates:       PR template, issue forms, document templates
```

A behaviour is **covered** only when the review can name a file from this list.
Keep it current: add a skill or a gate and it goes here.

**If you skip it:** the review guesses at what you have, and "covered" turns
into a feeling.

## Customization 3: Your agent tool

**Where it's used:** SPEC.md, steps 1 and 8.

Where skills load from, and what a drafted change looks like, depends on the
tool. The quarantine folder has to sit outside all of these.

| Tool | Loads skills from | Rules file | Notes |
|---|---|---|---|
| Claude Code | `.claude/skills/`, `~/.claude/skills/`, installed plugins | `CLAUDE.md` (can import `AGENTS.md`) | Hooks and permissions live in `.claude/settings.json`. A skill asking you to edit that file is a HIGH flag |
| Codex | `.agents/skills/` in the repo and up the tree, plus a user-level skills folder | `AGENTS.md` | Check your installed version's docs for the exact user-level path |
| Kiro | Its own skills and steering folders under `.kiro/`, workspace and user level | Steering files | Steering can be set to load on every request, which makes a broad outside steering file worse than a broad skill |
| Anything else | Whatever it scans | Whatever it reads first | Find out before your first review, not during it |

Paths move between releases. Confirm against your tool's current docs and
write the confirmed paths into Customization 1.

If you draft a change for more than one tool, draft it once in the shared
place (usually `AGENTS.md` or a plain `skills/` folder) and point each tool at
it, rather than drafting three copies.

**If you skip it:** the quarantine ends up somewhere your tool auto-loads, which
is the one thing quarantine exists to prevent.

## Customization 4: Your conventions for a drafted change

**Where it's used:** SPEC.md, step 8.

Drafts have to look like the rest of your harness, or they don't get adopted.
Write down:

- The skill folder shape you use (one `SKILL.md`, or several files per skill)
- Your frontmatter fields (`name`, `description`, anything else you require)
- How you word a rule: imperative, one line, with or without a reason
- Where provenance goes: top of file, commit message, or both

The provenance block the skill ships with:

```text
Source:  <URL at the reviewed commit>
Commit:  <sha>
Licence: <licence>. Rewritten, not vendored.
```

**If you skip it:** drafts arrive in the outside author's style, and the next
reader can't tell which parts of the harness are yours.

## Customization 5: The red-flag list

**Where it's used:** SPEC.md, step 6, and `scripts/scan-skill.py`.

Add what's specific to your environment. Common additions:

- Your cloud CLI's secret commands, if they're not already covered
- Your internal hostnames, so a skill posting to one gets noticed
- Your deploy commands, so a skill that deploys is flagged rather than trusted
- Tools you've banned outright

The scanner's patterns are a list at the top of the script (`PATTERNS`). Each
entry is a severity, a category and a regular expression. Add yours there, and
run the script against a sample that should trip it before you trust the new
entry.

**Don't delete a pattern because it's noisy on one skill.** Clear the finding
with a reason in the report instead. A pattern you delete stops catching the
next skill too.

**If you skip it:** the generic list catches generic attacks and misses the
ones shaped to your stack.

## Customization 6: Who clears a flag

**Where it's used:** SPEC.md, *What a flag does*.

A HIGH flag stops the review until a human clears it. Name who that is:

```
Clears HIGH flags:     <a named person or role, not "the team">
Approves adoption:     <same person, or the owner of the harness>
Where clearances go:   the review report, next to the flag, with the reason
```

For a solo builder this is you, and the point of writing it down is the reason
field: a flag cleared with no reason wasn't reviewed.

**If you skip it:** flags get cleared by whoever is in a hurry.

## Customization 7: Licence policy

**Where it's used:** SPEC.md, step 2.

Decide which licences you'll adopt ideas from and which you'll copy text from:

| Licence | Copy text? | Adopt ideas? |
|---|---|---|
| MIT, BSD, Apache-2.0 | Yes, with attribution. Still prefer rewriting | Yes |
| CC-BY | Yes, with attribution | Yes |
| Copyleft (GPL, CC-BY-SA) | Only if your repo can take the obligation | Yes, in your own words |
| None found | No | Read-only. Your own words, from your own understanding |

If your organisation has a legal or open-source policy, it overrides this table.

**If you skip it:** the default is read-only for anything without a clear
permissive licence, which is safe and occasionally slower than it needs to be.

## Customization 8: Where the quarantine is enforced

**Where it's used:** the whole skill.

This is a procedure an agent follows. If you want the dangerous half to hold
when nobody's following it, back it with something mechanical:

- The quarantine outside every repository, so reviewed material can't be committed by accident
- A pre-commit check that fails if a new file under your skills directory has no
  provenance line (only if you adopt enough outside ideas to justify it)
- Your agent's permission rules denying writes to the skills directory without
  approval
- `scripts/scan-skill.py` as a CI step on any PR that adds a skill, so a new
  skill gets at least the mechanical sweep. The default `--fail-on HIGH` blocks
  only on HIGH findings, so a clean skill passes. A skill that has to quote
  attack patterns (this one does) fails by design; clear it with a reason
  rather than lowering the bar for every skill

A rule in a document shapes behaviour. A required check enforces it.

**If you skip it:** quarantine holds exactly as long as everyone remembers it.

## Final checklist

- [ ] The quarantine is outside every repository and every skill-loading path
- [ ] The places a behaviour can be covered are listed
- [ ] Your tool's skill paths are confirmed against its current docs
- [ ] Drafts follow your folder shape, frontmatter and rule wording
- [ ] Your environment-specific red flags are in the list and the scanner
- [ ] A named person clears HIGH flags, with a reason recorded
- [ ] The licence policy is written down
- [ ] At least one mechanical control backs the quarantine

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The trigger and the procedure |
| `SPEC.md` | Why, the red-flag checklist, the worked example, the verdicts, the limitations |
| `CUSTOMIZE.md` | This file: the decisions that bind it to your harness |
| `scripts/scan-skill.py` | The mechanical sweep. Standard library only |
