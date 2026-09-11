# README format specification

The section-by-section format `generate-readme` writes against, with the Mermaid
diagram patterns and the extended sections. Read it after Stage 2 of the pipeline
in SPEC.md, once the project's stack and shape are known, and before generating
any section body. Most projects use a minority of what is here.

The format adapts to project complexity. Simple tools get a short README. Complex multi-component systems get the full treatment.

### Core Sections (always include)

```markdown
# {Project Name}

{One clear sentence describing what this does and who it's for.}

## Quick Start

{3-5 commands from clone to running. No prose, just the commands with brief inline comments.}

\```bash
# Install dependencies
uv sync  # or: npm install

# Set up environment
cp .env.example .env  # fill in required values

# Run locally
uv run python agent/agent.py  # or: npm run dev
\```

## Architecture

{2-4 sentence overview of how the system works, followed by a Mermaid diagram.}

\```mermaid
graph LR
    A[Entry Point] --> B[Processing]
    B --> C[(Storage)]
    B --> D[Output]
\```

{Brief explanation of key components and their responsibilities.}
```

### Architecture Diagrams (for systems with 3+ components)

For complex systems, include a Mermaid architecture diagram showing entry points, processing layers, storage, and external services. Mermaid renders natively on GitHub, Notion, and most documentation platforms.

```markdown
## Architecture

\```mermaid
graph LR
    subgraph Entry Points
        TG[Telegram]
        WEB[Web App]
        VOICE[Voice]
    end

    subgraph Processing
        GW[API Gateway]
        AGENT[Agent Runtime]
        SHARDS[Cognitive Shards]
    end

    subgraph Storage
        DDB[(DynamoDB)]
        S3[(S3)]
    end

    TG --> GW
    WEB --> GW
    VOICE --> GW
    GW --> AGENT
    AGENT --> SHARDS
    AGENT --> DDB
    AGENT --> S3
\```
```

**Mermaid diagram rules:**
- Use `graph LR` (left-to-right) for architecture overviews
- Use `graph TD` (top-down) for flow diagrams
- Group related components with `subgraph`
- Label edges when the relationship isn't obvious (`-->|"async"|`)
- Keep diagrams under 30 nodes: split into multiple diagrams if larger
- Use shape syntax: `[service]` for processes, `[(queue)]` for queues, `[(database)]` for storage, `{decision}` for decisions

### Data Flow Diagrams (for systems with non-trivial request paths)

For each major request path, use a Mermaid flowchart showing how a request moves through the system. These answer "what actually happens when X?"

```markdown
## Message processing flow

\```mermaid
graph TD
    A[User sends message] --> B[Webhook Lambda]
    B --> C{User status?}
    C -->|new| D[Create pending user]
    C -->|pending/denied| E[Reply with status]
    C -->|approved| F[Queue in DynamoDB]
    F --> G[Async self-invoke]
    G --> H[Worker acquires lock]
    H --> I[Batch messages 1.5s]
    I --> J[Call AgentCore Runtime]
    J --> K[Send response]
    K --> L[Log usage + cost]
\```
```

Include 2-4 of these for complex systems, cover the most common paths a developer needs to understand.

### Business Flow Diagrams (for products with user lifecycles)

For products with users, document the key lifecycle and state-change flows using Mermaid stateDiagram or flowchart. These answer "what happens when a user does X?", state transitions and decision points.

Common business flows worth documenting:

| Flow | When to include |
|------|-----------------|
| User onboarding / signup | Product has user registration or approval |
| Subscription / tier changes | Product has paid tiers or entitlements |
| Approval workflows | Actions require human sign-off |
| Content publishing | User-generated content with review/moderation |
| Billing / payment | Usage-based pricing or invoicing |
| Account deletion / offboarding | Data lifecycle obligations |
| Escalation / alerting | Automated responses to thresholds |

```markdown
## User onboarding flow

\```mermaid
stateDiagram-v2
    [*] --> Pending: /start or sign up
    Pending --> Approved: Admin approves
    Pending --> Denied: Admin denies
    Approved --> Onboarding: First session
    Onboarding --> Active: Preferences set
    Denied --> [*]

    note right of Pending
        notify admin (Discord + Telegram)
        generate ref_id
    end note

    note right of Onboarding
        5 steps, ~30s
        language, TTS, privacy
    end note
\```

## Subscription tiers

\```mermaid
graph LR
    FREE[Free<br/>100K tokens] -->|upgrade| PRO[Pro $29/mo<br/>1M tokens, shards]
    PRO -->|upgrade| TEAM[Team $99/mo<br/>shared workspace]
    TEAM -->|upgrade| ENT[Enterprise<br/>unlimited]
    PRO -->|cancel/expire| FREE
    TEAM -->|cancel/expire| FREE

    style FREE fill:#f9f9f9
    style PRO fill:#e8f4fd
    style TEAM fill:#d4edda
    style ENT fill:#fff3cd
\```
```

