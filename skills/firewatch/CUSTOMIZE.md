# Incident Triage: Customization Guide

> **There is no firewatch binary.** This skill is a specification an agent
> executes. The config below is real: you create it, and the agent reads it.
> The `triage.sh` invocations in this guide are the spec's vocabulary for the
> options, not something on your PATH and not a package to install.
> See [README.md](./README.md) for how to invoke it.

## What to Customize

This skill ships with generic defaults. Adapt it to your systems, error patterns, and team structure using the customization points below.

---

## 1. Alert Ingestion Format

**What it is:** How to parse your monitoring system's alert JSON.

**Where it lives:** `triage/ingest.py`

**To customize:**

Edit the `parse_alert()` function to map your monitoring system's JSON schema to the canonical event structure:

```python
def parse_sentry(payload):
    # Sentry sends different fields than Datadog
    # Map them to canonical format
    return {
        'alert_id': payload['id'],
        'exception_type': payload['exception']['type'],
        'exception_message': payload['exception']['value'],
        'stack_trace': parse_stacktrace(payload['stackTrace']),
        'commit_sha': payload.get('release'),
        'environment': payload.get('environment', 'prod'),
        'event_count': payload['stats']['total'],
        'affected_users': payload.get('user_count', 0),
        'first_seen': payload['firstSeen'],
        'last_seen': payload['lastSeen'],
    }

def parse_datadog(payload):
    # Datadog alert structure is different
    # This returns the same canonical format
    return {
        'alert_id': payload['alert_id'],
        'exception_type': payload['error_type'],
        'exception_message': payload['message'],
        # ... rest of mapping
    }
```

**How to know it works:** Test with an actual alert from your monitoring system and verify all fields populate.

**Supported systems (examples provided):**
- Sentry (SaaS error tracking)
- Datadog (monitoring + APM)
- CloudWatch (AWS logs + metrics)
- New Relic (APM + monitoring)
- Custom JSON webhook

---

## 2. Repository Configuration

**What it is:** Mapping your repositories to ownership, on-call contacts, and escalation paths.

**Where it lives:** `config/repository-map.yaml`

**To customize:**

```yaml
repositories:
  - name: api-backend
    github: yourorg/api
    branch: main
    owner: Platform Team
    on_call_service: pagerduty-api      # PagerDuty service name
    contact_email: platform@example.com
    slack_channel: "#platform-incidents"
    slack_escalation_to: "@platform-lead"   # Slack handle for escalation
    
  - name: web-frontend
    github: yourorg/web
    branch: main
    owner: Frontend Team
    on_call_service: pagerduty-web
    contact_email: frontend@example.com
    slack_channel: "#frontend-incidents"
    slack_escalation_to: "@frontend-lead"
```

**Questions to answer:**
- What repositories does your company maintain?
- Who owns each one (team name)?
- Do you have PagerDuty service IDs for on-call routing?
- Which Slack channel should incidents post to?
- Who should be escalated to for critical issues?

---

## 3. Severity Classification Rules

**What it is:** How to classify alerts into Critical/High/Medium/Low based on your error patterns.

**Where it lives:** `config/severity-map.yaml`

**To customize:**

Start with these questions, then update your rules accordingly:

**Q: What error types are always Critical?**

Add them to `critical` rules:
```yaml
severity_rules:
  critical:
    - error_pattern: "OOM|OutOfMemory"
    - error_pattern: "auth.*failed|permission.*denied"
    - error_pattern: "database.*corruption"
```

**Q: What user-impact threshold triggers High severity?**

```yaml
  high:
    - affected_users: "> 100"
    - event_frequency: "> 100 per minute"
```

**Q: Do your production and staging environments have different rules?**

Yes. Staging environment errors should generally be lower severity:
```yaml
  low:
    - environment: staging
    - environment: dev
```

**Q: Are there errors that are always Low even if frequent?**

```yaml
  low:
    - stack_contains: "test_fixtures"  # Test code, not production
    - error_pattern: "cache.*miss"      # Expected and harmless
```

**Validation:** Run the skill on 10 recent real alerts and verify the assigned severity matches your intuition. Adjust rules if most are being classified incorrectly.

---

## 4. Known Noise & Suppressions

**What it is:** Alerts you want to acknowledge but not act on (vendor bugs, test leaks, expected behavior).

**Where it lives:** `config/exclusions.yaml`

**To customize:**

**Known vendor bug example:**
```yaml
suppressed_patterns:
  - id: postgres-connection-idle-leak
    error_match: "^idle.*connection"
    stack_contains: "postgres.*client"
    reason: "PostgreSQL driver v1.3 known leak; fixed in vX.Y upstream"
    tracked_at: "https://github.com/vendor/postgres-driver/issues/456"
```

**Test environment false positive:**
```yaml
  - id: test-memory-spike
    stack_contains: "test_fixtures|conftest"
    environment: staging
    reason: "Test framework allocates large dataset; not production"
```

**Expected high-load behavior:**
```yaml
  - id: connection-pool-exhaustion-under-load
    error_pattern: "no.*available.*connection"
    event_frequency: "> 5000 per minute"
    reason: "Planned capacity upgrade; current limit is 1000 concurrent users"
```

**Build up your list incrementally:** Start empty. As patterns emerge in production, add suppressions for known noise rather than leaving them to alert repeatedly.

---

## 5. Decision Logic Thresholds

**What it is:** When to auto-fix vs. file an issue.

**Where it lives:** `triage/decide.py`

**To customize:**

Edit these thresholds based on your risk tolerance:

