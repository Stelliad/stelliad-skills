# Dead Code Sweep

**Find what nothing reaches: orphaned files, unused exports, dead dependencies.
Report it with a confidence level. Delete nothing.**

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r find-dead-code /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/find-dead-code

or: "what in this repo is unused?"
```

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly.
[CUSTOMIZE.md](./CUSTOMIZE.md) is where you declare entry points and the paths
your framework reaches by string.

## What it does

Reads the project's config for entry points, traces the import graph from each,
and reports what the graph never reaches: orphaned files, unused exports, dead
functions, stale imports, dead dependencies, orphaned tests, dead routes and
large commented-out blocks.

Every row carries a confidence level, and that is the part to read. 🟢 means no
reference of any kind. 🟡 means it could be reached dynamically. 🔴 means the
sweep is probably misconfigured.

## Who uses it

- **Teams shipping to a browser**, where dead code is bundle size
- **Anyone inheriting a codebase** and trying to tell live from present
- **Security-minded teams**, since unused code is still attack surface
- **Repos after a big refactor**, where scaffolding outlives its purpose

## What it will not do

It never deletes, and it cannot see a dynamic import, a string-resolved route,
or another repository that depends on your exports. In active development
"unused" often means "not wired yet". The Limitations section in
[SPEC.md](./SPEC.md) is the full list.

A sweep that reports nothing is more likely misconfigured than clean.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
