# Alert Triage

**Automate production incident response.** Ingest monitoring alerts, diagnose root cause, route to appropriate action: fix, file, escalate, or suppress.

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r triage-alert /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/triage-alert

or: "triage this alert and tell me whether to fix it or file it"
```

The agent reads [SPEC.md](./SPEC.md) and does the work. The `triage.sh` invocations in the spec are its
vocabulary for the four routes, not a script that ships here.

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly.
[CUSTOMIZE.md](./CUSTOMIZE.md) is where you set the thresholds and policy for
your stack.

## What It Does

When a production alert fires:

1. **Ingest**: Pull the error from your monitoring system (Sentry, Datadog, CloudWatch, New Relic)
2. **Diagnose**: Trace stack trace to code, find the introducing commit, classify severity and data impact
3. **Decide**: Route to fix (pull request), file (tracked issue), escalate (incident), or suppress (known noise)
4. **Act**: Create artifacts, notify team, update audit trail

**Core principle:** Most alerts warrant investigation before code changes. This skill enforces rigor.

---

## Quick Start

### Configure
```bash
cp config/repository-map.example.yaml config/repository-map.yaml
# Edit: add your repositories and on-call contacts

cp config/severity-map.example.yaml config/severity-map.yaml
# Edit: tune severity rules for your error patterns

cp config/exclusions.example.yaml config/exclusions.yaml
# Edit: add known noise patterns
```

### Try It
```bash
# Dry run: see decision without taking action
./triage.sh --alert-id sentry-567 --dry-run

# Triage a single alert from Sentry
./triage.sh --alert-id sentry-567

# Output JSON for CI/automation
./triage.sh --alert-id sentry-567 --output json

# File an issue without auto-fixing
./triage.sh --alert-id sentry-567 --file

# Attempt automated fix (only if small + testable)
# Budget: 2 attempts by default, 3 at the ceiling, each from a different
# hypothesis. Then it files and records what was tried.
./triage.sh --alert-id sentry-567 --fix
```

`--fix` is bounded on purpose. Read **When to Abandon** in [SPEC.md](./SPEC.md)
before raising the budget, and read **Hard Rules** before wiring this into
anything that runs unattended. The short version of the hard rules: it never
deploys, never pushes to a protected branch, never closes the tracker issue, and
never patches a failure it could not reproduce in a test.

---

## Common Tasks

| Task | Command |
|------|---------|
| Dry run (preview decision) | `./triage.sh --alert-id <ID> --dry-run` |
| Triage an alert | `./triage.sh --alert-id <ID>` |
| Get JSON output | `./triage.sh --alert-id <ID> --output json` |
| Create an issue | `./triage.sh --alert-id <ID> --file` |
| Auto-fix if safe | `./triage.sh --alert-id <ID> --fix` |
| Suppress known noise | `./triage.sh --alert-id <ID> --suppress` |
| Review decisions | `./triage.sh --audit --since 24h` |

---

## How It Works

### Severity Levels

| Level | User Impact | Data Risk | Response Deadline | Example |
|-------|------------|-----------|-------------------|----------|
| Critical | > 10% users, widespread outage | Auth fail, data breach | < 15 minutes | Secrets leaked to logs |
| High | 1–10% users, significant degradation | Customer data at risk | < 1 hour | 500+ errors/min, regression |
| Medium | < 1% users, isolated failure | No data risk | < 1 business day | Rare race condition |
| Low | Dev/test only, no user impact | None | < 1 week | Test environment leak |

### Decision Tree

```
Alert ingested
    ↓
Critical or data incident? → Escalate to on-call + incident commander
    ↓
Known suppression? → Close as expected behavior
    ↓
Small (< 50 lines) + fully tested? → Create PR (if --fix)
    ↓
Otherwise → Create tracked issue
```

### Output Examples

**Interactive (Human-Readable)**
```
HIGH · issue-8901 · REGRESSION

Connection Pool Exhaustion
  Events: 2,847 · Affected Users: 1,234

Root Cause
  handler.py:142: auth_check() method
  Introduced 2 hours ago (commit 7c3a9d2)
  Author: jane.smith@example.com

Decision: FILE
  Why: Multiple possible fixes require team input
```

**CI (JSON)**
```json
{
  "severity": "high",
  "decision": "file",
  "issue_url": "https://github.com/org/repo/issues/8901",
  "root_cause": {"file": "handler.py", "line": 142}
}
```

---

## Integration

### Webhook (Auto-Triage Alerts)

Point your monitoring system's webhook to:
```
POST https://your-domain.com/webhook/triage
```

The skill processes alerts automatically and posts decisions to Slack. Endpoint requires valid HMAC signature verification (see SPEC.md § Security).

### CI/CD Pipeline

Add to your deployment pipeline:
```yaml
- name: Check production alerts
  run: |
    ./triage.sh --check-alerts \
      --env prod \
      --output json > alerts.json
    # Fail if any Critical alerts unresolved
```

### Slack (Get Notifications)

1. Set `SLACK_WEBHOOK_URL` environment variable
2. Skill posts decisions to configured channels automatically
3. Include full diagnosis, suggested owner, and next steps

---

## Configuration

All configuration is in `config/` and is YAML-based:

- **`repository-map.yaml`**: Your repos, owners, on-call contacts
- **`severity-map.yaml`**: Severity classification rules
- **`exclusions.yaml`**: Known noise patterns to suppress

See `CUSTOMIZE.md` for detailed tuning instructions.

---

## Key Files

**`triage-alert/scripts/sentry-fetch.sh` is the only script this skill ships.** It
pulls a Sentry issue and its latest event and prints a triage-shaped JSON digest,
which is stage 1 of the pipeline. It needs `curl`, `jq`, and `SENTRY_AUTH_TOKEN`,
reads the token from the environment, and never prints it. Set `SENTRY_HOST` for
self-hosted.

```bash
triage-alert/scripts/sentry-fetch.sh PROJ-4F
```

It exists because MCP servers are not available inside a CI runner: use your
monitoring tool's integration interactively, and this in a pipeline. Adapt it, or
write the equivalent for Datadog or CloudWatch. Everything downstream only needs
the digest shape.

Everything else below is vocabulary from the spec, not files that ship:

| File | Purpose |
|------|---------|
| `./triage.sh` | CLI entry point |
| `triage/ingest.py` | Parse monitoring system JSON |
| `triage/classify.py` | Severity + recurrence classification |
| `triage/investigate.py` | Git blame, root cause tracing |
| `triage/decide.py` | Route to fix/file/escalate/suppress |
| `config/repository-map.yaml` | Repo ownership & on-call routing |
| `config/severity-map.yaml` | Severity rules |
| `config/exclusions.yaml` | Known noise patterns |

---

## Requirements

- Git (for blame/log queries)
- GitHub/GitLab CLI (`gh` or `glab`)
- Monitoring system API access (Sentry, Datadog, etc.)
- Python 3.9+ (or Node 16+ / Go 1.19+ depending on implementation)
- API keys: GitHub, monitoring system, Slack (optional)

---

## Troubleshooting

**Alert not parsing?** Check `triage/ingest.py`: you may need a custom parser for your monitoring system.

**Wrong severity?** Tune `config/severity-map.yaml` rules to match your error patterns.

**Too many auto-fixes?** Lower `MAX_FIX_SIZE` in `triage/decide.py` or remove `--fix` flag to require manual approval.

**Notifications not arriving?** Verify Slack webhook URL and GitHub CLI authentication.

For more, see `CUSTOMIZE.md`.
