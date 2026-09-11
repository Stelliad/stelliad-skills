# Setup Guide: Skill Quality Gates

**Last Updated: 2026-09-11 15:32**

> **This is for contributors to this repository, not for people using the skills.**
>
> If you want to *use* a skill, you do not need any of this. Read the skill's
> `SKILL.md`, then its `SPEC.md`, and adapt it via `CUSTOMIZE.md`. There is
> nothing to install and no API key to set. See the [README](README.md).
>
> Everything below wires up the checks that run when you edit a skill in this
> repo and commit the change.

## What actually gates a change

Two layers, and only one of them is a gate.

| Layer | Where | Skippable? |
|---|---|---|
| `scripts/validate-skills.sh` via `.github/workflows/validate.yml` | CI, on every push and pull request | **No** |
| The same script via `.githooks/pre-commit` | Your machine, before the commit | Yes: absent on a fresh clone, and `--no-verify` bypasses it |
| `scripts/skill-review` via `.githooks/pre-commit` | Your machine, if a review backend is configured | Yes, and it skips itself with a warning when none is |
| The commit-on-main guard in `.githooks/pre-commit` | Your machine, before the commit | Yes: one git config setting, or `--no-verify` |

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

The model review below is a separate, optional layer. It reads for quality; the
validator reads for the boundary. Neither substitutes for the other.

## 1. Install the Hooks (optional, and not the gate)

```bash
# Clone the repo (if not done)
git clone https://github.com/Stelliad/stelliad-skills.git
cd stelliad-skills

# Tell git to use .githooks directory
git config core.hooksPath .githooks

# Verify it worked
git config core.hooksPath
# Should print: .githooks
```

That one setting turns on everything in `.githooks/`:

| Hook | What it does |
|---|---|
| `pre-commit` | Refuses a commit made directly on main, then runs the boundary check and the model review |
| `post-commit`, `post-merge`, `post-checkout` | Nothing on their own. They exist so a personal hook can run; see section 3 |

**`core.hooksPath` replaces `.git/hooks` completely.** Anything you already had
in `.git/hooks/` stops firing the moment you set it, with no warning. That is
the reason the `post-*` hooks above exist at all.

## 2. Branching and Pull Requests

Changes reach main through a pull request. The `pre-commit` hook refuses a
commit made while main is checked out, because at that point the fix costs one
command and nothing is lost: staged changes follow you onto a new branch.

```bash
git switch -c fix/something-specific   # staged changes come along
git add ...
git commit -m "fix: something specific"
git push -u origin fix/something-specific
gh pr create --fill
```

CI runs the boundary check on the pull request, and that is the gate that
actually holds. After the pull request merges:

```bash
git switch main
git pull
```

To commit on main anyway, either once or for good:

```bash
git commit --no-verify                     # this commit only
git config stelliad.allowMainCommits true  # this clone, permanently
```

## 3. Personal Hooks (optional)

Anything executable at `.githooks/local/<hook-name>` runs when the matching
tracked hook fires, and receives the same arguments. `.githooks/local/` is
gitignored, so machine-specific wiring never ships to anyone who clones this
repo. A personal hook that exits non-zero prints a note and is otherwise
ignored: it runs after the fact, and the repository has no stake in whether it
worked.

The case this was built for is a maintainer who has this checkout registered as
a local plugin marketplace. An install pins a commit and copies the tree into
the plugin cache, so the skills Claude Code loads keep reflecting whatever was
there at install time until something reinstalls them. A
`.githooks/local/post-commit` closes that gap:

```bash
#!/bin/zsh
# .githooks/local/post-commit  (gitignored)
source ~/.zsh_extensions/.zsh_claude_code
cld-plugin-reset stelliad stelliad && echo "stelliad plugin reset"
```

The same script as `post-merge` and `post-checkout` keeps the installed copy
tracking whatever you have checked out: your branch while you work on it, main
again once the pull request lands and you pull. `post-checkout` only fires on a
real branch switch, never on a file checkout.

## 4. Configure a Review Backend

`scripts/skill-review` ships in this repo, but it needs a model behind it. Four
backends are supported so that no single vendor account is a prerequisite for
contributing. Configure whichever one you already have.

With `SKILL_REVIEW_BACKEND` unset, the script picks the first configured
backend in the order below and prints which one it chose. Set the variable to
pin a specific one.

**Option A: Anthropic API.** Claude Opus 5 on the Messages API.

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
export SKILL_REVIEW_BACKEND=anthropic   # optional, this is auto-detected
```

**Option B: OpenRouter.** The same model through an independent reseller, which
is useful if your billing already lives there. Create a key under Settings then
API Keys at https://openrouter.ai/.

```bash
export OPENROUTER_API_KEY="sk-or-your-key-here"
export SKILL_REVIEW_BACKEND=openrouter  # optional, this is auto-detected
```

**Option C: Amazon Bedrock.** Goes through the AWS CLI, so it uses whatever
credential chain and profile you already have. There is no default model id:
on Bedrock the id is an inference profile specific to your account and region,
so you have to supply it.

```bash
export SKILL_REVIEW_BEDROCK_MODEL="the-inference-profile-id-for-your-account"
export AWS_REGION="us-east-1"           # only if your AWS profile has no region
export SKILL_REVIEW_BACKEND=bedrock     # optional, this is auto-detected
```

Find the id with `aws bedrock list-inference-profiles` and pick the Claude model
your account is entitled to. Requires `aws` and `jq`.

**Option D: your local Claude Code (`claude -p`).** No account of any kind here,
no API key in this repo, and nothing leaves your machine beyond whatever that
CLI is already configured to talk to (which is how Bedrock users usually want to
run this).

```bash
export SKILL_REVIEW_BACKEND=claude
```

By default this runs `claude -p`. Point `SKILL_REVIEW_CLAUDE_CMD` at something
else if you want a different local command:

```bash
export SKILL_REVIEW_CLAUDE_CMD="claude -p --model opus"
```

**Where to put these.** Any of them can go in `.env.local` instead, as plain
`KEY=value` lines with no quoting. That file is gitignored. The environment
always wins over the file, so an `export` in your shell profile overrides it.

```bash
cat > .env.local <<'ENV'
SKILL_REVIEW_BACKEND=claude
ENV
```

Run the tool directly to check the wiring before you commit anything:

```bash
scripts/skill-review skills/plumb
```

## 5. Test the Setup

Try committing a change to verify the hook runs:

```bash
# Make a small change
echo "# Test" >> skills/bloodhound/SPEC.md

