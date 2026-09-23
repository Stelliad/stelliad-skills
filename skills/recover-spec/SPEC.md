# Spec Recovery Specification

## System Overview

The system arrives built. It runs, it has users, and the person who decided why
the retry limit is three has left. "Specs before code" is the right rule for a
system you start. It's no help for the ones that arrive finished, which is most
of them.

This skill recovers the specification from the artifact.

The failure it exists to prevent is subtle and common: **a description of the
code, formatted as a specification.** A description says what these files happen
to do. A spec says what the system must do. Generate the first and label it the
second, and every bug in the codebase becomes a requirement, permanently, because
the next engineer reads the spec and preserves the behaviour it documents. That's
worse than having no spec: it reads as authoritative and is silently wrong.

The defence is grading. Every statement in a recovered spec is marked with what
it rests on, and the statements that rest on nothing become the question list.

## Where the output goes

Two routes, and the choice isn't a preference.

| Situation | Output |
|---|---|
| You hold the repo and will build in it | `SPEC.md` at the repo root, subsystems in `docs/specs/` |
| You're reading a system you won't commit to: diligence, evaluation, a vendor's product, an audit | A dated reading, outside the governed tree (default `docs/readings/system-spec-{YYYYMMDD}.md`, bind yours in CUSTOMIZE.md) |

The test is whether the document will **define what gets built** or **record
what you found**. Run with neither `--as-spec` nor `--as-reading` and you get a
reading. Default to a reading when it's genuinely unclear, too. A reading
can be promoted into the repo later; a spec that never governed anything is just
a reading in the wrong place.

A `--subsystem` run follows the same route as the whole-system document: into
`docs/specs/{name}.md` beside a governing `SPEC.md`, or beside the reading
(default `docs/readings/{name}-spec-{YYYYMMDD}.md`) when you're recording what
you found. A subsystem reading never lands in `docs/specs/`, because that
directory governs.

**Never write both.** Two copies drift. If a repo already carries a `SPEC.md`,
this skill doesn't overwrite it: it reads it as an *intended* source and reports
where the code disagrees.

## What it reads

| Source | What it takes | Why it matters |
|---|---|---|
| Entry points: routes, handlers, CLI commands, jobs, listeners, webhooks | Every way work enters the system | The boundary is drawn here or it isn't drawn |
| **Tests** | Every assertion | The only place the system states a requirement about itself |
| Schema, migrations, table definitions | Entities, keys, access patterns | Migrations carry the history the code has forgotten |
| Infrastructure-as-code | Resources, network topology, access policy, account layout | Where the trust boundaries actually sit |
| Config and environment variable **names** | What's tunable and what was hardcoded | Names only, never values |
| Git history on the load-bearing files | The commit that introduced a constant sometimes carries its reason | The cheapest source of intent in the repo |
| README, `docs/`, decision records, code comments | Stated intent | Graded *intended*, never *observed* |
| Issues and pull requests | Known defects, deferred decisions | An open issue is an undecided with a ticket number |
| Any written commitment the system was built against: a scope document, a contract, a product brief | What someone promised the system does | Graded *intended*. Disagreements go on the question list |

## The grade

Every statement in the output carries one. This is the whole method.

| Grade | Means | Test |
|---|---|---|
| **Observed** | The path was read end to end, or better, exercised | Point at the code, or at the test that proves it |
| **Inferred** | One reading says this. Nothing exercises it | Would survive a rename, not a rewrite |
| **Intended** | A comment, README, name, ticket or contract says so. The code may or may not agree | Cite the document. Never promote to observed without reading the path |
| **Undecided** | The code makes a choice and nothing records whether it was a decision | **The most valuable output of the run** |
| **Contradiction** | Two parts of the system disagree, or the code contradicts its documentation | Name both sides. Don't pick a winner |

**Never promote a grade to make the document read better.** A spec that's 90%
observed is strong. A spec that claims 90% observed and is 40% inferred is a
liability, and nobody downstream can tell the difference by reading it.

### Undecided is the deliverable

A constant isn't a requirement. `MAX_RETRIES = 3` is an *observed behaviour* and
an *undecided requirement*, and the difference is the entire value of working
backwards. Somebody either chose three against a rate limit, or typed three
because three is a number. One of those must survive a rewrite and the other
mustn't, and no amount of reading the code tells you which.

So the run produces a question list, and each question is addressed to a person:

> Retry limit on the send path is 3 with a fixed 200ms backoff
> (`services/notify/retry.py:41`). Requirement or default? If it was set against
> a provider's rate limit, which provider, because the code now calls a
> different one.

## Procedure

### 1. Pin the reading

