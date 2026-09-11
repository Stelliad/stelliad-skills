# Repo Audit: Specification

## Overview

Repo Audit is a repository validation and scoring tool that performs 10 categories of baseline checks against a codebase, reports compliance against delivery phase expectations, and provides prioritized remediation guidance. It runs concurrently across check categories, applies phase-aware severity mapping, and exports results in Markdown and JSON formats for integration with CI pipelines and phase gates.

## System Architecture

### Components

**Tech Stack Detector**
Identifies repository language(s), frameworks, and build tooling from directory structure, config files, and manifest inspection. Produces a stack profile that drives all downstream check selection.

**Ruleset Engine**
Loads applicable checks based on detected stack and current engagement phase. Checks carry phase applicability metadata so that a test-failure finding escalates from warning in Shape to CRITICAL in Build. The engine applies no checks outside their applicable phase range.

**Audit Runner**
Executes all applicable checks concurrently using subprocess pools. Failures in one check do not block others. Enforces per-check timeouts (default 30 seconds) and captures stderr for error reporting.

**Scoring Module**
Calculates a weighted phase-aware score: `(checks_passed / checks_applicable) × 100%`. Only applicable checks contribute to the numerator and denominator, so a project with no tests does not fail on testing checks in Discover phase but does in Build. Severity scores are independent of pass/fail (a passed CRITICAL check still counts).

**Report Generator**
Assembles findings into structured Markdown and JSON. Includes finding detail, remediation steps, estimated time-to-fix, and gate status.

**Remediation Suggester**
Auto-generates templates and command snippets for fixes. Templates are language-specific and copy-paste ready.

### Data Flow

```
Input: (repo path, phase, flags)
  ↓
Stack detection (git, file tree scan, manifest parse)
  ↓
Load applicable ruleset (phase + stack match)
  ↓
Execute checks in parallel (timeout: 30s each)
  ↓
Aggregate results with severity & details
  ↓
Score & threshold comparison
  ↓
Generate remediation suggestions & templates
  ↓
Output report (Markdown + JSON metadata)
```

## Check Categories (10)

### 1. Security Foundations

**What it checks:**
- `.gitignore` file exists and is not empty
- Git history does not contain secrets (regex scan: `password`, `token`, `key`, `secret`, AWS key patterns)
- `.git/config` does not expose credentials
- No large binary files (>50MB) in history
- `.gitignore_global` or core.excludesFile configured (optional)

**Applicable phases:** All

**Time to fix:** 15 minutes

### 2. Pre-commit Hooks

**What it checks:**
- `.pre-commit-config.yaml` exists (or `husky` config for Node projects)
- `detect-secrets` or equivalent hook installed
- Hooks executable (`chmod +x` verified)
- At least one security-related hook present
- `.pre-commit-hooks.yaml` is valid YAML if present

**Applicable phases:** Shape, Build, Validate, Scale

**Time to fix:** 10 minutes

### 3. Git Workflow

**What it checks:**
- `staging` or `develop` branch exists (or configured equivalent)
- Branch protection rules applied to main/master (no force-push, linear history)
- Commit signing configured (user.signingkey or SSH key present)
- No orphaned branches older than 30 days
- Default branch is main/master (not develop)

**Applicable phases:** Build, Validate, Scale

**Time to fix:** 20 minutes

### 4. Linting

**What it checks:**
- Stack-appropriate linter installed: ruff/pylint (Python), ESLint (JavaScript), clippy (Rust), golangci-lint (Go), SwiftLint (Swift)
- Linter config file exists (`.eslintrc.json`, `pyproject.toml[tool.ruff]`, `.clippy.toml`)
- Linter is executable and returns no violations
- Linter configured in CI (script or workflow step)
- Baseline score (if documented) is met

**Applicable phases:** Build, Validate, Scale

**Time to fix:** 30 minutes

### 5. Formatting

**What it checks:**
- Stack-appropriate formatter installed: Prettier (JavaScript), Black (Python), rustfmt (Rust), gofmt (Go)
- Formatter config file exists (`.prettierrc`, `pyproject.toml[tool.black]`)
- Pre-commit hook or CI format-check exists
- All tracked files pass formatting check
- Formatter auto-fixes do not produce warnings

**Applicable phases:** Build, Validate, Scale

