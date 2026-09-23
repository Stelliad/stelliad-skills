# Ticket Authoring Standard

What a work item has to contain before a human or an unattended agent can pick
it up. `review-ticket` grades against this file and `create-ticket` writes to
it. It's the only copy: `create-ticket` links here rather than carrying its own,
because two copies of a standard drift and the stale one still reads as
authoritative.

A ticket defines **what** has to happen, **why**, **what done looks like**, and
**where the boundaries are**. It doesn't define **how** engineering gets done.
That already lives elsewhere and shouldn't be copied into an issue:

| Layer | Usually lives in |
|---|---|
| How code gets written in the repo | the repo's contributor guide, agent rules file, or linters |
| What "done" means for a change | the repo's pull request template and required CI checks |
| What a feature must do, in requirement form | a spec document, where the work is big enough to have one |
| Repo-wide gates | CI configuration |

Never restate secure coding, testing, logging, observability, least privilege,
error handling, review, or CI in a ticket. They're already required. State an
**exception** to a standard, never the standard itself.

## The ticket is the worker's prompt

When an agent picks up a ticket, the issue body usually goes into its prompt
whole, often on **every pass** of a work loop, with an instruction to do the
next unfinished acceptance criterion. Three consequences follow, and they
aren't style preferences:

1. **Acceptance criteria are the work queue.** Write them as a flat `- [ ]`
   list. One observable outcome per line. No nesting, no sub-bullets, no prose
   paragraphs between items. A nested or narrated list isn't iterable, and the
   agent re-reads it as one undifferentiated blob.
2. **Order the list in execution order.** The agent takes the next unfinished
   item, so the list is a sequence, not a set.
3. **Every section costs tokens on every pass.** A ticket carrying eight
   sections of boilerplate pays for them n times. Write the core, and add a
   conditional section only when it changes what gets built.

A human reader benefits from all three too. They're just less expensive when a
human ignores them.

## Section set

Two tiers. Required sections appear in every implementation ticket. Conditional
sections appear only when they carry real information, and are **omitted
entirely** rather than filled with `N/A`.

### Required

```markdown
## Objective

One or two sentences describing the outcome that should exist when this is
done. The result, not the implementation.

## Why

Why this is needed. Enough product or technical context that someone with no
memory of the conversation that created the ticket understands the point.

## Acceptance Criteria

- [ ] Observable, independently verifiable outcome
- [ ] Failure behaviour is stated, not implied
- [ ] The edge case that actually matters

## Scope

**In:** what this ticket changes.
**Out:** what it deliberately doesn't touch.

## Risk

`Low | Medium | High | Critical`, with one line of reason for High or Critical.
```

### Conditional

| Section | Include when |
|---|---|
| `## Context` | Existing behaviour, architecture, or a prior decision the implementer would otherwise have to go find |
| `## Requirements` | Behaviour or constraints that aren't directly observable as acceptance criteria |
| `## Constraints` | A real architectural boundary: must preserve an API contract, must not add a datastore, must use the existing identity provider |
| `## Dependencies` | `Depends on #N`, `Blocked by #N`, a spec, a decision, a migration, an external service. Omit it when there are none rather than writing `None`. Put the reference straight after the phrase: "Blocks #9" is a relation a tool can read, "Blocks the criterion in #9" is prose it can't |
| `## Human Approval` | Anything an agent may prepare but must not execute: a production deploy, an IAM change, a production migration, a secrets rotation, anything destructive |
| `## Verification` | Task-specific checks only, never repo-wide ones. See below |
| `## Assumptions` | A safe assumption was made in place of a missing answer. State each one so it can be challenged |
| `## References` | A spec path, an ADR, a design doc, an API reference, a related issue. Only ones someone will actually open |

## Verification, and who's authoritative

Two gates exist and they can disagree. The rule:

**The project-level gate is authoritative**: the CI checks a pull request must
pass, or the test command and completion requirements your agent runner
enforces. The ticket's `## Verification` section is an additional,
change-specific check that the project gate is too coarse to express: "the
existing login still works", "an unauthenticated request returns 401", "the
migration rolls back".

A ticket may never weaken a project-level gate. If a ticket genuinely needs a
different gate, that's a change to the gate's configuration in its own commit,
not a sentence in an issue body.

**Where the project has no real test command, `## Verification` stops being
optional.** A runner configured with a test command that always passes proves
nothing, and in that repo the ticket's own verification steps are the only
real check. A finished issue there should go to human review rather than close
on its own.

