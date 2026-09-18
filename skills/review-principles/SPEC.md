# SPEC.md: Code Review Skill Framework

## Overview

**Purpose:** Automated architectural and design review of code repositories against engineering principles, catching maintainability debt, design anti-patterns, and structural issues before they compound into expensive refactors.

**Scope:** Single file, directory, or full project with smart sampling for large codebases. Reviews source code structure, not syntax, the review complements, not replaces, linting.

**Output:** Structured markdown report with severity-bucketed findings, per-principle health ratings (star scale), impact-ordered recommendations, and effort estimates.

---

## Principles Framework

### The Seven Core Principles

| Principle | Definition | What It Catches |
|-----------|-----------|-----------------|
| **DRY** (Don't Repeat Yourself) | Logic and data structures should have single sources of truth | Copy-paste code, duplicated logic, parallel implementations of the same behavior, duplicated data stores |
| **KISS** (Keep It Simple) | Straightforward solutions trump clever ones | Over-engineered abstractions, premature optimization, unnecessary indirection, multi-layer wrappers around single operations |
| **SRP** (Single Responsibility) | Each module/function has one reason to change | God classes mixing business logic with persistence, controllers handling validation, services mixing orchestration and data access |
| **OCP** (Open/Closed) | Open for extension, closed for modification | Brittle systems requiring edits to existing code for new features, conditional branches on type checks, inflexible pipelines |
| **DIP** (Dependency Inversion) | Depend on abstractions, not concrete implementations | Tight coupling to external systems, hard-coded service instantiation, circular dependencies between modules |
| **Modularity & Separation** | Code partitions by concern with clear boundaries | Tangled imports, circular dependencies, unclear module boundaries, leaky abstractions, private details exposed |
| **Naming Clarity** | Names reflect intent and scope | Cryptic variable names, misleading function titles, scope ambiguity (is this global? local?), inconsistent naming patterns |

---

## Scoring Methodology

### Severity Model

Severity combines **likelihood** (will this actually cause a problem?) with **blast radius** (how many parts of the system break if it does?).

**🔴 Critical (Severity 1):** Likelihood × Blast Radius = high-probability defect or scaling blocker. Examples: DRY violation in the request pipeline (every request touches it), circular dependency between core modules, SRP violation in a hot path.

**🟡 Significant (Severity 2):** Real maintenance cost or technical debt, but not an immediate production risk. Examples: God class in a utility module, over-abstraction in the persistence layer (change is rare), naming inconsistency in non-critical code.

**🟢 Minor (Severity 3):** Improvement opportunity with low impact. Examples: single-file abstraction opportunity, unused conditional branch, cosmetic naming inconsistency.

### Per-Principle Rating Scale

Each principle receives a star rating (1–5) based on adherence across the reviewed code:

- ⭐ **1 star** = Severe violations, foundational issues affecting multiple modules
- ⭐⭐ **2 stars** = Frequent violations, scattered concerns across the codebase
- ⭐⭐⭐ **3 stars** = Mostly sound with isolated problem areas
- ⭐⭐⭐⭐ **4 stars** = Consistent adherence with minor notes
- ⭐⭐⭐⭐⭐ **5 stars** = Exemplary implementation across the scope

---

## Input Specification

### Scope Parameter

| Scope | Behavior |
|-------|----------|
| **Single file** | Review the specified file in full; report findings specific to that file |
| **Directory** | Review all source files in the directory and immediate subdirectories; treat as a module |
| **`--all` (full project)** | Smart sampling: entry points (main, index, bootstrap), top 15 largest files by LOC, top 20 most-imported modules. Prevents timeout on monoliths; report indicates coverage |

### Metadata Extraction

Before analysis, extract and report:
- Primary language(s) and version(s) (e.g., "Python 3.11", "TypeScript 5.2")
- Build system / package manager (cargo, npm, gradle, maven, pip, go modules)
- File count in scope
- Lines of code (LOC) in scope
- Key external dependencies (top 5–10 by import frequency)
- Estimated complexity (average cyclomatic complexity of functions)

---

## Output Specification

### Report Structure

**1. Header Block**
```
# Code Review: [scope name]
**Language:** Python 3.11  
**Files Analyzed:** 24 of 127 (smart sampling)  
**Lines of Code:** 8,432  
**Review Date:** 2026-08-23  
**Key Dependencies:** Flask, SQLAlchemy, Pydantic, pytest
```

**2. Executive Summary** (2–3 sentences)
- Overall code health assessment (e.g., "Strong architecture with clear separation of concerns")
- Single biggest concern (e.g., "Data access logic leaks into service layer")
- One specific win (e.g., "Excellent test coverage and naming consistency")

**3. Critical Findings** (🔴)
Each finding includes:
- **Principle Violated:** [e.g., SRP]
- **Title:** [e.g., "UserService mixes business logic with database queries"]
- **Location:** File, line range, function/class name (e.g., `src/services/user.py:45–180, class UserService`)
- **Why It Matters:** 1–2 sentences on likelihood and blast radius (e.g., "Every user-related change requires touching this class; high risk of regression.")
- **Code Example:** Actual snippet from the codebase (5–15 lines showing the violation)
- **Recommended Fix:** Concrete action (e.g., "Extract database queries into a repository class; inject it into the service")
- **Effort:** Time to fix (1–2 hours, 4–8 hours, 1–2 days, 1+ week)

**4. Significant Findings** (🟡)
Same structure as Critical, but with lower-priority fixes.

**5. Minor Findings** (🟢)
Same structure, condensed (1–2 sentences per finding).

**6. Per-Principle Ratings**
One line per principle, formatted as:
```
**SRP:** ⭐⭐⭐: Most modules have clear, single responsibilities. Exception: UserService 
(src/services/user.py) mixes business logic with data access; recommend refactor per Critical finding #1.
```

**7. Recommendations (Ordered by Impact)**
Group by refactoring phase or by principle:
```
## Phase 1: Decouple Data Access (Critical, 4–8 hours)
1. Create `UserRepository` class to encapsulate all DB queries
2. Inject repository into `UserService` constructor
3. Update tests to mock repository

## Phase 2: Simplify Configuration (Significant, 2–3 hours)
1. Remove 3 unused configuration parameters from bootstrap.py
2. Update documentation
```

**8. What's Working Well** (2–3 positive observations)
- "Test coverage is comprehensive; every public method has corresponding tests"
- "Naming is consistent and descriptive throughout; minimal guessing about intent"
- "Module boundaries are clear; imports are organized by layer"

---

## Review Process (Five Phases)

### Phase 1: Static Analysis
- Detect copy-paste code (string similarity matching on functions/classes)
- Identify unused imports, unreachable code, dead branches
- Measure cyclomatic complexity; flag functions > 10
- Detect deep nesting (> 4 levels); flag as KISS violation
- Identify circular imports using a module dependency graph

### Phase 2: Pattern Matching
- Match against known SOLID anti-patterns (e.g., ServiceLocator, God object, FeatureEnvy)
- Detect tight coupling: hard-coded `new` instantiation, static method dependencies, hidden globals
- Find naming inconsistencies: camelCase mixed with snake_case, abbreviations without definition
- Identify missing abstractions: repeated conditionals on type, repeated parameter sets

### Phase 3: Dependency & Coupling Analysis
- Build a module graph; detect circular dependencies, deep coupling chains (> 3 levels)
- Flag high-import modules (may be doing too much; potential SRP violation)
- Identify cross-cutting concerns: logging, error handling, validation scattered across modules

### Phase 4: Context & Pragmatism
- **Distinguish intentional from problematic:** A script is allowed to be simpler than production code. A test can mix concerns. Legacy code may have well-known defects that are acceptable.
- **Document exceptions:** If a violation is pragmatic (e.g., a single utility module wrapping a third-party API), note it and don't flag it as Critical.
- **Respect language idioms:** Python's duck typing is not loose coupling; Go's interface-based design is not SOLID-free.

### Phase 5: Severity Assignment & Reporting
- Assign severity by: (likelihood of causing a problem) × (scope of damage if it does)
  - A DRY violation in a utility function used in 50 places: High severity (one bug cascades)
  - A DRY violation in a script run once a week: Low severity (rare edit path)
- Group findings by severity, then by principle
- Create recommendations with effort estimates (based on lines of code to change, test coverage, dependency complexity)
- Generate final report in markdown

---

## Configuration Defaults

| Setting | Default | Notes |
|---------|---------|-------|
| **Critical threshold** | Issues blocking scalability or causing bugs in production | Adjust per org risk appetite; conservative orgs raise bar, startup may lower it |
| **Reporting depth** | All findings ≥ Minor severity | Can filter to `--severity critical,significant` for executive summary |
| **Sampling strategy (full project)** | Entry points (3) + top 15 largest files + top 20 most-imported | Adjustable in config for smaller projects |
| **Principle weighting** | Equal (1.0× each) | Can customize per org priorities (e.g., security-critical org weights DIP higher) |
| **Exclude patterns** | `**/vendor/**`, `**/generated/**`, `**/*.test.*` by default | Override in config |
| **Language support** | JavaScript/TypeScript, Python, Go, Java, C#, Rust | Extensible; add language config files |

---

## Output Formats

| Format | Use Case |
|--------|----------|
| **Markdown** (default) | Human-readable reports, version control, wiki storage |
| **JSON** | Tool integration, automated dashboards, severity filtering |
| **HTML** | Standalone reports, email distribution, archived reviews |
| **SARIF** | IDE integration, build-step violations, SonarQube import |

---

## Error Handling & Edge Cases

| Scenario | Behavior |
|----------|----------|
| **File does not exist** | Report error, skip file |
| **File is not code (binary, image, config)** | Report as skipped, document reason |
| **Language not supported** | Report limitation, skip file, suggest adding config |
| **Permission denied** | Report error, skip |
| **Scope is very large (> 1M LOC)** | Apply sampling strategy; report coverage (e.g., "Analyzed 127k LOC of 1.2M total; 11% coverage") |
| **No issues found** | Report "clean" assessment: all principles 4–5 stars, brief summary of strengths |
| **Circular dependency detected** | Report as Critical DIP violation; include cycle path (Module A → B → C → A) |
| **Ambiguous code** | Assume pragmatic intent; flag only if the pragmatism is undocumented |

---

## Metrics & Interpretation

### Cyclomatic Complexity Thresholds

- **≤ 3:** Excellent (low risk)
- **4–8:** Good (manageable)
- **9–15:** High risk (candidate for refactoring)
- **> 15:** Unacceptable (flag as Critical KISS violation)

### Coupling Metrics

- **High-import modules** (> 20 internal imports): Potential SRP violation
- **Circular dependencies:** Always Critical DIP violation
- **Coupling depth** (A → B → C → ...): > 3 levels is flagged as Significant Modularity violation

### Naming Consistency

- Measure snake_case vs. camelCase usage per file and per module; flag inconsistency > 20%
- Identify unexplained abbreviations (e.g., `usr` without a pattern); flag as Minor Naming violation

---

## Exit Conditions

The review is **complete** when:
- All files in scope have been analyzed (or sampling strategy has been applied)
- All findings are categorized and severity-scored
- Per-principle ratings are assigned (1–5 stars with 1–2 sentence justification)
- Recommendations are ordered by impact and effort-estimated
- Report is generated in requested format(s)
- Metadata and coverage summary are included

## Cross-File Reference

- **README.md**: Quick reference, getting started, common scenarios, troubleshooting
- **CUSTOMIZE.md**: Configuration options, principles adaptation, severity thresholds, language support
