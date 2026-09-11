# Incident Triage: Specification

## System Purpose

Automate production incident triage by ingesting monitoring alerts, performing root-cause diagnosis, and routing to the appropriate response (file, fix, escalate, suppress). Prioritizes investigation over immediate code changes.

## Core Principle

**Diagnosis-first.** Most production alerts warrant careful investigation and tracked issues rather than reflexive code fixes. This skill enforces investigation rigor before committing to a remediation path.

---

## Architecture

### Input Contract

The skill accepts alerts from monitoring systems in a canonical event format:

```json
{
  "alert_id": "sentry-567",
  "exception_type": "ConnectionPoolExhausted",
  "exception_message": "No available connections",
  "stack_trace": [
    {"file": "handler.py", "line": 142, "function": "auth_check"},
    {"file": "db.py", "line": 89, "function": "get_connection"}
  ],
  "commit_sha": "7c3a9d2f",
  "release_tag": "v2.14.1",
  "environment": "prod",
  "event_count": 2847,
  "affected_users": 1234,
  "first_seen": "2024-01-15T10:15:00Z",
  "last_seen": "2024-01-15T10:30:45Z",
  "event_rate": "89 per minute",
  "user_context": {"session_id": "...", "user_id": "..."},
  "deployment_timestamp": "2024-01-15T10:00:00Z"
}
```

### Processing Stages

#### 1. Ingest & Validate
- Normalize alert from monitoring system into canonical structure
- Validate required fields present (exception, stack trace, commit, environment)
- Query repository for commit metadata (author, timestamp, diff)
- Fetch alert history to determine recurrence pattern

#### 2. Triage
- **Severity Classification:** Apply rules to map alert characteristics to Critical/High/Medium/Low
- **Recurrence Analysis:** New error, regression (was working), or chronic problem
- **Data Impact Assessment:** Does stack trace touch sensitive data (auth, payment, PII)?
- **Scope Estimation:** How many users, what systems affected, estimated business impact

#### 3. Investigation
- Trace stack frames to source files and line numbers
- Run git blame on topmost frame to identify introducing commit
- Query git log for recent changes in affected files
- Search existing issues and pull requests for related problems
- Measure fix complexity (code size, design changes, test coverage gaps)

#### 4. Decision Engine

Route alert to one of four outcomes:

**Fix:** Create a pull request with code change when all these hold:
- Stack trace pinpoints specific file and line number
- Fix is ≤ 50 lines of code
- Existing test suite covers the code path or fix includes new tests
- No architectural redesign required
- Safe to deploy without formal design review
- High confidence in root cause

**File:** Create a tracked GitHub/GitLab issue when:
- Root cause identified but fix requires design discussion
- Multiple possible causes need investigation
- Fix scope is unclear or likely > 50 lines
- Affects delivery timeline or cross-team coordination
- Requires team discussion before committing to solution

**Escalate:** Immediate notification to on-call and incident commander when:
- Data breach, auth bypass, or customer data exposure
- Critical customer-facing outage (> 10% user impact)
- Regulatory or contractual deadline at risk
- Requires incident commander coordination
- Requires executive notification per your escalation policy

**Suppress:** Close alert without action when:
- Matches known noise pattern with documented reason
- Expected behavior under high load (capacity issue, not defect)
- Vendor bug with upstream tracking and fix timeline
- Test/dev environment artifact, not production
- False positive from monitoring tool misconfiguration

#### 5. Execution
- Create pull request or GitHub/GitLab issue with full diagnosis attached
- Link monitoring alert to tracking system
- Post status update to team notification channel
- Record decision in audit journal with timestamp and reasoning
- Route notifications based on severity and escalation rules

### Output Modes

#### Interactive (Human Reader)

