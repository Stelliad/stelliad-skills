# Coverage Analysis Skill Specification

## Overview

The Coverage Analysis skill audits test coverage across unit tests, end-to-end flows, and infrastructure tooling. It operates across three distinct layers of a codebase, identifies gaps in test coverage, prioritizes findings by business risk, and recommends specific, actionable tests in priority order.

**Purpose**: Enable development teams to systematically understand where tests are missing, prioritize which gaps matter most, and measure progress over time.

**Input**: Project directory path, source code language(s), test framework(s), and customization parameters for risk classification and thresholds.

**Output**: Structured audit report with executive summary, categorized gap analysis, risk-prioritized recommendations, and a concrete 5-10 item action list.

**Audience**: Development teams, QA leads, engineering managers, release managers.

---

## Three Audit Layers

### Layer 1: Unit Test Coverage

**Scope**: All source files, exported functions, and associated unit test files.

**Discovery process**:
1. Walk source directory tree recursively, identifying all files matching language patterns (`.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rb`, etc.)
2. Extract all exported functions, methods, and named exports from each source file
3. Walk test directory tree, matching test files to source files by naming convention (`*.spec.ts`, `*.test.js`, `test_*.py`, etc.)
4. For each source file, determine whether a corresponding test file exists
5. For each exported function, check whether it appears in the test file by name (simple text search)
6. If coverage reports exist (JSON, LCOV format), parse them to get exact coverage percentages per file

**Coverage detection**:
- Presence of test file: Yes/No
- Approximate function coverage (functions named in tests vs. total exports)
- Common edge cases missing from tests (null values, empty strings/arrays, boundary values, error conditions, state transitions)
- Coverage percentage per file (if available from coverage tool output)

**Gaps identified**:
- Files with no corresponding test file (high risk if the file exports critical functions)
- Exported functions that appear in source but not in test files
- Common edge cases that are likely untested (negative numbers, 0, empty collections, special characters, malformed input)
- Error paths and exception handling not exercised
- Coverage ratio per file (under-covered: below 70%, well-covered: 80%+)

**Output format**:
```
Unit Test Gaps
File: src/auth/token-validation.ts
Status: No test file found
Risk level: CRITICAL
Exported functions: validate(), refresh(), revoke()
Coverage: 0%
Suggested test file: src/auth/__tests__/token-validation.spec.ts
Key test cases to add:
  - Valid token passes validation
  - Expired token rejected with specific error
  - Malformed token (missing claims, invalid signature) rejected
  - Refresh token updates expiry time
  - Revoked token no longer validates
  - Token with null/empty claims rejected
```

---

### Layer 2: E2E and Integration Coverage

**Scope**: Routes (API endpoints, pages, navigation), critical user workflows, state management paths, form submission flows, and error scenarios.

**Discovery process**:
1. Identify route definitions by parsing framework-specific files:
   - Express/Koa: `routes/`, `api/` folders, or route registration files
   - Next.js: `app/` or `pages/` directory structure
   - FastAPI: Endpoint decorator analysis
   - GraphQL: Schema definition files
   - REST API: OpenAPI/Swagger spec if available
2. Extract list of all routes with HTTP method, path, and required authentication level
3. Walk E2E test directory for test files (`*.e2e.ts`, `e2e/`, `cypress/`, `playwright/`)
4. For each route, search test files for references to that path or test descriptions mentioning it
5. Identify critical user workflows (login → action → logout, payment flow, data export, etc.) from domain knowledge
6. Check whether each critical workflow has corresponding E2E tests

**Coverage detection**:
- Route has E2E test: Yes/No
- Test covers authenticated request: Yes/No (for protected routes)
- Test covers error case (network failure, 500 error, validation failure): Yes/No
- Test covers state transitions (loading → success, loading → error): Yes/No
- Route coverage percentage per API or page grouping

**Gaps identified**:
- Routes with no E2E tests
- Protected routes that don't test authentication/authorization (missing 401/403 scenarios)
- Routes that return lists/collections but don't test empty state
- Routes without error-case testing (network failures, validation errors)
- Critical user workflows (sign-up, payment, export) missing integration tests
- Form submission and validation paths not exercised
- Redirect and error page behavior untested

**Output format**:
```
E2E Coverage Gaps
Route: POST /api/users/create
Method: POST, Protected: Yes
Status: Partial coverage (50%)
Existing tests: Happy path only
Risk level: HIGH
Missing coverage:
  - Unauthenticated request returns 401
  - Duplicate email rejected with 409
  - Invalid email format rejected with 400
  - Validation errors return clear messages
  - Race condition if two users sign up simultaneously
Suggested test scenarios:
  1. Valid user creation succeeds
  2. Unauthenticated request denied
  3. Duplicate email causes 409 error
  4. Empty password field rejected
  5. Email validation fails for invalid format
```

