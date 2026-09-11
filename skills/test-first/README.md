# TDD Enforcement

**Test-driven development discipline across any language and framework.**

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r test-first /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/test-first

or: "use the test-first discipline for this change"
```

The agent reads [SPEC.md](./SPEC.md) and does the work. The `npm test` and `pytest` calls in the spec are your own
test runner, and those are real.

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly.
[CUSTOMIZE.md](./CUSTOMIZE.md) is where you set the thresholds and policy for
your stack.

## What It Does

TDD Enforcement guides you through the RED-GREEN-REFACTOR cycle for every production code change:

1. **RED**: Write a test that fails for the intended reason
2. **GREEN**: Write minimum code to make it pass
3. **REFACTOR**: Improve the code while keeping the test green

For bug fixes, it adds a verification step: revert the fix, confirm the test fails again, then restore it. This proves the test actually catches the bug.

## Who Uses It

- Teams adopting TDD or enforcing it consistently across a codebase
- Codebases with flaky tests or coverage that doesn't reflect reality
- Bug-fix workflows where a regression is costly (production, security, payments)
- Code reviews that want to verify test quality, not just test count
- Organizations moving from "testing" (after code) to "test-driven" (before code)

## Time Required

- **Single behavior**: 15–30 minutes (RED + GREEN + REFACTOR)
- **Bug fix with verification**: 20–40 minutes (includes revert step)
- **Team onboarding**: 1–2 hours for setup and your first behavior together
- **Ongoing**: Integrated into normal code review; no extra time needed

## Key Concepts

### RED-GREEN-REFACTOR

Each cycle implements one behavior. Don't try to implement everything at once.

**RED**: Write a test that fails. The failure message should describe the expected behavior, not a syntax error.
```python
def test_adds_two_positive_numbers_correctly(self):
    self.assertEqual(add(2, 3), 5)
# Run: python -m pytest
# Output: NameError: name 'add' is not defined ❌
```

**GREEN**: Write the minimum code that makes the test pass. Hardcoded returns are fine.
```python
def add(a, b):
    return a + b
# Test passes ✓
```

**REFACTOR**: Clean it up while the test stays green. If the code is already clear, you're done.
```python
# Code is already minimal and clear; no refactoring needed
```

If stuck in RED, the test might be too strict. If GREEN takes too long, the behavior might be too big, pick something simpler first.

### Bug-Fix Verification

For production bugs, security fixes, and critical paths: verify the test actually catches the bug.

```
1. Write a test that reproduces the bug (test fails)
2. Revert the bug fix (code breaks again)
3. Run the test (it must fail for the same reason)
4. Restore the fix (code correct again)
5. Run the test (it must pass)
```

If step 3 doesn't fail, the test was never broken by the bug, it's a false positive.

### Coverage Isn't Everything

A test passing doesn't mean it's good. Check:
- Does the test fail when the code is wrong?
- Does the test read like documentation?
- Does refactoring improve readability without changing behavior?
- Is coverage growing toward your target?

## How to Use This Skill

For documentation on framework-specific setup, test discovery, and debugging, see **SPEC.md**. For customizing this to your team's workflow and terminology, see **CUSTOMIZE.md**.

## Quick Start

### 1. Verify Your Test Framework Works

```bash
# TypeScript / JavaScript
npm test

# Python
pytest

# Rust
cargo test

# Go
go test ./...
```

It should run and show results. If not, install the test framework for your language.

### 2. Pick One Small Behavior

Start tiny. One thing, one test.

**Good first behavior**: "Adds two positive numbers correctly"

**Avoid**: "Complete user authentication system" (too big)

### 3. Write the Test (RED)

```typescript
test("adds two positive numbers correctly", () => {
  expect(add(2, 3)).toBe(5);
});
```

Run it. Watch it fail. Verify the failure describes what's missing.

### 4. Write Minimum Code (GREEN)

```typescript
function add(a: number, b: number): number {
  return a + b;
}
```

Run the test. It should pass.

### 5. Refactor (if needed)

If the code is clear, stop. If not, clean it up while the test stays green.

### 6. Repeat

Pick the next behavior. Go to step 2.

## Verification Checklist

After each RED-GREEN-REFACTOR cycle, confirm:

- [ ] Test fails in RED for the intended reason
- [ ] Minimum code makes it GREEN
- [ ] Refactoring doesn't change test output
- [ ] Test is deterministic (runs same way every time)
- [ ] Coverage increased
- [ ] Code is more readable than it was

For bug fixes, also confirm:
- [ ] Reverted fix causes test to fail again
- [ ] Restored fix causes test to pass

## Common Patterns

### Test Naming

**Good**: `test_adds_two_positive_numbers_correctly()`

**Bad**: `test_addition()` (says what function, not what it does)

Name the behavior you're testing.

### Single Assertion Per Test

One test, one logical outcome.

```python
def test_user_gets_welcome_email_on_signup(self):
    user = create_user("alice@example.com")
    assert user.received_email("welcome")
```

Not:
```python
# Don't do this
def test_user_creation(self):
    user = create_user("alice@example.com")
    assert user.email == "alice@example.com"
    assert user.id is not None
    assert user.is_active is True
```

(Write three tests instead.)

### Use Real Code, Mock Externals Only

```typescript
// Good: Real calculation
test("calculates total with tax", () => {
  expect(calculateTotal(100)).toBe(110);
});

// Mock only external dependencies
test("fetches user from API", async () => {
  jest.spyOn(api, "get").mockResolvedValue({ id: 1 });
  const user = await getUser(1);
  expect(user.id).toBe(1);
  expect(api.get).toHaveBeenCalledWith(1); // Verify mock was actually called
});
```

## Stop Signals

If any of these happen, something's wrong:

**First test run passes**: Test is not strict. Either behavior already exists, or test is incomplete.

**Production code added before test**: You're testing after, not before. Restart with a test.

**Cannot explain why test failed**: Test is ambiguous. Rewrite it to be clearer.

**Coverage dropped**: Refactoring removed used code. Review what was deleted.

**Test passes but behavior isn't testable**: Test mocks too much or verifies implementation details. Rewrite it to test from outside.

When you see a stop signal, halt and debug before continuing.

## Getting Help

**Stuck in RED?**
- Test might be too strict. Break it into smaller tests.
- Behavior might be too big. Pick a simpler one first.

**Stuck in GREEN?**
- Code might be incomplete. Check what the test requires.
- Test might be incomplete. Verify it fails properly.

**Refactoring broke things?**
- Run test after every single change.
- If test fails, undo the last refactor step.

## Next Steps

- [ ] Run your test suite to confirm it works
- [ ] Pick one small behavior
- [ ] Write a test for it
- [ ] Watch it fail
- [ ] Write code to pass it
- [ ] Clean it up while test stays green

That's one cycle. Repeat for the rest of your codebase.

## Cross-File Reference

- **SPEC.md**: Complete workflow specifications, framework support, test design patterns, and failure modes
- **CUSTOMIZE.md**: Adapt TDD to your team's stack, processes, and risk tolerance

## Further Reading

- **Test-Driven Development** by Kent Beck (book, foundational)
- **Growing Object-Oriented Software, Guided by Tests** by Freeman & Pryce (book, practice)
- **The Three Rules of TDD** by Robert C. Martin (essay, discipline)
