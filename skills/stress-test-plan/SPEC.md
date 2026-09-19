# Adversarial Plan Interrogation Specification

## System Overview

Most plans fail on an assumption nobody said out loud. This skill finds that
assumption by questioning, in an order that makes the questioning tractable.

Two ideas do the work:

- **The design tree.** Every decision branches into the decisions that hang off
  it. "Which database" hangs off "do we store this at all", and asking them in
  the wrong order produces answers that get thrown away.
- **The frontier.** The set of decisions whose prerequisites are already
  settled: the questions that can be answered *now*, without guessing at
  something still open. The frontier is what gets asked, and nothing else.

It produces no artifact. The output is the conversation and what the person
decides because of it.

## When it runs

- Before a decision that is hard to undo
- When a plan feels right and nobody can say why
- When a team has been circling the same argument
- Before committing budget, a migration, or a public commitment

It is wasted on a two-way door. If the cost of being wrong is a revert, decide
and move.

## The round

Ask the **whole frontier** in one round. Number each question, give it a title,
and attach the answer you would give:

```
❓ **Q1** - **<title>**: <the question, with the choices if there are choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<title>**: <the question>

➡️ <your recommended answer>
```

Then stop and wait. The recommendation is not decoration: it turns an interview
into a review, which is faster for the person answering and surfaces
disagreement immediately.

**A question whose answer depends on another question in this round belongs to
the next round.** That rule is what keeps the tree honest; break it and you get
answers conditioned on guesses.

## Between rounds

Each set of answers settles decisions, which pushes the frontier outward and
unblocks questions that were waiting. Recompute and ask again.

**Facts are yours to find, decisions are theirs to make.** If a frontier
question needs something knowable, read the file, run the query, check the
dependency, rather than asking. Do not block the round on it: a lookup in
progress is an unsettled prerequisite for the questions downstream of it and no
others. Ask the rest of the frontier now.

## Stopping

The session ends when the frontier is empty: every branch visited, nothing left
silently assumed. Say so, and do not act on the plan until the person confirms
you have reached the same understanding.

A session that ends with "looks good" and no changed assumptions was either a
very good plan or a very polite interrogation. The second is more common.

## What good questions look like

- **Name the assumption, not the gap.** "This assumes every customer has one
  account. What happens to the ones with three?" beats "Have you thought about
  multi-account?"
- **Ask for the evidence behind a number.** Where did the 20% come from?
- **Ask what would have to be true.** For the timeline to hold, what has to go
  right, and what is the chance of all of it going right?
- **Ask what it costs to be wrong**, and whether the cost is recoverable.
- **Ask what was already tried**, and why it stopped.

## Limitations

- **It interrogates the plan you brought.** A well-defended plan for the wrong
  problem passes this cleanly.
- **The recommendations are judgments**, and confident ones. Disagree with them;
  their job is to be specific enough to argue with.
- **It cannot supply missing expertise.** It surfaces the question a specialist
  would ask and cannot answer it for you.
- **Rounds cost time.** A deep tree runs to several rounds, which is the point
  and is also why it is wrong for a small decision.
- **Politeness defeats it.** If the answers are "yes, we thought about that"
  and nothing changes, the interrogation stopped being adversarial.