---

### Layer 3: Infrastructure & Tooling

**Scope**: Test runner configuration, coverage collection, CI/CD integration, and test discoverability.

**Checks performed**:
1. **Test runner**: Is a test runner installed (Jest, Vitest, pytest, RSpec, Go test)? Can it be invoked from command line? Does `npm test` or equivalent work?
2. **Coverage tool**: Is a coverage collector installed (Istanbul, pytest-cov, coverage.py)? Is it configured to run automatically?
3. **Coverage reports**: Are coverage reports generated in a parseable format (JSON, LCOV, COBERTURA)? Can they be located?
4. **CI integration**: Does the CI pipeline (GitHub Actions, GitLab CI, Jenkins) run tests on every commit? Are coverage results published or accessible?
5. **Documentation**: Is the test command documented in README or contributing guide?
6. **Coverage gating**: Is coverage drop prevented at the PR or CI level?

**Output format**:
```
Infrastructure Status
Test Runner: Vitest (✓ configured)
  Command: npm run test
  Status: Runs successfully on sample test
  
Coverage Tool: @vitest/coverage-v8 (✓ installed)
  Format: JSON, LCOV
  Reports location: coverage/
  Status: Generates reports on test run
  
CI Integration: GitHub Actions (✓ configured)
  Pipeline file: .github/workflows/test.yml
  Status: Runs tests on push to main and PRs
  Coverage upload: Reports uploaded to Codecov
  
Setup Gaps:
  ⚠ Coverage threshold not enforced (no failure if coverage drops)
  ⚠ Coverage report not published in PR comments
```

---

## Risk Prioritization System

All findings are categorized by business and technical risk. This determines the order in which gaps should be addressed.

**Risk levels**:

| Level | Examples | Why it matters |
|-------|----------|---|
| CRITICAL | Authentication & authorization, cryptography, data validation, payment processing, access control, PII/sensitive data handling | A bug here compromises security or violates compliance. Cannot go to production untested. |
| HIGH | Data mutations (create, update, delete operations), core business logic, error handling, database transactions | A bug here loses data or breaks core workflows. Directly impacts production stability. |
| MEDIUM | User-facing workflows, form submission and state management, navigation and routing | A bug here degrades user experience but doesn't lose data or crash the system. Should be tested before release. |
| LOW | Utility functions, formatters, constants, type-safe wrappers around libraries, view logic without state | A bug here is usually caught by type checking or is low-impact. Test coverage is valuable but not urgent. |

**Customization**: Organizations working in healthcare (HIPAA), finance (PCI, regulatory), or child-oriented services (COPPA) should upgrade relevant code sections to CRITICAL. Organizations with high incident rates in specific areas should upgrade those modules.

---

## Coverage Semantics

Different coverage metrics measure different aspects of test completeness:

### Line Coverage
**Definition**: Percentage of lines of code that were executed by at least one test.

**Example**: A function with 10 lines of code where 7 lines were executed = 70% line coverage.

**Limitation**: Doesn't detect if all branches (if/else, switch cases) were tested. A test that runs through one branch counts as full line coverage for that function even if other branches were not tested.

### Branch Coverage
**Definition**: Percentage of conditional branches (if/else, switch cases) that were taken by at least one test.

**Example**: A function with an if/else block has 2 branches; if only one path is tested = 50% branch coverage.

**Limitation**: Doesn't guarantee all meaningful combinations of conditions are tested. Also called "decision coverage."

### Function Coverage
**Definition**: Percentage of functions/methods that are called by at least one test.

**Example**: A file with 10 exported functions where 8 are called by tests = 80% function coverage.

**Limitation**: A called function may only be tested on happy path; error cases and edge cases are not guaranteed to be covered.

### Recommended practice
Use **line coverage** as the primary metric for reporting (easier to understand), but examine **branch coverage** to ensure condition branches are actually tested, and verify **function coverage** to ensure all exported functions have at least one test.

---

## Test Quality Checks

Every metric in the section above measures whether code *ran* under test. None of
them measures whether anything was *asserted* about it. A test file that imports
a module and never asserts on it still produces coverage, so all three metrics
improve while nothing is being verified.

Coverage with no assertion behind it reports as green and catches nothing. Run
these checks alongside the coverage read and report what they find as
**false-confidence gaps**, kept separate from untested files. A file with no test
is a known gap. A file with a hollow test is an unknown one, and it will stay
unknown until something breaks in production.

### Structural checks, language-agnostic

