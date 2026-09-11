# Repo Audit

Baseline audit for code quality and security. Validates repositories against your delivery phases, scores compliance, and reports what to fix and in what priority order.

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r repo-audit /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/repo-audit

or: "audit this repo against the baseline and tell me what blocks the next phase"
```

The agent reads [SPEC.md](./SPEC.md) and does the work. The `audit` invocations in the spec are its vocabulary for
the scan and its flags, not a binary that ships here.

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly.
[CUSTOMIZE.md](./CUSTOMIZE.md) is where you set the thresholds and policy for
your stack.

## What It Does

Repo Audit scans your codebase across 10 categories (security, linting, testing, CI/CD, documentation, etc.) and produces:

- **Phase-aware score** (0–100%, with thresholds per your delivery phase)
- **Prioritized remediation list** (estimated time-to-fix for each)
- **Gate status** (pass/fail against phase advancement criteria)
- **Exportable report** (Markdown for humans, JSON for CI tooling)

**Scan time:** 2–5 minutes per repository  
**Common first run:** Find 3–7 actionable gaps

## Quick Start

### Basic Usage

```bash
# Scan current repo
./audit --repo .

# Audit another repository
./audit --repo ../my-project

# Audit for a specific phase (defaults to Build)
./audit --repo . --phase <your_phase_name>

# Generate templated fixes
./audit --repo . --fix

# Check gate status (for CI pipelines)
./audit --repo . --gates

# Output as JSON
./audit --repo . --json > audit.json
```

## Report Overview

### What the Score Means

```
90–100%  ✓ Pass. Code is production-ready for this phase.
80–89%   ○ Good. Address 1–2 gaps before next phase.
70–79%   ⚠ Fair. Several gaps; close before advancing phase.
Below 70% ✗ At-risk. Major gaps; do not ship yet.
```

Thresholds vary by phase. Early phases expect 40%+ (critical checks only); later phases expect 80%+ (full rigor). Configure thresholds in CUSTOMIZE.md.

### Common Categories & Time-to-Fix

| Category | Checks | Time to Fix |
|---|---|---|
| Security | Secrets in git, .gitignore | 15 min |
| Pre-commit Hooks | Hook installation, secret detection | 10 min |
| Git Workflow | Branch protection, linear history | 20 min |
| Linting | Linter installed, config present, no violations | 30 min |
| Formatting | Formatter config, all files pass format check | 20 min |
| Testing | Test suite exists, tests pass | 4–8 hours |
| Dependencies | Lock file present and up-to-date | 15 min |
| CI Pipeline | Workflow file, lint/test gates | 45 min |
| Supply Chain | Dependabot, SBOM, vulnerability scanning | 30 min |
| Documentation | README with sections, API guide | 1–2 hours |

## Sample Findings & Quick Fixes

### CRITICAL: Hardcoded Secret Found

```bash
# Run the scanner to identify specific secrets and their locations
# (The audit tool detects and reports credential patterns with full context)

# Remove from history (choose one method)
git-filter-repo --invert-paths --path config/secrets.env

# Rotate the actual secret immediately
aws secretsmanager rotate-secret --secret-id prod-db-password
```

### CRITICAL: No Branch Protection

```bash
# Set up protection on main branch
gh api repos/[owner]/[repo]/branches/main/protection \
  --method PUT \
  --input - <<EOF
{
  "required_status_checks": {"strict": true, "contexts": ["ci/build", "ci/test"]},
  "enforce_admins": true,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

### WARNING: No Linter Configured

```bash
# For Python projects
pip install ruff
echo -e '[tool.ruff]\nline-length = 100' >> pyproject.toml
git add pyproject.toml && git commit -m "ci: add ruff linter config"
```

### WARNING: No CI Pipeline

```bash
# Generate GitHub Actions workflow
audit --repo . --fix

# Copy and customize
cp remediations/github-actions-ci.yml .github/workflows/ci.yml
git add .github/workflows/ci.yml && git commit -m "ci: add GitHub Actions pipeline"
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Audit passed; score meets or exceeds phase threshold |
| 1 | Audit failed; score below phase threshold or CRITICAL findings present |
| 2 | Audit error (invalid phase, repo path not found, configuration error) |
| 3 | Audit skipped (no checks applicable for phase) |

Use in CI pipelines:
```bash
audit --repo . --phase <your_phase_name> || exit 1  # Block build on audit failure
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Audit
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # There is no package to install. This skill is a specification an agent
      # executes, so make this folder available to your agent runner and have it
      # read SPEC.md. The line below is the vocabulary from SPEC.md, not a binary.
      - run: |
          audit --repo . --phase Build --json > audit.json
      - uses: actions/upload-artifact@v4
        with:
          name: audit-report
          path: audit.json
```

### As a Phase Gate

```yaml
# .gates.yaml (phase advancement)
gates:
  <phase1_to_phase2>:
    - gate: audit_baseline
      config:
        phase: <phase2>
        min_score: 80
        block_on_critical: true
```

When running your phase advancement gate workflow, Audit validates the score and CRITICAL findings before allowing advancement. Set thresholds per phase in CUSTOMIZE.md.

## See Also

- **SPEC.md**: Technical architecture, 10 check categories, scoring model, output specification
- **CUSTOMIZE.md**: Configuration guide, tool selection, custom checks, phase-specific rules

## Who Uses This

- **Security teams:** Enforce baseline controls across all repos
- **Platform/DevOps:** Verify deployment readiness
- **Engineering leads:** Quantify code quality without manual audits
- **Contributors:** Understand repo requirements before opening a PR
- **CI/CD pipelines:** Block merges that don't meet baseline standards

## Configuration

Audit is configurable at three levels:

1. **Organization-wide:** `.audit.baseline.yaml` (shared standards)
2. **Project-specific:** `.audit.yaml` (repo root)
3. **Runtime:** `--phase`, `--deep`, `--fix` flags

Full guide: [CUSTOMIZE.md](./CUSTOMIZE.md)

## Outputs

- **Markdown report**: Human-readable, shareable
- **JSON report** (`--json`): For dashboards and CI tooling
- **Remediation templates** (`--fix`): Copy-and-paste fixes
- **Gate status** (`--gates`): Pass/fail for phase gates

## Support

- Report issues: GitHub Issues in the repo
- Suggest custom checks: Submit a PR with examples
- Share your baseline: Open a discussion for community baselines

## License

[Your Organization License]
