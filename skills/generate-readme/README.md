# Auto README Skill

Generate accurate READMEs by analyzing your actual codebase, no templates, no guessing. The README automatically reflects your dependencies, structure, frameworks, and deployment setup and stays synchronized with what's really in your repo.

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r generate-readme /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/generate-readme

or: "generate a README for this project from what is actually in it"
```

The agent reads [SPEC.md](./SPEC.md) and does the work. The `auto-readme` flags in the spec are its vocabulary
for the update modes, not a command on your PATH.

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly.
[CUSTOMIZE.md](./CUSTOMIZE.md) is where you set the thresholds and policy for
your stack.

## Prerequisites

- A project with at least one configuration file (`package.json`, `pyproject.toml`, `go.mod`, etc.)
- Git repository initialized in the project root
- Read access to project files (no special permissions required)

## Quick Start

Generate or update your README:

```bash
auto-readme                    # Generate README.md for current project
auto-readme --update           # Refresh existing README, preserve custom sections
auto-readme --dry-run          # Preview without writing
auto-readme --validate         # Check if README matches project state
```

## How It Works

The pipeline scans four areas and generates relevant sections automatically:

1. **Manifests** (`package.json`, `pyproject.toml`, `go.mod`, etc.): detects language, dependencies, versions
2. **Directory structure**: identifies tests, source code, documentation, deployment targets
3. **Configuration** (`Dockerfile`, Terraform, workflows, `.env.example`): extracts deployment and runtime details
4. **Entry points**: locates main functions and frameworks (Express, Django, Spring Boot, etc.)

**Result:** A README that documents what's actually there.

## Supported Sections

Each section appears only if the detection rules match:

- **Overview**: Project name and description
- **Quick Start**: Installation and run commands for your language
- **Installation**: Package manager instructions
- **Usage**: How to invoke the project
- **Configuration**: Environment variables and `.env.example` fields
- **Development**: Dev dependencies, setup scripts, local testing
- **Testing**: Detected test framework and commands
- **Deployment**: Docker, Kubernetes, AWS, Terraform instructions
- **API Reference**: HTTP routes from detected frameworks
- **Contributing**: Link to `CONTRIBUTING.md` if present
- **License**: License type if license file found

## Preserving Custom Content

Wrap your own sections with markers to survive regeneration:

```markdown
<!-- auto-readme-custom -->
## Deployment Checklist

- [ ] Run database migrations
- [ ] Coordinate with ops
- [ ] Monitor error rates

<!-- /auto-readme-custom -->
```

All content between these markers stays unchanged through every update. Auto-generated sections refresh; custom sections never do.

## Common Use Cases

**New project?** Generate initial README:
```bash
auto-readme && git add README.md && git commit -m "docs: initial README"
```

**Keep it in sync?** Update after dependency or structure changes:
```bash
auto-readme --update
```

**Enforce standards?** Fail CI if README is out of date:
```bash
auto-readme --validate || exit 1
```

**Team-specific sections?** Mark them as custom and add once:
```markdown
<!-- auto-readme-custom -->
## Team Contacts
Contact @alice for architecture, @bob for ops.
<!-- /auto-readme-custom -->
```

## Options & Configuration

```bash
auto-readme [PATH]
  --update              Refresh README, preserve custom sections
  --dry-run             Preview without writing
  --validate            Exit non-zero if README is outdated
  --config FILE         Load .auto-readme.yaml from custom path
  --exclude SECTIONS    Omit sections (comma-separated list)
  --verbose             Show detailed analysis
```

Create `.auto-readme.yaml` at your project root:

```yaml
title: "My Project"
sections: [overview, quick_start, development, testing, deployment]
exclude_sections: [monitoring]
output:
  tone: technical
```

See `CUSTOMIZE.md` for full configuration including team-specific sections, deployment targets, org standards, and language support extensions.

## Integration

**GitHub Actions**: Auto-update README when manifests change:

```yaml
name: Sync README
on:
  push:
    paths: [package.json, pyproject.toml, Dockerfile]
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: auto-readme --update
      - run: |
          git config user.name "README Bot"
          git config user.email "bot@example.com"
          git add README.md
          git commit -m "chore: sync README" || true
          git push
```

**Pre-commit hook**: Validate before each commit:

```bash
#!/bin/bash
auto-readme --validate || exit 1
```

## Troubleshooting

**"No manifest found?"** Provide hints:
```bash
auto-readme --verbose
```

**"Section X didn't generate?"** Check detection rules:
```bash
auto-readme --verbose | grep "detection"
```

**"Custom section disappeared?"** Verify marker format:
```markdown
<!-- auto-readme-custom -->
Your content here
<!-- /auto-readme-custom -->
```

**"README out of date?"** Regenerate:
```bash
auto-readme --update
```

## Performance

Single-pass directory traversal with O(n) performance. Benchmarks on typical projects:
- 1,000 files, 8 config files, 8 sections: ~150ms
- 5,000 files (monorepo): ~400ms
- 50,000+ files with aggressive exclusions: ~1–2 seconds

See `SPEC.md` for detailed performance characteristics.

## What It Doesn't Do

- Write or fix code
- Generate diagrams automatically (detects infrastructure, suggests alternatives)
- Parse arbitrary business logic from source
- Extract full API docs from docstrings (detects framework routes only)

Hand-written content always wins. Use this to get 80% of the way there, then add project-specific details.

## See Also

- `SPEC.md`: Technical architecture, pipeline details, section generation logic, writing rules, performance characteristics
- `CUSTOMIZE.md`: Configuration reference, custom sections, team standards, CI/CD integration, language extensions
- `references/readme-format.md`: The full section-by-section format, with Mermaid diagram patterns
- `assets/readme-template.md`: The bare template at three complexity tiers
- `assets/example-readme.md` and `assets/example-architecture.md`: A worked pair for a fictional platform, showing the rules applied

## License

See LICENSE file.
