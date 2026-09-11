# Setup Guide: Skill Quality Gates

> **This is for contributors to this repository, not for people using the skills.**
>
> If you want to *use* a skill, you do not need any of this. Read the skill's
> `SKILL.md`, then its `SPEC.md`, and adapt it via `CUSTOMIZE.md`. There is
> nothing to install and no API key to set. See the [README](README.md).
>
> Everything below wires up the review gate that runs when you edit a skill in
> this repo and commit the change.

## What actually gates a change

Two layers, and only one of them is a gate.

| Layer | Where | Skippable? |
|---|---|---|
| `scripts/validate-skills.sh` via `.github/workflows/validate.yml` | CI, on every push and pull request | **No** |
| The same script via `.githooks/pre-commit` | Your machine, before the commit | Yes: absent on a fresh clone, and `--no-verify` bypasses it |
| `.githooks/skill-review` via OpenRouter | Your machine, if you set it up | Yes, and it skips itself when the tool is absent |

**The rules live in one place**, `scripts/validate-skills.sh`. The hook and the
workflow both call it. Neither carries its own copy, because two copies of a
pattern list drift and the drift is silent.

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

The independent model review below is a separate, optional layer. It reads for
quality; the validator reads for the boundary. Neither substitutes for the other.

## 1. Install the Hook (optional, and not the gate)

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

## 2. Set Up OpenRouter Credentials

The skill-review tool calls Claude Opus 5 via OpenRouter (independent vendor, not Anthropic's servers). Get an API key:

1. Go to https://openrouter.ai/
2. Sign up or log in
3. Go to Settings → API Keys
4. Create a new key

Then store it locally (never in git):

```bash
# Option A: .env.local (recommended, gitignored)
echo "OPENROUTER_API_KEY=sk-or-your-key-here" > .env.local

# Option B: Environment variable (terminal only)
export OPENROUTER_API_KEY="sk-or-your-key-here"

# Verify it's set
echo $OPENROUTER_API_KEY
```

## 3. Test the Setup

Try committing a change to verify the hook runs:

```bash
# Make a small change
echo "# Test" >> bloodhound/SPEC.md

# Stage it
git add bloodhound/SPEC.md

# Commit (hook will run automatically)
git commit -m "test: hook verification"
```

If the hook is working, you'll see:

```
🔍 Reviewing 1 skill(s) before commit...
📋 Reviewing bloodhound...
🔄 Calling OpenRouter (anthropic/claude-opus-5)...
## 🔍 Skill Review: bloodhound

[Review output...]

✅ bloodhound passed review
✅ All skills passed review. Committing...
```

If review finds issues:

```
❌ bloodhound review failed
[Review output with findings...]

❌ 1 skill(s) failed review. Fix issues and try again.
Override with: git commit --no-verify (not recommended)
```

## 4. What the Hook Checks

The pre-commit hook runs Claude Opus 5 to review:

| Check | What It Catches |
|---|---|
| **Tone & Voice** | Company names, internal references, assumes Sanvio context |
| **Example Quality** | Examples tied to specific tools or Sanvio workflows |
| **Hidden Sanvio References** | Subtle language that flags as internal (Patrick's voice patterns, methodology terms) |
| **Strategy Leaks** | Hints at roadmap, internal decisions, unfinished thoughts |
| **Structure** | Missing sections, unclear progression, incomplete guidance |

## 5. Fixing Review Failures

When a skill fails review:

1. Read the feedback carefully: it names the exact sections and issues
2. Edit the skill's SPEC.md, CUSTOMIZE.md, or README.md to fix them
3. Re-stage your changes
4. Commit again: the hook runs again automatically

Example:

```bash
# Hook failed because SPEC.md mentions "Sanvio's rate card"
# Edit it
nano bloodhound/SPEC.md

# Replace "Sanvio's rate card" with "your organization's rate card"
# Stage and commit
git add bloodhound/SPEC.md
git commit -m "fix: genericize rate card reference in bloodhound SPEC"
```

## 6. Bypassing the Hook (Last Resort)

**Do not do this unless absolutely necessary.** The `--no-verify` flag skips all hooks:

```bash
git commit --no-verify -m "msg"
```

This:
- Bypasses the skill-review check
- Disables all other pre-commit hooks (secrets validation, etc.)
- Leaves you with zero safety net

**Only use if:**
- OpenRouter is down and blocking legitimate commits
- You are fixing a broken hook setup
- You explicitly need to bypass safety checks (rare)

Then fix the underlying issue and re-enable checks:

```bash
# After bypassing, git config core.hooksPath back
git config core.hooksPath .githooks
git log -1  # Verify what went in without review
```

## 7. Troubleshooting

**"skill-review command not found in PATH"**

The hook calls a `skill-review` command that this repository does not ship. It
is a thin wrapper that reads a skill directory, sends the files to OpenRouter,
and prints the response. You have to supply it.

The hook is written so that this is not fatal: with no `skill-review` on your
PATH the review step is skipped and the commit proceeds. If you want the gate,
write the wrapper and put it on your PATH under that name.

**"OPENROUTER_API_KEY not set"**

The hook is looking for OpenRouter credentials. Set them:

```bash
# In .env.local (easy, persists)
echo "OPENROUTER_API_KEY=sk-or-your-key-here" > .env.local

# Or in terminal (session only)
export OPENROUTER_API_KEY="sk-or-your-key-here"
```

**"No skills changed, passing"**

The hook only runs if you edited a skill directory. It doesn't block commits that touch README, docs, or non-skill files. To test the hook:

```bash
echo "# test" >> counsel/SPEC.md
git add counsel/SPEC.md
git commit -m "test hook"
```

**"OpenRouter rate limit or quota"**

If you hit OpenRouter's rate limits:
- Wait a few minutes before retrying
- Check your account usage at https://openrouter.ai/usage
- Upgrade your plan if needed

The hook will fail the commit and let you retry once limits reset.

## 8. What's Next

Once the hook is active:

1. All commits to this repo run skill-review automatically
2. Failing reviews block the commit
3. Skills can only reach `main` if they pass Claude Opus 5 review
4. Push to GitHub with confidence that every skill was validated locally first

---

**Questions?** Check the [README](README.md) for skill descriptions or run `skill-review --help` for the review tool's options.