```bash
git -C <repo> rev-parse --short HEAD && git -C <repo> status --short | head
```

Record the SHA, the branch, and whether the tree was dirty. **A spec read off a
moving branch is a spec of nothing.** Six weeks later nobody can tell whether a
discrepancy is drift or an error in the run.

### 2. Fix the boundary before reading anything else

What is the system, and what is a dependency it calls? Write the list before
tracing anything. A surface that isn't listed isn't excluded from the spec: it's
missing from it, silently.

| In | Out | Undeclared |
|---|---|---|
| Code this spec governs | Third-party services, systems another team owns, vendor SDKs | Something that could be either, and nobody has said |

The undeclared column is a finding. A shared library two teams both change and
neither owns belongs in the report, not a footnote.

### 3. Inventory the surfaces

Every way work enters, leaves or persists. Infrastructure-as-code is the fastest
census where it exists:

```bash
grep -rhoE '^resource "[a-z0-9_]+"' infra/ --include=*.tf | sort | uniq -c | sort -rn
```

Entry points, scheduled work, queues and streams, data stores, outbound calls,
and the trust boundary each one crosses. Mark every surface with whether it's
authenticated, what it trusts about its caller, and what happens when it's
called with garbage. That last column is usually empty on the first pass, and
every empty cell is a question.

### 4. Trace the core data path end to end

**One walk, from the user action to the durable write and back.** This is the
spine of the spec and the section a new engineer actually reads. Everything else
is reference material.

Follow the unit of work the business recognises: an order, a booking, a
submitted form, a sent message. Not "a request." At each hop record what's
passed, what's stored, what leaves the boundary, and what the caller sees when
the hop fails.

Where the system handles sensitive or regulated data, record the data category
at each hop. The trace then doubles as the data-flow inventory a privacy or
compliance review needs, produced once.

### 5. Recover the data model, and its unenforced invariants

Entities, keys, relationships, access patterns, retention.

Then the part that only comes from working backwards: **the invariants the code
assumes and doesn't enforce.** A field every reader treats as non-null that the
schema allows to be null. An ordering two writers depend on that nothing
guarantees. A uniqueness the application checks and the database doesn't.

These are the requirements most likely to be lost in a rewrite, because they're
written down nowhere and everything currently depends on them.

### 6. Read the requirements out of the tests

**A test assertion is the system stating a requirement about itself.** It's the
only place in a codebase that does so, and the highest-grade source available: a
passing assertion is *observed*, not inferred.

So coverage is a specification question. Behaviour with no test is behaviour
nobody has committed to, and it can change under a refactor with nothing
objecting. Report which spec sections are test-backed and which aren't, and hand
the gap to [coverage-gaps](../coverage-gaps/SKILL.md).

### 7. Find the behaviour nobody owns

Two directions, both findings:

- **Code with no requirement.** Reachable paths that satisfy nothing anyone can
  name. Send unreachable ones to [find-dead-code](../find-dead-code/SKILL.md).
  The reachable ones go on the question list, because somebody may depend on them.
- **Requirements with no code.** A README, a scope document, a contract or an
  issue promises behaviour the system doesn't implement. That's a
  contradiction, and it goes on the question list with both sides cited.

### 8. Write it, then grade it

Structure per [references/spec-skeleton.md](./references/spec-skeleton.md). Then
hand the document to [tech-doc-review](../tech-doc-review/SKILL.md), which is the
quality bar for technical documents and takes this one unmodified.

## Rules

1. **Never write a bug into the spec as a requirement.** Where behaviour looks
   wrong, record it *observed* and flag it a candidate defect on the question
   list. Don't silently correct it and don't silently canonise it. This is the
   failure the skill exists to prevent.
2. **Never invent a rationale.** "Three retries, to stay under the provider's
   rate limit" is fabrication unless something says so. `MAX_RETRIES = 3` with
   no stated reason is an undecided, and a plausible reason written next to it
   destroys the only signal the line carried.
3. **Never promote a grade.** Intent found in a comment stays *intended* until
   the path is read.
4. **Grade a section at its weakest statement.** One observed line doesn't make
   an observed section.
5. **Pin the reading and say so in the frontmatter.** SHA, branch, clean or dirty.
6. **Read-only on the code.** Recovery produces a document. It never fixes what
   it finds, never adds the missing test, never tightens the schema. Those are
   separate, reviewed changes.
7. **Never read a secret value.** Environment variable *names* describe the
   system. Write `${DATABASE_URL}`, never what it resolves to. A secret found in
   the code is reported by file, line and type, never quoted, and goes to
   [secret-scan](../secret-scan/SKILL.md) as a rotation event.
