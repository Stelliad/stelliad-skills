# Coverage Analysis: Customization Guide

> **There is no coverage-gaps binary.** This skill is a specification an agent
> executes. The config below is real: you create it, and the agent reads it.
> The the command invocations in this guide are the spec's vocabulary for the
> options, not something on your PATH and not a package to install.
> See [README.md](./README.md) for how to invoke it.

## Overview

The Coverage Analysis skill ships with sensible defaults for a typical development team building a web or backend application. This guide walks through eight key areas you must adapt to match your specific project, risk profile, and organizational standards.

**Time to customize**: 30-60 minutes for an initial setup. Revisit every 6-12 months as your codebase and risk landscape evolve.

---

## 1. Language & Framework Detection

**What to customize**: Teach the skill which programming languages and testing frameworks your project uses.

### Questions to answer

- What languages does your codebase include? (JavaScript, Python, Go, Java, Ruby, C#, Rust, etc.)
- Are you in a monorepo with multiple languages?
- Does your project use non-standard file naming for tests? (e.g., `mytest.js` instead of `my.test.js`)
- Are tests co-located with source (`src/auth.ts` and `src/auth.test.ts` in same folder) or separated (`src/auth.ts` and `tests/auth.test.ts`)?
- Which test runners do you use? (Jest, Vitest, pytest, pytest-xdist, Go test, RSpec, Minitest, JUnit, xUnit)
- Do you use E2E testing? Which framework? (Playwright, Cypress, Selenium, WebdriverIO)
- Where is coverage configuration stored? (package.json, pyproject.toml, jest.config.js, .coveragerc, etc.)

### Configuration template

```yaml
# Detect these file patterns as source code
source_patterns:
  javascript: ["*.js", "*.jsx", "*.ts", "*.tsx", "*.mjs"]
  python: ["*.py"]
  go: ["*.go"]
  ruby: ["*.rb"]

# Detect these patterns as test files
test_patterns:
  javascript: ["*.spec.ts", "*.spec.js", "*.test.ts", "*.test.js", "__tests__/**"]
  python: ["test_*.py", "*_test.py", "tests/**"]
  go: ["*_test.go"]
  ruby: ["*_spec.rb"]

# E2E test discovery
e2e_patterns:
  - "e2e/**"
  - "playwright/**"
  - "cypress/e2e/**"
  - "**.e2e.ts"
  - "**.e2e.js"

# Test runners to detect
test_runners:
  - name: "jest"
    command: "npm test"
    config_files: ["jest.config.js", "jest.config.json"]
  - name: "vitest"
    command: "npm run test"
    config_files: ["vitest.config.ts"]
  - name: "pytest"
    command: "pytest"
    config_files: ["pyproject.toml", "pytest.ini", "setup.cfg"]

# Coverage tool configuration
coverage:
  tool: "vitest coverage"  # or "pytest-cov", "istanbul", "coverage.py"
  output_format: "json"    # or "lcov", "cobertura"
  report_location: "coverage/"
```

### Example: Monorepo with TypeScript and Python

```yaml
source_patterns:
  typescript: ["apps/**/*.ts", "apps/**/*.tsx", "packages/**/*.ts"]
  python: ["backend/**/*.py"]

test_patterns:
  typescript: ["apps/**/*.spec.ts", "packages/**/*.test.ts", "tests/**"]
  python: ["backend/tests/**", "backend/**/test_*.py"]

test_runners:
  - name: "vitest"
    command: "npm run test:coverage"
  - name: "pytest"
    command: "cd backend && pytest --cov"
```

---

## 2. Risk Classification

**What to customize**: Define what "critical," "high," "medium," and "low" mean for your specific domain and business.

### Default risk levels

| Category | Examples | Risk Level |
|----------|----------|-----------|
| Auth & security | Login, token validation, OAuth, encryption, access control | CRITICAL |
| Data handling | User input validation, SQL injection prevention, XSS protection | CRITICAL |
| Compliance | GDPR deletion, data retention, audit logging, PII masking | CRITICAL |
| Data mutations | Create, update, delete operations, bulk operations | HIGH |
| Business logic | Pricing, discounts, calculations, workflows | HIGH |
| Error handling | Exception handling, error messages, recovery paths | HIGH |
| User workflows | Sign-up, checkout, search, filtering, sorting | MEDIUM |
| UI state | Loading states, error states, empty states | MEDIUM |
| Navigation | Routing, page transitions, redirects | MEDIUM |
| Utilities | Formatters, parsers, type wrappers, helpers | LOW |
| Constants | Configuration values, static data | LOW |

### Questions to answer for your domain

- **Healthcare**: Do you handle PHI (Protected Health Information)? Upgrade `data-handling/`, `pii/`, and `compliance/` to CRITICAL.
- **Finance**: Do you handle payments or PCI-DSS data? Upgrade `payments/`, `billing/`, and `audit-logging/` to CRITICAL.
- **Child-oriented**: Do you serve users under 13? Upgrade `auth/`, `data-handling/`, and `tracking/` to CRITICAL under COPPA.
- **Regulated industry**: What audit or compliance frameworks apply? (SOC 2, ISO 27001, HIPAA, GDPR) Add those modules to CRITICAL.
- **High incident rate**: Which code areas have caused the most production incidents? Upgrade those to the next risk level.

### Risk remapping template

```yaml
# Upgrade specific modules to higher risk levels
risk_overrides:
  CRITICAL:
    - "src/auth/**"           # Authentication
    - "src/payments/**"       # Payment processing
    - "src/data-export/**"    # User data deletion
    - "src/compliance/**"     # Audit and compliance
    - "lib/crypto/**"         # Cryptography
    
  HIGH:
    - "src/users/**"          # User management (create/update/delete)
    - "src/api/**"            # API route handlers
    
  MEDIUM:
    - "src/ui/**"             # UI components
    - "src/formatting/**"     # Display formatters
    
# Downgrade specific modules to lower risk levels
  LOW:
    - "src/constants/**"
    - "lib/vendor/**"
```

---

## 3. Coverage Thresholds

**What to customize**: Set realistic coverage targets for each risk level based on your team's capacity and quality standards.

### Default recommendations

- **CRITICAL**: 90%+ (no untested functions)
- **HIGH**: 80%+ (edge cases tested)
- **MEDIUM**: 70%+ (main flows tested)
- **LOW**: 60%+ (basic coverage)

### Questions to answer

- Does your organization need accountability for coverage targets?
- Do you have internal audit or compliance requirements for code quality?
- What is your historical incident rate in each code area? Use that to inform targets.
- What coverage gaps have caused production incidents in the past?
- Is your team's capacity 10 new tests per sprint, or 100?
- Is coverage an aspirational metric or a gating requirement?

### Realistic targets by maturity

| Maturity | CRITICAL | HIGH | MEDIUM | LOW |
|----------|----------|------|--------|-----|
| Pre-launch startup | 85%+ | 70%+ | 50%+ | 30%+ |
| Scaling (6-24 months) | 90%+ | 80%+ | 60%+ | 40%+ |
| Enterprise/regulated | 95%+ | 90%+ | 80%+ | 70%+ |

### Configuration template

```yaml
coverage_thresholds:
  critical:
    target: 90
    acceptable: 85
    warning: 80
  high:
    target: 80
    acceptable: 75
    warning: 70
  medium:
    target: 70
    acceptable: 65
    warning: 60
  low:
    target: 60
    acceptable: 55
    warning: 50

# Enforce these thresholds in CI
ci_gating:
  block_pr_if_coverage_drops: true
  block_pr_if_critical_untested: true
  publish_report_to: "codecov"  # or "codeclimate", "sonarqube"
```

---

## 4. Test Quality Checks

**What to customize**: which hollow-test heuristics run, how hard they land, and
what counts as a legitimate exception in your codebase. These checks are
heuristics executed without a human in the loop, so tune them before you trust
their findings.

```yaml
test_quality:
  enabled: true

  checks:
    zero_assertions:        {enabled: true,  severity: high}
    empty_test_block:       {enabled: true,  severity: high}
    single_assertion_file:  {enabled: true,  severity: medium}
    skipped_but_counted:    {enabled: true,  severity: medium}
    assertions_only_on_mock:
      enabled: true
      severity: medium
      # Paths where a call-count assertion is the correct test, not a gap.
      # Event dispatch and fire-and-forget publishing have no return value.
      exempt_paths:
        - "src/events/"
        - "src/webhooks/"

  # Assertion helpers this codebase actually uses. Match these, not the word
  # "expect", or every chai and node:assert suite reports as hollow.
  assertion_helpers:
    javascript: ["expect", "assert", "should", "t.is", "t.deepEqual"]
    python:     ["assert", "assertEqual", "assertRaises", "pytest.raises"]
    go:         ["t.Error", "t.Fatal", "require.", "assert."]
    ruby:       ["expect", "should", "assert"]

  # Files under a test path that legitimately contain no tests.
  support_module_globs:
    - "conftest.py"
    - "__init__.py"
    - "**/factories*"
    - "**/fixtures*"
    - "**/helpers*"
    - "**/*utils*"
```

### Questions to answer

1. **Does your codebase have event dispatch or fire-and-forget publishing?** If so, list those paths under `exempt_paths` before enabling `assertions_only_on_mock`, or expect noise.
2. **Which assertion library do you actually use?** A project on chai or `node:assert` will report every suite as hollow until `assertion_helpers` names them.
3. **Do you keep factories or fixtures inside the test tree?** Add their glob to `support_module_globs` so they are not flagged as test files with no tests.
4. **Are snapshot tests acceptable in your stack?** Some teams use them deliberately for design-system regressions. Disable the snapshot-only signal if that is a considered position rather than an accident.

---

## 5. Excluded Directories & Files

**What to customize**: Teach the skill which code directories to skip (generated code, vendored dependencies, configuration).

### Default exclusions

```yaml
excluded_directories:
  - "node_modules/"
  - ".venv/"
  - "vendor/"
  - "dist/"
  - "build/"
  - "coverage/"
  - ".pytest_cache/"
  - ".git/"
  - ".vscode/"
  - "htmlcov/"
  - ".nyc_output/"
```

### Add project-specific exclusions

```yaml
excluded_directories:
  # Default exclusions (keep these)
  - "node_modules/"
  - ".venv/"
  - "vendor/"
  - "dist/"
  
  # Generated code (do not test)
  - "src/generated/"
  - "src/gql/generated/"
  - "backend/migrations/"
  
  # Configuration (not source code)
  - "config/"
  - "scripts/"
  
  # Third-party SDKs
  - "lib/third-party/"
  
  # Old/deprecated code
  - "src/legacy/"
  - "_old/"
```

### Questions to answer

- What directories contain generated code? (GraphQL schema, protocol buffers, ORMs)
- What directories contain configuration only, not source code?
- Do you have a `lib/` or `vendor/` directory with third-party code?
- Are there deprecated or legacy directories that should be skipped?

---

## 6. E2E Route Discovery

**What to customize**: Teach the skill how routes are defined in your application (Express, FastAPI, Next.js, GraphQL, etc.).

### Route definition patterns by framework

**Express.js**:
```javascript
// routes/users.js
router.post('/api/users', authenticate, validate, createUser);
router.get('/api/users/:id', authenticate, getUser);
```
Skill should parse `routes/` folder and look for `router.post`, `router.get`, etc.

**Next.js App Router**:
```
app/
  api/
    users/
      route.ts         // POST /api/users
      [id]/
        route.ts       // GET /api/users/[id]
```
Skill should map file structure to routes.

**FastAPI**:
```python
@app.post("/api/users")
def create_user(user: UserCreate):
    pass

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    pass
```
Skill should parse decorators.

**GraphQL**:
```
schema.graphql
  type Query
    user(id: ID!): User
    users: [User!]!
  type Mutation
    createUser(input: CreateUserInput!): User
```
Skill should parse schema file.

### Configuration template

```yaml
route_discovery:
  framework: "express"  # or "fastapi", "next", "graphql"
  
  # Express/Koa
  router_files: ["src/routes/**/*.ts", "src/api/**/*.ts"]
  route_pattern: "router\\.(get|post|put|patch|delete)\\('([^']+)'"
  
  # Next.js
  app_directory: "app/"
  
  # FastAPI
  decorators: ["@app.get", "@app.post", "@app.put", "@app.delete"]
  
  # GraphQL
  schema_file: "schema.graphql"
  
  # Protected routes (require authentication)
  protected_patterns:
    - "/admin/**"
    - "/api/users/**"
    - "/api/billing/**"
```

### Critical user workflows

Map the flows your business depends on:

```yaml
critical_workflows:
  authentication:
    name: "Sign up and log in"
    routes:
      - "POST /api/auth/signup"
      - "POST /api/auth/login"
      - "POST /api/auth/logout"
    priority: "CRITICAL"
    
  payment:
    name: "Create subscription"
    routes:
      - "POST /api/subscriptions"
      - "GET /api/subscriptions"
      - "PUT /api/subscriptions/:id"
    priority: "CRITICAL"
    
  data_export:
    name: "User downloads their data"
    routes:
      - "POST /api/exports"
      - "GET /api/exports/:id/download"
    priority: "HIGH"
```

---

## 7. Risk Override Examples

**What to customize**: Flag specific modules and functions as higher or lower risk based on your incident history and domain.

### Template by incident type

After a production incident, upgrade related code to reflect the risk:

```yaml
# After an incident in a specific module
incident_based_overrides:
  "<date> <incident-name>":
    files: ["<affected-file-1>", "<affected-file-2>"]
    new_risk: "CRITICAL"
    reason: "<brief description of what happened>"
```

**Examples:**
- "2024-01-15 Race condition in billing" → Upgrade `src/billing/**` to CRITICAL
- "2024-02-03 XSS in user-generated content" → Upgrade `src/profiles/display.**` to CRITICAL
- "2024-03-10 Authentication bypass" → Upgrade `src/auth/**` to CRITICAL

### Custom thresholds for specific modules

```yaml
module_thresholds:
  "src/auth/**":
    risk: "CRITICAL"
    coverage_target: 95
    coverage_acceptable: 90
    
  "src/ui/components/**":
    risk: "MEDIUM"
    coverage_target: 60
    coverage_acceptable: 50
```

---

## 8. CI/CD Integration

**What to customize**: Integrate the audit into your continuous integration pipeline so coverage trends are tracked and gates are enforced.

### Configuration template

```yaml
ci_integration:
  platform: "github-actions"  # or "gitlab-ci", "jenkins", "circleci"
  
  test_execution:
    command: "npm run test:coverage"
    timeout_minutes: 15
    
  coverage_reporting:
    # Upload to external service
    upload_to: "codecov"  # or "codeclimate", "sonarqube"
    report_file: "coverage/coverage-final.json"
    
    # Publish in PR
    comment_on_pr: true
    show_diff_only: false
    
  gates:
    # Fail the build if coverage drops
    fail_if_coverage_drops: true
    fail_if_critical_untested: true
    
    # Minimum thresholds
    minimum_coverage: 75
    critical_minimum: 85
```

### GitHub Actions example

```yaml
name: Test & Coverage
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests with coverage
        run: npm run test:coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
```

### Questions to answer

- Does your CI system run tests on every commit and PR?
- Are coverage reports published to a dashboard or comment?
- Does a coverage drop block the PR or build?
- Who is notified when coverage falls below threshold?

---

## 9. Audit Frequency & Retention

**What to customize**: Define how often the audit runs and how long to keep historical reports.

### Configuration template

```yaml
audit_schedule:
  # Run automatically on a schedule
  frequency: "weekly"  # or "daily", "monthly"
  day_of_week: "monday"
  time: "02:00 UTC"
  
  # Or run manually when triggered
  manual_trigger: true

audit_retention:
  # Keep historical reports for trend analysis
  keep_for_days: 90
  archive_location: "s3://coverage-reports/"
  
audit_comparison:
  # Compare to previous run
  compare_to: "1_week_ago"  # or "1_month_ago", "baseline"
  flag_regressions: true    # Alert if coverage dropped
  flag_improvements: true   # Report if coverage improved
```

---

## Integration Templates

### With project management (Jira, Linear, GitHub Issues)

```yaml
ticket_integration:
  create_tickets: true
  for_risk_levels: ["CRITICAL", "HIGH"]
  label: "test-gap"
  priority_mapping:
    CRITICAL: "P0 - Urgent"
    HIGH: "P1 - High"
    MEDIUM: "P2 - Medium"
  template: |
    # Write tests for [MODULE]
    
    **Risk**: CRITICAL
    **Impact**: [WHAT BREAKS]
    
    ## Test cases to add
    - [Case 1]
    - [Case 2]
    
    **Effort**: [Hours]
```

### With code review

```yaml
code_review_policy:
  # Flag new code without tests in review
  comment_on_untested_code: true
  block_merge_if_critical_untested: true
  
  # Request tests for fixes
  request_regression_test_on_fix: true
  
  # Acknowledge good coverage
  praise_high_coverage: true
```

### With incident management

```yaml
incident_integration:
  # After incident, add tests
  add_regression_test_to_ticket: true
  verify_coverage_in_affected_code: true
  require_test_before_close: true
```

## Cross-File Reference

- **README.md**: Quick start, setup, example output, at-a-glance overview
- **SPEC.md**: Technical architecture, three audit layers, risk prioritization, coverage semantics, output structure
