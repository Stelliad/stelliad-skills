# Repo Audit: Customization Guide

> **There is no repo-audit binary.** This skill is a specification an agent
> executes. The config below is real: you create it, and the agent reads it.
> The `audit` invocations in this guide are the spec's vocabulary for the
> options, not something on your PATH and not a package to install.
> See [README.md](./README.md) for how to invoke it.

## Overview

Repo Audit ships with sensible defaults for common tech stacks (Python, JavaScript, Go, Rust, Java). This guide covers adapting Repo Audit to your organization's standards, tooling preferences, and enforcement policies.

Customization happens at three levels: organization-wide baselines, project-specific overrides, and runtime flags.

## Organization-Level Customization

### 1. Define Your Baseline Standard

Create `.audit.baseline.yaml` and store it in a shared standards repository. This file defines requirements across all repos:

```yaml
organization_name: [Your Organization]
version: "1.0"
effective_date: 2024-01-01

requirements:
  all_phases:
    security_required: true
    gitignore_required: true
    dependency_lockfile_required: true
  
  shape_and_later:
    ci_pipeline_required: true
    documentation_required: true
  
  build_and_later:
    linting_required: true
    formatting_required: true
    testing_required: true
    pre_commit_hooks_required: true

phase_thresholds:
  Discover:
    pass_score: 40  # Only security and dependencies matter
    critical_blocks_advance: true
  
  Shape:
    pass_score: 60  # Add CI & docs to the mix
    critical_blocks_advance: true
  
  Build:
    pass_score: 80  # Full rigor expected
    critical_blocks_advance: true
  
  Validate:
    pass_score: 85
    critical_blocks_advance: true
  
  Scale:
    pass_score: 90
    critical_blocks_advance: true

tool_priorities:
  python:
    linter: ruff        # not pylint or flake8
    formatter: black
    test_runner: pytest # not unittest
    dependency_mgmt: uv
  
  javascript:
    linter: eslint
    formatter: prettier
    test_runner: jest
    dependency_mgmt: npm
  
  go:
    linter: golangci-lint
    formatter: gofmt
    test_runner: go test
    dependency_mgmt: go modules
```

**Usage:**
```bash
# In CI, fetch shared baseline
curl -s https://[internal-standards-repo]/.audit.baseline.yaml > .audit.baseline.yaml
audit --repo . --baseline .audit.baseline.yaml
```

### 2. Stack-Specific Tool Selection

Override tool detection in project `.audit.yaml`:

```yaml
stack:
  language: python
  frameworks: [fastapi, sqlalchemy]
  minimum_version: "3.9"

tool_choices:
  linter: ruff
  formatter: black
  test_runner: pytest
  ci_platform: github-actions
  dependency_manager: uv

# Audit will verify these tools exist and are configured correctly
```

This tells Audit to expect ruff (not pylint), black (not autopep8), and pytest (not unittest) when auditing this repository.

### 3. Custom Check Inclusion

Add organization-specific checks that all repos must satisfy:

```yaml
custom_checks:
  - category: compliance
    name: copyright_header_check
    description: "All source files must carry copyright header"
    command: |
      FILES_WITHOUT_HEADER=$(find src -type f \( -name "*.py" -o -name "*.js" \) \
        | xargs grep -L "Copyright (c) [Your Organization]" 2>/dev/null | wc -l)
      [ "$FILES_WITHOUT_HEADER" -eq 0 ]
    expect_exit_code: 0  # exit 0 when all files have copyright header
    applicable_phases: [Shape, Build, Validate, Scale]
    severity: warning
    remediation: "Run ./scripts/add-headers.sh to add copyright headers"

  - category: architecture
    name: no_direct_db_queries_in_handlers
    description: "API handlers must use repository/service layer"
    command: |
      grep -r "execute\\|query\\|sql" src/handlers/ 2>/dev/null | wc -l
    expect_output_le: 3  # Allow 3 matches (imports, type hints only)
    applicable_phases: [Build, Validate, Scale]
    severity: warning

  - category: security
    name: ai_off_switch
    description: "A repo that calls a model can disable every model call with one flag"
    command: |
      git grep -qIE \
        'anthropic|openai|bedrock-runtime|invoke_model|sagemaker-runtime|ollama|vllm|generativeai' \
        -- ':!*.md' ':!*.lock'
      case $? in
        1) exit 0 ;;   # no inference in this repo, nothing to switch off
        0) ;;          # calls a model, carry on to the flag
        *) echo "detection could not read this repo"; exit 1 ;;
      esac
      git grep -q AI_ENABLED -- ':!*.md' ':!.gates.yaml' ':!.audit.yaml'
    expect_exit_code: 0
    applicable_phases: [Build, Validate, Scale]
    severity: warning
    remediation: "One flag, read once at the configuration boundary, that disables every model call and every agent tool action. Default it on, resolve it per request so a flip needs no deploy, and define what the user gets while it is off."

  - category: security
    name: no_plaintext_credentials_in_config
    description: "Configuration files must not contain real credentials"
    command: |
      grep -r "password\|api_key\|secret" config/ \
        | grep -v "\[PLACEHOLDER\]" | wc -l
    expect_output_le: 0
    applicable_phases: [All]
    severity: critical
    remediation: "Replace all credentials with [PLACEHOLDER] or environment variables"
```

**Why the AI off switch is a custom check and not an eleventh category.** The
phase applicability matrix in `SPEC.md` derives `checks_applicable` from the
phase alone, so a core category applies to every repo at that phase. Most repos
call no model, and a category they can never satisfy would score them down for
a control they do not need. A custom check can carry its own condition, which
is what the first two lines of that command are doing: no inference found, exit
0, nothing to switch off.

Three things about it are deliberate:

- **Detection is wider than one SDK name.** The paths that get missed are the
  ones that do not import the obvious package: a Bedrock streaming client, a
  self-hosted model behind a base URL, an embeddings call that generates no
  text. Widen the pattern to whatever your stack actually reaches for.
- **The exclusions decide what counts.** Without them the check matches the
  README that documents the flag and the `.audit.yaml` that declares the check,
  so a repo with no flag passes on the mention.
- **An error is not an answer.** `git grep` exits 1 for "no match" and 128 for
  "could not read this repo", and a detection that redirects stderr and counts
  lines cannot tell them apart. It reports no inference either way and the
  check passes. That is a security check failing open, and it is not
  hypothetical: this recipe was first written with `2>/dev/null | wc -l` and
  tested green against a repo full of Bedrock calls whose clone had
  `core.bare = true`. Branch on the exit status instead.
- **Presence is all a grep can prove.** Whether the flag is resolved per
  request rather than at import, whether it stops a provider fallback chain
  instead of failing over, and whether anyone has ever flipped it are questions
  a command cannot answer. They belong with the Limitations section in
  `SPEC.md`, and they are the part a person has to check.

### 4. Gate Integration

Link audit findings to phase advancement gates in `.gates.yaml`:

```yaml
gates:
  discover_to_shape:
    - gate: audit_baseline
      config:
        phase: Shape
        min_score: 60
        block_on_critical: true
        checks_to_pass:
          - security_foundations
          - dependency_management

  shape_to_build:
    - gate: audit_baseline
      config:
        phase: Build
        min_score: 80
        block_on_critical: true
        checks_to_pass:
          - all_10_categories

  build_to_validate:
    - gate: audit_baseline
      config:
        phase: Validate
        min_score: 85
```

When a phase gate runs, it calls `audit --repo . --phase [next_phase] --gates` and fails the gate if any CRITICAL findings exist or the score falls below the threshold.

## Project-Level Customization

### 1. Language/Framework Detection Override

Some projects don't follow conventions. Hint to Audit:

```yaml
# .audit.yaml (project root)
stack_detection:
  primary_language: go
  secondary_languages: [python]  # for Makefiles, build scripts
  frameworks:
    - microservice
    - grpc
  skip_detection: false

detect_from:
  - go.mod
  - Makefile
  - Dockerfile
```

