# Auto README Skill: Customization Guide

> **There is no `auto-readme` binary.** This skill is a specification an agent
> executes. The config files below are real: you create them, and the agent
> reads them. The flag names that appear in this guide are the spec's vocabulary
> for the options, not a command on your PATH and not a package to install.
> See [README.md](./README.md) for how to invoke it.

## Configuration File

Create `.auto-readme.yaml` at your project root to customize behavior:

```yaml
# .auto-readme.yaml
title: "[Project Name]"
description: "[Project Description]"

# Sections to include (order matters)
sections:
  - overview
  - quick_start
  - installation
  - usage
  - configuration
  - development
  - testing
  - deployment
  - contributing
  - license

# Sections to skip
exclude_sections:
  - monitoring
  - api_reference

# Output style
output:
  format: markdown
  heading_levels: h2  # Start with ##
  code_fence: "```"
  tone: "technical"  # technical, friendly, minimal

# Language-specific settings
languages:
  python:
    package_manager: pip
    test_framework: pytest
  
  javascript:
    package_manager: npm
    runtime_version: node
```

## Custom Sections (Preservation)

To add sections that survive regeneration, wrap them in HTML comment markers in your README.md:

```markdown
<!-- auto-readme-custom -->
## Team Contacts

Reach out to:
- @alice for architecture questions
- @bob for deployment and ops

<!-- /auto-readme-custom -->
```

Content between `<!-- auto-readme-custom -->` and `<!-- /auto-readme-custom -->` is preserved unchanged through every update. Auto-generated sections refresh; custom sections persist.

## Language and Framework Support Extensions

Extend detection for custom languages or frameworks:

**Create `docs/auto-readme-extensions.yaml`:**

```yaml
technology_detection:
  custom_languages:
    - name: "elixir"
      manifest_file: "mix.exs"
      package_manager: "mix"
      test_framework: "exunit"
      version_command: "elixir --version"
    
    - name: "crystal"
      manifest_file: "shard.yml"
      package_manager: "shards"
      test_framework: "crystal spec"

  custom_frameworks:
    - name: "phoenix"
      marker_files: ["mix.exs"]
      detector: "contains_dependency(phoenix)"
      documentation_url: "https://phoenixframework.org"
    
    - name: "rails"
      marker_files: ["Gemfile"]
      detector: "contains_dependency(rails)"
      quick_start_command: "rails server"

section_generators:
  deployment:
    custom_rules:
      - condition: "has_docker_compose"
        template: "multi-container deployment"
        commands:
          - "docker-compose up -d"
          - "docker-compose logs -f"
      
      - condition: "has_kubernetes"
        template: "kubernetes deployment"
        commands:
          - "kubectl apply -f k8s/"
          - "kubectl port-forward svc/[Service] 8080:80"
```

The agent picks this up automatically when the file is at
`docs/auto-readme-extensions.yaml`. Point it somewhere else by naming the path
when you invoke the skill:

```
"generate the README, using the extensions in config/readme-extensions.yaml"
```

## Organizational Standards

Define company-wide section requirements and order:

**Create `.auto-readme-org-standards.yaml`:**

```yaml
org_standards:
  # Sections that every project must have
  required_sections:
    - overview
    - quick_start
    - contributing
    - license

  # Section order enforced across all projects
  canonical_section_order:
    - overview
    - quick_start
    - installation
    - configuration
    - development
    - testing
    - deployment
    - architecture
    - contributing
    - license
    - acknowledgments

  # Organization branding
  branding:
    company_name: "[Company Name]"
    company_url: "https://example.com"
    support_email: "support@example.com"
    
    default_license: "MIT"
    copyright_years: "2024"
    
    contributing_url: "https://example.com/contribute"
    code_of_conduct_url: "https://example.com/conduct"

  # Enforced style rules
  style:
    indent: 2
    line_length: 120
    heading_case: "title"
    code_comment_style: "bash"  # bash, python, javascript, etc.

  # Team assignment (shows in generated sections)
  team_contacts:
    devops_team: "devops@example.com"
    security_team: "security@example.com"
    documentation_team: "docs@example.com"
