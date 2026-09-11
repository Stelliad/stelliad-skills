# CUSTOMIZE.md: Adaptation & Configuration Guide

> **There is no plumb binary.** This skill is a specification an agent
> executes. The config below is real: you create it, and the agent reads it.
> The the command invocations in this guide are the spec's vocabulary for the
> options, not something on your PATH and not a package to install.
> See [README.md](./README.md) for how to invoke it.

## What Can Be Customized

### 1. Principles Set

**Current framework:** Seven principles (DRY, KISS, SRP, OCP, DIP, Modularity, Naming)

**Customization questions:**
- Should we add or remove principles? (e.g., add YAGNI, Law of Demeter, composition over inheritance; remove Naming if linters already cover it)
- Do we have domain-specific patterns or anti-patterns to enforce? (e.g., event sourcing architecture, microservices communication patterns, security boundaries)
- Should certain principles be weighted differently? (security-critical code may prioritize strict DIP; startup code may allow pragmatic shortcuts in non-core modules)
- Are there language-specific idioms to respect? (Python duck typing, Go's interface-based design, Rust's lifetime model)

**Implementation:**
1. Create `.codereviews/principles.config.yaml`:
   ```yaml
   principles:
     - name: "DRY"
       weight: 1.0
       definition: "Logic and data structures should have single sources of truth"
       enabled: true
     - name: "YAGNI"
       weight: 0.5
       definition: "Don't build features you ain't gonna need yet"
       enabled: false
       note: "Advisory only; not blockers"
   ```

2. Custom principle (add to config):
   ```yaml
     - name: "Event Sourcing"
       weight: 1.5
       definition: "State changes are immutable events; replay recreates state"
       enabled: true
       applies_to: ["event-store", "audit", "payment"]
   ```

3. Each principle gets a `weight: [0.5–2.0]` multiplier (default 1.0). Weights are advisory for severity calculation, not automatic escalation.

---

### 2. Severity Thresholds

**Current framework:** Likelihood × Blast Radius = Severity (Critical/Significant/Minor)

**Customization questions:**
- What's unacceptable risk in your domain? Medical device code has zero tolerance; startup internal tools are more lenient.
- Should high-blast-radius issues in unused code still be Critical? (Probably not: flag as Significant instead.)
- What's your tolerance for technical debt? (Aggressive refactor: accept only Critical. Pragmatic: accept Significant. Ship-now: defer all but Critical.)
- Do team size, codebase age, or deployment frequency influence severity? (Larger team = stricter review standards; older code = higher tolerance for KISS violations.)

**Implementation:**
1. Create `.codereviews/severity.config.yaml`:
   ```yaml
   severity_matrix:
     # Likelihood: Low / Medium / High
     # Blast Radius: Trivial (1 module) / Small (1–5) / Large (5–20) / Massive (20+)
     low_trivial: "🟢 Minor"
     low_small: "🟢 Minor"
     low_large: "🟡 Significant"
     low_massive: "🟡 Significant"
     
     medium_trivial: "🟢 Minor"
     medium_small: "🟡 Significant"
     medium_large: "🟡 Significant"
     medium_massive: "🔴 Critical"
     
     high_trivial: "🟡 Significant"
     high_small: "🟡 Significant"
     high_large: "🔴 Critical"
     high_massive: "🔴 Critical"
   ```

2. Override for specific contexts:
   ```yaml
   overrides:
     - path: "**/vendor/**"
       severity_multiplier: 0.5
       note: "External code; only flag if it blocks our code"
     - path: "**/legacy/**"
       severity_multiplier: 0.5
       note: "Known issues; defer refactoring to next major version"
     - path: "**/auth/**"
       severity_multiplier: 2.0
       note: "Security-critical; raise bar for all principles"
   ```

---

### 3. Scope & Sampling Strategy

**Current framework:** Single file, directory, or full project with smart sampling (entry points + largest + most-imported)

**Customization questions:**
- What's the maximum LOC per review? (Prevents timeout; default 500k.)
- When sampling, which files matter most? (Last modified? Most complex? Most imported?)
- Should certain files *always* be reviewed? (security.py, auth.ts, models/, payment/)
- Should certain files *always* be skipped? (generated code, vendored libraries, legacy code marked for rewrite)