**Time to fix:** 20 minutes

### 6. Testing

**What it checks:**
- Test directory structure exists (`tests/`, `spec/`, `__tests__/`, `test_*.py`)
- Test runner identified and configured (pytest, jest, cargo test, go test, rspec)
- Build manifest has `test` or `test:*` script
- Tests are executable and pass
- E2E or integration test suite exists (UI/backend projects only)
- Test coverage is >60% (optional; reports if present)

**Applicable phases:** Build, Validate, Scale

**Time to fix:** 4–8 hours (building the test suite, not installing)

### 7. Dependency Management

**What it checks:**
- Lock file present and committed (package-lock.json, uv.lock, Cargo.lock, go.sum, poetry.lock)
- Lock file matches current manifest (no drift)
- No unresolvable or yanked versions in lock file
- Transitive dependencies are declared and pinned
- `.npmrc`, `pip.ini`, or equivalent does not contain credentials

**Applicable phases:** All

**Time to fix:** 15 minutes

### 8. CI Pipeline

**What it checks:**
- GitHub Actions, GitLab CI, or equivalent workflow files exist (`.github/workflows/*.yml`, `.gitlab-ci.yml`)
- Workflow includes a lint step and it gates the build
- Workflow includes a test step and it gates the build
- Workflow has an artifact audit or SBOM step (Build phase)
- Workflow enforces deployment protection (Validate phase)
- Workflow runs on every PR and push
- No hardcoded secrets in workflow files

**Applicable phases:** Shape, Build, Validate, Scale

**Time to fix:** 45 minutes

### 9. Supply Chain Protection

**What it checks:**
- Dependabot or Renovate configured (`.github/dependabot.yml` or renovate.json)
- Dependency review action enabled (GitHub) or equivalent
- Lockfile integrity verified in pre-commit hooks
- SBOM generation step present in CI (Build phase)
- No dependency downgrades without documented justification
- Vulnerability sources configured (GitHub Advisory, OSV)

**Applicable phases:** Build, Validate, Scale

**Time to fix:** 30 minutes

### 10. Documentation

**What it checks:**
- README.md exists at repository root
- README has standard sections: Quick Start, Architecture, Contributing
- README has a "What is this?" section in first 100 words
- README includes a link to API reference or specification (if applicable)
- README documents any non-standard setup or prerequisites
- CONTRIBUTING.md exists (optional but recommended)
- Changelog or Release Notes file present (Build phase)

**Applicable phases:** Shape, Build, Validate, Scale

**Time to fix:** 1–2 hours

## Scoring

### Calculation

```
Phase-Aware Score = (checks_passed / checks_applicable) × 100%
```

Only checks flagged as applicable for the current phase count toward the denominator. A project in Discover phase that has no CI pipeline does not score lower for it; the CI check simply does not apply.

### Phase Applicability Matrix

| Check Category | Discover | Shape | Build | Validate | Scale |
|---|:---:|:---:|:---:|:---:|:---:|
| Security Foundations | ✓ | ✓ | ✓ | ✓ | ✓ |
| Pre-commit Hooks |: | ✓ | ✓ | ✓ | ✓ |
| Git Workflow |: |: | ✓ | ✓ | ✓ |
| Linting |: |: | ✓ | ✓ | ✓ |
| Formatting |: |: | ✓ | ✓ | ✓ |
| Testing |: |: | ✓ | ✓ | ✓ |
| Dependency Mgmt | ✓ | ✓ | ✓ | ✓ | ✓ |
| CI Pipeline |: | ✓ | ✓ | ✓ | ✓ |
| Supply Chain |: |: | ✓ | ✓ | ✓ |
| Documentation |: | ✓ | ✓ | ✓ | ✓ |

### Severity Mapping

Severity escalates by phase. A missing test suite is not a blocker in Shape (it warns) but becomes CRITICAL in Build (where tests are required).

| Finding Type | Discover | Shape | Build | Validate | Scale |
|---|---|---|---|---|---|
| Hardcoded secret | CRITICAL | CRITICAL | CRITICAL | CRITICAL | CRITICAL |
| No branch protection |: |: | CRITICAL | CRITICAL | CRITICAL |
| Missing test suite |: | Warning | CRITICAL | CRITICAL | CRITICAL |
| No CI pipeline |: | Warning | CRITICAL | CRITICAL | CRITICAL |
| No linter |: |: | Warning | Warning | Critical |
| Missing documentation |: | Warning | Warning | Warning | Warning |
| Outdated lock file | Warning | Warning | Warning | Critical | Critical |