### 2. Exemptions & Waivers

Temporarily exclude checks or mark them as not applicable:

```yaml
exemptions:
  - check: test_coverage_60_percent
    reason: "Proof of concept; coverage waived until Build phase"
    waived_until: 2024-12-31
    approved_by: tech_lead

  - check: formatting_consistency
    reason: "Third-party code in vendor/; not reformatted"
    path_pattern: "vendor/**"
    severity_override: info  # Report but don't fail

  - check: e2e_test_suite
    reason: "Backend service only; no UI to test"
    applicable_phases: []  # Remove from all phases
```

### 3. Modified Remediation Templates

Override default templates with project-specific guidance:

Create `.audit/remediations/linting-config.md`:

```markdown
# Linting Configuration for [This Project]

## Our setup

This project uses ruff for linting. Configuration is in `pyproject.toml`.

## To fix violations

1. Review the error: `ruff check src/`
2. Auto-fix where possible: `ruff check --fix src/`
3. Manual fixes for rule violations (see per-rule guidance below)
4. Commit with message: "fix: resolve linting violations"

## Custom rules for this project

We enforce:
- No imports except at module top
- Line length: 100 characters (not 88)
- docstrings on all public functions

See `docs/code-standards.md` for rationale.
```

Audit uses this template when generating remediation output instead of the generic default.

### 4. CI/CD Integration Path

Map Audit to your CI platform and define failure modes:

```yaml
# .audit.yaml
ci:
  platform: github-actions  # or gitlab-ci, circleci, azure-pipelines

  on_critical_finding:
    action: block_merge      # or notify, log, or report-only
    notify_channels:
      - slack: "#dev-alerts"
      - email: "tech-lead@[org].com"
    escalate_after_days: 3

  on_warning:
    action: report_comment   # Post comment on PR
    auto_resolve_in_days: 14 # Close comment after 2 weeks

  report_destinations:
    - artifact: "audit-report.json"
    - github_artifact: true
    - slack_thread: true
```

### 5. Dependency Audit Strictness

Configure how aggressive dependency checks are:

```yaml
dependencies:
  deny_unresolvable_versions: true
  deny_yanked_versions: true
  deny_pre_release_in_prod: true
  block_outdated_lockfile: true

  vulnerability_sources:
    - github      # GitHub Advisory Database
    - osv         # OSV (Open Source Vulnerabilities)
    - snyk        # Snyk (requires SNYK_TOKEN env var)

  max_vulnerability_age_days: 7
  
  ignore_vulnerabilities:
    - CVE-2024-1234  # Known false positive; internal security review completed
    - GHSA-xxxx-yyyy # Third-party risk accepted; documented in SECURITY.md

  update_cadence: weekly  # Dependabot runs weekly
```

## Multi-Repository Organization

### 1. Shared Baseline Across All Repos

Store `.audit.baseline.yaml` in a central standards repository:

```bash
# Central repo
/org-standards/
  ├── .audit.baseline.yaml
  ├── .pre-commit-config.yaml
  └── README.md

# In each project repo, fetch at CI time
BASELINE_URL="https://raw.githubusercontent.com/[org]/standards/main/.audit.baseline.yaml"
curl -s $BASELINE_URL > .audit.baseline.yaml
audit --repo . --baseline .audit.baseline.yaml --gates
```

Or use symlinks on local machines:
```bash
ln -s ../../org-standards/.audit.baseline.yaml .audit.baseline.yaml
```

### 2. Org-Wide Reporting

Collect audit results across all repositories:

```bash
#!/bin/bash
# scan-all-repos.sh

OUTPUT_DIR="./audit-results/"
mkdir -p $OUTPUT_DIR

# Scan each repo
for repo_dir in $(find . -name ".git" -type d | head -20); do
  repo=$(dirname $repo_dir)
  echo "Scanning $repo..."
  audit --repo $repo --json > "$OUTPUT_DIR/$(basename $repo).json"
done

# Results are now aggregated in $OUTPUT_DIR/*.json
# Process with your organization's reporting or dashboard tools
```

