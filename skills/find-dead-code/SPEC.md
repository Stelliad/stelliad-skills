# Dead Code Sweep Specification

## System Overview

Code that nothing reaches still costs: it is read during onboarding, it is
maintained during refactors, it ships in the bundle, and it widens the attack
surface. This skill finds it and hands the list to a person.

The one rule that shapes everything else: **report, never delete.** A sweep that
removes code is a sweep that eventually removes something live, and the cases it
gets wrong are exactly the cases a person would have caught in a second.

## When it runs

- Before a release, to cut bundle size and attack surface
- After a large refactor, when scaffolding is left behind
- On joining a codebase, to tell what is live from what is merely present
- On a periodic hygiene pass
- When the repository feels bigger than the product it produces

## What it finds

| Category | What | How |
|---|---|---|
| Orphaned files | Nothing imports or requires them | Trace the import tree from every entry point |
| Unused exports | Exported and never imported anywhere else | Cross-reference exports against imports |
| Dead functions | Internal functions never called in their module | AST analysis, or a name search within the file |
| Stale imports | Imported and never used in the file | Per-file static analysis |
| Unreachable code | After an early return, or inside an always-false branch | Control flow analysis |
| Dead dependencies | Declared in the manifest, never imported | Manifest against the set of imported packages |
| Orphaned tests | Test files whose subject no longer exists | Match test names to source names |
| Dead routes | Routes defined and never called by any client | Route definitions against client call sites |
| Commented-out code | Large comment blocks that parse as code | Heuristic, reported for review rather than removal |

## Procedure

### Step 1: Identify entry points

Every project has roots: the files the import tree starts from. Read the
project's own config rather than guessing.

| Project type | Entry points |
|---|---|
| Browser app | The bundler's entry, and the HTML that loads it |
| API service | The server entry, or each handler |
| Serverless | Every handler named in the infrastructure definition |
| CLI | The `bin` entries, or `__main__` |
| Library | Whatever the manifest's `exports` or `__all__` declares |

A missed entry point is the main source of false positives: everything reachable
only from it looks orphaned.

### Step 2: Build the import graph

From each entry point, follow imports recursively until the set stops growing.
That set is what is live. Everything else is a candidate, not a verdict.

### Step 3: Find orphans

Files present but absent from the graph. Exclude by default:

- Config files, and anything a build tool reads by convention
- Test files whose subject is live
- Type declarations
- The entry points themselves
- Anything named in a build config, a CI workflow or a container image

### Step 4: Find unused exports

For each live file, list its exports and search the rest of the tree for each
name. Zero references means unused, with one exception: an entry point's exports
are the public API and are never unused.

### Step 5: Find dead dependencies

Compare the manifest's declared dependencies against the set of packages
actually imported. Check the development dependencies separately; a tool used
only in CI is not dead.

### Step 6: Report

```markdown
# Dead Code Sweep: {project}

Scanned {N} files. Entry points: {list}
Found: {orphans} orphaned files, {unused} unused exports, {deps} dead dependencies

## Orphaned files
- `path`: not reached from any entry point   🟢

## Unused exports
- `path` → `name`: exported, never imported   🟡 barrel file re-exports it

## Dead dependencies
- `package`: declared, never imported   🟢

## Commented-out code (review)
- `path:45-62`: 17 lines that parse as code
```

Every row carries a confidence level, and the level is the useful part:

- 🟢 **High.** No references of any kind, including string references.
- 🟡 **Medium.** Could be reached dynamically: a lazy import, a barrel file, a
  plugin registry.
- 🔴 **Low.** Might be an entry point or a config the sweep did not recognise.

A report that is all 🟢 usually means the entry points are wrong.

## Language notes

**TypeScript and JavaScript.** Check path aliases in the compiler config, and
barrel files, which hide usage behind a re-export. Dynamic imports built from a
variable cannot be traced statically.

**Python.** Check `__init__.py` re-exports and `__all__`. Web frameworks
resolve views by string, and `importlib.import_module()` hides the dependency
entirely.

**Rust.** `pub` items unused outside the crate are candidates; an explicit
dead-code allowance is a declaration that someone already knows.

## Limitations

- **Dynamic references are invisible.** A file loaded by a name built at runtime
  is unreachable to static analysis and perfectly alive at runtime.
- **"Unused" can mean "not wired yet."** In active development, the newest code
  is often the least referenced.
- **Reflection, plugins and registries** defeat the import graph by design.
- **It cannot see other repositories.** An export unused here may be the
  contract another service depends on, which is why a published package's
  entry points are excluded.
- **The commented-out heuristic is a heuristic.** It flags prose that happens to
  parse, and misses code commented out one line at a time.

The safe reading of a result: 🟢 rows are worth acting on after a glance, 🟡 rows
need the person who knows the framework, and a sweep that finds nothing is more
likely misconfigured than clean.
