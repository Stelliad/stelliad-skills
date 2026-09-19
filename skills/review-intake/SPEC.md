# Review Intake Specification

## System Overview

A review arrives as a list. The cheapest thing to do with a list is work down it,
and that is the thing that ships regressions.

This skill treats each item as a claim that has to survive contact with the
codebase before it becomes a diff. Two steps carry the weight, and both are the
ones that get skipped: clarifying the whole set before starting, and verifying
each item against the code rather than against the reviewer's confidence.

It applies the same way to a senior engineer's comment and to a bot's finding,
except that the bot gets more scrutiny rather than less, because it has no
context at all.

## The sequence

```
1. READ         the entire set, before reacting to any of it
2. RESTATE      each item, in your own words
3. CLARIFY      anything ambiguous, before touching a file
4. VERIFY       each item against the actual codebase
5. DISPOSITION  accept, accept with change, push back, out of scope
6. IMPLEMENT    one item, one test, one at a time
7. REPLY        in the thread, stating what changed
```

## Clarify the whole set first

If any item is unclear, **stop before implementing any of them.** Items are
frequently related, and a partial reading produces a change that satisfies item
2 and contradicts item 5.

```
Six items. You understand 1, 2, 3, 6. Items 4 and 5 are ambiguous.

Wrong:  implement 1, 2, 3, 6 now, ask about 4 and 5 afterwards
Right:  "Clear on 1, 2, 3 and 6. Need 4 and 5 pinned down before I start,
         since 5 may change how I do 2."
```

## Verify before implementing

| Check | Question | How |
|---|---|---|
| Correct here | Is this right for *this* codebase, not in general? | Read the surrounding code |
| Breakage | Does it break something that currently works? | Run the suite; find the callers |
| Reason | Why is the current implementation the way it is? | Search the history for the line; look for a comment or a linked issue |
| Reach | What else touches this? | Search the symbol across the repository |
| Context | Does the reviewer have the whole picture? | Often not. Automated reviewers never do |
| Scope | Is this the branch's job, or a separate ticket? | Compare against the change's stated scope |

Where verification is not possible, say so rather than guessing: *"I cannot
confirm this without access to the staging data. Do you want me to investigate,
or take it on your read?"*

## Disposition every item

Four outcomes, and every item gets exactly one:

| Disposition | When | Then |
|---|---|---|
| **Accept** | Correct, in scope, verified | Fix it. Test it. Reply with what changed |
| **Accept with change** | The problem is real, the proposed fix is not | Fix the problem your way, say why the approach differs |
| **Push back** | Wrong for this codebase | Reply with the technical reason and the evidence |
| **Out of scope** | Real, but not this branch's job | File it, link the ticket in the reply, move on |

"Out of scope" is not a way to duck work. It is the correct answer when a
finding is real and unrelated, and it only works if the ticket actually gets
created. An out-of-scope disposition with no ticket behind it is a decline
wearing a process word.

## When to push back

Push back when the suggestion:

- Breaks working behavior
- Rests on context the reviewer does not have
- Adds a feature nothing calls. Search first, then say so
- Is wrong for this stack or this runtime version
- Exists the way it does for a compatibility or legacy reason
- Contradicts an architectural decision already made

With the reason and the evidence, not with defensiveness:

```
Reviewer: "Drop the legacy path."

Weak:  "You're absolutely right, removing it now."
Right: "Build target is 10.15+; the modern API needs 13+. The legacy path is
        load-bearing for pre-13. The identifier in it is wrong though,
        fix that, or drop pre-13 support and delete the whole branch?"
```

Run the same search before implementing anything described as "doing this
properly". If nothing calls it, propose deleting it rather than building it out.

## How to reply

State the fix. Do not perform.

```
Good:  "Fixed. Expired tokens now return 401 rather than 500. Test at auth.test.ts:44."
Good:  "Real bug, wrong location. The null check belongs in the caller; moved it there."
Good:  [the diff, with no commentary]

Bad:   "You're absolutely right!"
Bad:   "Great catch, thanks for flagging this!"
Bad:   "Let me implement that right away."   (before verifying)
```

Agreement noises carry no information and pad the thread. The diff is the
acknowledgment.

If you pushed back and were wrong, correct it in one line and continue:
*"Checked. You're right, `parseDate` does handle the timezone. Implementing."*
No apology paragraph, and no defence of why you pushed back.

## Implementation order

Once every item is clarified and dispositioned:

1. **Blocking**: breakage, security, data loss
2. **Cheap**: typos, imports, dead code
3. **Structural**: refactors, logic changes

One at a time. Each gets its own test, and the suite runs between items.
Batching five fixes and running the suite once tells you something broke and
nothing about which fix broke it.

## Replying in threads

Reply inside the comment thread, not as a new top-level comment. A top-level
reply orphans the finding and leaves the thread unresolved, which is how a
review ends with every item fixed and the pull request still blocked.

List the open threads before you start, so the count at the end means something.
`CUSTOMIZE.md` binds the commands for your review tool.

## Output

```markdown
# Review Intake: {change ref}

**Items:** {N} · accepted {a} · accepted-with-change {b} · pushed back {c} · out of scope {d}
**Clarification needed:** {none | items X, Y, asked, waiting}

| # | Item | Disposition | Evidence | Where |
|---|------|-------------|----------|-------|
| 1 | Expired tokens return 500 | Accept | Reproduced; test was missing | `auth.ts:88`, test at `auth.test.ts:44` |
| 2 | Add retry config options | Push back | Nothing calls this path: searched, 0 hits | reply posted |
| 3 | Extract the parser | Out of scope | Real, unrelated to this branch | issue #212 |

**Verification:** 51/51 pass, lint clean, types clean.
**Threads:** 3 of 3 replied. 0 unresolved.
```

## Rules

1. **Verify before implementing.** A reviewer's confidence is not evidence.
2. **Clarify the whole set before starting any of it.** Items interact.
3. **No performative agreement.** No "you're absolutely right", no thanks, no
   enthusiasm. State the fix.
4. **Push back when it is wrong**, with reasoning and evidence. Technical
   correctness beats social comfort.
5. **One item, one test, one run.** Never batch.
6. **Automated findings get more scrutiny, not less.** They have no context.
7. **Every item gets a disposition.** Silence on an item reads as agreement you
   never gave.
8. **Reply in the thread**, not at the top level.
9. **Escalate, do not absorb**, when a finding contradicts an architectural
   decision already made. That is a decision, not a fix.

## Limitations

- **It is downstream of the review.** It disposes of what was found, and says
  nothing about the bug nobody looked for. A thorough intake on a shallow review
  still ships the shallow review.
- **Push back needs standing.** The procedure assumes you can decline an item
  and have that be the end of it. Where a reviewer's word is final regardless of
  evidence, the honest disposition is accept, and the argument belongs somewhere
  other than the thread.
- **Verification has a floor.** Some items cannot be checked without data or
  access you do not have. Saying so is the correct move and it is also an item
  left unresolved.
- **It does not judge the reviewer.** A pattern of low-quality findings from one
  source is a conversation to have, not something this procedure will surface.
- **The disposition table is a claim, not a proof.** It records what was decided
  and the evidence cited. Whether the fix works is a separate gate.