## Titles

Short, specific, outcome-oriented. Start with a verb.

```
Add expiration to admin sessions
Prevent duplicate webhook processing
Fix mobile navigation overflow on the customer list
```

Not `Auth updates`, `API work`, `Bug fix`, `Cleanup`, `Various fixes`.

Prefix with a bracketed type only where the repo's issue form doesn't already
carry a type field: `[Bug]`, `[Security]`, `[Infra]`, `[Tech-Debt]`, `[Spike]`,
`[Docs]`. Where the form sets a `type:` label, the prefix is redundant. Don't
carry both.

## Requirements and acceptance criteria are different

A requirement says what the solution must do. An acceptance criterion says how
you'll know it was done. Never write a criterion that restates a requirement in
the same words.

```
Requirement:        Only authenticated administrators may regenerate an API key.

Acceptance Criteria:
- [ ] An admin regenerating a key receives the new key and the old one stops working
- [ ] A standard user requesting regeneration receives 403
- [ ] An unauthenticated request receives 401
```

Every criterion must resolve to PASS or FAIL by observation. "Authentication
works correctly" and "improve duplicate handling" aren't criteria. "A request
without authentication returns 401" and "duplicate event IDs are processed
exactly once" are.

Vague verbs are banned in requirements and acceptance criteria unless a
measurable target follows them: improve, optimise, clean up, make better,
handle properly, harden, refactor.

## Don't specify the implementation

The implementer, human or agent, chooses the approach from the repo's own
architecture and rules. A ticket that names the function, the table, and the
API call has removed the judgement the repo's standards exist to supply, and it
goes stale the moment the architecture moves.

State a constraint when it's a genuine architectural boundary. Don't state a
preference dressed as one. The test: would a different reasonable
implementation actually break something, or would it merely be different?

## Scope is a hard boundary

`Out` is binding. An agent or engineer that can't finish the work without
crossing it **stops and says so** rather than expanding quietly. A ticket that
grew mid-flight is a ticket nobody reviewed.

Write a `Scope` block whenever the work could plausibly expand, which is nearly
always. The cheap version is two lines.

## Risk

| Level | Means |
|---|---|
| `Low` | Localised change, small blast radius, obvious rollback |
| `Medium` | Touches important behaviour, rollback is straightforward |
| `High` | Touches authentication, authorisation, payments, data integrity, infrastructure, privacy, or a shared system |
| `Critical` | Could affect production security, customer data, availability, financial transactions, compliance, or an irreversible infrastructure change |

`High` and `Critical` carry a one-line reason. A `Critical` ticket is never
marked ready for an agent without a `## Human Approval` section naming what the
agent must not execute.

**A `## Human Approval` section states intent. It doesn't enforce anything.**
An unattended agent running with its permission prompts turned off is stopped
by nothing written in an issue body. Either the runner's own configuration
denies the operation, or the ticket isn't queued for unattended work and a
human runs it.

Where the work touches a regulated data category, your compliance obligations
govern and outrank this table.

## Definition of Ready

Pick one label that means Ready. This standard calls it `agent-ready`. There's
no second one. It's the signal an agent or a queue filters on, and an open issue
without it is backlog, not a queued task. Apply it deliberately, issue by issue,
never in bulk.

A ticket is Ready when all ten hold:

1. The objective states an outcome, not a task.
2. The reason is stated and doesn't depend on a conversation.
3. Requirements are specific, with no unqualified vague verb.
4. Every acceptance criterion resolves to PASS or FAIL by observation.
5. Acceptance criteria are a flat checkbox list in execution order.
6. Scope names what's out, not only what's in.
7. Dependencies are satisfied, or named and understood.
8. Every decision that changes architecture, security, scope, or product
   behaviour has been made.
9. Risk is classified, and any human-approval gate is named.
10. A fresh session with no history could execute it.

Failing 8 means the ticket is `BLOCKED`, not merely unready. Say which decision
is missing and who owns it.

## Quality score

The score is the ten Ready items, weighted. It exists so two weak tickets can be
compared, not as a second gate.

| Dimension | Ready items | Max |
|---|---|---|
| Objective clarity | 1 | 2 |
| Context sufficiency | 2, 10 | 2 |
| Requirements clarity | 3 | 2 |
| Acceptance criteria | 4, 5 | 2 |
| Scope clarity | 6 | 2 |
| Dependencies | 7 | 1 |
| Risk and approval | 9 | 1 |
| **Total** | | **12** |

