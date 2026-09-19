# Adversarial Plan Interrogation: Customization Guide

## Before you start

The shipped behaviour is deliberately uncomfortable: whole-frontier rounds, a
recommendation attached to every question, and a session that does not end until
nothing is assumed. Adapt the shape; keep the discomfort, because that is the
part that finds the weak assumption.

## Customization 1: Round size

**Where it is used:** SPEC.md, *The round*.

The whole frontier in one round is the default. On a large tree that can be
fifteen questions, which some people read as an interrogation and others as
efficient.

```
Maximum questions per round:  <e.g. 7, then the rest next round>
If the frontier is larger:    <ask the highest-leverage first / split by area>
```

**If you skip it:** rounds are as large as the tree makes them.

## Customization 2: Tone and register

**Where it is used:** the whole session.

Say how direct this should be, because the useful version is more direct than
most internal writing:

```
Register:        <peer review / board challenge / pre-mortem>
Address:         <"you" / "the plan" / "we">
Recommendations: <always attached / only where you have a view>
```

**Never soften the question to protect the answer.** Softening is how a plan
survives the session unchanged.

**If you skip it:** the default is direct, with a recommendation on every
question.

## Customization 3: What counts as a settled decision

**Where it is used:** SPEC.md, *Between rounds*.

The frontier moves when a decision is settled. Define settled:

```
Settled means:   <the person stated it / it is written in the doc / someone with authority agreed>
Provisional:     <how a "probably" is tracked so it is revisited>
```

**If you skip it:** a hedged answer can settle a branch it should not.

## Customization 4: Fact-finding boundaries

**Where it is used:** SPEC.md, *Between rounds*.

Facts are found, not asked for. Name what this may inspect without checking
first:

```
Freely:          <the repository, public docs, the ticket tracker>
Ask first:       <production data, customer records, anything billed>
Never:           <whatever your policy forbids>
```

**If you skip it:** fact-finding is limited to what is obviously safe, and more
questions come back to you.

## Customization 5: The stopping rule

**Where it is used:** SPEC.md, *Stopping*.

An empty frontier is the default. Some teams stop earlier on purpose:

```
Stop when:  <frontier empty / the top three risks are named / a time box expires>
Output:     <nothing written / a list of the assumptions that changed / a decision record>
```

If you want an artifact, say so here: the skill produces none by default, and
that is deliberate, since writing the document becomes a substitute for
answering the questions.

**If you skip it:** it runs until the tree is exhausted.

## Customization 6: Who is in the room

**Where it is used:** the whole session.

- Is this one person, or a group answering together?
- Does anyone have a veto, and is that stated up front?
- Where do unresolved disagreements go?

**If you skip it:** it addresses whoever is typing, and a group session drifts
into a two-person conversation.

## Final checklist

- [ ] Round size, and what happens when the frontier is larger
- [ ] Register and whether recommendations are always attached
- [ ] What counts as settled, and how provisional answers are tracked
- [ ] Fact-finding boundaries: free, ask-first, never
- [ ] The stopping rule, and whether anything is written down
- [ ] Who answers, and where disagreement goes

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The trigger and what the session is |
| `SPEC.md` | The design tree, the frontier rule, the round format, limitations |
| `CUSTOMIZE.md` | This file: size, tone, boundaries, stopping |