## Troubleshooting Customizations

### Check Not Running

**Problem:** Custom check defined but not executing

**Solutions:**
1. Verify phase applicability: `applicable_phases: [Build, Validate]`
2. Test the command manually: `eval "find src -name '*.py' | wc -l"`
3. Check for typos in check name and command
4. Confirm `.audit.yaml` is valid YAML: `python -m yaml .audit.yaml`

### False Positives

**Problem:** Check flagging issues that aren't real

**Solutions:**
1. Add path exclusion: `path_pattern: "!vendor/**"`
2. Adjust regex or threshold: `expect_output_le: 100`
3. Add exemption with waiver reason
4. Modify command to be more specific

### Remediation Template Not Used

**Problem:** Audit generates default remediation, not your custom one

**Solutions:**
1. Verify file location: `.audit/remediations/[check-name].md`
2. Verify filename matches check name exactly
3. Check YAML frontmatter format (if used)
4. Test template rendering: `audit --repo . --fix --dry-run`

## Examples by Industry

### Example 1: Financial Services (Strict)

```yaml
# Prioritizes security and auditability
baseline:
  score_threshold: 90
  critical_blocks_release: true

requirements:
  all_phases:
    security_required: true
    lockfile_required: true

custom_checks:
  - name: pii_not_in_logs
    command: "grep -r 'log\\|print' src/ | grep -i 'email\\|ssn\\|account' | wc -l"
    expect_output_le: 0
    severity: critical
    applicable_phases: [all]

  - name: encryption_used
    command: "grep -r 'https://\\|tls\\|encrypt' config/ | wc -l"
    expect_output_ge: 5
    severity: critical

  - name: audit_logging_present
    command: "grep -r 'audit_log\\|security_log' src/ | wc -l"
    expect_output_ge: 3
    severity: warning
    applicable_phases: [Build, Validate, Scale]
```

### Example 2: Open Source Library (Community)

```yaml
# Emphasizes documentation and contribution process
baseline:
  score_threshold: 70

phase_thresholds:
  Discover:
    pass_score: 50
  Shape:
    pass_score: 60  # Lenient; community moves at own pace

custom_checks:
  - name: changelog_updated
    command: "head -20 CHANGELOG.md | grep -q $(git describe --tags | head -1)"
    expect_exit_code: 0
    severity: warning
    applicable_phases: [Scale]

  - name: contributing_guide_exists
    command: "test -f CONTRIBUTING.md && wc -l CONTRIBUTING.md | awk '{if($1>100) exit 0; else exit 1}'"
    expect_exit_code: 0
    severity: warning
    applicable_phases: [Build, Validate, Scale]

  - name: license_file
    command: "test -f LICENSE"
    expect_exit_code: 0
    severity: warning
    applicable_phases: [all]
```

### Example 3: Startup MVP (Speed-First)

```yaml
# Minimal Discover, builds rigor as product matures
baseline:
  score_threshold: 40  # Low bar to ship fast

phase_thresholds:
  Discover:
    pass_score: 20  # Almost anything goes
  Shape:
    pass_score: 40
  Build:
    pass_score: 70  # Rigor increases here
  Validate:
    pass_score: 80
  Scale:
    pass_score: 85

# Few custom checks; focus on shipped product
custom_checks:
  - name: can_deploy
    command: "test -f scripts/deploy.sh && [[ -x scripts/deploy.sh ]]"
    expect_exit_code: 0
    severity: critical
    applicable_phases: [Build, Validate, Scale]
    remediation: "Create scripts/deploy.sh and make it executable"
```

## Cross-File Reference

- **README.md**: Quick start, sample findings, CI/CD integration, exit codes
- **SPEC.md**: Technical architecture, 10 check categories, scoring model, output specification
