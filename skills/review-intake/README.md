# Review Intake

**Process code review feedback as a technical exchange: verify every item
against the codebase before it becomes a diff, and argue with the ones that are
wrong.**

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r review-intake /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/review-intake <pull request | path to review output | pasted findings>

or: "the reviewer left comments", "process this PR feedback",
    "the bot flagged these"
```

**Working by hand:** [SPEC.md](./SPEC.md) is the sequence and the disposition
table. [CUSTOMIZE.md](./CUSTOMIZE.md) binds your review tool's commands, your
escalation path and your bar for pushing back.

## What it does

Reads the whole set before reacting to any of it. Clarifies what is ambiguous
**before** touching a file, because items interact and a partial reading
produces a change that satisfies item 2 and contradicts item 5. Checks each item
against the actual code rather than against the reviewer's confidence. Gives
every item one of four dispositions: accept, accept with change, push back, out
of scope. Then implements one at a time, with a test each and a suite run
between.

The failure it prevents is the agreeable one: implementing a suggestion because
a reviewer made it. That ships regressions under a polite covering note, and it
gets worse as more of the review comes from tools with no context at all. Which
is why the rule runs the other way from instinct: **automated findings get more
scrutiny, not less.**

## Who uses it

- **Anyone running coding agents against review feedback**, where agreeableness
  is the default failure
- **Engineers on a review-heavy team**, who need every item dispositioned rather
  than most of them done
- **Leads who want the pushed-back items visible**, with the evidence attached

## Pairs with

`test-first` gives each accepted item its test, `verify-done` refuses the
"review addressed" claim without evidence, and `review-principles`,
`find-dead-code` and `coverage-gaps` are automated reviewers whose output
arrives here.

## What it will not do

It is downstream of the review, so it says nothing about the bug nobody looked
for. Its push-back procedure assumes you can decline an item and have that be
the end of it. And some items cannot be verified without access you do not have,
where saying so is the correct move and still leaves the item open. The
Limitations section in [SPEC.md](./SPEC.md) is the full list.

## Credit

Adapted from `receiving-code-review` in [obra/superpowers](https://github.com/obra/superpowers)
(MIT). Rewritten rather than vendored.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
