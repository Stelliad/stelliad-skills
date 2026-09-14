# Setup Guide: Skill Quality Gates

**Last Updated: 2026-09-14 10:07**

> **This is for contributors to this repository, not for people using the skills.**
>
> If you want to *use* a skill, you do not need any of this. Read the skill's
> `SKILL.md`, then its `SPEC.md`, and adapt it via `CUSTOMIZE.md`. There is
> nothing to install and no API key to set. See the [README](README.md).
>
> Everything below wires up the checks that run when you edit a skill in this
> repo and commit the change.

## What actually gates a change

One layer is a gate. Everything else is a local convenience.

| Layer | Where | Skippable? |
|---|---|---|
| `scripts/validate-skills.sh` via `.github/workflows/validate.yml` | CI, on every push and pull request | **No** |
| The same script via `.githooks/pre-commit` | Your machine, before the commit | Yes: absent on a fresh clone, and `--no-verify` bypasses it |
| The main-branch guards in `.githooks/pre-commit` and `.githooks/pre-push` | Your machine, before a commit or push | Yes: one git config setting, or `--no-verify` |
| `scripts/skill-review` via `.githooks/pre-commit` | Your machine, **only if you turn it on** | Off by default |

**The boundary rules live in one place**, `scripts/validate-skills.sh`. The hook
and the workflow both call it. Neither carries its own copy, because two copies
of a pattern list drift and the drift is silent.

What it checks: strings that must not cross the distribution boundary, secret
values (a name bound to a value, never a bare name), em dashes, invisible
characters, unbalanced code fences, broken local links, and that every skill
folder ships all four files with valid frontmatter. CI adds a sweep of git
history for committed credentials, which the working-tree scan structurally
cannot see, and a check that every skill has a row in the root README.

Run it yourself any time:

```bash
bash scripts/validate-skills.sh              # everything tracked
bash scripts/validate-skills.sh path/to.md   # one file
```

## 1. Install the Hooks (optional, and not the gate)

```bash
git clone https://github.com/Stelliad/stelliad-skills.git
cd stelliad-skills
git config core.hooksPath .githooks
```

| Hook | What it does |
|---|---|
| `pre-commit` | Refuses a commit made directly on main, runs the boundary check, then the model review if you turned it on |
| `pre-push` | Refuses a push that would update this repository's main. A fork's own main is left alone |

**`core.hooksPath` replaces `.git/hooks` completely.** Anything you already had
in `.git/hooks/` stops firing once you set it, with no warning. If you keep
hooks of your own, point `core.hooksPath` at your own directory instead, and
have each of your hooks call the matching one here first:

```bash
#!/usr/bin/env bash
# pre-commit, in your own hooks directory
root=$(git rev-parse --show-toplevel)
"$root/.githooks/pre-commit" "$@" || exit $?
# then whatever else you want to run
```

## 2. Branching and Pull Requests

Changes reach main through a pull request. The `pre-commit` hook refuses a
commit made while main is checked out, because at that point the fix costs one
command and nothing is lost: staged changes follow you onto a new branch. The
`pre-push` hook refuses the other route, `git push origin HEAD:main`.

```bash
git switch -c fix/something-specific   # staged changes come along
git commit -m "fix: something specific"
git push -u origin fix/something-specific
gh pr create --fill
```

CI runs the boundary check on the pull request, and that is the gate that
actually holds. Finishing a conflicted merge, cherry-pick or revert on main is
allowed, since that commit concludes an operation git already started.

To work on main directly anyway, turn the guard off for this clone:

```bash
git config stelliad.allowMainCommits true
```

That setting lifts only the main-branch guards. `--no-verify` also gets past
them, but it skips every other hook too, including the boundary check and its
secrets scan, so keep it for a broken hook setup (see section 5).

## 3. Turn On the Model Review (optional)

`scripts/skill-review` asks a model to read a skill for the things a pattern
matcher cannot catch. It is **off until you name a backend** with
`SKILL_REVIEW_BACKEND`. Nothing is auto-detected: having Claude Code installed
or an API key in your shell is not a request for a billed review that can block
your commits.

**Option A: Anthropic API.** Claude Opus 5 on the Messages API.

