# Secrets Scanner - Technical Specification

## Overview

Secrets Scanner is a deterministic credential detection and management system designed to identify, classify, and track secrets across code repositories, configuration files, and infrastructure definitions. It operates across nine layers of analysis and supports five configurable scanning modes to balance speed against depth.

The system is built for organizations that need to find credentials before they leak, verify whether found credentials are actually active, and maintain a baselined inventory of known secrets without storing their values.

## Architecture: Nine Layers

### Layer 1: Pattern Matching
Regex-based detection across 150+ credential patterns organized by category:
- **Cloud providers**: AWS access keys, GCP service accounts, Azure credentials
- **Version control**: GitHub, GitLab, Bitbucket tokens
- **APIs**: Stripe, Twilio, SendGrid, DataDog, PagerDuty, Auth0
- **Databases**: PostgreSQL, MySQL, MongoDB connection strings
- **Infrastructure**: SSH keys, TLS certificates, Docker credentials
- **AI providers**: OpenAI, Anthropic, Claude API keys
- **Message queues**: RabbitMQ, Kafka, SQS credentials
- **Custom patterns**: Organization-specific formats via regex templates

Pattern matching produces high recall at the cost of false positives. It is the foundation for all subsequent filtering layers.

### Layer 2: Entropy Analysis
Statistical analysis of candidate strings to distinguish high-entropy secrets from random strings in logs. Applies Shannon entropy thresholds (typically 4.0+ bits per character) to filter false positives from code comments, UUIDs, and hashes.

### Layer 3: Format Verification
Structural validation that a matched credential conforms to the actual format of real credentials in that service. Example: AWS access keys must start with `AKIA`, have the right character set, and pass validation checksum rules.

### Layer 4: Active Verification
Attempt contact with the named service to determine whether a discovered credential is actually active or dead. Uses non-destructive read operations only (list buckets, get account metadata, check rate limits). Dead credentials are marked `Unverified` and deprioritized. Requires opt-in API access and is skipped for sensitive credentials by default.

### Layer 5: Git History Scanning
Traverse commit history to find credentials introduced and later deleted. Uses shallow clones to reduce scanning time and identifies the commit that first introduced a credential and when it was removed. Marks credentials present in the live tree differently from those already deleted by a later commit.

### Layer 6: Environment File Analysis
Dedicated scanning of `.env`, `.env.local`, `*.envrc`, and similar files with relaxed formatting requirements because these files intentionally store secrets. Applies different thresholds than general code.

### Layer 7: Terraform State Scanning
Stateful resource inspection for credentials embedded in Terraform state files (`.tfstate`, `terraform.tfvars`). Recognizes cloud provider credentials, database passwords, and API keys in resource attributes. Scans both local files and remote state backends if accessible.

### Layer 8: Vendored Dependency Scanning
Deep inspection of `node_modules/`, `vendor/`, `.venv/`, and similar vendored directories for credentials in package configurations, lockfiles, and embedded examples. Can be disabled for large monorepos to improve performance.

### Layer 9: Documentation & Example Scanning
Optional layer that identifies credentials in markdown, JSON examples, API documentation, and README files where they appear as examples or walkthroughs. Marked with lower confidence since examples are sometimes intentionally sanitized.

## Entry Points (CLI Surface)

The scanner is invoked with a mode argument and optional flags:

```
scan [MODE] [OPTIONS]

Modes:
  quick: Fast local scan (Layers 1, 3; ~5s)
  verify: Standard CI/CD scan (Layers 1, 2, 3, 4; ~30s)
  deep: Comprehensive audit (Layers 1-9; ~2min)
  rotation: Post-rotation verification (Layers 1, 2, 3, 4; ~10s)
  full: Complete baseline (Layers 1-9, unlimited history; ~3min)

Sub-commands:
  baseline create        Write a new baseline. Requires --approval-by
  baseline update        Add or change one entry. Requires --approval-by
  baseline audit         List every baselined entry with its age, status, and
                         reason. Re-tests entries older than reverify_after_days
                         and drops any whose credential is already dead when
                         drop_rotated_entries is set. Read-only otherwise

Options:
  --output FORMAT        Output format: terminal, json, markdown, sarif
  --baseline FILE        Baseline file for comparison
  --approval-by NAME     Person accountable for a baseline write. Recorded in
                         the entry. Required when require_baseline_approval is
                         set. See Baseline Governance for what it does and does
                         not guarantee
  --rotation-health      With rotation mode: read credential ages from the
                         configured secrets manager and print the Rotation
                         Health Report instead of the layer findings
  --fail-on SEVERITY    Fail exit code on: critical, warning, info
  --config FILE         Path to .secrets-scanner.yaml
  --verbose            Increase verbosity
```