`10-12` READY. `7-9` NEEDS_REFINEMENT. `0-6` is also NEEDS_REFINEMENT, and
usually means a rewrite rather than an edit. Item 8 is a separate `BLOCKED`
verdict and isn't scored, because a missing decision isn't a quality problem
with the writing.

## Sizing

A ticket is the right size when one worker can hold its context, one branch
represents it, one PR can be reviewed, and a failed attempt can be retried
safely.

It's too large when it spans unrelated subsystems, has more than one
independently deliverable outcome, needs more than one deployment, or can't be
summarised in a sentence. There's no line-count rule. Logical boundaries only.

Don't split tightly coupled work to make the pieces smaller. The goal is
independently reviewable work, not small work.

Prefer vertical slices. `Add user notification preference`, carrying the
minimal data, API, and UI change for one complete outcome, beats a frontend
ticket plus a backend ticket plus a database ticket. Use a horizontal
infrastructure ticket only when a real architectural prerequisite forces it.

## Spec-backed work gets one ticket, not many

If your team writes specs, a spec's own task list is the execution state.
Minting one issue per requirement or acceptance criterion puts that state in
two places, and the two drift.

So **a feature with a spec gets one parent issue** whose body is short and
points at the spec. It references requirement IDs and never copies their text.
The spec's task list stays the work queue, and the checkboxes live there.

```markdown
## Objective

Implement SPEC-014, account API keys.

## Why

<one or two sentences, so the issue is legible from a phone>

## Acceptance Criteria

- [ ] Every acceptance criterion in `specs/014-account-api-keys/SPEC.md` verified
- [ ] The spec's traceability table has no row without PASS
- [ ] An independent review of the implementation run, findings resolved or accepted

## Scope

**In:** SPEC-014 as written.
**Out:** anything not in SPEC-014. A gap goes to the spec's open questions, not
into this ticket.

## Risk

...

## References

`specs/014-account-api-keys/`
```

Work with no spec gets ticketed normally. Work large enough to need
decomposition gets a spec first, not a pile of issues. The dividing line is
whether the work has requirements that need reviewing and tracing, or just an
outcome that needs building.

## A child is attached to its parent, not just pointed at it

Where a parent issue does have children, attach each one with GitHub's native
sub-issues API:

```bash
CHILD_ID=$(gh api repos/{owner}/{repo}/issues/{child} -q .id)
gh api repos/{owner}/{repo}/issues/{parent}/sub_issues -X POST -F sub_issue_id=$CHILD_ID
```

It takes the child's `id`, not its issue number. The two are different, and the
error you get when you pass the wrong one doesn't say so.

A `Part of #100` line in the child's body is worth keeping, because it tells
whoever opens the child what it belongs to. It does nothing for whoever opens
the parent: GitHub doesn't walk that line backwards, so the parent shows
nothing, and the only way to see the set is to search every issue body for a
reference to it.

Attached, the parent renders its children inline with a completion count, `gh`
can list them, and closing one moves the parent's progress. Attach at creation.
Retrofitting works, but every issue minted before someone notices is an issue
nobody can find from the top.

The parent must be an issue. A pull request is rejected with "Parent may only
be an issue", which is also the tell that a `part of #N` in prose was a sentence
about a PR rather than a declaration of parentage.

## Types

A feature, an infrastructure change, a security fix, and a tech debt ticket all
use the required section set above, and differ only in which conditional
sections they carry.

A **bug** and a **spike** substitute equivalents for `## Objective` and
`## Why`, because in both the outcome isn't the natural opening:

| Shape | Required sections |
|---|---|
| Task | Objective, Why, Acceptance Criteria, Scope, Risk |
| Bug | Summary, Impact, Current Behavior, Expected Behavior, Reproduction, Acceptance Criteria, Risk |
| Spike | Decision Needed, Why, Scope, Expected Deliverable, Decision Criteria, Risk |

Risk is required in every shape, without exception.

Acceptance criteria are required in a task and a bug. **A spike has none**, and
substitutes Expected Deliverable and Decision Criteria. That isn't a
convenience: a spike's outcome is a decision, and forcing an implementation
checkbox list onto it is how a spike becomes an implementation ticket without
anyone deciding it should.