```
HIGH · issue-8901 · REGRESSION

Database Connection Pool Exhaustion
  Events: 2,847 · Affected Users: 1,234 · Window: 15 minutes
  Last 24 hours: This error appeared twice before (2024-01-14)

Root Cause
  handler.py:142 in auth_check()
  Introduced by commit 7c3a9d2 (2 hours ago)
  Author: jane.smith@example.com
  Change: Added synchronous database call in auth middleware

Evidence
  - Stack trace shows connection leak in db.get_connection()
  - Related issue #8887 (resolved 3 months ago) was same error
  - Deployment 2024-01-15 10:00:00 correlates with spike start
  - No recent connection pool config changes

Data Impact
  Customer session data not exposed (read-only operation)
  User experience degraded but no data loss

Decision: FILE
  Why: Multiple possible fixes (increase pool size, add retry logic,
  refactor to async). Requires team discussion.
  
  Suggested Owner: Backend team lead
  Next Steps: Create issue, assign to backend team, discuss approach
```

#### CI/Structured (Tooling Integration)

```json
{
  "issue_id": "sentry-567",
  "severity": "high",
  "recurrence": "regression",
  "data_incident": false,
  "notification_deadline": "2024-01-15T11:15:00Z",
  "root_cause": {
    "file": "handler.py",
    "line": 142,
    "commit_sha": "7c3a9d2f",
    "commit_author": "jane.smith@example.com",
    "confidence": "high"
  },
  "investigation": {
    "event_count": 2847,
    "affected_users": 1234,
    "recurrence_history": ["2024-01-14 13:30", "2024-01-14 18:45"],
    "related_issues": ["#8887"],
    "fix_complexity": "medium"
  },
  "decision": "file",
  "decision_reasoning": "Multiple possible solutions require team input",
  "fix_attempted": false,
  "artifacts": {
    "issue_url": "https://github.com/[org]/[repo]/issues/8901",
    "pr_url": null
  },
  "summary": "Connection pool exhaustion in auth middleware; requires design discussion"
}
```

### Severity Levels

| Level | User Impact | Data Risk | Response Deadline | Example |
|-------|------------|-----------|-------------------|----------|
| **Critical** | > 10% users, widespread outage | Auth fail, data breach | < 15 minutes | Unencrypted secrets exposed in logs |
| **High** | 1–10% users, significant degradation | Customer data at risk | < 1 hour | New error affecting 500+ events/min |
| **Medium** | < 1% users, isolated failure | No data risk | < 1 business day | Race condition affecting rare code path |
| **Low** | Dev/test only, no user impact | None | < 1 week | Linting warning, test environment artifact |

### Recurrence Classes

- **New:** First occurrence of this error type
- **Regression:** Error reappeared after being resolved
- **Chronic:** Recurring issue, known and unresolved

### Module Organization

```
incident-triage/
├── spec.md                         (this file)
├── README.md
├── CUSTOMIZE.md
├── triage/
│   ├── ingest.py                   (parse monitoring system JSON)
│   ├── classify.py                 (severity, recurrence, data impact)
│   ├── investigate.py              (git blame, related issues)
│   └── decide.py                   (route to fix/file/escalate/suppress)
├── output/
│   ├── format.py                   (human-readable report)
│   ├── json_output.py              (CI/structured JSON)
│   └── artifacts.py                (issue/PR generation)
├── config/
│   ├── severity-map.yaml           (classification rules)
│   ├── repository-map.yaml         (repo ownership, contacts)
│   └── exclusions.yaml             (known noise patterns)
├── integrations/
│   ├── sentry.py
│   ├── datadog.py
│   ├── cloudwatch.py
│   └── newrelic.py
├── api/
│   └── webhook.py                  (HTTP endpoint for alerts)
├── tests/
│   ├── fixtures/                   (sample alerts)
│   └── test_*.py
└── scripts/
    └── triage.sh                   (CLI entry point)
```

### Entry Points

**CLI:**
```bash
./triage.sh --alert-id <ID>           # Triage single alert
./triage.sh --alert-id <ID> --fix     # Attempt automated fix (budget: 2, ceiling 3)
./triage.sh --alert-id <ID> --file    # Create tracked issue
./triage.sh --audit --since 24h       # Review recent decisions
```

**Ingestion helper (ships in this folder):**
```bash
firewatch/scripts/sentry-fetch.sh PROJ-4F            # short id
firewatch/scripts/sentry-fetch.sh <issue-url>        # full URL
firewatch/scripts/sentry-fetch.sh <issue-id> --raw   # full objects
```

