# README Template: Your Organization

> This is the standard README format for all Your Organization projects. Sections are included based on project complexity, not every project needs every section.

---

## Minimal (scripts, prototypes, simple tools)

````markdown
# {Project Name}

One sentence: what it does, who it's for.

## Quick Start

```bash
# Install
uv sync

# Run
uv run python main.py
```

## Project Structure

```
├── src/          # Source code
├── tests/        # Tests
└── scripts/      # Operational scripts
```

## Development

### Prerequisites
- Python 3.12+
- uv

### Testing
```bash
uv run pytest
```
````

---

## Standard (most projects)

Adds: Architecture, Deployment, Configuration, Contributing.

````markdown
# {Project Name}

One sentence: what it does, who it's for.

## Quick Start

```bash
uv sync
cp .env.example .env       # fill in values
uv run python main.py
```

## Architecture

2-3 sentences on how it works.

```
[Input] → [Processing] → [Storage] → [Output]
```

## Project Structure

```
├── src/
├── infra/
├── tests/
└── scripts/
```

## Development

### Prerequisites
- Python 3.12+, uv, AWS CLI, Terraform

### Setup
```bash
git clone ...
uv sync
uv run pre-commit install
```

### Testing
```bash
uv run pytest tests/unit/ -v
```

### Linting
```bash
uv run ruff check .
uv run ruff format .
```

## Deployment

```bash
./scripts/deploy.sh staging
./scripts/deploy.sh prod
```

| Environment | Branch | Notes |
|-------------|--------|-------|
| Staging | staging | Auto-deploy on merge |
| Production | main | Manual only |

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Connection string |
| `API_KEY` | Yes | Service key |

## Contributing

- Branch from `staging`
- PRs require passing CI
- Linear history enforced
````

---

## Complex System (production products)

Adds: Business Flows, Infrastructure Table, Feature List, Test Suite Table, Dev Workflow, npm Scripts.

See the **Example README** (`example-readme.md`) for a complete real-world example.

---

## Section Reference

| Section | When to include | Complexity |
|---------|-----------------|-----------|
| Quick Start | Always | All |
| Architecture (text) | Always | All |
| Architecture (ASCII diagram) | 3+ services | Standard+ |
| Data Flow diagrams | Async processing, webhooks | Standard+ |
| Business Flow diagrams | User lifecycles, subscriptions, approvals | Complex |
| Project Structure | Always | All |
| Features (grouped) | Products with users | Complex |
| Development | Always | All |
| Testing (suite table) | 5+ test areas | Complex |
| Deployment | Deploy script exists | Standard+ |
| Infrastructure (table) | 5+ cloud resources | Complex |
| API Reference | HTTP endpoints | Standard+ |
| Configuration | 3+ env vars needed | Standard+ |
| Scripts (table) | 5+ operational scripts | Complex |
| Dev Workflow (cheatsheet) | Defined daily flow | Complex |
| npm shortcuts | 10+ package.json scripts | Complex |
| Contributing | Branch protection active | Standard+ |

---

## Writing Rules

1. **Commands over prose.** Show the command, not a paragraph about it.
2. **Specific over generic.** Real paths, real scripts, real URLs.
3. **Current over aspirational.** Document what exists, not what's planned.
4. **Scannable.** A developer should find what they need in <60 seconds.
5. **No duplication.** Link to DEVELOPMENT.md / ARCHITECTURE.md for deep dives.

## Anti-patterns

- ❌ Badge walls (shields.io spam)
- ❌ Table of contents for short READMEs
- ❌ "Built with" logo grids
- ❌ Screenshot galleries
- ❌ Feature checklists (✅❌)
- ❌ "This is the README for Project X" (obviously)
- ❌ License section (there's a LICENSE file)
- ❌ Verbose setup narratives ("First you'll want to...")

## Length Targets

| Complexity | Lines |
|-----------|-------|
| Simple script/tool | 50–100 |
| Standard app | 100–200 |
| Complex system | 200–400 |
| Monorepo | 300–500 |

If >500 lines, split into README + DEVELOPMENT.md + ARCHITECTURE.md.