**Rules for business flows:**
- Use `stateDiagram-v2` for lifecycle/state machines
- Use `graph TD` for decision trees and branching logic
- Focus on state changes and decision points, not implementation details
- Show what happens at each branch (approve vs. deny, upgrade vs. downgrade)
- Add `note` blocks for side-effects (notifications, data persistence)
- If a flow has a "sad path" (failure, timeout, edge case), show it

### Project Structure

```markdown
## Project Structure

\```
project/
├── src/              # Application source code
│   ├── api/          # HTTP route handlers
│   ├── models/       # Data models and schemas
│   └── services/     # Business logic
├── tests/            # Test suites
│   ├── unit/         # Unit tests (fast, isolated)
│   └── integration/  # Integration tests (real services)
├── infra/            # Infrastructure as code (Terraform)
├── scripts/          # Operational scripts
└── docs/             # Documentation
\```
```

Only include directories that exist. One-line descriptions only for non-obvious items.

### Development

```markdown
## Development

### Prerequisites

- {Runtime} {version} ({how to install if non-obvious})
- {Tool} ({what it's used for})

### Setup

\```bash
{Step-by-step from clone to working dev environment}
\```

### Testing

\```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_specific.py
\```

### Linting & Formatting

\```bash
# Check
uv run ruff check .

# Auto-fix
uv run ruff check . --fix

# Format
uv run ruff format .
\```
```

### Deployment

```markdown
## Deployment

\```bash
# Deploy to staging
./scripts/deploy.sh staging

# Deploy to production
./scripts/deploy.sh prod
\```

### Environments

| Environment | URL | Branch | Notes |
|-------------|-----|--------|-------|
| Staging | {url} | staging | Auto-deploys on push |
| Production | {url} | main | Manual deploy only |
```

### Extended Sections (include when applicable)

#### Infrastructure Table (for AWS/cloud-heavy projects)

When the project has 5+ cloud resources, use a component → service → purpose table:

```markdown
## Infrastructure

| Component | Service | Purpose |
|-----------|---------|---------|
| Agent runtime | Bedrock AgentCore | Hosts the agent |
| Webhook | Lambda + API Gateway | Telegram bot entry point |
| Users | DynamoDB | User profiles and state |
| File storage | S3 | Workspace bucket |
| Secrets | SSM Parameter Store | API keys, tokens |
| Monitoring | CloudWatch | Alarms and logs |
```

#### Test Suite Table (for projects with 5+ test suites/areas)

```markdown
## Testing

| Suite | What it tests |
|-------|---------------|
| `core` | Basic response, math, time awareness |
| `memory` | Same-session and cross-session recall |
| `admin` | Role gating, approve/deny operations |
| `edge-cases` | Empty input, emoji, long messages |

\```bash
# Run all
uv run pytest

# Run specific suite
uv run pytest tests/unit/test_core.py

# List suites
uv run pytest --co -q
\```
```

#### Scripts Table (for projects with 5+ operational scripts)

```markdown
## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/deploy.sh` | Deploy to staging or prod |
| `scripts/test-harness.py` | Comprehensive integration tests |
| `scripts/costs.py` | AWS daily cost report |
| `scripts/troubleshoot.py` | Diagnose stuck users |
```

If there are npm scripts, include those too:

```markdown
### npm shortcuts

\```bash
npm run deploy:staging     # deploy to staging
npm run test:quick         # smoke tests
npm run costs              # AWS cost report
npm run troubleshoot       # diagnose issues
\```
```

#### Dev Workflow Cheatsheet (for projects with a defined workflow)

When the project has a specific flow developers follow daily:

```markdown
## Dev Workflow

\```
triage → work → ship → verify
\```

| Step | Command | What it does |
|------|---------|-------------|
| Triage | `npm run feedback:triage` | Review incoming issues |
| Work | `npm run work -- "fix X"` | Build the fix |
| Ship | `npm run ship` | Validate → push → open PR |
| Verify | `npm run test:quick` | Smoke test the deployment |
```

#### Feature List (for products, not libraries)

Group features by domain. Use bold category headers. Keep each feature to one line. Call out security model, privacy, and observability separately:

```markdown
## Features

**Core capabilities**
- Feature one: brief description
- Feature two: brief description

**Security model**
- Session-scoped binding: actor_id from session, not LLM
- Admin tools code-gated: _gate_admin() checks role

**Privacy & data lifecycle**
- 30-day conversation retention, then scrubbed
- Account deletion purges all stores
```

#### API Reference (when HTTP endpoints exist)

```markdown
## API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /api/chat | Bearer | Send message |
| GET | /api/users | Admin | List users |
```

#### Configuration (when env vars are needed)

```markdown
## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `API_KEY` | Yes | External service API key |
| `DEBUG` | No | Enable debug logging (default: false) |
```

#### Contributing

```markdown
## Contributing

- Branch from `staging` (never commit directly to `main`)
- PRs require passing CI (lint + test)
- Linear history enforced (rebase, no merge commits)
- Pre-commit hooks run automatically (install with `uv run pre-commit install`)
```