This is the one thing in this repository that actually executes. It pulls a
Sentry issue and its latest event and prints a triage-shaped JSON digest on
stdout, which is stage 1 of the pipeline above. It exists because MCP servers
are not available inside a CI runner: use your monitoring tool's MCP integration
interactively, and this in a pipeline.

Needs `curl` and `jq`, and `SENTRY_AUTH_TOKEN` with `event:read` and `org:read`.
`SENTRY_HOST` defaults to sentry.io, so set it for self-hosted. It reads the
token from the environment and never prints it.

Adapt it, or write the equivalent for Datadog, CloudWatch, or whatever you run.
Everything downstream only needs the digest shape.

**API:**
```
POST /triage
Content-Type: application/json
[event JSON payload]

Responses:
200 OK: {decision, artifacts, summary}
400 Bad Request: Missing required fields
```

**Webhook:**
```
GET /health
POST /webhook/sentry
POST /webhook/datadog
POST /webhook/cloudwatch
POST /webhook/newrelic
```

### Configuration Schemas

**severity-map.yaml**

Defines rules for classifying alerts. The skill evaluates each rule in order and assigns the highest matching severity.

```yaml
severity_rules:
  critical:
    - error_pattern: "OOM|OutOfMemory"
    - error_pattern: "auth.*denied|permission.*denied"
      environment: prod
    - error_pattern: "database.*connection.*failed"
      event_count: "> 1000"
      time_window: "5 minutes"
    - data_category: "PII"
      
  high:
    - event_frequency: "> 100 per minute"
    - affected_users: "> 100"
    - stack_contains: "payment|billing|charge"
    - recurrence: "regression"
      event_count: "> 50"
      
  medium:
    - recurrence: "new"
      affected_users: "> 10"
    - event_frequency: "> 10 per minute"
    - stack_trace_depth: "> 15 frames"
      
  low:
    - event_frequency: "< 1 per hour"
    - environment: "staging|dev"
    - stack_contains: "test_fixtures|mock"
```

**repository-map.yaml**

```yaml
defaults:
  incident_channel: "#incidents"
  escalation_timeout: "1 hour"

repositories:
  - name: backend-api
    github: myorg/backend
    branch: main
    owner: Backend Team
    on_call_service: pagerduty-backend
    contact_email: backend-team@example.com
    slack_channel: "#backend-incidents"
    environments: [prod, staging, dev]
    
  - name: mobile-client
    github: myorg/client-ios
    branch: main
    owner: Mobile Team
    on_call_service: pagerduty-mobile
    contact_email: mobile-team@example.com
    slack_channel: "#mobile-incidents"
    environments: [prod, staging]
```

**exclusions.yaml**

```yaml
suppressed_patterns:
  - id: vendor-lib-connection-leak-1234
    error_match: "^vendor_lib.*connection"
    reason: "Known issue in vendor_lib v1.2.3; fix available in v2.0"
    status: upstream
    tracked_at: "https://github.com/vendor/lib/issues/1234"
    
  - id: test-fixture-memory-spike
    stack_contains: "test_fixtures"
    environment: staging
    reason: "Test framework memory spike; not production issue"
    
  - id: expected-high-load-response-time
    error_match: "response.*timeout"
    event_threshold: "> 5000 per minute"
    reason: "Expected during load tests; will optimize connection pooling"
```

### Known Failure Modes

**Duplicate Alerts:** Same error fires multiple times within minutes. Configure alert deduplication by error signature (stack trace + exception type) to report once per hour or window. Group events by `alert_id` before triage.

**Git Blame Failures:** `git blame` fails when:
- File no longer exists (deleted in later commit): investigate from commit metadata instead
- Line number is out of range: fall back to file-level blame on the file itself
- Repository history is corrupted or shallow clone: mark finding as "unverified" and skip blame-based attribution

**Alert Storms:** When event frequency exceeds 10,000 per minute, sampling may occur. Triage reports the sampled result, not the true volume. Escalate all storms to on-call regardless of severity; let humans decide if it's a real outage or a monitoring system bug. Configure alert volume thresholds in `repository-map.yaml` to auto-escalate.

**Remediation:** Before auto-fixing, verify the alert is not a duplicate or storm artifact. Mark triage decisions on alerts known to be noise; the audit log separates signal from noise for post-mortems.