**Implementation:**
1. Create `.codereviews/sampling.config.yaml`:
   ```yaml
   max_scope_loc: 500000
   
   sampling_strategy:
     # For --all scope, review in this order of priority
     entry_points: 3           # main.py, index.ts, __init__.py, etc.
     largest_files: 15         # by LOC
     most_imported: 20         # highest fan-in (imported by most modules)
   
   always_include:
     - "**/security/**"
     - "**/auth/**"
     - "**/payment/**"
     - "config.py"
     - "models/*"
   
   always_exclude:
     - "**/generated/**"
     - "**/vendor/**"
     - "**/node_modules/**"
     - "**/*.min.js"
     - "**/*.test.ts"
     - "**/*_test.go"
   ```

---

### 4. Language Support

**Current framework:** Extensible; default support for JavaScript/TypeScript, Python, Go, Java, C#, Rust

**Customization questions:**
- Which languages does your team use? (Add support only for what's needed.)
- For each language, which analysis tools should we use? (AST parsers, complexity analyzers, import graph builders)
- Are there language-specific idioms or conventions to respect?

**Implementation:**
1. Create language configs in `.codereviews/languages/`:

   **`python.config.yaml`:**
   ```yaml
   language: "Python"
   extensions: [".py"]
   
   complexity_analyzer: "ast"
   import_parser: "ast"
   
   naming_convention: "snake_case"
   naming_exceptions:
     - "ClassName"
     - "CONSTANT_NAME"
   
   common_patterns:
     - name: "Repository Pattern"
       regex: ".*Repository\\.py"
       principle: "SRP"
   ```

   **`typescript.config.yaml`:**
   ```yaml
   language: "TypeScript"
   extensions: [".ts", ".tsx"]
   
   complexity_analyzer: "escomplex"
   import_parser: "ts-eslint"
   
   naming_convention: "camelCase"
   naming_exceptions:
     - "ClassName"
     - "CONSTANT_NAME"
   ```

---

### 5. Output Format

**Current framework:** Markdown (human-readable, version-control-friendly)

**Customization questions:**
- Do you need JSON for tool integration?
- Should output include inline code snippets, or just file:line references?
- Do you need HTML or PDF export for stakeholders?
- Should findings be actionable checklist items or narrative guidance?

**Implementation:**
1. Create `.codereviews/templates/report.md` (override default)
2. Create `.codereviews/templates/report.json` (machine-readable)
3. Create `.codereviews/templates/report.html` (web-viewable, with syntax highlighting)
4. Command-line flag:
   ```bash
   code-review --all --format json --output review.json
   code-review --all --format html --output review.html
   ```

---

### 6. Effort Estimation Scale

**Current framework:** Hours-based (1–2, 4–8, 1+ week)

**Customization questions:**
- Does your team prefer T-shirt sizing (XS, S, M, L, XL) or story points (1, 3, 5, 8, 13)?
- Should effort include testing and code review, or just implementation?
- Do you have historical velocity data to calibrate estimates?

**Implementation:**
1. Create `.codereviews/effort-scale.yaml`:
   ```yaml
   default_scale: "hours"
   
   scales:
     hours:
       xs: "< 1 hour"
       s: "1–2 hours"
       m: "4–8 hours"
       l: "1–2 days"
       xl: "1+ week"
     
     points:
       xs: 1
       s: 3
       m: 5
       l: 8
       xl: 13
     
     tshirts: [XS, S, M, L, XL]
   
   calibration: |
     Based on lines of code affected, test coverage, and deployment risk.
     Assume 1 developer, no blockers, standard review cycle.
   ```

---

### 7. Principle Definitions (Org-Specific)

**Current framework:** Generic SOLID + Modularity + Naming

**Customization questions:**
- Does your organization interpret SOLID differently?
- Do you have enforcement thresholds (e.g., "SRP means ≤ N reasons to change")?
- Should definitions include code examples or anti-patterns?

**Implementation:**
1. Create `.codereviews/principles/SRP.md`:
   ```markdown
   # Single Responsibility Principle
   
   ## Our Definition
   Each class or module should have exactly one reason to change.
   
   ## In Our Context
   - A service handles *either* business logic *or* data access, never both
   - A controller handles *either* HTTP concerns *or* routing, not validation
   - A utility module does *one* thing (parsing, encryption, formatting)
   
   ## Red Flags
   - Service class with both `.execute()` and `.query()` methods
   - Controller calling `database.insert()` directly
   - Utility file with helpers for 3+ unrelated tasks
   
   ## Green Lights
   - Service constructor injects dependencies; no "new" instantiation inside
   - Clear separation: `UserService` calls `UserRepository`
   - Utility module has a single purpose and few imports
   ```

---

### 8. Context & Pragmatism

**Current framework:** Reviews considers intent and applies common sense

**Customization questions:**
- Should scripts, tests, and throwaway prototypes be reviewed differently than production code?
- What's "acceptable" technical debt? (Strategic deferred work vs. negligent shortcuts)
- Should we flag only fixable issues, or also acknowledge hard tradeoffs?

**Implementation:**
1. Create `.codereviews/context.yaml`:
   ```yaml
   exceptions:
     - path: "**/tests/**"
       strictness: "low"
       note: "Test code prioritizes readability over DRY; duplication is acceptable"
       principles_exempted: ["DRY"]
     
     - path: "**/scripts/**"
       strictness: "low"
       note: "Scripts are one-off; KISS > SRP"
       principles_exempted: ["SRP", "OCP"]
     
     - path: "**/legacy/**"
       strictness: "low"
       note: "Known issues in legacy code; defer full refactoring. Flag only defects affecting new code."
       principles_exempted: ["SRP", "DRY"]
       only_flag: ["KISS", "Naming"]
     
     - path: "**/proto/**"
       strictness: "medium"
       note: "Prototype; less rigorous than production, but not exempt"
   ```

---

### 9. Positive Observations

**Current framework:** 2–3 positive observations per report

**Customization questions:**
- Should positives be always included, or only if code is reasonably good?
- What patterns should we actively praise? (TDD, dependency injection, strong naming)
- Does feedback on strengths feel encouraging or patronizing to your team?

**Implementation:**
1. Create `.codereviews/positive-patterns.yaml`:
   ```yaml
   patterns_to_praise:
     - "Comprehensive test coverage (> 80%)"
     - "Strong naming: functions names describe behavior"
     - "Clear module boundaries with minimal imports"
     - "Consistent error handling across functions"
     - "Well-organized directory structure"
     - "DI used consistently; no global state"
     - "Comments explain *why*, not *what*"
   ```

---

## Template Customization

### Finding Template

```markdown
### [Principle]: [Title]

**Severity:** 🔴 Critical | 🟡 Significant | 🟢 Minor  
**Location:** {file}:{line_start}–{line_end} in {function_name}()  
**Impact:** {1–2 sentence explanation of why this matters}

**Example:**
\`\`\`{language}
{code snippet from codebase showing the violation}
\`\`\`

**Recommendation:** {Specific fix, concrete action, 1–3 sentences}  
**Effort:** {Time estimate}
```

---

### Recommendation Template

```markdown
## Recommendation: [Title]

**Principle:** [SRP/OCP/DRY/etc.]  
**Severity:** {Critical/Significant/Minor}  
**Effort:** {Time estimate}  
**Impact:** {Why fixing this matters}

**Steps:**
1. {Action 1}
2. {Action 2}
3. {Test and validation step}
```

---

### Principle Rating Template

```markdown
**[Principle Name]:** ⭐⭐⭐ 
[Assessment: 1–2 sentences on adherence, with specific file or pattern references]
```

---

## Customization Checklist

- [ ] Define principles set (add/remove from default seven)
- [ ] Configure severity thresholds and likelihood × blast radius matrix
- [ ] Set scope and sampling strategy (max LOC, which files always review/skip)
- [ ] Add language support configurations for your stack
- [ ] Choose output format(s) and create templates
- [ ] Define effort estimation scale (hours, points, T-shirts)
- [ ] Customize principle definitions if divergent from SOLID
- [ ] Set context exceptions (scripts, legacy, generated code)
- [ ] Document org-specific positive patterns to flag
- [ ] Create `.codereviews/` folder structure and copy configs
- [ ] Test on 1–2 sample codebases and iterate
- [ ] Document any custom patterns or anti-patterns your org cares about

## Cross-File Reference

- **README.md**: Quick reference, getting started, common scenarios, CI/CD integration
- **SPEC.md**: Technical architecture, principles framework, scoring methodology, output specification
