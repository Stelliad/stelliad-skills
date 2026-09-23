#!/usr/bin/env bash
set -uo pipefail

# Regression suite for review-ticket.py against the fixtures in ../fixtures.
#
#   bash scripts/run-fixtures.sh
#
# Each fixture has an expected mechanical verdict in fixtures/expected.json,
# and optionally a list of strings that must each appear in a BLOCKING line.
# Run this after any change to the checker or to a fixture. Needs only
# python3 (3.9 or later) and bash.

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="$(dirname "$HERE")"
FIXTURES="$SKILL/fixtures"
CHECKER="$HERE/review-ticket.py"
EXPECTED="$FIXTURES/expected.json"

fail=0
pass=0

# Read one field of one fixture's expectation. Paths go in as arguments, never
# spliced into the Python source, so a directory name with a quote in it works.
field() {
  python3 - "$EXPECTED" "$1" "$2" <<'PY'
import json, sys
path, name, key = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path) as handle:
    data = json.load(handle)
if name == "":
    print("\n".join(k for k in data if not k.startswith("_")))
elif key == "labels":
    print("\n".join(data[name].get("labels", [])))
elif key == "must_block":
    print("\n".join(data[name].get("must_block", [])))
else:
    print(data[name][key])
PY
}

names=$(field "" "")

while IFS= read -r name; do
  [ -z "$name" ] && continue
  # One value per call. A title has spaces in it, so never pack several values
  # into one line and re-split on whitespace.
  title=$(field "$name" title)
  expected=$(field "$name" verdict)
  # bash 3.2 on macOS has no mapfile, so build the argument array by hand.
  args=(--file "$FIXTURES/$name.md" --title "$title")
  while IFS= read -r label; do
    [ -n "$label" ] && args+=(--label "$label")
  done <<<"$(field "$name" labels)"

  out=$(python3 "$CHECKER" "${args[@]}" 2>&1)
  actual=$(printf '%s\n' "$out" | sed -n 's/^Mechanical verdict: //p')

  if [ "$actual" = "$expected" ]; then
    echo "  PASS  $name ($actual)"
    pass=$((pass + 1))
  else
    echo "  FAIL  $name: expected $expected, got ${actual:-<none>}"
    printf '%s\n' "$out" | sed 's/^/        /'
    fail=$((fail + 1))
  fi

  while IFS= read -r needle; do
    [ -z "$needle" ] && continue
    if ! printf '%s\n' "$out" | grep -q "^\[BLOCKING\].*$needle"; then
      echo "  FAIL  $name: no BLOCKING line mentioning '$needle'"
      fail=$((fail + 1))
    fi
  done <<<"$(field "$name" must_block)"
done <<<"$names"

echo
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