## Input & Configuration

### Runtime Arguments

```bash
audit --repo <path> [--phase <phase>] [--deep] [--fix] [--json] [--gates]
```

**--repo <path>** (required)
Repository root directory.

**--phase <phase>** (optional)
Current engagement phase. Examples: Discover, Shape, Build, Validate, Scale (customize in `.audit.yaml`). Defaults to Build if not specified.

**--deep** (optional)
Enable extended scanning: entropy analysis on secret detection, dependency graph traversal, vulnerability database lookup. Adds 2–3 minutes to scan time.

**--fix** (optional)
Generate remediation templates and config skeletons. Writes to `./remediations/` directory.

**--json** (optional)
Output results in JSON format instead of Markdown. Useful for CI integration and dashboard consumption.

**--gates** (optional)
Report pass/fail against phase gates defined in `.gates.yaml`. Enables enforcement in CI pipelines.

**--dry-run** (optional)
Run the audit but do not write files. Displays what would be generated.

### Configuration File

Audit auto-detects and loads `.audit.yaml` from repository root (see canonical schema reference in `.audit.schema.yaml`):

```yaml
baseline:
  score_threshold: 75          # minimum passing score (0–100)
  critical_blocks_release: true # CRITICAL findings block CI merge
  phases: [<your-phase-1>, <your-phase-2>, <your-phase-3>, <your-phase-4>]  # customize your phases

phase_overrides:
  <your-phase-1>:
    score_threshold: 40
    skip_categories: [git-workflow, linting, formatting, ci-pipeline]
  
  <your-phase-2>:
    linting_warning_only: true  # linting failures warn, don't fail

stack_detection:
  primary_language: python
  frameworks: [fastapi, sqlalchemy]
  
# Custom checks added by the organization or project
custom_checks:
  - name: custom_logging_format
    description: "Verify log statements use org logging framework"
    command: "grep -r 'print\\|console.log' src/ | wc -l"
    expect_output_le: 5
    applicable_phases: [Build, Validate]
    severity: warning
    remediation: "Replace debug prints with org logger. See logging-guide.md"

auto_fix:
  generate_templates: true
  output_dir: ./remediations/
  overwrite: false  # don't replace existing templates
```

## Output Specification

### Report Structure (Markdown)

```markdown
# Repo Audit Report

**Repository:** [project-name]  
**Phase:** Build  
**Scan Date:** 2024-01-15  
**Overall Score:** 78% (7/9 checks passed)  
**Status:** ⚠ At-Risk

---

## Results by Category

### Security Foundations: PASS
- ✓ .gitignore present and comprehensive
- ✓ No hardcoded secrets found
- ✓ Git repository properly initialized

### Pre-commit Hooks: PASS
- ✓ .pre-commit-config.yaml detected
- ✓ detect-secrets hook installed

### Git Workflow: WARNING
- ✓ Staging branch exists
- ⚠ Branch protection not configured on main
  - **Remediation:** Run branch-protection setup script
  - **Time:** 10 minutes
- ✓ Commit signing configured

### Testing: CRITICAL
- ✗ No test suite found
  - **Remediation:** Create tests/test_*.py files
  - **Time:** 4–8 hours
  - **Details:** No test runner detected in CI or build manifest

### [More categories...]

---

## Remediation Steps (Priority Order)

### 1. CRITICAL: Establish Test Suite: 4–8 hours
The repository has no automated tests. A test suite is required before Build phase.

**Steps:**
1. Create `tests/` directory
2. Install test framework: `pip install pytest`
3. Write tests for core functionality (minimum 60% coverage)
4. Add `test` step to CI pipeline
5. Verify tests pass locally and in CI

**Template:** See `remediations/test-skeleton.py`

### 2. WARNING: Configure Branch Protection: 10 minutes
Branch protection is not enabled on the main branch.

**Command:**
```bash
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

### [More remediation steps...]

---

## Gate Status

**Phase Gate Check:** shape_to_build  
**Status:** ⚠ Cannot Advance  
**Reason:** CRITICAL findings must be resolved before Build phase entry

