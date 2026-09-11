# TDD Enforcement: Customization Guide

## Before You Start

This guide helps you adapt TDD Enforcement for your team, stack, and workflow. The core RED-GREEN-REFACTOR cycle is universal; customization is about terminology, guardrails, and integration.

## Customization 1: Test Framework Binding

**Problem**: Your team uses a test framework not listed in SPEC.md.

**Solution**: Add framework support by defining four essentials:
1. How tests are discovered (file patterns, function naming)
2. How to run a single test file
3. How to run in watch mode (for rapid RED-GREEN cycles)
4. How to measure coverage

**Framework Template**:

```markdown
### [Language/Framework Name]

**Discovery**: [Describe how tests are found]
Example: "Files matching `*_test.rb` in `spec/` directory, methods prefixed with `test_`"

**Run Single File**:
[Command]
Example: `rspec spec/user_spec.rb`

**Watch Mode**:
[Command]
Example: `rspec-watch spec/user_spec.rb`

**Coverage**:
[Command]
Example: `rspec --format RcovText spec/`

**Exit Codes**: [Pass code] = success, [Fail code] = failure
Example: "0 = pass, 1 = failure"
```

**Customization Question for Your Team**: What test framework and runner does your codebase use? Write the template above for it.

## Customization 2: Naming and Terminology

**Problem**: Your organization uses different terms for testing concepts.

**Solution**: Map your terminology to the skill's terms.

**Mapping Template**:

| SPEC Term | Your Organization | Example |
|---|---|---|
| RED-GREEN-REFACTOR | [Your term] | "Test-First-Then-Code" |
| Behavior | [Your term] | "Feature" or "Requirement" |
| Test-Driven | [Your term] | "Specification-First" |
| Minimum Code | [Your term] | "Stub Implementation" |
| Unit vs. Integration | [Your term] | [Describe your distinction] |
| Coverage Floor | [Your term] | [What % does your team track?] |

**Questions to Answer**:
1. Does your team distinguish between unit, integration, and end-to-end tests? How?
2. What do you call the "minimum code" phase? "Stub"? "Happy path"?
3. Do you use "TDD", "BDD", "SDD", or another acronym?
4. When you say "testing," do you mean before-code or after-code?

**Action**: Post the filled-in mapping in your team's development guide or wiki.

## Customization 3: Minimum Code Definition

**Problem**: "Minimum code" is ambiguous. Can you hardcode a return? Skip error handling? Skip logging?

**Solution**: Define it for your context. Answer these questions:

**Question 1: Hardcoded Returns**
- Can a test pass via hardcoded return? (E.g., `return 42` if test only checks `add(2, 3) == 5`)
- **Recommendation**: Yes. GREEN is about making the test pass with zero waste. If you later write a test that fails on a hardcoded return, you refactor. The test drives the code.

**Question 2: Error Handling**
- Must GREEN include error handling, or only if tested?
- **Recommendation**: Only if tested. If no test checks error handling, don't add it in GREEN. Refactor adds it later when needed.

**Question 3: Performance**
- Must GREEN code be performant, or only correct?
- **Recommendation**: Correct first. If a test fails on performance, refactor adds optimization.

**Question 4: Logging and Instrumentation**
- Do you log in GREEN, or add it during REFACTOR?
- **Recommendation**: Don't log in GREEN unless the test verifies it. Adds noise without test coverage.

**Question 5: Configuration**
- Does GREEN use configuration, environment variables, or defaults?
- **Recommendation**: Hardcode in GREEN. Refactor extracts configuration if multiple tests need variation.

**Definition Template**:
```
Minimum code in our context means:
- Correct behavior only (test passes)
- Hardcoded values are acceptable
- Error handling only if tested
- No logging unless tested
- No performance optimization unless tested
- Configuration hardcoded initially, extracted if needed
```

**Action**: Write this for your team and link it in your development playbook.

## Customization 4: Refactoring Scope

**Problem**: What is safe refactoring without breaking the contract? When should you commit before refactoring?

**Solution**: Define safe and unsafe refactoring for your codebase.

**Safe During REFACTOR** (no commit beforehand):
- Renaming (variables, functions, files)
- Extracting functions or constants
- Reordering statements (preserving side effects)
- Simplifying conditionals
- Replacing manual logic with library calls
- Adding comments and docstrings
- Removing unreachable code (inside test boundaries)

**Unsafe** (commit before attempting):
- Changing algorithm without new test
- Altering error conditions
- Modifying input/output types or contracts
- Removing code paths outside test coverage
- Adding new dependencies
- Changing how data is stored