## Operating Modes

Modes compose layers to balance scan time against detection depth.

### Quick (5 seconds)
**Layers**: 1, 3 (Pattern + Format Verification)

Fast pre-commit and local development scan. Pattern matching with basic format validation. No history traversal, no API calls. Intended to catch obvious mistakes before commit.

### Verify (30 seconds)
**Layers**: 1, 2, 3, 4 (Pattern + Entropy + Format + Active Verification)

Default CI/CD mode. Includes entropy filtering and active verification to reduce false positives. Reports only high-confidence credentials and verifies they are actually active. May skip API calls for sensitive services that should never appear in logs.

### Deep (2 minutes)
**Layers**: 1-9 (All layers)

Comprehensive scan of history, state files, vendored dependencies, and documentation. Intended for periodic audits and compliance reviews. Generates full intelligence on all credential types and locations.

### Rotation (10 seconds)
**Layers**: 1, 2, 3, 4 (Pattern + Entropy + Format + Active Verification)

Post-rotation verification. Run after rotating a credential to confirm the old one is still active (if immediate revocation was deferred) or already dead. Helps validate that old credentials are not lingering in the system after they should have been removed.

With `--rotation-health`, this mode instead reads credential ages from the configured secrets manager and prints the Rotation Health Report described below. The two are separate questions: the layer scan asks whether a specific rotated credential is dead, and the health report asks which credentials in the store have gone stale.

### Full (3 minutes)
**Layers**: 1-9, plus cross-repo search and history depth

Complete baseline establishment and audit. Runs all layers with unlimited history depth, searches across all repositories in an organization, and produces a full credential inventory. Intended for one-time baseline creation and periodic audits.

## Output Formats

### Terminal
Human-readable format with color codes by severity. Includes file path, line number, credential type, and confidence level. Suitable for local development and CI/CD console logs.

```
[CRITICAL] AWS Access Key at src/config.py:42
Pattern: AWS_ACCESS_KEY (AKIA*)
Status: Active (verified via STS)
First seen: 2026-01-15
Action: Rotate immediately
```

### Markdown
Formatted report suitable for email, documentation, and internal wikis. Groups findings by severity and includes metadata, remediation steps, and timeline.

### JSON
Structured format for programmatic consumption. Includes all metadata, confidence scores, and verification results. Suitable for secrets managers, ticketing systems, and custom automation.

### SARIF
Standard Analysis Results Interchange Format for integration with GitHub Advanced Security, GitLab SAST, and other security platforms. Reports findings as code vulnerabilities with full remediation guidance.

## Severity Levels

### Critical
**Definition**: A credential that is verified active and present in the live repository.

**Action**: Rotate immediately. The credential must be assumed compromised.

**Examples**:
- AWS access key that responds to STS calls
- Database password in source code that connects to a production database
- API token that returns a successful authentication response

### Warning
**Definition**: A high-confidence credential match that has not been verified as active, or a credential in git history that was deleted by a later commit but was exposed for some period.

**Action**: Review and clarify. Determine whether it is a false positive, already rotated, or legitimately exposed. Set a baseline if legitimate and known.

**Examples**:
- A credential pattern match that cannot be verified (service is offline, API key is revoked)
- A credential in a two-month-old commit that was deleted in a later commit
- A high-entropy string in documentation that matches credential format

### Info
**Definition**: A low-confidence match, an example credential, or a finding that is blocked by policy but not actionable (e.g., it matches the pattern but is a UUID or hash).

**Action**: None required unless the pattern is generating false positives, in which case tune the pattern or baseline it.

**Examples**:
- A commented-out credential
- A credential in the git history that was deleted more than 6 months ago
- A string that matches the entropy threshold but fails format validation

## Integration Points