| Type | Emphasises |
|---|---|
| Feature | Desired behaviour, the boundary, acceptance criteria |
| Bug | Current behaviour, expected behaviour, reproduction, impact, evidence, regression coverage |
| Security | Affected boundary, the weakness in general terms, expected behaviour after the fix, human approval |
| Infrastructure | Target state, which environments, blast radius, rollback, human approval, cost |
| Tech debt | The current problem, why it matters now, the end state, and what behaviour must not change |
| Spike | The question, the boundary, the expected deliverable, the decision criteria, an effort limit |

Two type-specific rules that aren't negotiable:

**A bug doesn't need a root cause to exist.** Requiring diagnosis before filing
is how bugs go unfiled. Current behaviour, expected behaviour, and a
reproduction are enough.

**A spike produces a decision, not code.** Its deliverable is a recommendation,
an ADR, a benchmark, or a throwaway prototype, never shipped behaviour. A spike
that quietly became an implementation ticket has skipped the decision it
existed to produce, and the follow-up implementation ticket it names is where
the code goes.

### Security tickets

Include enough to remediate, and no more. Never put a credential, token, key,
customer record, or a working exploit path into an issue. Sanitise evidence.
Where the detail is genuinely needed, reference where it's held rather than
reproducing it.

Finding a live credential is a rotation event first and a ticket second.

## No invented context

If the input says "add notifications", don't invent an email provider, an SMS
gateway, or a websocket service. Name what the repo already uses, or record the
choice as an unresolved decision.

Where a missing answer has a safe default, state it under `## Assumptions` and
carry on. Where a missing answer changes architecture, security, scope, or
product behaviour, mark the ticket `BLOCKED` and name the decision. Don't ask
about implementation details that reading the repo would resolve.

## Labels

Reuse what your tooling already reads. Don't build a taxonomy. The names below
are defaults; `CUSTOMIZE.md` covers renaming them.

| Label | Meaning |
|---|---|
| `P1-urgent` `P2-high` `P3-medium` `P4-low` | Queue order. Oldest first within a tier, unlabelled last. An open `Depends on #N` outranks all of them: the issue waits until #N closes |
| `agent-ready` | The Definition of Ready above is met. The queue-eligibility signal |
| `agent:blocked` `agent:needs-review` | Written by your agent runner. Never applied by hand |
| `type:bug` `type:spike` | Applied by type-specific issue forms |
| `type:feature` `type:security` `type:infra` `type:tech-debt` `type:docs` | Applied at triage. A single task form can cover all of these behind a Type dropdown, and **a GitHub issue form can't turn a dropdown answer into a label** |
| `risk:low` `risk:medium` `risk:high` `risk:critical` | Applied at triage, for the same reason |
| `agent:human-required` | Carries a `## Human Approval` gate. Never marked ready without a human on the run |
| `status:blocked` | Ready item 8 fails: a decision is open. The `BLOCKED` verdict, made visible on the issue |
| `status:ready-to-merge` | The work is done, its PR is open and every check is green. The only thing left is somebody pressing merge |

The triage rows matter more than they look. A form can't set a label from a
dropdown, so on a repo where nobody triages, `type:` and `risk:` are simply
absent and every filter built on them silently returns nothing. Either someone
applies them when the issue is read, or a project board field carries them
instead and the labels get dropped. Don't assume the form did it.

Anything beyond status, priority, risk, owner, iteration, and parent belongs in
a project board field, not a label.

### An issue that's only waiting on a merge says so

`status:ready-to-merge` goes on the moment the PR closing the issue is open and
green, and comes off when the PR merges and the issue closes.

An issue with finished work sitting behind an unmerged PR reads, from the issue
list, exactly like an issue nobody has started. The PR knows, the issue is where
the work is tracked, so the two disagree and the list is the one being read. An
`in-progress` label is worse than nothing here: it says somebody's still typing.

It's a status rather than something inferred from a linked PR, because the
inference only holds where the PR body carries a closing keyword, and a status
that silently means nothing on the issues that forgot one isn't a status.

**A PR that finishes an issue says `Closes #N`.** Without it neither side learns
about the other: nothing can tell which issues are finished and waiting, and
GitHub closes none of them on merge either. Put it in the body, not the title,
and only where the PR really does finish the issue. A PR that advances an issue
without closing it references it plainly and leaves the status alone.

## Issue forms are instances of this file

Issue forms (`.github/ISSUE_TEMPLATE/*.yml`) carry the structure for a human
filing an issue, and GitHub requires them per repo. This file carries the
standard for whoever authors, reviews, or queues a ticket. When a form and this
file disagree, this file is right and the form is stale. Don't paste this prose
into each repo to fix the drift; fix the form.