```

Apply org standards:

```bash
# Nothing to run. Commit .auto-readme-org-standards.yaml at the repo root, or
# somewhere your agent can read across projects, and name it when you invoke
# the skill if it is not in the default location.
```

## Deployment Target Integration

Generate deployment instructions for specific platforms:

```yaml
deployment_targets:
  aws:
    services:
      - lambda
      - ec2
      - ecs
      - s3
    detect_markers:
      - "*.tf"
      - "serverless.yml"
      - "sam.yaml"
    generated_sections:
      - aws_account_setup
      - aws_credentials_setup
      - deployment_command
      - monitoring_cloudwatch

  kubernetes:
    detect_markers:
      - "k8s/*.yaml"
      - "helm/Chart.yaml"
    generated_sections:
      - kubernetes_prerequisites
      - kubectl_commands
      - helm_setup
      - scaling_notes

  heroku:
    detect_markers:
      - "Procfile"
      - "runtime.txt"
    generated_sections:
      - heroku_login
      - deploy_command
      - log_viewing

  docker:
    detect_markers:
      - "Dockerfile"
      - "docker-compose.yml"
    generated_sections:
      - docker_build_command
      - docker_run_command
      - docker_compose_commands
```

## CI/CD Workflow Auto-Updates

Automatically update README when code changes:

**GitHub Actions example:**

```yaml
name: Sync README
on:
  push:
    paths:
      - package.json
      - pyproject.toml
      - go.mod
      - Dockerfile
      - .github/workflows/**
      - docs/**

jobs:
  readme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # There is no package to install. Make this skill's folder available to
      # whatever agent runner you use in CI, and have it read SPEC.md and update
      # README.md in place. Substitute your own runner for the placeholder.
      - name: Regenerate the README
        run: |
          <your-agent-runner> \
            --skill .claude/skills/generate-readme \
            --prompt "Update README.md from what is actually in this repo. Preserve custom sections."

      - name: Commit and push
        run: |
          git config user.name "README Bot"
          git config user.email "bot@example.com"
          git add README.md
          git commit -m "chore: sync README with latest project state" || true
          git push
```

**GitLab CI example:**

```yaml
sync-readme:
  # Your agent runner's image. There is no auto-readme image to pull.
  image: <your-agent-runner-image>
  script:
    - >
      <your-agent-runner>
      --skill .claude/skills/generate-readme
      --prompt "Update README.md from what is actually in this repo. Preserve custom sections."
  rules:
    - if: '$CI_PIPELINE_SOURCE == "push"'
      changes:
        - package.json
        - pyproject.toml
        - Dockerfile
  artifacts:
    name: readme-diff
    paths:
      - README.md
    expire_in: 1 day
```

## Custom Section Preservation

Sections wrapped with custom markers persist through regenerations:

```markdown
<!-- auto-readme-custom -->
## Deployment Checklist

1. Review changes with the team
2. Coordinate with ops
3. Run pre-deployment tests
4. Deploy to staging first
5. Monitor error rates for 30 minutes
6. Deploy to production

<!-- /auto-readme-custom -->
```

**Marker format:** `<!-- auto-readme-custom -->` ... `<!-- /auto-readme-custom -->`

Multiple custom sections are supported. Each persists independently.

**Important:** Custom content must not contain top-level Markdown headings (`#`) that conflict with auto-generated section titles, or both will appear in the output.

### Example: Adding Team-Specific Content

```markdown
<!-- auto-readme-custom -->
## Team Contacts

**Questions?** Reach out to:
- Architecture: [@alice](https://github.com/alice)
- DevOps: [@bob](https://github.com/bob)
- Documentation: [@carol](https://github.com/carol)

<!-- /auto-readme-custom -->
```

This section survives every README regeneration and can be manually edited without affecting auto-generated content.

## Configuration Validation

Ask the agent to check the configuration before relying on it:

```
"check .auto-readme.yaml against the spec before generating anything"
```

What it should confirm:
- YAML syntax validity
- Required fields present
- Section order contains only valid names
- Custom section markers properly formatted
- No duplicate section definitions

## Cross-File Reference

- **README.md**: Quick start, supported sections, common use cases, troubleshooting
- **SPEC.md**: Technical architecture, pipeline details, section generation logic, performance characteristics
