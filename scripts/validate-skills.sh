#!/usr/bin/env bash
#
# The distribution boundary check. One copy of every pattern and rule, called
# from two places:
#
#   .githooks/pre-commit          --from-index  (what you are about to commit)
#   .github/workflows/validate.yml --from-worktree (what is actually on the branch)
#
# Keeping the rules here rather than in the hook is the point. A hook is
# client-side, needs a manual `git config core.hooksPath`, and dies to
# `--no-verify`. CI is the gate that actually holds. Neither should carry its
# own copy of the patterns, because the copies drift and the drift is silent.
#
# Usage:  validate-skills.sh [--from-index|--from-worktree] [file ...]
#         No files given means every tracked text file.

set -uo pipefail

MODE="--from-worktree"
case "${1:-}" in
  --from-index|--from-worktree) MODE="$1"; shift ;;
esac

RED=$'\033[0;31m'; YEL=$'\033[1;33m'; GRN=$'\033[0;32m'; DIM=$'\033[2m'; NC=$'\033[0m'
ERRORS=0
WARNINGS=0

fail() { printf '%s✗%s %s: %s\n' "$RED" "$NC" "$1" "$2"; [ -n "${3:-}" ] && printf '  %s%s%s\n' "$DIM" "$3" "$NC"; ERRORS=$((ERRORS+1)); }
warn() { printf '%s⚠%s %s: %s\n' "$YEL" "$NC" "$1" "$2"; WARNINGS=$((WARNINGS+1)); }

# Read one file the way this mode says to.
read_file() {
  if [ "$MODE" = "--from-index" ]; then git show ":$1" 2>/dev/null; else cat "$1" 2>/dev/null; fi
}

# bash 3.2 on macOS has no mapfile, and this has to run there and on CI.
FILES=()
if [ "$#" -gt 0 ]; then
  FILES=("$@")
else
  while IFS= read -r line; do FILES+=("$line"); done < <(git ls-files)
fi
[ "${#FILES[@]}" -eq 0 ] && { echo "No files to check."; exit 0; }

# ---------------------------------------------------------------------------
# 1. Strings that must never cross the distribution boundary.
#    Personal identifiers are deliberately absent: listing one here to block it
#    is one way of publishing it.
#
#    Everything in this repo ships to anyone, so it must read as written for no
#    org in particular.
# ---------------------------------------------------------------------------
BLOCKED=( "Sanvio Labs" "sanvio-twin" "company/legal" "company/business" "clients/" ".kiro/steering" ".kiro/skills" "__pycache__" )

# Files that enforce the blocked list necessarily quote it, so they match
# themselves. They are exempt from that sweep and from nothing else: a workflow
# file is a plausible place for a pasted token, and excluding it outright the
# way the rule scripts are excluded would stop the secret check reading the one
# file most likely to carry one.
carries_the_rules() {
  case "$1" in .github/workflows/validate.yml) return 0 ;; *) return 1 ;; esac
}

# Attribution, not content. The company name on a metadata author or source line
# says who wrote the skill, which is the point of publishing it.
ATTRIBUTION='^[[:space:]]*(author|source|homepage|copyright|maintainer):'

# ---------------------------------------------------------------------------
# 2. Secrets. A secret is a NAME BOUND TO A VALUE, never a name on its own.
#    Matching bare names stops documentation naming the variable to set, and the
#    workaround people reach for is a placeholder that reads as text and behaves
#    as code.
# ---------------------------------------------------------------------------
SECRETS=(
  "(API_KEY|api_key|SECRET|secret|TOKEN|token|PASSWORD|password)[[:space:]]*[=:][[:space:]]*['\"]?[A-Za-z0-9_/+.-]{12,}"
  "sk-[A-Za-z0-9]{16,}"
  "ghp_[A-Za-z0-9]{16,}"
  "AKIA[0-9A-Z]{16}"
  "BEGIN [A-Z ]*PRIVATE KEY"
)
PLACEHOLDER='([Yy]our|YOUR|[Xx]{3}|[Ee]xample|EXAMPLE|[Pp]laceholder|changeme|CHANGEME|sk-or-your|redacted|REDACTED)'

echo "Validating the distribution boundary..."

