# Coverage Analysis Skill

Quick reference for teams implementing test coverage strategy and measuring progress.

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r harvest /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/harvest

or: "find the test coverage gaps in this repo, ranked by risk"
```

The agent reads [SPEC.md](./SPEC.md) and does the work.

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly.
[CUSTOMIZE.md](./CUSTOMIZE.md) is where you set the thresholds and policy for
your stack.

## At a Glance

| Aspect | Description |
|--------|---|
| **What** | Audit test coverage gaps across unit tests, E2E flows, and CI/CD infrastructure |
| **When** | Weekly or monthly; before major releases or after production incidents |
| **For** | Development teams, QA leads, engineering managers, release managers |
| **Output** | Categorized gaps ranked by risk, prioritized test recommendations, progress tracking |
| **Time** | 15-45 minutes depending on project size (initial setup: 30-60 min) |

---

## Who Uses This

- **Developers writing new features**: Understand what to test before opening a PR
- **QA leads planning sprints**: Prioritize testing work by business risk
- **Tech leads managing code quality**: Track coverage trends and identify risky modules
- **Release managers**: Verify quality gates before shipping to production
- **Incident responders**: Add regression tests after bugs are fixed

---

## What It Analyzes

### Layer 1: Unit Tests
Which functions and files have no tests? What edge cases are missing (null values, empty data, boundary conditions)?

### Layer 2: E2E Coverage
Which user workflows, routes, and critical paths aren't tested end-to-end? Are error cases and auth scenarios covered?

### Layer 3: Infrastructure
Is your test runner configured? Does your CI system run tests and collect coverage? Are reports generated and accessible?

### Across all three: test quality
Coverage says the code ran. It does not say anything was checked. The audit also
looks for tests that produce coverage and verify nothing: files that import and
never assert, empty suite blocks, skipped tests still counted by the runner,
snapshot-only component tests, and tests whose only assertions are on a mock's
call count. These are reported as **false-confidence gaps**, separately from
untested files, because a hollow test is the gap you do not know you have.

---

## See Also

- **SPEC.md**: Technical architecture, three audit layers, test quality checks, risk prioritization, output structure, coverage semantics
- **CUSTOMIZE.md**: Configuration guide, language detection, risk classification, coverage thresholds, CI/CD integration

## Quick Start

### Step 1: Prepare Your Project
- Ensure test framework is installed (Jest, Vitest, pytest, Playwright, etc.)
- Ensure coverage tool is configured (istanbul, pytest-cov, coverage.py)
- Note your tech stack and project structure

### Step 2: Customize Configuration (30 min)
Follow [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt:
- Programming languages and test file patterns
- Risk classification for your domain
- Coverage targets per risk level
- Excluded directories (generated code, vendor libs)
- E2E route discovery patterns
- CI/CD integration

### Step 3: Run the Audit (5 min)
```bash
# Analyze your project (via Claude Code)
/harvest --project .

# Or specify a different path
/harvest --project /path/to/project
```

### Step 4: Review Report (15 min)
- Read **Executive Summary** for overall picture
- Focus first on **CRITICAL** risk gaps
- Use **Prioritized Action List** to plan next tests
- Note **Well-Tested Sections** to understand coverage patterns

### Step 5: Implement & Measure (Ongoing)
- Create tickets for priority gaps from the action list
- Estimate effort and integrate into sprint planning
- Re-run audit after 2-4 weeks to measure progress
- Track trend toward your coverage targets

---

## Example Output

```
COVERAGE ANALYSIS REPORT
───────────────────────────────────────────
Project: acme-backend
Scanned: 2024-01-15 at 14:32 UTC

Executive Summary
─────────────────
Total source files:         847
Files with tests:           623 (73%)
Exported functions:       1,204
Functions with test coverage: 1,089 (90%)
E2E routes tested:         34/42 (81%)
Trend since last run:      ↑ +3% (improving)

Unit Test Gaps (Priority Order)
────────────────────────────────
[CRITICAL] src/auth/token-validation.ts
  Status: No test file
  3 exported functions: validate(), refresh(), revoke()
  Suggested file: src/auth/__tests__/token-validation.spec.ts
  Key tests:
    - Expired token rejected with 401
    - Malformed token (invalid signature) rejected
    - Valid token passes validation
    - Revoked token no longer validates

[HIGH] src/billing/charge.ts
  Status: 38% coverage (3/8 functions tested)
  Missing: refund(), retry(), batch_charge()
  Suggested additions:
    - Refund reduces balance correctly
    - Retry on failure reuses same request ID
    - Batch charge rolls back all if one fails

