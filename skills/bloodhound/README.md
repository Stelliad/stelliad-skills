# Secrets Scanner - Quick Reference

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r bloodhound /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/bloodhound

or: "scan this repo for exposed credentials"
```

The agent reads [SPEC.md](./SPEC.md) and does the work. The mode names in the spec (`quick`, `verify`, `deep`, `full`) are its
vocabulary for scan depth, not executables on your PATH.

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly.
[CUSTOMIZE.md](./CUSTOMIZE.md) is where you set the thresholds and policy for
your stack.

## Prerequisites

- Git repository initialized in project root
- Git version 2.0+ for history scanning (required for `deep` and `full` modes)
- Network egress allowed for active verification (optional; can be disabled in config)
- IAM credentials for cloud provider verification (AWS, GCP, Azure; optional)
- `read` permissions on all scanned files and git history

## Quick Start

### 1. First Scan (Quick mode)

```bash
cd /path/to/repo
scan quick
```

**Output**: Lists any obvious credentials found in the current files (5-10 seconds).

### 2. Verify Mode (for CI/CD)

```bash
scan verify
```

**Output**: Pattern matches plus entropy filtering and active verification (30 seconds). This is the standard CI/CD mode.

### 3. Deep Audit (with history)

```bash
scan deep
```

**Output**: Everything in Verify mode plus git history and configuration files (2 minutes). Run when onboarding or after policy changes.

## Sample Output

### Terminal (default)

```
[CRITICAL] AWS Access Key at api/config.py:42
Pattern: AWS_ACCESS_KEY_ID (AKIA*)
Status: Active (verified)
First seen: 2026-01-15
Action: Rotate immediately

[WARNING] GitHub Token in .env.example:8
Pattern: GITHUB_TOKEN
Status: Unverified (expired or revoked)
First seen: 2026-02-20
Action: Review and clarify

[INFO] Test API key in test_fixtures.json:15
Pattern: INTERNAL_KEY
Status: Marked as legitimate (baseline)
First seen: 2026-03-01
Action: None
```

### JSON (for automation)

```json
{
  "summary": {
    "total": 3,
    "critical": 1,
    "warning": 1,
    "info": 1,
    "scan_time": "28s"
  },
  "findings": [
    {
      "severity": "critical",
      "type": "AWS_ACCESS_KEY",
      "file": "api/config.py",
      "line": 42,
      "verified_active": true,
      "first_seen": "2026-01-15T10:42:00Z"
    }
  ]
}
```

## How It Works

**Pattern Matching**: Scans files for 150+ credential patterns (AWS keys, tokens, passwords, etc.)

**Entropy Analysis**: Filters out false positives like UUIDs and hashes using statistical analysis

**Format Verification**: Confirms matches conform to actual credential formats (checksums, prefixes, etc.)

**Active Verification**: Attempts non-destructive contact with named services to confirm credentials are actually active

**History Search**: Traverses git commits to find credentials that were introduced and later deleted

**Configuration & State**: Scans `.env`, `terraform.tfvars`, and other configuration files for embedded credentials

**Full Coverage**: Includes vendored dependencies, documentation, and examples

## Setup & Configuration

### Create `.secrets-scanner.yaml`

```yaml
scanner:
  modes:
    verify:
      timeout: 30s
      
verification:
  aws:
    enabled: true
  github:
    enabled: true

output:
  format: terminal
  redact: true

policy:
  block_commits_on_critical: true
```

### Environment Variables

```bash
export SECRETS_SCANNER_CONFIG=/path/to/.secrets-scanner.yaml
export SECRETS_SCANNER_BASELINE=.secrets-scanner.baseline.json
```

## Integration

### GitHub Actions (one-liner)

```yaml
- name: Scan for secrets
  run: scan verify --output sarif --output-file results.sarif
- uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: results.sarif
```

### Pre-commit Hook (one-liner)

```bash
echo 'scan quick --fail-on critical' > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

### CI/CD (generic)

```bash
scan verify --fail-on critical
```

## Response Workflow

### Critical Finding (Verified Active)

1. **Rotate immediately**: Generate new credential and revoke old one
2. **Search for usage**: Find all systems using the old credential
3. **Update systems**: Deploy new credential everywhere it's needed
4. **Verify rotation**: Run `scan rotation` to confirm old one is dead
5. **Update baseline**: Mark as rotated in baseline if legitimate

### Warning Finding (Unverified or Historical)

1. **Review**: Determine if it's a false positive, dead, or legitimately exposed
2. **Clarify**: If unclear, treat as Critical and rotate
3. **Baseline**: If legitimate (test fixture, historical), mark as reviewed
4. **Document**: Record why this finding is acceptable

### Info Finding (Low Confidence)

1. **Review pattern**: Confirm the pattern is not generating noise
2. **Tune or ignore**: Disable pattern if false positive, baseline if legitimate

## Baseline Creation

On first deployment, create a baseline of current findings to avoid alert fatigue.

**Read Baseline Governance in [SPEC.md](./SPEC.md) before you run any of this.**
Four rules govern the baseline and they are not tuning: the file stores hashes
and never values; every write records a named approver; no directory is ever
auto-baselined, test fixtures least of all; and entries expire and get
re-verified rather than living forever. A baseline that can grow without anyone
looking reports clean for the same reason a disconnected smoke alarm does.

Re-verification is yours to schedule. `reverify_after_days` sets the threshold;
`scan baseline audit` is what acts on it. Run it on the same cadence as your
weekly Full scan.

```bash
# Scan everything
scan full --output json > findings.json

# Review findings manually
cat findings.json | jq '.findings[] | select(.severity=="critical")'

# Create baseline with reviewed findings
scan baseline create \
  --findings findings.json \
  --status reviewed \
  --reason 'Initial scan - approved by security team' \
  --approval-by <name>
```

