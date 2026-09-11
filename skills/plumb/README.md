# Code Review Skill: Quick Reference

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r plumb /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/plumb

or: "review this codebase against SOLID and tell me what actually costs something"
```

The agent reads [SPEC.md](./SPEC.md) and does the work. The `code-review` invocations in the spec are its
vocabulary, not a command on your PATH.

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly.
[CUSTOMIZE.md](./CUSTOMIZE.md) is where you set the thresholds and policy for
your stack.

## What This Does

**Architectural design review** of your codebase against engineering principles (DRY, KISS, SOLID, Modularity, Naming). Catches anti-patterns, maintainability debt, and structural issues that linters miss.

**Not linting.** This reviews *architecture*, not syntax. Run both.

**Output:** Structured markdown with findings bucketed by severity, per-principle health ratings, and prioritized fixes.

---

## Who Uses This

- **Architects**: Catch structural problems before compounding
- **Tech leads**: Review large PRs and refactoring plans
- **Teams**: Understand codebase health and technical debt
- **Onboarding**: Rapid overview of how code is organized
- **CI/CD**: Automatic review on schedule or per-PR

---

## Time Required

| Scope | Duration |
|-------|----------|
| Single file (< 500 LOC) | 2–5 min |
| Directory (5–20 files) | 5–15 min |
| Full project (smart sampling) | 10–30 min |

---

## Getting Started

### 2. Configure (optional)
```bash
mkdir -p .codereviews

# Create modular configuration files
cp templates/principles.config.yaml .codereviews/
cp templates/severity.config.yaml .codereviews/
cp templates/sampling.config.yaml .codereviews/

# Edit to match your org's priorities
# See CUSTOMIZE.md for full configuration guide
```

### 3. Run

Invoke via Claude Code:

```bash
# Review one file
/code-review --file src/models/user.py

# Review a directory
/code-review --dir src/services/

# Review the whole project (smart sampling)
/code-review --all
```

### 4. Read Report Output

Markdown output with:
- **Executive summary** (one key finding)
- **Critical findings** (🔴) with concrete fixes
- **Significant findings** (🟡)
- **Minor findings** (🟢)
- **Per-principle ratings** (⭐–⭐⭐⭐⭐⭐)
- **Recommendations** (ordered by impact, with effort estimates)
- **What's working well** (strengths)

---

## What You'll See

### Findings Ordered by Severity

- **🔴 Critical:** Will cause bugs or block scaling
- **🟡 Significant:** Maintenance cost; technical debt
- **🟢 Minor:** Cosmetic improvements

### Principles Rated ⭐–⭐⭐⭐⭐⭐

Each principle (DRY, KISS, SRP, OCP, DIP, Modularity, Naming) gets a star rating with a brief assessment:

```
**SRP:** ⭐⭐⭐: Most modules have clear responsibilities; 
UserService (src/services/user.py) is an exception.
```

### Recommendations Come with Effort Estimates

```
## Decouple UserService (4–8 hours)
1. Create UserRepository class
2. Inject into UserService
3. Update tests
```

### Positives Included

"Test coverage is comprehensive (92%)", builds confidence in the feedback.

---

## Configuration

**Defaults:**
- Reviews source code only (skips tests, generated, vendor)
- All principles weighted equally
- Smart sampling for large projects (entry points + largest + most-imported)
- Markdown output

**Customize:** See `CUSTOMIZE.md` for:
- Custom principles
- Severity thresholds
- What files to include/exclude
- Output formats
- Effort scales
- Org-specific context (legacy code, scripts)

---

## Common Scenarios

### Just the critical issues
```bash
code-review --all --severity critical
```

### Include test code (if needed)
By default, tests are excluded from review. To include them, edit `.codereviews/config.yaml`:
```yaml
always_include:
  - "**/*.test.ts"
  - "**/*_test.py"
```

### Export as JSON
```bash
code-review --all --format json > review.json
```

### Review only Python
```bash
code-review --all --language python
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Review hangs on large project | Use `--dir [subdirectory]` or increase LOC limit in config |
| Too many Minor findings | Run with `--severity critical,significant` |
| Disagree with a finding | Check custom principle definitions in `.codereviews/principles/` |
| Language not supported | Add config in `.codereviews/languages/` |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Review completed; no critical findings (or only non-critical findings depending on severity filter) |
| 1 | Review completed; critical findings present |
| 2 | Review failed (file not found, permission denied, unsupported language) |

Use in CI/CD:
```bash
code-review --all --severity critical || exit 1
```

## CI/CD Integration

**GitHub Actions example:**

```yaml
name: Architectural Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run architectural review
        run: code-review --all --severity critical,significant --format json --output review.json
      - name: Fail on critical findings
        run: |
          if grep -q '"severity": "Critical"' review.json; then
            echo "Critical findings detected; please review before merge"
            exit 1
          fi
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: code-review-report
          path: review.json
```

---

## FAQ

**Q: Does this replace linting?**  
A: No. Linters catch syntax/style; this reviews *architecture*.

**Q: Can I use this in CI?**  
A: Yes. Export JSON and fail build on Critical findings.

**Q: How often should I run?**  
A: After refactors, before releases, or weekly.

**Q: Can I ignore a finding?**  
A: Yes. Document in `.codereviews/context.yaml` (e.g., legacy code).

**Q: Does this understand my framework?**  
A: Yes, if written in a supported language. Add framework-specific patterns to `.codereviews/principles/`.

---

## See Also

- **SPEC.md**: Technical architecture, principles framework, scoring methodology, output specification
- **CUSTOMIZE.md**: Configuration options, severity thresholds, language support, context exceptions

## Next Steps

1. Run: `code-review --all`
2. Pick one Critical finding to fix
3. Customize config to match your priorities (see CUSTOMIZE.md)
4. Integrate into CI/CD using the example above
