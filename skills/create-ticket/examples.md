# Worked examples

Fourteen scenarios, each a real file in
[review-ticket/fixtures/](../review-ticket/fixtures/). They're the reference
material for what a ticket should look like, and they're also the checker's
regression suite, which CI runs on every pull request, so they can't quietly
rot into examples that no longer pass.

```bash
bash ../review-ticket/scripts/run-fixtures.sh
```

The bodies aren't reproduced here. Read the fixture.

| Scenario | Fixture | Mechanical verdict | What it shows |
|---|---|---|---|
| Vague feature idea | `01-vague.md` | FAIL | The failure mode, below |
| Well-defined feature | `02-well-defined.md` | PASS | The reference shape |
| Bug report | `03-bug.md` | PASS | Summary and Current/Expected instead of Objective and Why |
| Security issue | `04-security.md` | PASS | Enough to remediate, no exploit path |
| Infrastructure change | `05-infra.md` | PASS | Critical risk, irreversible, human approval on the apply |
| Technical debt | `06-tech-debt.md` | PASS | The end state plus what behaviour mustn't change |
| Research spike | `07-spike.md` | PASS | A decision as the deliverable, no implementation criteria |
| Unresolved decision | `08-blocked.md` | PASS, and BLOCKED on judgement | See below |
| Requires human approval | `09-human-approval.md` | PASS | What an agent may build against what it may run |
| Issue form submissions | `10-form-task.md`, `11-form-bug.md`, `12-form-spike.md` | PASS | Form labels normalise to the standard's sections (sample forms, not shipped) |
| Critical, approval says "None" | `13-critical-no-approval.md` | FAIL | A placeholder Human Approval counts as absent |
| Vague word inside a longer one | `14-word-boundaries.md` | PASS | "incorrectly" isn't "correctly" |

## The one that matters: mechanically clean, still not Ready

`08-blocked.md` passes every mechanical check. Its sections are present, its
acceptance criteria are flat and observable, its scope names an out. It's still
not Ready: the repo has no email, SMS or push provider, and the ticket asks for
a notification. The delivery channel is an unmade architectural decision, which
is Ready item 8, and item 8 is a `BLOCKED` verdict rather than a score
deduction.

That's the division of labour working. The checker doesn't fail here; it says
in its own output that it didn't attempt the judgement checks. `review-ticket`
reads the repo, finds no provider, and returns BLOCKED naming the decision.

The wrong response is to pick a provider so the ticket passes. That's the
invented context the standard forbids, and it turns an obvious stall into a
non-obvious wrong build.

## The failure mode, and the fix

Filed as:

```
Improve login.
```

Written out as `01-vague.md`, it still fails on five blocking defects. Expanding
a vague request into more words doesn't make it Ready, and the checker is
deliberately unimpressed by volume:

| Defect | Why it stops execution |
|---|---|
| Title is generic | Unidentifiable in a queue of forty issues |
| Objective is two words | Nothing says what would be true when it's done |
| Why is three words | A session with no history can't tell whether this matters |
| "Login works better" | Can't resolve to PASS or FAIL by observation |
| Scope names no out | Nothing stops this becoming a login redesign |

The objective's "improve" isn't one of the five. The checker bans vague verbs
only in requirements and acceptance criteria; an objective that names a
direction rather than a destination fails Ready item 1, which is judgement.

`02-well-defined.md` is the same underlying request after the questions were
asked. What changed: the objective states the security outcome rather than the
change, the acceptance criteria include the failure behaviour (a 401) and the
negative case (non-admin sessions unaffected), the constraints name a real
boundary (the refresh-token format other clients depend on) rather than a
preference, and the scope explicitly gives up the login screen redesign that
"improve login" was quietly inviting.

Notice what `02-well-defined.md` doesn't contain: nothing about test coverage,
structured logging, input validation, code review or CI. The repo's own rules
and PR template already require all of that. A ticket that restates them pays
tokens on every pass to say what was already true.
