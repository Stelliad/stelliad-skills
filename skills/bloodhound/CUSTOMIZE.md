# Secrets Scanner - Customization Guide

> **There is no bloodhound binary.** This skill is a specification an agent
> executes. The config below is real: you create it, and the agent reads it.
> The `scan` invocations in this guide are the spec's vocabulary for the
> options, not something on your PATH and not a package to install.
> See [README.md](./README.md) for how to invoke it.

## Configuration Structure

### .secrets-scanner.yaml

The main configuration file controls scanning behavior, output formats, and integration points.

```yaml
# .secrets-scanner.yaml

scanner:
  modes:
    quick:
      layers: [pattern, format]  # Fastest, local only
      timeout: 10s  # Typical scan: 5-10 seconds
    verify:
      layers: [pattern, entropy, format, verify]  # Default CI/CD
      timeout: 60s  # Typical scan: 30-60 seconds with network
      verify_read_only: true  # Never modify during scan
    deep:
      layers: [pattern, entropy, format, verify, history, env, terraform, vendored, docs]
      timeout: 5m  # Typical scan: 2-5 minutes
      history_depth: unlimited
    rotation:
      layers: [pattern, entropy, format, verify]  # Post-rotation check
      timeout: 20s  # Typical scan: 10 seconds
    full:
      layers: [pattern, entropy, format, verify, history, env, terraform, vendored, docs]
      timeout: 10m  # Typical scan: 3-10 minutes
      history_depth: unlimited

patterns:
  built_in:
    enabled: true
    exclude: []  # Patterns to disable by name
  custom:
    - name: <custom_pattern_name>
      regex: '<YOUR_PATTERN_HERE>'  # Pattern to match anywhere in the line (remove ^ anchor for mid-line matching)
      entropy_threshold: 3.5
      confidence: high  # high, medium, low
      category: <custom_category>

verification:
  aws:
    enabled: true
    region: us-east-1
    timeout: 10s
  github:
    enabled: true
    timeout: 5s
  <other_services>:
    enabled: false  # Opt-in for sensitive services

baseline:
  file: .secrets-scanner.baseline.json
  mode: <create | verify | update>  # How to handle baseline
  # Off by default and it should stay off. A scanner that adds findings to its
  # own ignore list is a scanner you stop hearing from. See Baseline Governance
  # in SPEC.md before turning this on for any directory.
  auto_baseline_test_dirs: false
  reverify_after_days: 90        # Re-test baselined entries on this cadence
  drop_rotated_entries: true     # A baselined secret that gets rotated leaves the baseline

git:
  enabled: true
  shallow_clone: true  # Faster scanning, limited history
  max_history_commits: 1000  # Limit for performance
  exclude_branches: []

output:
  format: <terminal | json | markdown | sarif>
  severity_filter: <critical | warning | info>  # Minimum severity to report
  redact: true  # Never print actual credential values
  store_findings: false  # Never persist findings to disk without encryption

integration:
  secrets_manager:
    type: <aws_secrets_manager | vault | webhook | none>
    # Additional config depends on type selected
  ci_cd:
    platform: <github_actions | gitlab | jenkins | none>
    fail_on_critical: true
    fail_on_warning: false
  slack:
    enabled: false
    webhook_url: ${SLACK_WEBHOOK_URL}  # Environment variable only
    notify_on: <critical>

logging:
  level: <debug | info | warn | error>
  format: <text | json>
  output: stdout  # or file path
  metrics:
    enabled: false
    prometheus_port: 8080

policy:
  block_commits_on_critical: true
  # A human confirms every baseline write. This is the control that keeps a
  # baseline from silently becoming a mute button.
  require_baseline_approval: true
  auto_rotate_on_detect: false  # Dangerous; requires secrets manager
  incident_response_webhook: ${INCIDENT_WEBHOOK_URL}
```

## Adding Custom Patterns

### Template: Organization-Specific Credential

```yaml
patterns:
  custom:
    - name: internal_api_key
      regex: '^INTERNAL_KEY_[A-Z0-9]{32}$'
      entropy_threshold: 3.8  # Adjust based on your format
      confidence: high
      category: internal_api
      examples:
        - INTERNAL_KEY_A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6
      false_positives:  # Patterns to exclude
        - 'INTERNAL_KEY_EXAMPLE_.*'
        - 'INTERNAL_KEY_TEST_.*'
```

### Process for Adding a Pattern

1. **Define the regex**: Match the actual format of your credential (prefix, length, character set)
2. **Set entropy threshold**: Test against real credentials and false positives to find the sweet spot
3. **Add examples**: Include one real (but revoked) example and one false positive
4. **Test**: Scan a repository with both known examples and known false positives
5. **Adjust**: Tighten the regex or entropy threshold if false positives appear
6. **Deploy**: Add to configuration and run in Verify mode first

## Secrets Manager Integration

### AWS Secrets Manager

```yaml
integration:
  secrets_manager:
    type: aws_secrets_manager
    region: us-east-1
    prefix: /myorg/  # All secrets under this prefix
    auto_report: true
    report_on_critical: true
    auto_create_rotation: false  # Requires Lambda function
```

With this configuration, any Critical finding matching a secret name in Secrets Manager is marked `managed` and the baseline is auto-updated.

### HashiCorp Vault

```yaml
integration:
  secrets_manager:
    type: vault
    address: https://vault.example.com
    auth_method: aws_iam  # or userpass, token, etc.
    namespace: secret
    path_prefix: myorg/
```

### Custom Webhook