Then verify against baseline:

```bash
scan verify --baseline .secrets-scanner.baseline.json
```

Review what the baseline is holding, and let it expire what no longer applies:

```bash
scan baseline audit --baseline .secrets-scanner.baseline.json
```

Only NEW findings are reported.

## Common Patterns by Category

| Category | Patterns | Example |
|---|---|---|
| **AWS** | ACCESS_KEY, SECRET_KEY, SESSION_TOKEN | AKIA2EXAMPLE, wJalr7UFlEMI/K7MDENG... |
| **GCP** | SERVICE_ACCOUNT, PRIVATE_KEY | {"type": "service_account", ... |
| **GitHub** | GITHUB_TOKEN, PAT | ghp_Exampletoken1234567890 |
| **Stripe** | API_KEY, SECRET_KEY | sk_test_Examplekey1234567890 |
| **Twilio** | ACCOUNT_SID, AUTH_TOKEN | ACxxxxxxxxxxxxxxxxxxxxxxxx |
| **Database** | POSTGRES_URL, MYSQL_PASSWORD | postgres://user:pass@host |
| **SSH/TLS** | RSA_KEY, PRIVATE_KEY, CERT | [private-key-format] |
| **Kubernetes** | SERVICE_ACCOUNT_TOKEN | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... |
| **Internal** | [Custom patterns defined in config] | [Your org-specific format] |

## Time & Resources

| Scan Mode | Repo Size | Typical Time | CPU | Memory |
|---|---|---|---|---|
| Quick | 10K files | 5-10s | 20% | 50MB |
| Verify | 10K files | 30-60s | 25% | 100MB |
| Quick | 100K files | 20-30s | 40% | 200MB |
| Verify | 100K files | 2-3min | 45% | 300MB |
| Deep | 10K files + history | 2-3min | 50% | 400MB |
| Full | 100K files + history | 3-5min | 60% | 500MB |

*Times vary by hardware, network (for verification), and git history depth.*

## Security & Privacy

The Rotation Health Report is output that needs the same care as a finding. It
is a ranked list of an organization's stalest live credentials, which is useful
to whoever owns them and equally useful to anyone else. Treat it like a finding:
do not paste it into a ticket, a chat channel, or a build log that outlives the
run.

When secrets are found, report them by location and type only, never store, print, or transmit the credential value itself. All findings are hashed in the baseline file (one-way, not reversible). The scanner never transmits credentials to external services unless explicitly configured for active verification, and verification is read-only (no modifications to remote systems). Disable active verification for highly sensitive services where credential exposure during testing is unacceptable.

## See Also

- **SPEC.md**: Technical architecture, nine layers, operating modes, baseline mode and its governance rules, the rotation health report, performance characteristics
- **CUSTOMIZE.md**: Configuration reference, custom patterns, integration points, policy settings

## Troubleshooting

### "Too many false positives"

**Cause**: Pattern is too broad or entropy threshold too low

**Fix**: Disable pattern for that category or tighten regex in `.secrets-scanner.yaml`

```yaml
patterns:
  built_in:
    exclude: [low_entropy_pattern]
```

### "Scan is slow"

**Cause**: Deep history or large vendored directories

**Fix**: Use Quick or Verify mode for development; reserve Full for scheduled audits

```bash
scan quick  # Local only, 5 seconds
scan verify  # Standard CI/CD, 30 seconds
```

### "Too many false positives"

**Cause**: Pattern is too broad or entropy threshold too low

**Fix**: Disable pattern for that category or tighten regex in `.secrets-scanner.yaml`

```bash
scan verify --fail-on critical
```

### "Baseline verification failing"

**Cause**: Credentials were rotated but baseline not updated

**Fix**: Update baseline with new status

```bash
scan baseline update --file .secrets-scanner.baseline.json --approval-by <name>
```

### "Active verification fails"

**Cause**: Service offline, authentication issue, or credential actually revoked

**Fix**: Disable verification for that service or check service status

```yaml
verification:
  [service_name]:
    enabled: false
```

### "Credentials appearing in git history"

**Cause**: Credentials were committed in the past and still in history

**Fix**: This is expected. Use `git filter-branch` or `git rebase` to remove from history, then verify with `scan rotation`

### "Webhook not receiving notifications"

**Cause**: Webhook endpoint unreachable or authentication failing

**Fix**: Test webhook URL manually and verify authentication headers

```bash
curl -X POST https://endpoint.example.com/api/secrets \
  -H 'Authorization: Bearer TOKEN' \
  -d '{\"test\": true}'
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Scan successful; no findings above threshold |
| 1 | Findings detected at configured severity level |
| 2 | Scan failed (config error, permission denied, etc.) |
| 3 | Invalid command line arguments |

Use in CI/CD:
```bash
scan verify --fail-on critical
# Exit 0 if no critical findings, exit 1 if critical findings found
```

## Git History Behavior

**Shallow Clone (default for Quick/Verify modes)**:
- Scans only the current commit and recent commits
- Much faster (~30s for Verify mode)
- Appropriate for pre-commit and pull request checks
- May miss credentials from distant history

**Unlimited History (Deep/Full modes)**:
- Scans entire git history from repository inception
- Slower (~2-10 minutes depending on size)
- Comprehensive baseline and audit tool
- Can identify credentials that were committed years ago

Configure in `.secrets-scanner.yaml`:
```yaml
git:
  shallow_clone: true   # Fast, limited history
  max_history_commits: 1000  # Cap for performance
```

## Output Formats (Examples)

### Terminal
Color-coded for console display with file paths and line numbers

### JSON
Full structured data for parsing and automation

### Markdown  
Formatted for email and documentation

### SARIF
GitHub Advanced Security, GitLab SAST, and general SIEM integration