```bash
export SKILL_REVIEW_BACKEND=anthropic
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**Option B: OpenRouter.** The same model through an independent reseller.

```bash
export SKILL_REVIEW_BACKEND=openrouter
export OPENROUTER_API_KEY="sk-or-your-key-here"
```

**Option C: Amazon Bedrock**, through the AWS CLI and whatever credential
chain you already have. There is no default model id: on Bedrock it is an
inference profile specific to your account and region. Find yours with
`aws bedrock list-inference-profiles`.

```bash
export SKILL_REVIEW_BACKEND=bedrock
export SKILL_REVIEW_BEDROCK_MODEL="the-inference-profile-id-for-your-account"
export AWS_REGION="us-east-1"   # only if your AWS profile has no region
```

**Option D: your local Claude Code**, using the login you already have.

```bash
export SKILL_REVIEW_BACKEND=claude
```

This runs `claude -p --restricted --strict-mcp-config --model claude-opus-5`
from an empty temporary
directory, so the review does not depend on who commits: your CLAUDE.md files,
your settings (and with them your hooks and plugins), and your MCP servers are
all left out, and the tools that run commands are removed. The review
instructions go in as the system prompt and the skill text as the message, the
same split the API backends make, so a file under review cannot pose as the
instructions. Set `SKILL_REVIEW_CLAUDE_CMD` to run something else, knowing that
you give up that isolation and that split: a custom command gets the
instructions and the skill text together on stdin.

**Timeouts.** Each review gives up after 300 seconds and counts as unable to
run. Change it with `SKILL_REVIEW_TIMEOUT`, which takes a positive whole number
of seconds. Zero is rejected rather than treated as "no limit".

**Where to put these.** Any of them can go in `.env.local` instead, as
`KEY=value` lines. A value wrapped in quotes and a leading `export` both work,
so a file you also `source` needs no changes, and a trailing `# comment` or
trailing whitespace is stripped rather than becoming part of the value. That
file is gitignored. The environment always wins over the file.

Check the wiring before you commit anything:

```bash
scripts/skill-review skills/plumb
```

## 4. What the Review Checks

Every text file in the skill folder is sent, not only the four core docs. Files
inside a dot-directory are left out, and anything that is not text is named on
stderr rather than dropped quietly. The model is asked for exactly five things:

| Check | What It Catches |
|---|---|
| **Tone & Voice** | Company names, internal references, anything assuming the reader is inside one organization |
| **Example Quality** | Examples tied to one company's specific tools or workflows instead of the general case |
| **Hidden Internal References** | Language that reads as an internal methodology term, one person's phrasing, or single-team jargon |
| **Strategy Leaks** | Hints at roadmap, internal decisions, unfinished thoughts that were not meant to ship |
| **Structure** | Missing sections, unclear progression, incomplete guidance |

In the hook, the review reads the staged version of each changed skill, the
same content the commit will take, not whatever is on disk. If that snapshot
cannot be made (no temp directory, or `git checkout-index` fails), the hook
prints a warning and reviews the working tree copy instead.

| Result | Exit | What the hook does |
|---|---|---|
| The whole response is the single line `Clean, ready for distribution` | 0 | Passes |
| Anything else | 1 | Blocks the commit and prints the findings |
| The review could not run this time (timeout, network, an API error) | 2 | Warns and lets the commit through |
| The review is misconfigured (unknown backend, missing key or dependency) | 3 | Blocks, because the next commit would fail the same way |

The pass condition is deliberately strict. A response that mentions the phrase
inside a sentence, or adds anything around it, is treated as a finding.

## 5. Bypassing the Hooks (Last Resort)

`--no-verify` skips every hook: the main-branch guards, the boundary check
including the secrets scan, and the review.

```bash
git commit --no-verify -m "msg"
```

CI still runs the boundary check on the pull request, so this buys you a later
failure, not a pass. Use it for a broken hook setup, not to get past a finding.

## 6. Troubleshooting

**Nothing happened when I committed a skill change.** Either
`git config core.hooksPath` is not `.githooks`, or `SKILL_REVIEW_BACKEND` is
not set. The review is silent when it is off.

**"timed out after 300s".** The backend did not answer in time. Retry, or raise
`SKILL_REVIEW_TIMEOUT`.

**"Not logged in" with the `claude` backend.** Log in to Claude Code
interactively once, or set `ANTHROPIC_API_KEY`.

**"set SKILL_REVIEW_BEDROCK_MODEL".** The Bedrock backend has no default model
id on purpose. See option C.

**"curl is required" or "jq is required".** The three API backends need both.
The `claude` backend needs neither.

**A skill I believe is clean keeps failing.** Read the output: the model added
text around the verdict, or found something real. If you set
`SKILL_REVIEW_CLAUDE_CMD`, check that it still runs isolated from your own
configuration.
