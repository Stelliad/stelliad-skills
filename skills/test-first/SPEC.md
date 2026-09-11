# TDD Enforcement Specification

## System Overview

TDD Enforcement applies test-driven development discipline to production code changes through the universal RED-GREEN-REFACTOR cycle. Each cycle implements one behavior, one test at a time, with explicit verification steps.

This specification is framework-agnostic. It applies to any language and test framework that supports:
- Writing and running tests programmatically
- Capturing failure messages
- Deterministic test execution

## Core Workflow

### Standard Path (Features & Refactoring)

#### 1. RED: Write a Single Failing Test

**Objective**: Create a test that fails for the intended reason, not for syntax errors or import failures.

**Steps**:
1. Choose one behavior to implement
2. Write a test that describes the expected behavior
3. Run the test and watch it fail
4. Verify the failure message describes the expected behavior, not an import error
5. Note the exact failure reason

**Verification**:
- Test runs and produces a clear failure message
- Failure is specific ("expected true, got false" not "cannot call undefined")
- Failure message would make sense to someone reading the test

**Example** (TypeScript with Jest):
```typescript
test("adds two positive numbers correctly", () => {
  expect(add(2, 3)).toBe(5);
});
// Run: npm test
// Output: ReferenceError: add is not defined ❌
```

That failure tells you what's missing. Proceed to GREEN.

#### 2. GREEN: Write Minimum Code to Pass

**Objective**: Make the test pass with the smallest amount of code possible. No speculative work. No "while we're here" additions.

**Steps**:
1. Write the minimum code that makes the test pass
2. Accept hardcoded returns if the test passes
3. Do not add error handling unless the test checks for it
4. Do not optimize performance unless the test measures it
5. Run the test and verify it passes

**Verification**:
- Test passes
- The code does exactly what the test requires, nothing more
- You could explain why each line is necessary to pass the test

**Example**:
```typescript
function add(a: number, b: number): number {
  return a + b;
}
// Test now passes ✓
```

If the test only checked for a single case (add(2, 3) = 5), a hardcoded return would be acceptable in GREEN, though the above is already minimal.

#### 3. REFACTOR: Improve While Staying Green

**Objective**: Improve code quality, readability, or structure without changing what the test verifies.

**Steps**:
1. Identify what could be improved (naming, extraction, simplification)
2. Make one refactoring change
3. Run the test immediately
4. If test fails, undo the change
5. Repeat until code is clean

**Safe Refactoring Actions**:
- Renaming variables, functions, or files
- Extracting functions or constants
- Reordering statements (preserving side-effect order)
- Replacing manual logic with library calls
- Adding comments and docstrings
- Reorganizing imports or class structure

**Unsafe Actions** (commit before attempting):
- Changing the algorithm without a new test
- Altering error conditions
- Modifying input or output types
- Removing code paths the test doesn't exercise

**Verification**:
- Test passes after every refactoring step
- Code is more readable than it was
- No duplication introduced
- Complexity metrics stable or improved

### Bug-Fix Path (Adds Verification Step)

Use this path for production bugs, security fixes, and critical paths where a false-positive test is costly.

**Steps**:
1. Write a test that reproduces the bug (fails with current code)
2. Verify it fails for the right reason
3. **Write the fix**: implement the correction to production code
4. Run the test: it must pass (GREEN state)
5. **Revert the bug fix**: the broken production code comes back, restoring the bug
6. Run the test again: it must fail with the same assertion failure  
7. **Restore the fix**: production code corrected
8. Run the test: it must pass
9. This proves the test actually guards the bug (it would catch regression)

**Verification Checklist**:
- [ ] Test written and fails (step 1)
- [ ] Failure message describes the bug correctly (step 2)
- [ ] Fix implemented (step 3)
- [ ] Test passes (step 4)
- [ ] Code reverted to broken state (step 5)
- [ ] Test fails again with same error (step 6)
- [ ] Fix restored (step 7)
- [ ] Test passes (step 8)

**Why This Matters**:
A test that passes on the broken code is a false positive. The revert-fail-restore sequence proves the test would catch this bug if it regressed.

**Example** (Python):
```python
def test_does_not_divide_by_zero(self):
    """Bug: divide(10, 0) crashes instead of raising ValueError"""
    with self.assertRaises(ValueError):
        divide(10, 0)

# RED: Test fails because divide(10, 0) crashes, not raises

# REVERT: Remove the zero-check, crash happens
# confirm test fails as expected

# RESTORE: Add zero-check back
# GREEN: Test passes
```