# Stage it
git add skills/bloodhound/SPEC.md

# Commit (hook will run automatically)
git commit -m "test: hook verification"
```

If the hook is working, you'll see the boundary check, then:

```
Reviewing 1 skill(s) before commit...

Reviewing skills/bloodhound...
Backend: anthropic (auto). Pin it with SKILL_REVIEW_BACKEND.
Calling the Anthropic Messages API (claude-opus-5)...
Clean, ready for distribution
skills/bloodhound passed review

1 skill(s) passed review, 0 skipped.
```

If review finds issues:

```
skills/bloodhound review failed
[findings, one bullet per issue]

1 skill(s) failed review. Fix the findings and commit again.
Override with: git commit --no-verify (not recommended)
```

## 6. What the Review Checks

The review asks the model for five things, and nothing else:

| Check | What It Catches |
|---|---|
| **Tone & Voice** | Company names, internal references, anything assuming the reader is inside one organization |
| **Example Quality** | Examples tied to one company's specific tools or workflows instead of the general case |
| **Hidden Internal References** | Language that reads as an internal methodology term, one person's phrasing, or single-team jargon |
| **Strategy Leaks** | Hints at roadmap, internal decisions, unfinished thoughts that were not meant to ship |
| **Structure** | Missing sections, unclear progression, incomplete guidance |

A clean review returns one line, `Clean, ready for distribution`, and the script
exits 0. Anything else exits 1 and the hook blocks the commit. A backend that
could not run at all exits 2, and the hook warns and lets the commit through:
trouble with your own network or credentials should never be the reason
`--no-verify` starts feeling routine.

## 7. Fixing Review Failures

When a skill fails review:

1. Read the feedback carefully: it names the exact file and section
2. Edit the skill's SPEC.md, CUSTOMIZE.md, or README.md to fix them
3. Re-stage your changes
4. Commit again: the hook runs again automatically

Example:

```bash
# Review flagged that SPEC.md names a specific company's rate card
nano skills/bloodhound/SPEC.md

# Replace it with "your organization's rate card", then stage and commit
git add skills/bloodhound/SPEC.md
git commit -m "fix: genericize rate card reference in bloodhound SPEC"
```

## 8. Bypassing the Hook (Last Resort)

**Do not do this unless absolutely necessary.** The `--no-verify` flag skips all hooks:

```bash
git commit --no-verify -m "msg"
```

This:
- Bypasses the commit-on-main guard
- Bypasses the skill review
- Bypasses the local boundary check, including the secrets scan
- Leaves you with no local safety net at all

CI still runs the boundary check on push, so `--no-verify` buys you a later
failure, not a pass.

**Only use if:**
- Your review backend is down and blocking a legitimate commit, and the warning
  path did not already let you through
- You are fixing a broken hook setup

Then check what went in without review:

```bash
git log -1
bash scripts/validate-skills.sh
```

## 9. Troubleshooting

**"no review backend is configured"**

None of the four options in section 4 are set. Configure one, or accept that the
review layer is off: the hook treats an unrunnable review as a warning and lets
the commit proceed.

**"scripts/skill-review missing or not executable, skipping review"**

The script ships in the repo, so this should not happen on a normal checkout.
Check that the file exists and its executable bit survived:

```bash
chmod +x scripts/skill-review
```

**"set SKILL_REVIEW_BEDROCK_MODEL ..."**

The Bedrock backend has no default model id on purpose. List what your account
can reach and export one:

```bash
aws bedrock list-inference-profiles
```

**"curl required" or "jq required"**

The three API backends parse JSON with `jq` and call out with `curl`. Install
both, or use the `claude` backend, which needs neither.

**No review ran and the commit went straight through**

The review only runs when you staged a change under `skills/`. Commits touching
the README, docs, or scripts skip it. To exercise it:

```bash
echo "# test" >> skills/counsel/SPEC.md
git add skills/counsel/SPEC.md
git commit -m "test hook"
```

**Rate limits or quota**

Wait for the window to reset, or switch backends for the commit:

```bash
SKILL_REVIEW_BACKEND=claude git commit -m "msg"
```

## 10. What's Next

Once the hook is active:

1. Work happens on a branch, and main moves only through a pull request
2. Every commit that touches a skill runs the boundary check and the review
3. A review that finds something blocks the commit
4. CI re-runs the boundary check on the pull request, and that one cannot be skipped

---

**Questions?** Check the [README](README.md) for skill descriptions, or run
`scripts/skill-review --help` for the review tool's options.