for f in "${FILES[@]}"; do
  [ -z "$f" ] && continue
  # The rule files themselves carry the patterns as documentation.
  case "$f" in
    .githooks/pre-commit|scripts/validate-skills.sh|LICENSE) continue ;;
    # A plugin manifest exists to say who publishes this and where it lives.
    # Naming the publisher is its whole job, so it cannot be held to "generic
    # for any org" the way a skill is. Excluded by path rather than by widening
    # ATTRIBUTION, because the JSON keys that would need allowing are `name`
    # and `description`, and allowing those everywhere lets a real leak through
    # on any frontmatter line.
    .claude-plugin/*.json) continue ;;
  esac
  [ "$MODE" = "--from-worktree" ] && [ ! -f "$f" ] && continue

  content="$(read_file "$f")"
  [ -z "$content" ] && continue
  # Skip binaries. Do not ask `file` whether this is text: macOS reports a
  # manifest as "JSON data" and Linux as "JSON text data", so a `grep -q text`
  # here skipped every JSON file on a developer's machine while CI checked it.
  # The hook passed and the branch failed, which is the worst way for two
  # copies of one rule to disagree.
  #
  # Test for a byte that cannot appear in text instead. Not $'\0': bash cannot
  # hold a NUL in a string, so that pattern is the empty string and matches
  # every file, skipping all of them and reporting Clean against nothing.
  if printf '%s' "$content" | LC_ALL=C grep -q '[^[:print:][:space:]]'; then
    continue
  fi

  if ! carries_the_rules "$f"; then
    for p in "${BLOCKED[@]}"; do
      if printf '%s' "$content" | grep -Ev "$ATTRIBUTION" | grep -qF "$p"; then
        fail "$f" "contains '$p'" "Generic for any org, or it does not ship."
      fi
    done
  fi

  for s in "${SECRETS[@]}"; do
    if printf '%s' "$content" | grep -Ev "$PLACEHOLDER" | grep -Eq "$s"; then
      fail "$f" "possible secret VALUE" "Naming a variable is fine. Committing its value is not."
    fi
  done

  case "$f" in
    *.md)
      # Em dashes. Repo convention since the first release: none anywhere.
      # An en dash in a numeric range is fine and is not matched here.
      if printf '%s' "$content" | grep -q '—'; then
        n=$(printf '%s' "$content" | grep -o '—' | wc -l | tr -d ' ')
        fail "$f" "$n em dash(es)" "Use a colon, a comma, or two sentences. En dashes in ranges are fine."
      fi

      # Invisible characters. Zero-width spaces get used to escape nested code
      # fences; they render correctly and hide text from a human reader but not
      # from a model. Four-backtick outer fences do the same job in the open.
      # BSD grep has no -P, so match the UTF-8 bytes directly. Covers
      # zero-width space, non-joiner, joiner, word joiner, and BOM.
      for zw in $'\xe2\x80\x8b' $'\xe2\x80\x8c' $'\xe2\x80\x8d' $'\xe2\x81\xa0' $'\xef\xbb\xbf'; do
        if printf '%s' "$content" | LC_ALL=C grep -qF "$zw"; then
          fail "$f" "invisible characters" "Zero-width or BOM. For nested fences use four backticks."
          break
        fi
      done

      # Unbalanced code fences swallow headings and tables into a literal block.
      fences=$(printf '%s\n' "$content" | grep -c '^```' || true)
      if [ $((fences % 2)) -ne 0 ]; then
        fail "$f" "unbalanced code fences ($fences)" "An odd count means a block never closes."
      fi

      # Local links that point at nothing. Strip fenced blocks and inline code
      # spans first: a link inside code is an example of what to write, not a
      # link, and flagging it teaches people to ignore the checker.
      prose=$(printf '%s\n' "$content" \
        | awk '/^```/{f=!f; next} !f' \
        | sed 's/`[^`]*`//g')

      while IFS= read -r target; do
        [ -z "$target" ] && continue
        case "$target" in http*|\#*|mailto:*) continue ;; esac
        base=$(dirname "$f"); clean="${target%%#*}"
        [ -z "$clean" ] && continue
        [ -e "$base/$clean" ] || fail "$f" "broken local link: $target"
      done < <(printf '%s' "$prose" | grep -oE '\]\([^)]+\)' | sed 's/^](//;s/)$//')
      ;;
  esac
done

# ---------------------------------------------------------------------------
# 3. Skill folder completeness. Every skill ships the same four files, and each
#    one's See Also points at the others. A folder missing one is a folder whose
#    cross-references are already broken.
# ---------------------------------------------------------------------------
# Skills live under skills/ because that is where the plugin runtime looks.
# Iterating */ instead would silently match nothing and report Clean.
for d in skills/*/; do
  d="${d%/}"
  [ -f "$d/SKILL.md" ] || continue
  for required in SKILL.md SPEC.md CUSTOMIZE.md README.md; do
    [ -f "$d/$required" ] || fail "$d" "missing $required" "Every skill ships all four."
  done
  for key in name description license; do
    head -20 "$d/SKILL.md" | grep -q "^$key:" || fail "$d/SKILL.md" "frontmatter missing '$key'"
  done
done

echo
if [ "$ERRORS" -gt 0 ]; then
  printf '%s%d error(s)%s' "$RED" "$ERRORS" "$NC"
  [ "$WARNINGS" -gt 0 ] && printf ', %d warning(s)' "$WARNINGS"
  printf '\n'
  exit 1
fi
if [ "$WARNINGS" -gt 0 ]; then printf '%s%d warning(s)%s\n' "$YEL" "$WARNINGS" "$NC"; fi
printf '%sClean%s\n' "$GRN" "$NC"
exit 0