False-Confidence Gaps (Priority Order)
──────────────────────────────────────
[HIGH] src/billing/invoice.py  ->  tests/test_invoice.py
  Check: test file with zero assertions
  Imports build_invoice() on line 3, never calls assert. Counts as covered.
  Make it real: assert the returned total, tax line, and currency

[HIGH] src/notifications/dispatch.ts  ->  dispatch.test.ts
  Check: test declared but empty
  describe('dispatch') contains no it() blocks
  Make it real: one test per delivery channel, asserting the payload sent

[MEDIUM] src/webhooks/emit.ts  ->  emit.test.ts
  Check: assertions only on a test double
  Only assertion is expect(send).toHaveBeenCalledTimes(1)
  Possible exception: fire-and-forget dispatch has no return value to assert.
  Confirm before treating as a gap

[MEDIUM] tests/test_reconcile.py
  Check: skipped but counted
  @pytest.mark.skip since commit 4a19c02, still reported as a passing test

E2E Coverage Gaps (Priority Order)
──────────────────────────────────
[CRITICAL] POST /api/auth/login
  Status: Happy path only (50% coverage)
  Missing scenarios:
    - Invalid credentials (wrong password) rejected with 401
    - Missing email or password field rejected with 400
    - Rate limiting after 5 attempts
    - Account lockout after 10 attempts

[HIGH] GET /api/users/:id
  Status: No auth testing
  Missing:
    - User cannot access another user's profile (403)
    - Deleted user returns 404

Infrastructure Status
─────────────────────
✓ Test runner: Vitest (npm run test)
✓ Coverage tool: @vitest/coverage-v8
✓ CI integration: GitHub Actions
✗ Coverage drops not enforced (no CI gate)

Well-Tested Sections
────────────────────
✓ API error handling:      95% coverage
✓ User authentication:     91% coverage
✓ Database transactions:   89% coverage

Prioritized Action List (Next 5 Tests)
──────────────────────────────────────
1. [CRITICAL] Write auth/token-validation.spec.ts: ~2 hours
   Impact: Protects 3 auth functions, prevents 401 failures

2. [CRITICAL] Add E2E login rate-limiting test: ~1 hour
   Impact: Prevents brute-force attacks from reaching production

3. [HIGH] Add billing refund edge-case tests: ~3 hours
   Impact: Improves charge.ts coverage from 38% to 80%

4. [HIGH] Write E2E access-control tests: ~2 hours
   Impact: Prevents unauthorized profile access

5. [MEDIUM] Add null-safety tests to utilities: ~2 hours
   Impact: Improves overall coverage from 73% to 75%
```

---

## Common Questions

**Q: How often should I run this audit?**  
A: Weekly if you're actively improving coverage, monthly for steady-state maintenance. Run extra audits after major refactoring or production incidents.

**Q: Can I use this for legacy code with no tests?**  
A: Absolutely. The audit prioritizes by risk, so start with Critical modules (auth, payments, data handling) and work outward.

**Q: Should I aim for 100% coverage?**  
A: No. Aim for 90%+ on CRITICAL code, 80%+ on HIGH, 70%+ on MEDIUM, 60%+ on LOW. The diminishing returns on the last 20% aren't worth the effort.

**Q: How do I handle generated code?**  
A: Exclude it in configuration (add directories to `excluded_directories`). Generated code like GraphQL resolvers or ORMs shouldn't count against your coverage.

**Q: My team can't implement all gaps at once. What do I prioritize?**  
A: Follow the prioritized action list. CRITICAL gaps first, then HIGH. Medium and Low gaps can wait until you have capacity.

**Q: How do I integrate this with CI/CD?**  
A: See CUSTOMIZE.md, section 8 (CI/CD Integration). Most teams run the audit weekly and upload reports to Codecov or similar for trend tracking.

**Q: What if coverage drops between audits?**  
A: This is your signal to investigate. Either new code was added without tests, or tests were removed. Review the diff and decide whether to add tests or adjust your threshold.

---

## Key Metrics to Track

Track these over time to measure progress:

| Metric | What it shows | Target |
|--------|---|---|
| % files with tests | Test coverage breadth | 85%+ |
| % functions tested | Function-level coverage | 85%+ |
| CRITICAL untested | High-risk gaps | 0 |
| Test-to-code ratio | How much testing per 100 lines | 1:2 to 1:3 |
| Time to add a test | Development velocity | < 30 min for simple case |
| Incident coverage | % of production incidents with pre-existing tests | 80%+ |

---

## Support

**For configuration questions**: See [CUSTOMIZE.md](./CUSTOMIZE.md)  
**For technical details**: See [SPEC.md](./SPEC.md)  
**For test framework questions**: Consult your framework's documentation (Jest, Vitest, pytest, Playwright)

---

**Version**: 1.0  
**Status**: Ready for distribution  
**Last updated**: 2026-08-26