---
```

### Export Formats

**Markdown** (default)
Human-readable HTML-compatible report.

**JSON** (--json flag)
Structured data for CI tooling and dashboards:
```json
{
  "repository": "my-project",
  "phase": "Build",
  "scan_date": "2024-01-15",
  "score": 78,
  "passed": 7,
  "applicable": 9,
  "status": "at_risk",
  "categories": {
    "security": {"status": "pass", "findings": []},
    "testing": {"status": "critical", "findings": [{"title": "No test suite...", "severity": "CRITICAL"}]}
  },
  "gate_status": {"name": "shape_to_build", "status": "fail", "blocking_findings": ["No test suite"]}
}
```

## Auto-Fix Capabilities

### Can Generate

Audit can write templates and config files:

- `.pre-commit-config.yaml` (auto-detect stack and populate hooks)
- Linter configs (`.eslintrc.json`, `pyproject.toml[tool.ruff]`, `.clippy.toml`)
- Formatter configs (`.prettierrc`, `pyproject.toml[tool.black]`)
- GitHub Actions workflow (`.github/workflows/ci.yml`)
- `.gates.yaml` (default phase gates for your repo)
- `.editorconfig` (language-agnostic formatting rules)
- Improved `.gitignore` (stack-specific patterns)
- Branch protection CLI commands
- Dependabot config (`.github/dependabot.yml`)
- README skeleton (Quick Start, Architecture, Contributing sections)
- Test skeleton (test_*.py, test_*.js, etc. with sample structure)

### Cannot Auto-Fix

- Test code (generates skeleton only; you write assertions)
- CVE patches (recommends versions and links only)
- Branch protection (offers `gh api` command; requires manual approval)
- Secrets removal from history (recommends tools: git-filter-repo, BFG Repo-Cleaner)
- Linter/formatter fixes (recommends running: `ruff --fix`, `black .`)

## Execution Model

### Phase Progression

Each phase builds on the prior one. Audit runs independently at each phase transition, and findings escalate in severity:

- **Discover:** Only security and dependency checks apply. Tests and CI are informational.
- **Shape:** CI pipeline and documentation required. Linting/formatting are warnings.
- **Build & beyond:** Full rigor. All 10 check categories apply with CRITICAL severity on failures.

### CI Integration

Audit runs after dependency install in CI pipeline:

1. **Install audit tool** (dependency or pre-built binary)
2. **Run audit** with `--phase [branch]` flag
3. **Export results** as JSON artifact
4. **Block merge if `--gates` status is FAIL**
5. **Report findings** as PR comment or artifact

## Error Handling

### Missing Configuration

- **No `.audit.yaml`:** Use built-in defaults (score_threshold: 75, all checks enabled)
- **Phase not specified:** Default to Build
- **Stack detection fails:** Log warning, run language-agnostic checks only
- **Check dependency missing (e.g., linter not installed):** Skip that check category with WARNING

### Partial Failures

- **Check timeout (30s):** Skip that check and note in output
- **Linter crashes:** Report linter is broken, do not pass/fail the check
- **CI API rate limit:** Use cached results or skip rate-limited checks
- **Git command fails:** Skip Git-dependent checks; audit still completes

## Extension Points

### Custom Check Registration

Add checks via `.audit.yaml`:

```yaml
custom_checks:
  - name: api_schema_validation
    description: "Validate OpenAPI spec is well-formed"
    command: "npm run validate:schema"
    applicable_phases: [Build, Validate, Scale]
    severity: warning
    remediation: "Run `npm run validate:schema` to fix errors"
```

### Custom Remediation Templates

Place Markdown files in `.audit/remediations/`:

```markdown
# [Check Name] Remediation

## Steps

1. First action
2. Second action

## Command

\`\`\`bash
[your command here]
\`\`\`
```

### Phase-Specific Rulesets

Extend applicability via project config:

```yaml
phase_rules:
  Discover:
    enabled_categories: [security, dependency-mgmt]
  Scale:
    additional_checks: [performance-baseline, documentation-completeness]
```

## Cross-File Reference

- **README.md**: Quick start, sample findings, CI/CD integration, exit codes
- **CUSTOMIZE.md**: Configuration guide, tool selection, custom checks, phase-specific rules
