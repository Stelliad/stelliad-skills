# Adversarial Plan Interrogation

**Question a plan in rounds until its weakest assumption is named. No document,
no edits: the output is what you conclude.**

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r stress-test-plan /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/stress-test-plan

or: "poke holes in this", "grill me on this plan"
```

**Working by hand:** read [SPEC.md](./SPEC.md). The design tree and the frontier
rule are what make the questioning tractable rather than scattershot.

## What it does

Maps the plan as a tree of decisions, then asks every question whose
prerequisites are already settled, in one round, each with a recommended answer
attached so you are reacting rather than composing. Your answers settle
branches, the frontier moves outward, and the next round follows. It ends when
nothing is left silently assumed.

Facts it finds itself. Decisions it always puts to you.

## Who uses it

- **Founders and leads** before a decision that is hard to undo
- **Architects** pressure-testing a design before it becomes a migration
- **Anyone circling the same argument** without finding the disagreement
- **Solo operators**, who have no colleague to play the sceptic

## What it will not do

It interrogates the plan you brought, so a well-defended plan for the wrong
problem passes cleanly. It cannot supply expertise you do not have, and it is
wasted on a decision a revert would undo. Politeness defeats it: if every answer
is "yes, we considered that" and nothing changes, it stopped being adversarial.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