**Context-Specific Unsafe Actions** (ask your team):
- Are there code paths considered "too fragile to touch"?
- Are there subsystems that need architectural review before refactoring?
- Do you have legacy code with no tests that should stay untouched?

**Action**: List unsafe actions specific to your codebase and post them where developers refactor.

## Customization 5: Coverage Threshold

**Problem**: What coverage is enough? Line, branch, or both? What triggers a refactor to improve coverage?

**Solution**: Set a measurable floor and communicate it.

**Questions**:
1. **Line coverage or branch coverage?**
   - Line: "At least 75% of lines are run"
   - Branch: "At least 60% of if/else paths are tested"
   - **Recommendation**: Both. 75% line, 60% branch.

2. **What code is excluded?**
   - Generated code (protobuf, OpenAPI clients)
   - Boilerplate (constructors, getters)
   - Vendor code (node_modules, venv, .cargo)
   - **Recommendation**: Exclude generated and vendor; report on your code only.

3. **When does coverage dip get flagged?**
   - Any decrease triggers review
   - Decreases > 5% block merge
   - Decreases bounded by time (e.g., refactoring debt, acceptable if repaid in sprint)
   - **Recommendation**: Block decreases > 2%; time-bounded debt requires a ticket.

4. **How is coverage measured?**
   ```bash
   # After tests pass, measure coverage
   npm test -- --coverage
   pytest --cov=src
   cargo tarpaulin
   ```

**Coverage Floor Statement Template**:
```
Our coverage requirements:
- Minimum [X]% line coverage
- Minimum [Y]% branch coverage
- Excludes: [list]
- Measured: [tool]
- Decreases > [Z]% trigger review
```

**Action**: Document your floor and run it on every merge.

## Customization 6: Bug-Fix Verification Scope

**Problem**: The revert-fail-restore verification step takes time. Which bugs require it?

**Solution**: Define categories and require verification for high-stakes code only.

**Verification-Required Categories**:
- **Production user-facing paths**: Features users interact with daily
- **Security checks**: Authentication, authorization, encryption, access control
- **Financial code**: Payment, billing, accounting logic
- **Data deletion**: Anything that removes data permanently
- **Compliance code**: GDPR, HIPAA, SOC2 controls
- **Issues flagged "critical" or "P0"**: Severity-based inclusion

**Verification-Optional Categories**:
- **Internal utilities**: Helpers, formatters, internal APIs
- **Infrastructure code**: Build scripts, deployment automation
- **Developer tools**: CLI utilities, internal dashboards
- **Experimental features**: Behind feature flags, not released

**Configuration Template**:
```yaml
bug_fix_verification:
  always_verify:
    - security
    - payment
    - data_deletion
    - compliance
    - severity_critical
  optional:
    - internal_utilities
    - infrastructure
    - experiments
```

**Questions**:
1. What categories of code carry the highest risk if a bug regresses?
2. Who decides if verification is required? (Developer? Tech lead? Incident severity?)
3. If verification is skipped, how is that documented?

**Action**: Define your categories and update your bug-fix process to require verification where it matters.

## Customization 7: Integration with Your Pipeline

**Problem**: You have CI/CD, linters, formatters, and security checks. Where does TDD fit?

**Solution**: TDD happens before the pipeline; the pipeline verifies afterward.

**Sequence**:
```
1. Developer writes test (RED)
2. Developer writes code (GREEN)
3. Developer refactors (REFACTOR)
4. Developer runs linter locally and fixes
5. Developer runs formatter locally and commits
6. Push to feature branch
7. CI runs: tests, lint, coverage, security checks
8. If CI passes, PR is mergeable
```

**Pipeline Responsibilities**:
- Re-run all tests (verify locally + CI match)
- Run linter (catch style violations)
- Measure coverage (confirm floor met)
- Run security checks (SAST, dependency scanning)
- Block merge if any gate fails

**TDD + CI Checklist**:
- [ ] Tests written before code locally
- [ ] All tests pass locally
- [ ] Coverage measured locally
- [ ] Code runs through linter/formatter
- [ ] Pushed with clean commit history
- [ ] CI re-runs tests, coverage, lint, security
- [ ] CI gates pass before merge

**Questions**:
1. Do you run tests on feature branches, or only on merge?
   - **Recommendation**: Both. Local + CI catch different issues.
2. Do you auto-format on push, or fail if formatting is wrong?
   - **Recommendation**: Auto-format on pre-commit hook; never block on format.