```python
# Max lines of code to auto-fix
MAX_FIX_SIZE = 50  # Increase to 100 if confident, decrease to 30 if conservative

# Min test coverage required for auto-fix
MIN_TEST_COVERAGE = 80  # Percent of modified code

# Auto-fix only in these environments
AUTO_FIX_ENVS = ["prod"]  # Remove "staging" if too risky

# Never auto-fix security-sensitive code paths
NO_AUTO_FIX_PATTERNS = [
    "auth", "payment", "encryption", "secret", "credential"
]

# Auto-escalate if unresolved after this duration
ESCALATION_TIMEOUT = "1 hour"

# The attempt budget. See "When to Abandon" in SPEC.md.
# Every threshold above decides WHETHER to try. This one decides when to STOP,
# and it is the only one whose absence costs money rather than risk.
MAX_FIX_ATTEMPTS = 2            # 3 is the ceiling, not a target
REQUIRE_DISTINCT_HYPOTHESIS = True   # attempt 2 must not be attempt 1 adjusted
ON_EXHAUSTION = "file"          # never "keep_trying"
```

**Safe defaults:** Start conservative (MAX_FIX_SIZE=30, require --fix flag). Increase thresholds only after observing 10+ successful auto-fixes.

**Do not raise `MAX_FIX_ATTEMPTS` above 3.** The other thresholds trade risk
against convenience and are yours to tune. This one is different: past the third
attempt the diagnosis is wrong, and each further attempt spends tokens, CI
minutes, and a reviewer's attention on a pull request that was never going to
land. An automated fixer with no cap does not fail loudly. It fails expensively
and quietly, and the first symptom is the bill.

---

## 6. Data Sensitivity Mappings

**What it is:** Which error paths handle regulated or sensitive data and should trigger escalation.

**Where it lives:** `triage/classify.py`

**To customize:**

Update the data sensitivity checker:

```python
SENSITIVE_DATA_PATTERNS = {
    'PII': [r'user.*email', r'phone.*number', r'ssn|tax_id'],
    'Payment': [r'credit.*card|payment.*method|stripe|payment_token'],
    'Health': [r'medical|diagnosis|prescription|ehr'],
    'Auth': [r'password|oauth.*token|session.*secret'],
}

# If error stack trace contains code from these paths, mark as data incident
SENSITIVE_MODULES = [
    'payment/stripe.py',
    'auth/session.py',
    'user/profile.py',
]
```

**Questions to answer:**
- What data categories does your system handle?
- Which are regulated (GDPR/PII, HIPAA/health, PCI-DSS/payment)?
- Which code modules process sensitive data?
- Should data incidents always escalate to security team, or just on-call?

---

## 7. Notification Channels & Routing

**What it is:** Where alerts should post based on severity and team.

**Where it lives:** `config/repository-map.yaml` (per-team routing) + environment variables (API keys)

**To customize:**

**Set up Slack integration:**
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

**Configure per-team Slack channels in repository-map.yaml:**
```yaml
repositories:
  - name: api-backend
    slack_channel: "#backend-incidents"
    slack_escalation_to: "@on-call-backend"
```

**Set up PagerDuty integration (optional):**
```bash
export PAGERDUTY_ROUTING_KEY="<your-integration-key>"
```

The skill will check `repository-map.yaml` for the on-call service name and create an incident in PagerDuty if severity >= High.

---

## 8. Audit & Compliance

**What it is:** Recording every triage decision for audit trail and post-mortem analysis.

**Where it lives:** `config/audit.yaml` (path configuration)

**To customize:**

**File-based audit log:**
```yaml
audit:
  storage: file
  path: /var/log/incident-triage/audit.jsonl
  retention_days: 90
```

**Database audit log (for larger volumes):**
```yaml
audit:
  storage: postgresql
  connection_string: "postgresql://user:pass@localhost/audit_db"
  table: incident_decisions
  retention_days: 365
```

**What gets logged:** Every decision, reasoning, and artifacts created. Use for:
- Post-mortem analysis (why did this get suppressed?)
- Metrics (what fraction of alerts are fixed vs. filed?)
- Compliance (prove all critical incidents were escalated)

---

## Customization Checklist

- [ ] Monitoring system integration tested (your alerts parse correctly)
- [ ] repository-map.yaml created (all repos listed, correct owners, valid contacts)
- [ ] Severity rules tuned (run skill on 10 recent alerts, verify classifications match intuition)
- [ ] Exclusions list started (identify 5-10 known noise patterns)
- [ ] Decision thresholds reviewed (auto-fix size, test coverage requirements)
- [ ] Data sensitivity rules updated (PII, payment, health patterns defined)
- [ ] Slack webhook configured (messages actually deliver)
- [ ] GitHub/GitLab CLI authenticated (`gh repo list` works)
- [ ] Audit log path writable (skill can write decisions)
- [ ] Dry-run test: process 3-5 real alerts with `--dry-run` and verify decisions
- [ ] Live test: process one real alert end-to-end without `--dry-run`

---

## Quick Reference: Example Customizations

**For a microservices architecture:** List all services in repository-map.yaml with separate on-call rotations.

**For a startup (everyone on-call):** Point all repos' escalation_to to a single @on-call handle.

**For a regulated business (healthcare, finance):** Lower severity thresholds for data-related errors and always escalate data incidents to legal/compliance.

**For a mobile-first company:** Add iOS/Android-specific error patterns and stack frame mappings.

---

## Testing Your Customization

1. **Ingest:** Process a sample alert from your monitoring system → verify all fields populate
2. **Classify:** Check severity assignment matches your expectation
3. **Investigate:** Verify git blame returns correct author and commit
4. **Decide:** Confirm routing (fix/file/escalate/suppress) is correct
5. **Notify:** Test that Slack message actually arrives in the right channel
6. **Artifact:** If creating issue, verify GitHub/GitLab issue has all diagnostic info

Run this flow with 3-5 recent real alerts before enabling in production.