```yaml
integration:
  secrets_manager:
    type: webhook
    endpoint: https://incident-response.example.com/api/secrets
    method: POST
    headers:
      Authorization: Bearer ${WEBHOOK_TOKEN}
    payload_format: json
```

Payload includes credential type, location, status, and recommended actions.

## CI/CD Integration

### GitHub Actions

```yaml
name: Secrets Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history
      - name: Run Secrets Scanner
        run: |
          scan verify \
            --output sarif \
            --output-file results.sarif
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results.sarif
          category: secrets-scanner
```

### GitLab CI

```yaml
secrets-scan:
  image: [secrets-scanner-image]
  script:
    - scan verify --output sarif --output-file gl-sast-report.json
  artifacts:
    reports:
      sast: gl-sast-report.json
  allow_failure: true
```

### Generic CI/CD (Jenkins, CircleCI, etc.)

```bash
#!/bin/bash
scan verify --output json --output-file findings.json

# Count critical findings
CRITICALS=$(jq '[.findings[] | select(.severity=="critical")] | length' findings.json)

if [ "$CRITICALS" -gt 0 ]; then
  echo "FAILED: $CRITICALS critical findings detected"
  exit 1
fi
```

## Pre-commit Hook Setup

```bash
#!/bin/bash
# .git/hooks/pre-commit

set -e

echo "Running Secrets Scanner (Quick mode)..."
if ! scan quick --severity-filter critical; then
  echo "❌ Commit blocked: credentials detected"
  exit 1
fi

echo "✅ Passed"
```

Install system-wide:
```bash
# Install
scan install-hooks --location pre-commit

# Verify
cat .git/hooks/pre-commit
```

## Baseline Management

### Creating a Baseline

When first deploying the scanner, create a baseline of current findings to avoid alert fatigue:

```bash
# Scan and create baseline with all findings marked as "reviewed"
scan full --output json |
scan baseline create \
  --status reviewed \
  --reason 'Initial baseline' \
  --approval-by team-lead \
  --output .secrets-scanner.baseline.json
```

### Verifying Against Baseline

```bash
# Daily verify against baseline
scan verify \
  --baseline .secrets-scanner.baseline.json \
  --output terminal
```

Only NEW findings or CHANGED findings are reported.

### Updating Baseline

When findings are legitimate and should be tracked:

```bash
# Add new finding to baseline
scan baseline update \
  --add 'path/to/file:42' \
  --reason 'test fixture' \
  --status legitimate \
  --approval-by <name>   # required while require_baseline_approval is set
```

## Logging & Monitoring

### Structured Logging

```yaml
logging:
  level: info
  format: json  # Machine-readable
  output: /var/log/secrets-scanner.json
```

Logs include: timestamp, severity, finding details, verification results, baseline status.

### Prometheus Metrics

```yaml
logging:
  metrics:
    enabled: true
    prometheus_port: 8080
```

Metrics exposed:
- `secrets_scanner_findings_total{severity="critical"}`: Counter
- `secrets_scanner_scan_duration_seconds`: Histogram
- `secrets_scanner_baseline_coverage_percent`: Gauge
- `secrets_scanner_verification_failures_total`: Counter

### Alert Integration

```yaml
integration:
  incident_response_webhook: https://alerts.example.com/api/incidents
```

Critical findings trigger incident creation with:
- Credential type and location
- Verification status
- Recommended remediation (rotate, revoke, review)
- Baseline status and history

## Customization Decision Tree

Answer these eight questions to configure the scanner for your organization:

1. **How often should scanning run?**
   - Pre-commit only: Use Quick mode in .git/hooks/pre-commit
   - On every PR: Use Verify mode in CI/CD
   - Weekly audit: Schedule Full mode nightly

2. **Which services should we verify against?**
   - Only non-sensitive: Enable GitHub, Stripe, etc.
   - No active verification: Set verification.enabled: false for all
   - Sensitive only: Enable AWS/GCP with read-only operations

3. **How deep should history scanning go?**
   - Recent only: shallow_clone: true, max_history_commits: 100
   - Complete history: shallow_clone: false, max_history_commits: unlimited

4. **What should block a commit or PR?**
   - Only Critical findings: fail_on_critical: true, fail_on_warning: false
   - Both Critical and Warning: fail_on_critical: true, fail_on_warning: true
   - Warn only, never block: fail_on_critical: false

5. **Do we have a secrets manager?**
   - AWS Secrets Manager: Configure integration
   - HashiCorp Vault: Configure integration
   - Manual management: type: none

6. **What's the baseline strategy?**
   - Clean slate: create a baseline on first run and update it as credentials rotate. This is the intended posture
   - None: disable the baseline and report everything. Correct for a young codebase with nothing to suppress
   - **Not an option: create a baseline and never revisit it.** An unreviewed
     baseline ages into a list of secrets nobody is watching any more, and it
     grows every time someone waves a finding past. If the review cadence is the
     problem, shorten `reverify_after_days` rather than abandoning it

7. **Who should be notified of findings?**
   - Security team only: Configure incident webhook
   - Slack channel: Configure Slack webhook with notify_on: [critical]
   - No notifications: Disable integration

8. **How sensitive are findings?**
   - Store locally: store_findings: true (requires encryption)
   - Never store: store_findings: false (always output to stdout)
   - Store encrypted: Use env variable for encryption key

## Cross-File Reference

- **README.md**: Quick start, setup, integration examples, troubleshooting, exit codes
- **SPEC.md**: Technical architecture, nine layers, operating modes, baseline mode, performance characteristics
