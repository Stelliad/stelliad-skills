# Ticket Creation: Customization Guide

## Before you start

Most of what you'd customize here lives in `review-ticket`, because the
standard does: labels, risk levels, section names and the checker all live in
[review-ticket/CUSTOMIZE.md](../review-ticket/CUSTOMIZE.md). Do that one first.
This file covers what's specific to writing and creating tickets.

## Customization 1: Your issue tracker

**Where it's used:** SKILL.md step 7, and *Splitting*.

The default is GitHub:

```bash
gh issue create --repo {owner/repo} --title "{title}" --body-file {path} --label "{labels}"
```

For another tracker, write the create command down here and the skill uses it
as given:

```
Create issue:     <CLI or API call taking title, markdown body, labels>
Link dependency:  <how "depends on" is recorded: a body line, a link type, a field>
Attach to parent: <sub-issue, epic link, parent field>
Body format:      <markdown, or the conversion your tracker needs>
```

Keep the "ask before creating" step whatever the tracker. The ticket is shown,
the human says yes, and only then does anything get created.

**If you skip it:** on a non-GitHub tracker the skill produces the finished
markdown ticket and stops, which is a fine place to stop.

## Customization 2: Where your repo's rules live

**Where it's used:** SKILL.md step 1.

The skill reads the repo's standards so it can leave them out of the ticket.
Tell it where they are if they're not in the obvious places:

```
Contributor guide:   <CONTRIBUTING.md, docs/engineering.md>
Agent rules:         <the rules file your coding agent reads>
PR template:         <.github/pull_request_template.md>
Project-level gate:  <required CI checks, or your runner's test command>
Specs:               <e.g. specs/{id}-{slug}/>
```

**If you skip it:** the skill looks in the usual places and may restate a rule
it didn't find.

## Customization 3: When work gets a spec instead of tickets

**Where it's used:** SKILL.md step 3.

Decide your threshold and write it as a sentence someone can apply: "anything
touching more than one service", "anything with more than about eight
acceptance criteria", "anything a customer will be told about". If your team
doesn't write specs, delete that row from the shape table and let big work
split into tickets.

**If you skip it:** the skill uses the standard's test, which is whether the
requirements need reviewing and tracing.

## Customization 4: What the skill may ask

**Where it's used:** SKILL.md *Rules*, and SPEC.md *Assumptions against
decisions*.

The default is to ask only about decisions that change architecture, security,
scope or product behaviour. If your team wants more questions (say, always
confirm priority) or fewer (never block, always record an assumption and flag
it), write the rule here. Be careful with fewer: an assumption about an
architectural choice is how a wrong build starts.

**If you skip it:** the default holds.

## Customization 5: The refinement cap

**Where it's used:** SKILL.md step 6.

Three passes through `review-ticket` is the default. At the cap, the skill
reports the remaining gaps and who owns them. Raise it only if your standard is
stricter than the shipped one; a ticket that fails three times is almost
always missing a fact, not a sentence.

**If you skip it:** three passes.

## Customization 6: Upstream drafts

If tickets reach you from somewhere else (meeting notes, a transcript, a form, a
support queue), have that step mark whatever its source can't supply as
`UNFILLED` rather than filling it by inference. The checker blocks on the
marker, and this skill's job becomes closing those gaps with a human rather than
guessing past them.

**If you skip it:** drafts arrive looking complete, and the gaps are hidden
inside plausible sentences.

## Final checklist

- [ ] `review-ticket` is installed beside this skill and customized first
- [ ] The create command for your tracker is written down, or you're happy
      stopping at markdown
- [ ] Your repo's rules, PR template and project gate are findable
- [ ] The spec threshold is a sentence someone can apply
- [ ] The question policy and refinement cap are set

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | Triggers and the procedure |
| `SPEC.md` | Why the steps are in that order, assumptions against decisions, limitations |
| `examples.md` | Twelve worked examples, which are `review-ticket`'s fixtures |
| `CUSTOMIZE.md` | This file |
| `../review-ticket/STANDARD.md` | The Ticket Authoring Standard, the one copy |