### Data Flow

```
Monitoring Alert (from Sentry/Datadog/CloudWatch)
    ↓
[Ingest & Normalize]
  ↓ Validate structure
  ↓ Query repository (git metadata)
  ↓ Fetch alert history
    ↓
[Classify]
  ↓ Severity (Critical/High/Medium/Low)
  ↓ Recurrence (new/regression/chronic)
  ↓ Data impact (sensitive data touched?)
    ↓
[Investigate]
  ↓ Git blame (who introduced this?)
  ↓ Related issues (seen this before?)
  ↓ Fix complexity (how hard to fix?)
    ↓
[Decide]
  ↓ Critical & data issue? → Escalate
  ↓ Known noise? → Suppress
  ↓ Small & testable? → Fix (if --fix flag)
  ↓ Otherwise → File issue
    ↓
[Execute & Artifact]
  ├→ Create PR (--fix)
  ├→ Create GitHub/GitLab issue (--file)
  ├→ Notify on-call (escalate)
  ├→ Close as suppressed
  └→ Record in audit journal
    ↓
[Output]
  └→ Interactive report OR JSON
```

### Integration Points

- **Monitoring webhook:** `POST /webhook/triage` (configurable monitoring system integrations)
- **Repository:** GitHub, GitLab (via CLI)
- **Tracking:** GitHub Issues, GitLab Issues
- **On-Call:** PagerDuty, OpsGenie
- **Notification:** Slack
- **Audit:** File-based or database (configurable)

---

## Hard Rules

Everything above describes what the system does. These say what it may not do,
and the difference matters. A Limitation is a note about scope that an agent
reads past. A hard rule is a boundary it does not cross. Where the two sections
overlap, this one governs.

1. **Never deploy.** No deploy scripts, no `terraform apply`, no infrastructure
   changes, in any mode. Triage produces a pull request at most. Something else
   ships it.
2. **Never push to a protected branch.** Feature branch and pull request, always,
   even when the fix is one line and obviously correct. A token scoped to block
   merges is not the same control as never pushing to the branch.
3. **Never resolve the tracker issue.** A deploy and a quiet error rate resolve an
   incident. Closing the ticket because a pull request opened is how an
   unverified fix gets recorded as a fix.
4. **Never put a raw event payload in a public artifact.** Redact user context,
   headers, and request bodies before anything reaches an issue, a comment, or a
   chat channel. The payload is where the personal data is, and an issue is
   forever.
5. **Never fix without a test.** If the failure cannot be reproduced in a test, it
   gets filed, not patched. The reproduction includes the revert check: confirm
   the test fails with the fix removed, then restore it. That check is what
   separates a regression test from a test that happens to be green.
6. **Never batch unrelated incidents.** One root cause, one issue. A batched issue
   gets half-fixed and closed.
7. **Never exceed the attempt budget.** See below.

---

## Decision Framework in Detail

### When to Automatically Fix

The skill creates a pull request only when all criteria pass:

1. **Confidence:** Root cause identified with high confidence (git blame clear, stack trace unambiguous)
2. **Scope:** Change ≤ 50 lines of code
3. **Testing:** Existing test suite has > 80% coverage on modified code path
4. **No redesign:** Solution requires no architectural changes or database migrations
5. **Safety:** Change does not affect security-sensitive code (auth, encryption, payment)
6. **Review:** No complex dependencies or coordination required

If any criterion fails, the skill files an issue instead and leaves the decision to the team.

### When to File Instead

Create a tracked issue for any of:
- Multiple possible root causes (investigation needed)
- Fix likely > 50 lines or requires refactoring
- Impacts cross-team workflow (coordination needed)
- Requires design discussion or RFC
- Affects third-party integrations
- Affects multiple services

### When to Abandon

**Two fix attempts by default. Three at the absolute most. Then stop and file.**

Each attempt must proceed from a **different hypothesis** about the cause. A
second attempt that adjusts the first patch is not a second attempt, it is the
same attempt continued, and it does not consume budget so much as waste it.

```yaml
fix:
  max_attempts: 2          # 3 is the ceiling, not a target
  require_distinct_hypothesis: true
  on_exhaustion: file      # never: keep_trying
```