## Framework Support

### TypeScript / JavaScript

**Frameworks**: Jest, Vitest, Mocha

**Setup**:
```bash
npm install --save-dev [jest|vitest|mocha]
```

**Test discovery**: Files matching `**/*.test.ts`, `**/*.spec.ts`, `test/` directory

**Run single file**:
```bash
npm test -- path/to/test.ts
```

**Watch mode**:
```bash
npm test -- --watch
```

**Coverage**:
```bash
npm test -- --coverage
```

**Exit codes**: 0 = all pass, 1 = failure

### Python

**Frameworks**: pytest, unittest

**Setup**:
```bash
pip install pytest
```

**Test discovery**: Files matching `test_*.py`, `*_test.py`; functions named `test_*`

**Run single file**:
```bash
pytest path/to/test_file.py
```

**Watch mode**:
```bash
pytest-watch  # requires pytest-watch plugin
```

**Coverage**:
```bash
pytest --cov=src
```

**Exit codes**: 0 = all pass, 1 = failure

### Rust

**Framework**: cargo test (built-in)

**Setup**: No additional setup; tests live in `#[cfg(test)]` modules

**Test discovery**: Functions annotated with `#[test]`

**Run single file**:
```bash
cargo test --lib path::to::module
```

**Watch mode**:
```bash
cargo watch -x test
```

**Coverage**: Use `tarpaulin` or `llvm-cov` (external tools)

**Exit codes**: 0 = all pass, 101 = failure

### Go

**Framework**: go test (built-in), testify/assert for assertions

**Setup**: No additional setup; tests live in `*_test.go` files

**Test discovery**: Functions named `Test[Capitalized]`

**Run single file**:
```bash
go test -run TestName ./...
```

**Watch mode**: Use `gotestsum` or `entr` (external tools)

**Coverage**:
```bash
go test -cover ./...
```

**Exit codes**: 0 = all pass, 1 = failure

### End-to-End (UI/Browser)

**Frameworks**: Playwright, Cypress, Selenium

**Setup**:
```bash
# Playwright
npm install --save-dev @playwright/test

# Cypress
npm install --save-dev cypress
```

**Test discovery**: Files matching `*.spec.ts`, `*.e2e.ts`

**Run single file**:
```bash
# Playwright
npx playwright test path/to/test.spec.ts

# Cypress
npx cypress run --spec path/to/test.spec.ts
```

**Watch mode**: Built-in (`--headed`, `--watch`)

**Exit codes**: 0 = all pass, 1 = failure

## Test Design Patterns

### Good Pattern: Behavior-Focused Test

**Characteristics**:
- Name describes the behavior, not the function
- Setup is minimal and clear
- Arrange-Act-Assert structure visible
- Single logical assertion (one outcome tested)
- Deterministic (no randomness, timeouts, or flakes)

**Example**:
```python
def test_removes_duplicates_preserving_order(self):
    """Given a list with duplicates, returns unique items in original order"""
    result = remove_duplicates([1, 2, 2, 3, 1, 4])
    self.assertEqual(result, [1, 2, 3, 4])
```

### Good Pattern: Testing Behavior, Not Implementation

```typescript
// Good: Test what the function returns
test("user email is normalized to lowercase", () => {
  const user = createUser({ email: "ALICE@EXAMPLE.COM" });
  expect(user.email).toBe("alice@example.com");
});

// Avoid: Testing internal implementation details
test("toLowerCase is called", () => {
  const spy = jest.spyOn(String.prototype, "toLowerCase");
  createUser({ email: "ALICE@EXAMPLE.COM" });
  expect(spy).toHaveBeenCalled(); // Tests the how, not the what
});
```

### Anti-Pattern: Multiple Independent Assertions

```python
# Don't do this
def test_user_creation(self):
    user = create_user("alice@example.com", "password123")
    self.assertEqual(user.email, "alice@example.com")
    self.assertIsNotNone(user.id)
    self.assertTrue(user.is_active)
    self.assertIsNotNone(user.created_at)

# Do this instead (split into separate tests)
def test_user_email_is_stored(self):
    user = create_user("alice@example.com", "password123")
    self.assertEqual(user.email, "alice@example.com")

def test_user_gets_id_on_creation(self):
    user = create_user("alice@example.com", "password123")
    self.assertIsNotNone(user.id)

def test_user_is_active_by_default(self):
    user = create_user("alice@example.com", "password123")
    self.assertTrue(user.is_active)
```

