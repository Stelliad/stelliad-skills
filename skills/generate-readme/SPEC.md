# Auto README Skill: Technical Specification

## Pipeline Architecture

The Auto README skill generates project documentation through a staged discovery pipeline. Each stage produces normalized metadata that feeds into conditional section generation logic.

### Stage 1: File Inventory and Classification

The pipeline begins with recursive filesystem traversal from the repository root, applying exclusion patterns and classifying files by type and purpose.

**Universal exclusion patterns:**
- Directories: `node_modules/`, `venv/`, `.git/`, `dist/`, `build/`, `[language-cache]/`, `.cache/`, language-specific vendor directories
- Dotfiles: `.env`, `.env.local`, credential files, private keys
- Temporary files: `*.tmp`, `*.swp`, `.DS_Store`
- Compiled artifacts: `.pyc`, `.o`, `.class`, binary files

**File classification taxonomy:**
Each file receives one or more tags: `config` (manifest, config files), `source` (code), `test` (test files), `docs` (documentation), `build` (build scripts), `deploy` (deployment infrastructure), `script` (executable scripts), `data` (sample or fixture data).

Examples:
- `package.json` → `[config, source]`
- `Dockerfile` → `[deploy, config]`
- `src/main.py` → `[source]`
- `.github/workflows/ci.yml` → `[deploy, config]`
- `tests/test_api.go` → `[test]`

### Stage 2: Technology Detection

Pattern matching identifies the technology stack by examining file presence and content:

**Mandatory matches (filename-based):**
- `package.json` present → Node.js project
- `pyproject.toml` or `requirements.txt` → Python project
- `go.mod` → Go project
- `Cargo.toml` → Rust project
- `pom.xml` or `build.gradle` → JVM project
- `Dockerfile` → containerized deployment
- `.github/workflows/` → GitHub Actions CI/CD

**Inference matches (content or combination):**
- `tsconfig.json` + `package.json` → TypeScript project (refines Node type)
- `requirements-dev.txt` → Python with separated dev dependencies
- `docker-compose.yml` → multi-container local development
- `*.tf` files → Terraform infrastructure

The result is a `technologies` map: `{language: "Python", build: "setuptools", deploy: "Docker", cicd: "GitHub Actions"}`.

### Stage 3: Metadata Extraction

Structured metadata from configuration files:

**package.json (Node.js):**
- Name, description, version
- Main entry point, scripts section
- Dependency and dev-dependency counts
- Node version requirement (from `engines` field)

**pyproject.toml (Python):**
- Project metadata from `[project]` section
- Python version requirement from `requires-python`
- Dependencies organization (modern or legacy format)

**go.mod (Go):**
- Module path and Go version requirement
- Dependency count and versions

**Dockerfile:**
- Base image, exposed ports
- Entrypoint and CMD directives
- Multi-stage build detection

**GitHub Actions workflows:**
- Trigger events, job names, environment detection

Metadata is normalized to a common schema: `{key: value, source_file: path, confidence: "high"|"inferred"}`.

### Stage 4: Custom Section Detection

The pipeline identifies user-defined sections that must be preserved across regeneration:

**Detection rule:** Any top-level Markdown heading followed by the marker `<!-- auto-readme-custom -->` is treated as custom content and persists untouched.

Example:
```markdown
## Deployment Checklist
<!-- auto-readme-custom -->
Our team requires approval from [Role Name] before production deployments.
Coordinate with the platform team using [Process Link].

<!-- /auto-readme-custom -->
```

The pipeline stores the byte range of each custom block and re-injects it verbatim during updates, preserving formatting and embedded code.

**Limitation:** Custom sections must not contain top-level headings that conflict with generated section titles, or both versions will appear.

## Section Generation Logic

Before generating any section body, read `references/readme-format.md`. It
carries the section-by-section format, the Mermaid diagram patterns, and the
extended sections. Most projects use a minority of it, which is why it is read
here rather than up front: the project's stack and shape are known by this stage.

Each section has one or more **gates**: conditions that must be met for generation:

| Section | Gate Conditions | Data Source |
|---------|-----------------|-------------|
| Overview | Always | Name and description from config |
| Quick Start | `build_commands OR executable` | Package manager, scripts, entry point |
| Installation | `package_manager_detected` | `package.json`, `setup.py`, `go.mod`, etc. |
| Usage | `executable_script OR exported_api` | Entry point detection + framework detection |
| Configuration | `config_file OR env_vars_in_code` | `.env.example` presence, config patterns |
| Testing | `test_directory_exists AND test_framework_identified` | `/tests`, `/test` + framework detection |
| Deployment | `docker_present OR ci_cd_present` | Dockerfile, CI/CD workflow files |
| Development | `dev_dependencies_present OR setup_script` | Separate dev dependencies, setup scripts |
| API Reference | `http_framework_detected` | Framework detection in imports/dependencies |
| Contributing | `repository_url_present` | GitHub/GitLab URL presence |
| License | **Never.** See the License row in Writing Rules → Anti-patterns | Link to `LICENSE` from the footer instead |

### Section Content Examples

**Quick Start section** for Python:
```bash
pip install -e .
python -m [module_name]
```

**Testing section** detects framework and generates appropriate command:
- Jest/Vitest: `npm test`
- pytest: `pytest`
- Go: `go test ./...`
- Cargo: `cargo test`

**Deployment section** generates instructions based on detected infrastructure:
- Dockerfile present: Includes build and run commands
- GitHub Actions: Links to workflow files
- Kubernetes manifests: Resource summary

## Writing Rules

Detection decides which sections exist. These rules decide what goes inside them.
A README that is structurally correct and reads like a filled-in template has
failed, and it is the failure this skill exists to prevent.

### Voice and style

- **Direct and scannable.** People read a README when they are stuck or new. Respect their time.
- **Commands over prose.** Show the command, not a paragraph describing what the command would be.
- **Specific over generic.** Real paths, real script names, real URLs. Never "configure as needed".
- **Current over aspirational.** Document what exists, not what is planned. Where something is incomplete, say so plainly.
- **One source of truth.** Do not restate what another document already covers. Link to it.

### Anti-patterns

Never generate any of these, whatever the detection stages found:

| Anti-pattern | Why not |
|---|---|
| Badge walls | A row of shields.io badges is decoration. One, for CI status, if it earns its place |
| Table of contents on a short README | Under two screens, a ToC is noise |
| "Built with" logo grids | The stack belongs in prerequisites, not in a marketing strip |
| Screenshot galleries | One screenshot if the project has a UI. Zero if it is a backend |
| Feature checklists | Tick-and-cross feature lists belong on a marketing site |
| Verbose setup narratives | "First you will want to..." Just show the commands |
| Acknowledging the obvious | "This is the README for Project X." They are reading it |
| A License section | If a LICENSE file exists, people know where to look |

The License row overrides the `license_file_present` gate in the section table
above. Detect the file and link to it from the footer if you link at all. Do not
generate a section restating its terms.

These rules govern READMEs this skill **generates**. A hand-written README,
including the ones shipped alongside these skills, may carry whatever its author
decided.

### Images and diagrams

Capping the screenshot count says nothing about whether anyone can read it.

- **Every image gets alt text** that describes what it shows, not what it is
  called. "Dashboard with three panels: throughput, error rate, and cost" beats
  "screenshot".
- **Every diagram gets a prose lead-in** of one or two sentences carrying the
  same information the diagram carries. A Mermaid block is unreadable to a screen
  reader, and it is also unreadable in any context that does not render Mermaid.
  If the only place a fact appears is inside the diagram, it is not documented.
- **Never put a command, a credential name, or a path only in an image.** Text
  that a reader has to retype from a picture is text in the wrong format.

### Length targets

| Project complexity | Target length |
|---|---|
| Single script or small tool | 50–100 lines |
| Standard application | 100–200 lines |
| Complex multi-component system | 200–400 lines |
| Monorepo with many subsystems | 300–500 lines |

Past 500 lines, split it: README plus DEVELOPMENT.md plus ARCHITECTURE.md. The
README stays the entry point and links out to both.

### Multi-stack projects

Where a project has several subsystems in different languages:

1. The top-level README covers the whole system: architecture, quick start, structure.
2. Each subsystem gets a row in the structure table, not a section of its own.
3. Deep-dive documentation lives in the subsystem directory or in `docs/`.
4. Quick Start shows the single most common developer workflow, not one per subsystem.

### Existing documentation

Where the repository already carries `DEVELOPMENT.md`, `ARCHITECTURE.md`,
`CONTRIBUTING.md`, or an agent instruction file:

- Do not duplicate their content.
- Reference them, do not inline them: `See [DEVELOPMENT.md](./DEVELOPMENT.md) for detailed setup.`
- The README stays the high-level entry point.
- Extract the key commands, quick start and deploy, into the README even where
  they also appear elsewhere. A reader should not have to open a second file to
  run the project. This is the one place where the one-source-of-truth rule
  yields, and it yields only for commands.