### Pre-commit Hooks
Run Quick mode before any commit is allowed. Blocks commits that would introduce credentials. Operates entirely locally with no network calls.

### CI/CD Pipeline
Run Verify mode on every pull request. Can block merges if Critical findings are present. SARIF output integrates with GitHub Advanced Security, GitLab SAST, and other platforms.

### Scheduled Audits
Run Full mode once per week or on demand. Performs complete repository and history scan. Compares results against baseline to identify new credentials or changes in status.

### Secrets Manager Integration
Automatically report new findings to AWS Secrets Manager, HashiCorp Vault, or similar. Where a finding matches a secret already held in the store, the integration can propose a `managed` baseline status for it.

**Proposing is not writing.** This path is subject to Baseline Governance rule 2 exactly like any other: the entry is queued for a human to approve, and it does not enter the baseline until someone does. An integration that could write its own baseline entries would be the auto-baselining that rule 3 exists to prevent, arriving through a different door.

### Incident Response
Run Rotation mode immediately after discovering and rotating a credential. Verify the old credential is still accessible (validation that it needs to be rotated) or already dead (validation that rotation is complete).

## Baseline Mode

Baseline mode allows tracking of credentials without storing their values. A baseline entry contains:
- Hash of the credential value (one-way, not reversible)
- Credential type and location (file, line number)
- Date first discovered
- Status (active, rotated, deleted, managed)
- Reason (legitimate in tests, managed by secret provider, historical)

This allows the scanner to report "credential X is still present in the code" without requiring storage of the credential itself in the baseline file.

Creating a baseline:
```
scan full --output json |
scan baseline create --status legitimate \
  --reason 'test_credentials in fixtures' \
  --approval-by <name> \
  --output .secrets-scanner.baseline.json
```

Verifying against a baseline:
```
scan deep --baseline .secrets-scanner.baseline.json
```

Only findings that are new or have changed status are reported.

### Baseline Governance

A baseline exists so a legacy codebase can adopt the scanner without drowning in
findings it already knows about. It stops doing that the moment it can grow
without anyone looking. Four rules keep it honest, and they are not optional
tuning:

1. **Store the hash, never the value.** Covered by the entry format above. A
   baseline file gets committed, and a baseline holding real credentials is a
   second copy of the leak.
2. **Every baseline write needs human confirmation.** `create` and `update` both
   require `--approval-by`, and the name is recorded on each entry. A finding
   enters the baseline because a person decided it should, not because a job ran.

   Be clear about what this is. `--approval-by` is a recorded attestation, not a
   verified control: nothing checks the name against a directory, and an
   automated caller can supply one. What it buys is that suppressing a finding
   leaves a name and a reason in a committed file, so the decision is auditable
   after the fact. If you need a real gate, put the baseline file behind code
   review and let the pull request be the control. The flag is the paper trail;
   your branch protection is the enforcement.

   `baseline audit` re-verifying an entry or dropping a rotated one is not a new
   suppression and does not need approval. It only ever narrows the baseline.
3. **A new secret is never auto-baselined.** No directory is exempt, test
   fixtures included. Real credentials end up in test fixtures constantly, and a
   fixture directory on an allow-list is the single most reliable place for a
   live key to sit unreported for a year. Auto-baselining is the one setting that
   converts this tool into a tool that agrees with you.
4. **Baselined entries expire.** Re-verify on a cadence, 90 days by default. An
   entry whose credential has since been rotated leaves the baseline rather than
   sitting there as a permanent exception to a secret that no longer exists.

The failure these prevent is a baseline that has quietly become the list of
secrets nobody is watching. It reports clean, and it reports clean for the same
reason a disconnected smoke alarm does.

## Rotation Health Report

Rotation mode also answers a question the layer scan cannot: of the credentials
held properly in a secrets manager, which ones have gone stale? Read the
creation and last-modified timestamps from the store and group by age.

```
Rotation Health Report (profile: default)

Never rotated
   /prod/webhook_url        created 2026-01-15   195 days
   /prod/payments_key       created 2026-02-01   178 days

Overdue (>90 days)
   /prod/inference_key      modified 2026-03-15  136 days
   /prod/third_party_key    modified 2026-04-01  119 days

Healthy (<90 days)
   /prod/primary_token      modified 2026-07-01   28 days
   /prod/auth_service_key   modified 2026-06-15   44 days

Summary: 2 never rotated, 2 overdue, 2 healthy
```

