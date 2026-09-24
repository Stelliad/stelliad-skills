# Spec Creation

**Turn an idea into a draft spec in a fixed shape and a fixed place, with every
gap left open as a question for a named person.**

## Running it

This is a specification an agent executes, not a binary. It is the first of
four skills that form one loop, and it carries the templates the other three
read, so copy the set:

```bash
cp -r create-spec plan-spec implement-spec review-spec /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/create-spec session-expiry

or: "spec out this feature", "start a spec for X"
```

**Working by hand:** copy [templates/SPEC.md](./templates/SPEC.md) into
`specs/{NNN}-{slug}/`, and read [SPEC.md](./SPEC.md) for what to fill and what
to leave open. [CUSTOMIZE.md](./CUSTOMIZE.md) binds the location and the ID
scheme for the whole loop.

## What it does

Assigns the next spec number, creates the folder, copies the template, and
fills the summary, problem, goals and non-goals from what was actually said.
Requirements it has no basis for stay as open rows, and the gaps become open
questions, each one addressed to a person. The spec leaves as a `draft`.

## Who uses it

- **Teams running coding agents against specs**, who need the spec in a shape
  an agent can find and plan from
- **Leads turning a conversation into work**, before it gets split into tickets
- **Anyone who has watched a plan confidently build the wrong thing** because
  the spec it came from filled its gaps with guesses

## Pairs with

[recover-spec](../recover-spec/SKILL.md) is the other way in, for code that
already runs. [plan-spec](../plan-spec/SKILL.md) is the next step once a person
marks the spec ready, then [implement-spec](../implement-spec/SKILL.md) builds
it and [review-spec](../review-spec/SKILL.md) checks it.

## What it will not do

It won't plan, write tasks, write code, or mark its own spec ready. It can't
tell a confident wrong answer from a right one. The Limitations section in
[SPEC.md](./SPEC.md) is the full list.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