## Update Mode Preservation Rules

The pipeline supports three modes for handling existing README files:

### Mode 1: Merge (Default)
Existing custom sections (marked with `<!-- auto-readme-custom -->`) are preserved in place. Auto-generated sections are regenerated and repositioned. If a custom section occupies a slot where auto-generated content would appear, the auto-generated section is skipped.

**Marker format:** Use `<!-- auto-readme-custom -->` ... `<!-- /auto-readme-custom -->` to wrap sections that must survive regeneration.

### Mode 2: Append-Only
If the README lacks custom markers and wasn't recently modified by this tool, the pipeline defaults to append-only mode: new sections are appended after existing content without modifying what exists. Used for cautious updates to hand-written READMEs.

### Mode 3: Overwrite
With `--force` flag, the entire README is regenerated from scratch. Custom sections are lost unless backed up with `--backup`.

## Configuration File Precedence

The pipeline loads configuration in this order, with later files overriding earlier ones:

1. **Built-in defaults**: Hardcoded section order and detection rules
2. **`.auto-readme-org-standards.yaml`**: Organization-wide standards (if passed via `--org-standards`)
3. **`.auto-readme.yaml`**: Project-level configuration (always loaded from project root)
4. **`docs/auto-readme-extensions.yaml`**: Custom language/framework extensions (if present)
5. **CLI flags**: `--exclude-sections`, `--config` override everything above

**Example precedence resolution:**
- Org standards define `sections: [overview, installation, deployment]`
- Project `.auto-readme.yaml` defines `sections: [overview, quick_start, installation]`
- Final result: `[overview, quick_start, installation]` (project config wins)
- CLI flag `--exclude-sections testing` removes `testing` if it existed at any level

**Config file paths:**
- `.auto-readme.yaml`: Required project root; project-level configuration
- `.auto-readme-org-standards.yaml`: Optional; pass via `--org-standards` flag
- `docs/auto-readme-extensions.yaml`: Optional; auto-discovered from `docs/` directory

## Edge Cases and Failure Modes

### Multiple Technology Stacks
If `package.json` and `pyproject.toml` both exist (monorepo or polyglot project):
1. Generate a "Supported Languages" section listing all runtimes
2. Include installation instructions for each package manager
3. Provide language-specific examples

### Empty Configuration
If no configuration files exist:
1. Infer language from file extensions (`.js`, `.py`, `.go`)
2. Generate only Overview section
3. Log a warning that metadata is inferred

### Monorepo Structure
If multiple project folders contain their own manifests:
1. Generate "Workspace" section listing sub-projects
2. Include workspace installation command
3. Add sub-project-specific instructions as subsections

Detection: Workspace config files (`lerna.json`, `pnpm-workspace.yaml`, `go.work`) or directory depth analysis.

### Stale Lock Files
If lock file was modified before the manifest:
1. Flag the dependency section as potentially stale
2. Recommend running package manager update
3. Include timestamp comparison in verbose output

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Directory not readable | Error: exit code 1, message to stderr |
| No configuration detected | Warning: generate from inferred language, prompt user to commit config file |
| Malformed JSON/YAML | Warning: skip that file, continue with other sources |
| Circular symlinks | Skip and log warning |
| Permission denied | Warning: skip file, continue |
| Conflicting metadata | Warning: report both, user resolves manually |

## Performance Characteristics

- Directory traversal: O(n) where n = number of files (excludes ignored paths)
- Metadata extraction: O(m) where m = config files (typically 3–8)
- Section generation: O(k) where k = generated sections (typically 5–12)
- Overall: sub-second for most projects on modern hardware

Benchmarks on typical projects:
- 1,000 files, 8 config files, 8 sections: ~150ms
- 5,000 files, monorepo: ~400ms
- 50,000+ files with aggressive exclusions: ~1–2 seconds

## Cross-File Reference

- **README.md**: Quick start, supported sections, common use cases, performance summary
- **CUSTOMIZE.md**: Configuration options, team sections, organizational standards, CI/CD integration
- **references/readme-format.md**: The section-by-section format this skill writes against, with Mermaid diagram patterns and the extended sections. Read it at generation time, once the project's stack and shape are known. Most projects use a minority of what is in it
- **assets/readme-template.md**: The bare template at three complexity tiers, minimal through full
- **assets/example-readme.md**: A worked README for a fictional multi-component platform, showing the writing rules applied rather than described
- **assets/example-architecture.md**: The companion ARCHITECTURE.md for the same project, showing what belongs outside the README once it passes 500 lines