| Check | Signal | Report as |
|---|---|---|
| Test file with zero assertions | Imports the module under test, never calls an assertion helper | False confidence, HIGH |
| Test declared but empty | A test or suite block with no body, or a body that only logs | False confidence, HIGH |
| Single-assertion test file | One assertion standing in for a whole module | Thin coverage, MEDIUM |
| Skipped or pending tests | The test exists, the runner counts it, it never executes | Acknowledged gap, MEDIUM |
| Assertions only on a test double | The only assertions are call counts and arguments on a mock, never a return value or a state change | Thin coverage, MEDIUM |

The last one is the most common and the least visible in a coverage report. A
test whose only assertion is `mock.calledTimes(2)` often verifies the test's own
wiring and nothing else. It is **MEDIUM rather than HIGH because it has genuine
exceptions**: event dispatch, fire-and-forget publishing, and retry or
idempotency logic frequently have no return value and no observable state to
assert on, and a call-count assertion is the correct test. Report it, name the
exception when it applies, and never auto-classify it as a defect.

**Every check here is a heuristic, and an agent runs them with no human in the
loop.** Report each finding with the line that triggered it so a reader can
overturn it in one glance. A false positive stated as a fact is how a coverage
audit loses its credibility.

### Per-ecosystem signals

**JavaScript and TypeScript (Jest, Vitest)**

- `describe` blocks containing no `it` or `test`
- `*.test.ts` and `*.spec.ts` files that import the module under test and call no
  assertion helper. Match the helper, not the word: `expect`, chai's `assert.*`
  and `.should`, `node:assert`, and any project-local wrapper around them
- `it.skip`, `test.skip`, `describe.skip`, `it.todo`
- Component tests that only snapshot, with no render-plus-interaction assertion.
  A snapshot proves the output did not change, not that it was ever right

**Python (pytest)**

- Files under a test path with no `test_`-prefixed functions **and** no test
  class. Exempt the support modules that legitimately have none: `conftest.py`,
  `__init__.py`, and anything matching `factories`, `fixtures`, `helpers`,
  `utils`, or a project-configured support glob
- `@pytest.mark.skip` and `@pytest.mark.xfail`, counted as acknowledged gaps
  rather than as passes
- `conftest.py` present: a **positive** signal. Shared fixtures indicate
  deliberate test design rather than tests bolted on per file
- `assert True`, and test bodies that are only `pass`

**Go**

- `*_test.go` files with no `t.Error`, `t.Fatal`, or assertion-library call
- `t.Skip`

**Ruby (RSpec)**

- `it` blocks with no `expect`, and none of the legacy `.should` or `assert`
  forms a given codebase may use instead
- `pending` and `xit`

**End-to-end (Playwright, Cypress)**

- Extract every `page.goto` (or `cy.visit`) target and compare it against the
  route list from Layer 2. A route that is reached but never asserted on is a
  navigation smoke test, not coverage
- Tests that navigate and then assert only on the page title or the HTTP status

---

## Recommendation Engine

Recommendations follow a strict priority order:

1. **Risk level first**: CRITICAL gaps are listed before HIGH gaps, regardless of coverage impact
2. **Coverage impact second**: Within each risk level, gaps affecting more code or more-frequent execution paths rank higher
3. **Effort and velocity third**: Smaller, quicker wins may be listed slightly ahead of larger gaps at the same risk level

Each recommendation includes:
- **Specific test case names**, not generic advice ("Test token expiry logic" not "Add more token tests")
- **Rationale**: Why this particular gap matters (e.g., "This is called on every API request")
- **Context**: What code path would be exercised (e.g., "When user submits invalid email")
- **Suggested filename and location** so developers know where to write the test
- **Acknowledgment of what is already tested**, so developers understand current coverage strengths

---

## Data Collection

### Discovery Phase

The skill performs the following scans:

1. **Language detection**: List all source file types in the project (`.ts`, `.py`, `.go`, `.rb`, etc.)
2. **Test file inventory**: Count test files per language and per source directory
3. **Route extraction**: Parse framework configuration to extract all routes/endpoints
4. **Coverage reports scan**: Look for existing coverage reports in common locations (`coverage/`, `htmlcov/`, `.coverage`)
5. **CI configuration scan**: Read `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, or equivalent to verify test execution

### File Pattern Recognition

The skill recognizes these common patterns:

**Source files by language**:
- JavaScript/TypeScript: `*.js`, `*.jsx`, `*.ts`, `*.tsx`
- Python: `*.py`
- Go: `*.go`
- Ruby: `*.rb`
- Java: `*.java`
- C#: `*.cs`

**Test files**:
- Jest/Vitest (JavaScript): `*.spec.ts`, `*.spec.js`, `*.test.ts`, `*.test.js`, `__tests__/`
- pytest (Python): `test_*.py`, `*_test.py`, `tests/`
- Go: `*_test.go`
- RSpec (Ruby): `*_spec.rb`
- JUnit (Java): `*Test.java`, `*Tests.java`

**E2E test files**:
- Playwright: `*.e2e.ts`, `e2e/`, `tests/`
- Cypress: `cypress/e2e/`, `*.cy.ts`
- Selenium: `e2e/`, `integration/`

**Coverage reports**:
- Jest/Vitest: `coverage/coverage-final.json`, `coverage/lcov.info`
- pytest: `.coverage`, `htmlcov/`, `coverage.json`
- Node: `coverage/lcov.info`

---

## Output Structure

### 1. Executive Summary
```
Coverage Analysis Report
Project: [Project name]
Scanned: [Date and time]
Total source files: [N]
Files with tests: [N] ([%])
Exported functions analyzed: [N]
Functions with test coverage: [N] ([%])
E2E routes tested: [N]/[N] ([%])
Overall trend: [Improved/Stable/Declined since last run]
```

### 2. Infrastructure Status
- Test runner configured: Yes/No, specific runner
- Coverage tool configured: Yes/No, format
- CI integration verified: Yes/No, pipeline location
- Coverage gating enforced: Yes/No
- Identified gaps (e.g., "Coverage drops not prevented in CI")

### 3. Unit Test Gaps (sorted by risk, then coverage impact)
- File name, risk level, reason
- Suggested test file name
- List of 3-5 key test cases to add

### 4. False-Confidence Gaps (sorted by risk)
- File name, the check that fired, risk level
- What the existing test does instead of asserting
- The assertion that would make it real

### 5. E2E Coverage Gaps (sorted by risk, then user impact)
- Route/workflow name, risk level
- Scenario or flow missing tests
- Suggested test case

### 6. Well-Tested Sections
- Modules/files with 80%+ coverage
- Critical paths fully tested
- Positive trends

### 7. Prioritized Action List
- Next 5-10 specific tests to write, in order
- Estimated effort per test (small/medium/large)
- Risk reduction or coverage gain per item

---

## Configuration

### Adjustable Parameters

**Coverage thresholds** (per risk level):
- CRITICAL path code: [default 90%+]
- HIGH risk code: [default 80%+]
- MEDIUM risk code: [default 70%+]
- LOW risk code: [default 60%+]

**Directory exclusions**:
- Default: `node_modules/`, `dist/`, `build/`, `.venv/`, `vendor/`, `coverage/`, `htmlcov/`, `.pytest_cache/`
- Customizable per project

**File pattern overrides**:
- Test file naming convention (e.g., `test/*.test.ts` instead of `*.spec.ts`)
- E2E test location (e.g., `qa/e2e/` instead of `e2e/`)
- Source file extensions per language

**Risk level remapping**:
- Modules to upgrade to CRITICAL (e.g., `payments/`, `auth/`, `pii-handling/`)
- Modules to downgrade to LOW (e.g., `ui-components/`, `formatting/`)

**Route discovery**:
- Router file paths (e.g., `src/server/routes.ts`)
- OpenAPI/Swagger spec location if present
- Protected route patterns (e.g., routes starting with `/admin/` require auth)

---

## Execution Model

The skill operates in this sequence:

1. **Initialization**: Read project structure, detect languages, load configuration
2. **Discovery**: Scan all source files, test files, routes, and coverage reports
3. **Analysis**: Match source files to test files, extract function lists, identify gaps
4. **Classification**: Assign risk levels to each gap using customizable rules
5. **Ranking**: Sort gaps by risk, then by impact on coverage percentage or user experience
6. **Generation**: Produce audit report with recommendations
7. **Output**: Render report to stdout, save JSON export, optionally push to CI reporting service

---

## Limitations & Assumptions

- **Analysis-driven coverage**: The skill parses existing coverage reports (JSON, LCOV) and infers gaps from test file structure and naming. It does not execute tests unless configured to do so in CI integration.
- **Naming convention dependent**: Accuracy relies on test file naming patterns matching source files. Non-standard naming may reduce accuracy.
- **Test quality is checked structurally, not semantically**: the Test Quality Checks section finds tests that assert nothing, assert only on a mock, or never run. It cannot judge whether an assertion that does exist is checking the *right* thing. A well-formed test of the wrong behaviour reads as healthy here.
- **Language-specific detection**: Accuracy varies by language; dynamic languages (Python, JavaScript) are easier to analyze than compiled languages (Go, Java).
- **Route detection limited to declared routes**: Routes generated dynamically at runtime may not be detected.

## Cross-File Reference

- **README.md**: Quick start, setup, example output, at-a-glance overview
- **CUSTOMIZE.md**: Configuration guide, language detection, risk classification, coverage thresholds, CI/CD integration
