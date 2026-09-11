#!/bin/bash
set -euo pipefail

# ─────────────────────────────────────────────────────────────────
# firewatch step 1: pull a Sentry issue + its latest event.
#
# Exists because MCP servers are not available in a CI runner. Use the
# Sentry MCP tools interactively; use this in GitHub Actions.
#
# Usage:
#   firewatch/scripts/sentry-fetch.sh PROJ-4F
#   firewatch/scripts/sentry-fetch.sh https://your-org.sentry.io/issues/1234567890/
#   firewatch/scripts/sentry-fetch.sh 1234567890 --raw
#
# Env:
#   SENTRY_AUTH_TOKEN  (required): token with event:read + org:read
#   SENTRY_ORG         (required unless the issue URL carries the org)
#   SENTRY_HOST        (optional): defaults to sentry.io; set for self-hosted
#
# Output: JSON on stdout, a triage-shaped digest by default, the full
# issue + event objects with --raw.
# ─────────────────────────────────────────────────────────────────

TARGET="${1:-}"
RAW=false
[[ "${2:-}" == "--raw" ]] && RAW=true

if [ -z "$TARGET" ]; then
  echo "Usage: $0 <sentry-url|short-id|issue-id> [--raw]" >&2
  exit 64
fi

for dep in curl jq; do
  command -v "$dep" >/dev/null 2>&1 || { echo "firewatch: $dep is required" >&2; exit 69; }
done

: "${SENTRY_AUTH_TOKEN:?firewatch: SENTRY_AUTH_TOKEN is not set}"
SENTRY_HOST="${SENTRY_HOST:-sentry.io}"
API="https://${SENTRY_HOST}/api/0"

api() {
  # $1 = path. Fails loudly on non-2xx so a bad token doesn't look like an empty issue.
  local body status
  body="$(curl -sS -w $'\n%{http_code}' \
    -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
    -H "Accept: application/json" \
    "${API}${1}")"
  status="$(tail -n1 <<<"$body")"
  body="$(sed '$d' <<<"$body")"
  if [[ "$status" != 2* ]]; then
    echo "firewatch: Sentry API ${1} returned HTTP ${status}" >&2
    echo "$body" >&2
    exit 70
  fi
  printf '%s' "$body"
}

# ── Resolve whatever we were handed into a numeric issue id ──────────
ISSUE_ID=""

if [[ "$TARGET" =~ ^https?:// ]]; then
  # .../issues/<id>/ , also picks up the org from <org>.sentry.io or /organizations/<org>/
  ISSUE_ID="$(sed -nE 's#.*/issues/([0-9]+).*#\1#p' <<<"$TARGET")"
  if [ -z "${SENTRY_ORG:-}" ]; then
    SENTRY_ORG="$(sed -nE 's#^https?://([^.]+)\.sentry\.io/.*#\1#p' <<<"$TARGET")"
    [ -z "$SENTRY_ORG" ] && SENTRY_ORG="$(sed -nE 's#.*/organizations/([^/]+)/.*#\1#p' <<<"$TARGET")"
  fi
  if [ -z "$ISSUE_ID" ]; then
    echo "firewatch: could not find an issue id in ${TARGET}" >&2
    exit 65
  fi
elif [[ "$TARGET" =~ ^[0-9]+$ ]]; then
  ISSUE_ID="$TARGET"
else
  # Short ID (PROJECT-4F). Needs the org to look up.
  : "${SENTRY_ORG:?firewatch: SENTRY_ORG is required to resolve a short id}"
  SHORT_UPPER="$(tr '[:lower:]' '[:upper:]' <<<"$TARGET")"
  ISSUE_ID="$(api "/organizations/${SENTRY_ORG}/shortids/${SHORT_UPPER}/" | jq -r '.groupId // empty')"
  if [ -z "$ISSUE_ID" ]; then
    echo "firewatch: short id ${SHORT_UPPER} did not resolve in org ${SENTRY_ORG}" >&2
    exit 65
  fi
fi

ISSUE="$(api "/issues/${ISSUE_ID}/")"
EVENT="$(api "/issues/${ISSUE_ID}/events/latest/")"

if $RAW; then
  jq -n --argjson issue "$ISSUE" --argjson event "$EVENT" \
    '{issue: $issue, event: $event}'
  exit 0
fi

# ── Triage digest ────────────────────────────────────────────────────
# Deliberately drops request bodies, headers, cookies, and user context.
# Those carry Client Personal Data under the DPA and must not flow into a
# GitHub issue. Use --raw only when reading locally, never in a CI artifact.
jq -n --argjson issue "$ISSUE" --argjson event "$EVENT" '
  def frames:
    ($event.entries // [])
    | map(select(.type == "exception"))
    | first
    | (.data.values // [])
    | map({
        type: .type,
        value: .value,
        frames: ((.stacktrace.frames // [])
                 | map(select(.inApp == true))
                 | map({file: .filename, line: .lineNo, function: .function})
                 | reverse | .[0:8])
      });

  {
    short_id:     $issue.shortId,
    issue_id:     $issue.id,
    permalink:    $issue.permalink,
    title:        $issue.title,
    culprit:      $issue.culprit,
    level:        $issue.level,
    status:       $issue.status,
    project:      $issue.project.slug,
    platform:     $issue.platform,
    event_count:  ($issue.count | tonumber? // $issue.count),
    user_count:   $issue.userCount,
    first_seen:   $issue.firstSeen,
    last_seen:    $issue.lastSeen,
    first_release: ($issue.firstRelease.shortVersion // null),
    last_release:  ($issue.lastRelease.shortVersion // null),
    environment:  (($event.tags // []) | map(select(.key == "environment")) | first | .value // null),
    release:      (($event.tags // []) | map(select(.key == "release")) | first | .value // null),
    server_name:  (($event.tags // []) | map(select(.key == "server_name")) | first | .value // null),
    substatus:    ($issue.substatus // null),
    is_regression: (($issue.substatus // "") == "regressed"),
    exceptions:   frames
  }
'