Never rotated is its own band rather than a long tail of Overdue. A credential
that has never been rotated has usually never had an owner either, and the
remediation is different: establish who owns it before setting a schedule for it.

The 90-day threshold is a default, not a standard. Set it from your own policy
and from what each credential protects.

## Pattern Categories (150+ patterns)

**Cloud**: AWS access/secret keys, GCP service account JSON, Azure subscription ID, DigitalOcean token, Linode token

**VCS**: GitHub personal access token, GitLab private token, Bitbucket app password, Gitea token

**APIs**: Stripe key, Twilio account SID, SendGrid API key, DataDog API key, PagerDuty token, Auth0 client secret, Slack bot token, Discord webhook

**Databases**: PostgreSQL connection string, MySQL password, MongoDB URI, Redis password, DynamoDB credentials

**Infrastructure**: SSH private key (RSA, ED25519), TLS certificate private key, Docker config auth, Kubernetes service account token

**AI Providers**: OpenAI API key, Anthropic API key, Hugging Face token, Cohere API key

**Message Queues**: RabbitMQ credentials, Kafka secrets, AWS SQS/SNS credentials

**VPN/Proxy**: OpenVPN client key, Tailscale key, WireGuard private key

**Package Managers**: npm auth token, pip index URL with credentials, Gem credentials, Maven repository password

**Custom**: Organization-specific patterns via regex templates in configuration

## Performance Characteristics

- **Quick mode**: O(n) file scan, constant time per file. Typical: 5-10 seconds for 10K files
- **Verify mode**: O(n) + API calls for active verification. Typical: 30-60 seconds with network
- **Deep mode**: O(n log n) with git history traversal. Typical: 2-5 minutes for full repository history
- **Full mode**: O(n log n) + deep history + vendored dependencies. Typical: 3-10 minutes depending on history depth and vendored code size

Scanning time scales linearly with repository size. Git history depth is the primary variable for Deep and Full modes.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Scan completed; no findings above configured severity threshold |
| 1 | Scan completed; findings at or above configured severity threshold (determined by `--fail-on` flag) |
| 2 | Scan failed (permission denied, invalid config, missing baseline file) |
| 3 | Invalid arguments or command line parsing error |
| 4 | Baseline write refused: `require_baseline_approval` is set and no `--approval-by` was supplied |

Exit 4 matters in CI. A pipeline that writes to the baseline will now stop rather than suppress a finding unattended, which is the intended behaviour and not a misconfiguration to route around.

Use in CI/CD with `--fail-on critical` to block deployments on critical findings:
```bash
scan verify --fail-on critical || exit 1
```

## Limitations

### Suppression Scope
Pattern-based detection cannot distinguish between real credentials and intentionally sanitized examples. The entropy layer filters some false positives, but examples in documentation or comments may still trigger. Use baseline mode to mark known examples as legitimate.

### IAM Scope
Active verification uses read-only API operations only (list, get, describe). It cannot verify whether a credential has been revoked or suspended unless the service explicitly returns an error on read operations. Some cloud providers do not distinguish between revoked and inactive credentials.

### Edge Cases
- **Credentials in compressed archives** (.zip, .tar.gz): Vendored dependency scanning does not decompress archives
- **Credentials in binary files**: Scanning is limited to text-based files and may miss secrets in serialized formats
- **Multi-line credentials** (PEM-encoded keys, certificates): Pattern matching works line-by-line and may miss credentials split across lines
- **Comments and strings in code**: A credential in a comment is detected the same as one in active code; classification depends on baseline status
- **Historical cleanup**: Removing credentials from current files does not remove them from git history; use `git filter-branch` or equivalent for complete removal

### Performance Limitations
Deep and Full modes scale linearly with repository size and git history depth. Repositories with >100K commits or >1GB of history may take 10+ minutes. Vendored dependency scanning can double scan time on repositories with large node_modules/ or vendor/ directories.

## Cross-File Reference

- **README.md**: Quick start, setup, integration examples, troubleshooting, git history behavior
- **CUSTOMIZE.md**: Configuration options, custom patterns, severity thresholds, integration points, and the `baseline` and `policy` blocks that enforce Baseline Governance