3. If CI fails, can developers push again, or does it require a fix?
   - **Recommendation**: Require a fix; no force pushes to main.

**Action**: Document your CI/TDD sequence and ensure developers understand it.

## Customization 8: Team Communication

**Problem**: Some developers will argue TDD slows them down or isn't necessary.

**Solution**: Prepare rebuttals grounded in your team's experience.

**Common Resistance & Reframes**:

| Pushback | Root Cause | Reframe |
|---|---|---|
| "Tests slow me down" | Conflates writing with delivery | Tests let you refactor without fear. Speed comes from refactoring safely. A feature with tests is shippable sooner than one without. |
| "I'll write tests after" | Wants to avoid test-writing | After-tests often skip edge cases and end up testing "the code that exists," not "the behavior required." TDD prevents this. |
| "This is too simple to test" | Underestimates test value | If it's simple, the test is fast and clear. That clarity is worth it. |
| "I'm not sure what to test" | Lacks test structure | Write the simplest test first. It clarifies what you're building. |
| "My team doesn't test" | Organizational norm | One person testing blocks more bugs than a team that doesn't. You go first. |
| "My test failed after I refactored" | Refactoring was too large | Run test after every single change. If it fails, undo the last step. |
| "Coverage metrics lie" | Coverage doesn't catch all bugs | True, but untested code has zero visibility. Coverage is a floor, not a ceiling. |

**Escalation Path**:
1. Developer raises concern
2. Pair on one behavior together (15–30 min)
3. Show how test-first made refactoring safe
4. Document the win and share with team

**Action**: When onboarding a new developer on TDD, pair on the first behavior.

## Customization 9: Escalation and Blockers

**Problem**: Developer is stuck in RED. Test won't pass. Behavior is unclear. What do they do?

**Solution**: Define time limits and escalation paths.

**Stuck in RED?** (30 minutes is the threshold)
- Test might be too strict: break into smaller tests
- Behavior might be too big: pick a simpler one first
- Test might be unclear: pair with someone and simplify the test
- **Escalation**: If stuck beyond 30 min, ask tech lead to review test design

**Stuck in GREEN?** (Code won't compile or test won't pass)
- Verify test is correct (did you test it in RED?)
- Write only what the test requires
- Check imports and dependencies
- **Escalation**: If stuck beyond 15 min, ask for a code review of the test itself

**Refactoring Broke Things?** (Test fails after refactoring)
- Undo the last change
- Run test (confirm it passes again)
- Refactor one smaller step
- Run test again
- **Escalation**: If patterns repeat, the refactoring is too aggressive; pair and refactor together

**Escalation Contact**: [Name], [Role], [Slack/Email]

**Action**: Add escalation contacts and time limits to your development guide.

## Customization 10: Metrics and Reporting

**Problem**: How do you know if TDD is working for your team?

**Solution**: Track these metrics:

**Velocity Metrics** (measure efficiency):
- Stories completed per sprint (should increase after TDD adoption)
- Refactoring time as % of feature time (should decrease; code gets cleaner faster)

**Quality Metrics** (measure correctness):
- Bugs found in QA vs. production (should decrease)
- Regressions in sprint vs. new bugs (should decrease)
- Test-to-code ratio (lines of test / lines of production code)

**Coverage Metrics** (measure visibility):
- Line coverage (track trend, target 75%+)
- Branch coverage (track trend, target 60%+)
- Untested code by module (identify weak spots)

**Team Metrics** (measure adoption):
- % of commits with new tests (track adoption)
- % of PRs with coverage increases (track behavior)
- Pair-programming sessions on TDD (track learning)

**Review Cadence**: Monthly review of metrics; quarterly trend analysis.

**Action**: Pick 2–3 metrics that matter to your team. Track them for 3 months.

## Final Checklist: Is Your Customization Complete?

- [ ] Test framework binding written for your stack
- [ ] Terminology mapped (RED-GREEN-REFACTOR → your terms)
- [ ] Minimum code definition documented
- [ ] Refactoring scope defined (safe/unsafe actions)
- [ ] Coverage floor set (line%, branch%, exclusions)
- [ ] Bug-fix verification scope defined
- [ ] CI/TDD sequence documented
- [ ] Common resistance rebuttals prepared
- [ ] Escalation path defined with contacts
- [ ] Metrics chosen and tracking started
- [ ] Documentation posted where developers can find it
- [ ] First team pairing session scheduled

## Cross-File Reference

- **README.md**: Quick start guide and key concepts
- **SPEC.md**: Complete workflow specifications, framework support, and failure modes