There is no case where a fourth attempt is the right call. By then the diagnosis
is wrong, and further attempts compound a wrong diagnosis at cost: every one
spends tokens, CI minutes, and a reviewer's attention on a pull request that was
never going to land.

On exhaustion, file the issue and **record what was tried**. Three abandoned
hypotheses are genuinely useful to whoever picks it up, and they are lost if the
run reports only that it failed:

```
Filed after 2 attempts. Neither landed.

  1. Connection leak in db.get_connection()
     Refuted: pool metrics flat across the window
  2. Middleware ordering after commit 7c3a9d2
     Refuted: error predates that commit by 40 minutes

Next: the two obvious causes are out. This needs someone who knows why
the pool config differs between staging and prod.
```

An automated fixer with no cap does not fail loudly. It fails expensively and
quietly, and the first symptom is the bill.

### When to Escalate

Notify on-call immediately for:
- **Data incidents:** Customer PII, payment data, health information exposed
- **Critical outages:** > 10% user impact, widespread service degradation
- **Auth failures:** Login system, permission checks, session management compromised
- **Regulatory deadline:** SLA violation, contractual response time at risk
- **Severity: Critical** (by severity map classification)

### When to Suppress

Close without action when:
- Error matches known suppression rule with documented reason
- Expected behavior during high load (known scaling limit, planned optimization)
- Vendor bug with public tracking and ETA for upstream fix
- Test environment only (dev/staging with no production correlation)
- False positive from monitoring tool configuration

---

## Operational Modes

### Dry-Run Mode

**Flag:** `--dry-run`

**What it does:** Performs all analysis and decision-making without taking any action. Outputs the routing decision and artifacts that *would* be created, but does not:
- Create pull requests
- File issues
- Send notifications
- Update audit journals

**When to use:**
- First-time setup: verify the skill's routing matches your expectations
- Configuration changes: validate new severity rules or suppression patterns before enforcement
- Testing: safe way to process production alerts without side effects

**Example:**
```bash
./triage.sh --alert-id sentry-567 --dry-run --output json
```

Output shows the decision and hypothetical artifacts without committing them.

### Production Mode

**Default behavior** (no `--dry-run` flag): Executes the routing decision fully, creating artifacts and sending notifications as specified.

---

## Limitations & Non-Goals

This skill provides **triage and routing**, not automatic remediation:

- **No rollback:** Auto-fix PRs may be merged; the skill does not handle reversions if a fix is wrong
- **No runtime remediation:** Does not apply fixes to live systems; only creates code changes for deployment
- **No cross-alert correlation:** Analyzes each alert independently; does not detect multi-alert cascades
- **No ownership inference:** Routes based on `config/repository-map.yaml`; does not infer ownership from git history or CODEOWNERS
- **No customer communication:** Does not automatically notify customers; handles internal triage only
- **Shallow git analysis:** Does not correlate to feature flags, configuration deployments, or non-code changes

---

## Security & Credential Requirements

### Credentials Held

The skill requires authentication to:
- **Monitoring systems:** API keys for Sentry, Datadog, CloudWatch, etc. (read-only access sufficient)
- **Repository:** GitHub or GitLab token with repo read + issue creation + PR write (if `--fix` enabled)
- **On-Call routing:** PagerDuty or OpsGenie integration key (incident creation)
- **Notifications:** Slack webhook URL (message posting)

### Webhook Security

If running a webhook (`POST /webhook/*` endpoint):
- **Signature verification:** All incoming alerts must carry a valid HMAC signature (implementation-specific; see integration guides)
- **TLS only:** Webhook endpoint must be served over HTTPS with valid certificate
- **Rate limiting:** Endpoint should implement per-source rate limiting to prevent alert storms from exhausting resources
- **No PII in logs:** User context (`user_id`, `session_id`) may appear in the `user_context` field; audit logs must redact this if retention > 7 days

### Least Privilege

- **Monitoring read-only:** No credentials with write access needed
- **Repository:** If `--fix` is not used, a read-only token suffices (git blame, log queries only)
- **With `--fix`:** Requires PR creation but not merge permission (human approval required on the PR)

---