8. **Cite, don't copy.** Reference code by path and line. A spec isn't a reason
   to paste someone else's source into a document that travels further than the
   repo does.
9. **A run with zero undecideds is a failed run**, not a clean one.
10. **One copy.** The repo gets a `SPEC.md` or you keep a reading. Never both.

## Output

```
┌─────────────────────────────────────────────────────────┐
│  RECOVERED: {system}                                    │
│  {repo} @ {sha} ({branch}, {clean|dirty})               │
│  {n} surfaces · {n} entities · {n} entry points         │
├─────────────────────────────────────────────────────────┤
│  Observed {n}   Inferred {n}   Intended {n}             │
│  Undecided {n}   Contradictions {n}                     │
├─────────────────────────────────────────────────────────┤
│  Spine: {the core data path, one line}                  │
│  Test-backed: {n} of {n} spec sections                  │
├─────────────────────────────────────────────────────────┤
│  Questions for {owner}: {n}                             │
│  Top question: {the one that changes the most}          │
└─────────────────────────────────────────────────────────┘
```

The grade split sits next to the counts because it qualifies them. A reader who
sees "42 requirements recovered" without "19 of them inferred" has been handed a
reading dressed as a fact.

**The document.** Sections in the order the skeleton gives: what the system is,
the boundary, the surfaces, the core data path, the data model and its
invariants, trust boundaries and account topology, the recovered requirements
with grades, the subsystem index, known defects and unowned behaviour.

**The question list.** Standalone, because it travels to a person and the spec
travels to a repo. Every undecided and every contradiction, each with the code it
came from, who can answer it, and what changes depending on the answer. Ordered
by what the answer changes, not where it was found.

**The findings.** Candidate defects, unenforced invariants, unowned behaviour,
and anything a written commitment promises that the code doesn't do.

**The chat summary.** Short: the spine in one line, the grade split, and the top
three questions.

## Integration

| Skill | Relationship |
|---|---|
| [tech-doc-review](../tech-doc-review/SKILL.md) | The quality bar. Always runs on the output. This skill writes the spec; that one decides whether it is one |
| [coverage-gaps](../coverage-gaps/SKILL.md) | Untested behaviour is unspecified behaviour. Step 6's gap list is its input |
| [find-dead-code](../find-dead-code/SKILL.md) | Unreachable code isn't part of the spec. Route it there rather than documenting it |
| [secret-scan](../secret-scan/SKILL.md) | Run it first on any inherited repo. A secret found mid-recovery is a rotation event, not a footnote |
| [generate-readme](../generate-readme/SKILL.md) | A README orients a newcomer. A spec governs the build. A README is never a substitute |
| [repo-audit](../repo-audit/SKILL.md), [review-principles](../review-principles/SKILL.md) | Grade how the code is built. This skill records what it does. Neither answers the other |
| [implement-spec](../implement-spec/SKILL.md) | Downstream, once the undecideds are answered and the settled requirements become a task list with verification commands. You write that plan and task list; nothing here generates them. Its CUSTOMIZE.md sections 1 and 2 give the shape it reads |

## When to run

| Trigger | Note |
|---|---|
| A codebase arrives that you didn't build | The reason this skill exists |
| Before scoping new work on an existing product | Scope written against an unread system is fiction |
| Before a rewrite or a migration | The undecided list is exactly what a rewrite loses |
| Before a security or compliance review | The review needs the surface inventory and the data path |
| Diligence on someone else's product | `--as-reading`, always |
| The person who knew it has left | Intent sources decay fastest. Read the git history while it still has names attached |
| A subsystem gets its first real change in a year | `--subsystem`, scoped to the blast radius |

## Limitations

- **The grades rest on discipline.** A promoted grade looks identical to an
  honest one. Nothing in the output catches an agent that called an inference an
  observation, so spot-check the observed claims against the code they cite.
- **It can't recover intent that was never recorded.** Where the reason for a
  choice lived only in someone's head, the best it can do is name the question.
  That's the point, and it's also the ceiling.
- **Static reading misses runtime configuration.** Feature flags, values held in
  a secrets store, and anything resolved at deploy time are seen by name only.
  Behaviour that depends on them is *inferred* at best.
- **The data path is one path.** The spine covers the primary unit of work.
  Secondary flows get surface entries, not full traces, unless you run
  `--subsystem` on them.
- **Tests can encode bugs too.** A passing assertion is observed behaviour that
  someone once committed to. It isn't proof the behaviour is right, and a test
  that asserts a defect makes that defect look like a requirement.
- **Large systems need more than one pass.** Past a few dozen surfaces, run a
  whole-system pass for the boundary and spine, then `--subsystem` for the parts.