One test, one logical outcome. Multiple assertion statements are fine if they verify the same outcome; multiple independent outcomes in one test signal that the test should be split. If setup is identical across several tests, they may be testing the same behavior from different angles, combine them or pick the strongest assertion.

### Anti-Pattern: Mock-Heavy Testing

```typescript
// Avoid: Mocking the function you're testing
test("calculates total with tax", () => {
  const calculateTotal = jest.fn().mockReturnValue(110);
  expect(calculateTotal(100)).toBe(110);
  // This tests the mock, not your implementation
});

// Prefer: Real code paths, mock only externals
test("calculates total with tax", () => {
  expect(calculateTotal(100)).toBe(110); // Tests actual implementation
});

// Mock only external dependencies
test("fetches user from API", async () => {
  jest.spyOn(api, "get").mockResolvedValue({ id: 1 });
  const user = await getUser(1);
  expect(user.id).toBe(1); // Tests your code, mocks the API
});
```

## Output Artifacts

### Per Behavior

**1. Test Code**
- Full test in RED state (failing)
- Explanation of why it fails
- What the test verifies

**2. Implementation**
- Minimum code in GREEN state (passing)
- Explanation of each line
- Why this is sufficient to pass

**3. Refactored Code** (if refactoring occurred)
- Code after cleanup
- What changed and why
- How readability improved

**4. Verification Checklist**
- Specific to this behavior
- Confirms test quality
- Tracks coverage impact

## Failure Modes (Stop Signals)

Process breakdown indicators. When you see one, halt, debug, and report:

**Stop Signal 1: First Test Run Passes**
- Test was not strict enough
- Either the behavior already exists, or the test is incomplete
- Action: Make the test stricter or pick a different behavior

**Stop Signal 2: Production Code Added Before Test Exists**
- This is test-after, not test-first
- Test may not catch what the code actually does
- Action: Delete production code, write test first, restart

**Stop Signal 3: Cannot Explain Why Test Failed in RED**
- Test is ambiguous or the failure message is unclear
- Action: Rewrite test to have a clearer failure mode

**Stop Signal 4: Refactor Changes Test Output Without Changing Code Behavior**
- Test was too strict about implementation details
- Action: Rewrite test to verify behavior, not implementation

**Stop Signal 5: Coverage Dropped During Refactoring**
- Refactoring removed or unreached code
- Action: Review what was removed; if it's unused, document why; if it's needed, restore it

**Stop Signal 6: Test Passes But Behavior Is Not Testable From Outside**
- Test relies on internal implementation details or mocks
- Action: Rewrite test to verify external behavior

## Integration Points

**Coverage Analysis**: Track line and branch coverage before and after each RED-GREEN cycle. Coverage should increase or stay stable; decreases signal removed paths.

**Code Structure Review**: Refactoring quality measured by cyclomatic complexity, duplication metrics, and readability (can someone unfamiliar understand it quickly?).

**Incident Response**: Bug-fix path verification proves the test would catch the bug if it regressed. Document this in the fix commit.

**Acceptance Gates**: Production code reaches release only if all behaviors have tests written first. Coverage floors (typically 75% line, 60% branch) must be met.

## How to Run

Follow the RED-GREEN-REFACTOR cycle manually:

```bash
# RED: Write a failing test
# Your test should fail because the feature doesn't exist yet

# GREEN: Write minimal code to pass the test
# Your test should now pass with the simplest implementation

# REFACTOR: Clean up code while test stays green
# Run tests after each refactoring step:
pytest              # Python
npm test            # JavaScript/TypeScript
cargo test          # Rust
go test ./...       # Go
```

## Exit Criteria

All of the following must be true before a behavior is considered complete:

- [ ] Test written in RED state, failure message verified
- [ ] Minimum code written to pass test (GREEN state)
- [ ] Test passes consistently (no flakes)
- [ ] Refactoring applied (if needed), test still passes
- [ ] No code duplication introduced
- [ ] Coverage increased or maintained
- [ ] Verification checklist for this behavior complete
- [ ] No stop signals triggered
- [ ] For bug fixes: revert-fail-restore verification completed

If any criterion cannot be met, the behavior is not complete. Debug and restart before moving to the next behavior.

## Cross-File Reference

- **README.md**: Quick start guide, key concepts, and common patterns
- **CUSTOMIZE.md**: Tailor RED-GREEN-REFACTOR to your framework, team, and risk model
