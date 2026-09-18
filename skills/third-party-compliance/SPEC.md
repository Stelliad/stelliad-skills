# Third-Party Compliance: Specification

Evaluate a third-party app, service, or platform against a regulatory framework and produce a structured compliance summary suitable for customer conversations, proposals, and engagement deliverables.

## Procedure

### 1. Research the Vendor

Gather compliance documentation using multiple sources:

**Standard:**
- Web search: `{vendor} {framework} compliance`
- Web search: `{vendor} trust page security`
- Web search: `{vendor} BAA business associate agreement` (for HIPAA)
- Web search: `{vendor} SOC 2 report`
- Web search: `{vendor} data processing agreement DPA` (for GDPR)
- Web search: `{vendor} COPPA children data`

**Deep mode** (when your research tooling supports multi-source synthesis, or when the standard pass leaves gaps):
- A broader query synthesizing `{vendor} compliance {framework} certification data handling`
- Check for recent incidents: `{vendor} data breach` for the last 12-18 months
- Check subprocessors: `{vendor} subprocessors list`

**What to look for:**
- Official certifications (SOC 2 Type II report, HITRUST, ISO 27001)
- Willingness to sign a BAA (HIPAA) or DPA (GDPR)
- Data residency and hosting details
- Encryption (at rest, in transit)
- Data retention and deletion policies
- Subprocessor list and notification process
- Incident response and breach notification timeline
- Role-based access controls
- Audit logging capabilities
- Children's data handling (COPPA/FERPA)

### 2. Evaluate Against Framework Checklist

Run the vendor's documentation against the framework-specific checklist in `references/framework-checklists.md`. Read only the one being assessed against.

For each item, assign:
- ✅ **Compliant**: vendor explicitly meets this requirement (with evidence)
- ⚠️ **Conditional**: vendor meets it, but only with specific configuration, a signed addendum, or another stated condition
- 🔴 **Non-compliant**: the vendor's own documentation shows it does not meet this
- ❓ **Insufficient evidence**: no documentation found either way
- ➖ **Not applicable**: requirement doesn't apply to how you'd use this vendor

The headline verdict follows from the applicable items (everything not ➖), checked in this order:

1. Any 🔴: **🔴 Non-compliant**
2. Otherwise any ❓: **❓ Insufficient evidence**. An unanswered requirement blocks any claim of compliance, conditional or not
3. Otherwise any ⚠️: **⚠️ Conditionally compliant**, with every condition listed
4. Otherwise: **✅ Compliant**

In the output, `Score: {passed}/{applicable}` counts ✅ items over applicable items.

### 3. Assess Data Flow

Map how data moves through this vendor in the context of your use case:

- What data enters the vendor? (PII, PHI, children's data, financial data)
- Where is it stored? (region, encryption)
- Who can access it? (vendor employees, subprocessors, your admins)
- How long is it retained?
- Can it be deleted on demand?
- Is it used for training/improvement? (critical for AI services)

### 4. Identify Gaps and Mitigations

For any ⚠️, 🔴, or ❓ items:
- Is there a mitigation? (e.g., "they don't encrypt field-level, but you can encrypt before sending")
- Is there a configuration that fixes it? (e.g., "HIPAA mode is available but must be enabled")
- Is it a blocker or a risk you accept with documentation?
- For ❓: what would settle it? Name the document to request or the question to put to the vendor

### 5. Produce Assessment

Write the assessment using the template in `references/output-format.md`. Where it goes (a client folder, a shared compliance doc, inline in the conversation) is yours to decide. See CUSTOMIZE.md.

## Stack Assessment Mode

When no single vendor is named and you want the whole technology stack assessed, run vendor discovery first.

### Step 0: Exhaustive Vendor Discovery (MANDATORY)

Do NOT rely solely on documentation to build the vendor list. Run ALL of the following discovery methods and merge the results into a unified inventory before assessing any vendor.

> **Names only, never values.** Vendor discovery needs the variable *name*:
> `STRIPE_SECRET_KEY` tells you Stripe is a vendor, and the value adds nothing.
> Printing the value pulls a live credential into the conversation. Every
> command below is written to emit names, never values. The flag doing that
> work is `-o`, which prints only the matched name, or `-l` in Source 6,
> which prints only the file name. Never drop either to see more context:
> without them `grep` prints the whole line, value included. (`-h` only hides
> file names and protects nothing.) Do not print a secret's value under any
> circumstance while running this skill. That rule holds regardless of what
> your organization's own credential-handling policy says, because a scan
> like this one is exactly the kind of place a credential leaks by accident.

**Source 1: Environment files** (highest signal)
```bash
# Every variable name, never a value: -o stops at the "=", sed drops "export" and the "=".
find {repo_path} \( -name ".env*" -o -name "*.env" \) -type f -print0 \
  | xargs -0 -r grep -hoE "^[[:space:]]*(export[[:space:]]+)?[A-Za-z_][A-Za-z0-9_]*[[:space:]]*=" \
  | sed -E 's/^[[:space:]]*(export[[:space:]]+)?//; s/[[:space:]]*=$//' | sort -u
```
Collect every name, not just the ones with a telling suffix: `SENTRY_DSN`, `GOOGLE_CLIENT_ID`, and `REDIS_HOST` all point at a vendor. Suffixes like `_API_KEY`, `_SECRET`, `_TOKEN`, `_DSN`, `_URL`, `_HOST`, and `_CLIENT_ID` help decide which names to look at first. They are not a filter.

**Source 2: Docker Compose / infrastructure**
```bash
# Images, then variable names. Neither command prints a value.
find {repo_path} -name "docker-compose*" -type f -print0 | xargs -0 -r grep -hoE "image: *[^ ]+" | sort -u
find {repo_path} -name "docker-compose*" -type f -print0 \
  | xargs -0 -r grep -hoE "[A-Z0-9_]+(_API_KEY|_SECRET|_URL|_TOKEN)" | sort -u
```
Every external image, every environment variable pointing to a service = a vendor.

**Source 3: Package manifests**
```bash
# Node: dependency lines from every package.json, at any depth, outside node_modules
find {repo_path} -name package.json -not -path "*/node_modules/*" -type f -print0 \
  | xargs -0 -r grep -hE '"@|"(stripe|twilio|openai|pinecone|supabase|firebase|aws-sdk|resend)"' | sort -u

# Python: dependency lines, skipping comments, blank lines, and any line with a URL
# (a private package index URL can carry a token)
find {repo_path} \( -name "requirements*.txt" -o -name pyproject.toml \) -not -path "*/node_modules/*" -not -path "*/.venv/*" -type f -print0 \
  | xargs -0 -r grep -hvE '://|^[[:space:]]*(#|$)' | sort -u
```
Look for SDK packages that imply a third-party service (e.g., `@supabase/supabase-js` = Supabase, `stripe` = Stripe, `twilio` = Twilio, `@pinecone-database/pinecone` = Pinecone).

**Source 4: Infrastructure-as-code**
```bash
# Terraform: provider, resource, module, and data block headers, at any depth
find {repo_path} -name "*.tf" -not -path "*/.terraform/*" -type f -print0 \
  | xargs -0 -r grep -hoE '^[[:space:]]*(provider|resource|module|data)[[:space:]]+"[^"]+"' | sort -u

# CDK/SAM/CloudFormation
find {repo_path} -name "*.yaml" -path "*infra*" -o -name "*.json" -path "*cdk*"
```

**Source 5: Frontend build-time variables**
```bash
# Frontend variable names only: -o prints the name, never the value after it
find {repo_path} \( -name "next.config*" -o -name ".env*" \) -not -path "*/node_modules/*" -type f -print0 \
  | xargs -0 -r grep -hoE '(NEXT_PUBLIC|REACT_APP|VITE)_[A-Za-z0-9_]+' | sort -u
```
Frontend env vars often reveal client-side SDK integrations (Google Maps, Stripe.js, analytics, etc.).

**Source 6: Committed credentials scan** (security finding, not just vendor discovery)
```bash
# Which env files hold something shaped like a real credential, not a placeholder.
# -l prints file names only. A prefix only counts right after "=" and when the value then has an
# uppercase letter or digit, so PRE_, CORE_ and re_index_all_documents don't match. KEY has to start
# a segment of the name, so API_KEY, AWS_ACCESS_KEY_ID, KEYCLOAK_CLIENT_SECRET and KEYSTORE_PASSWORD
# match and MONKEY_ doesn't.
find {repo_path} -name ".env*" ! -name "*.example" -type f -print0 \
  | xargs -0 -r grep -lE "=[[:space:]]*[\"']?(sk-|sk_|whsec_|re_)[a-z_-]*[A-Z0-9][A-Za-z0-9_-]{12,}|^[[:space:]]*(export[[:space:]]+)?([A-Za-z0-9]+_)*KEY[A-Za-z0-9]*(_[A-Za-z0-9]+)*[[:space:]]*=[[:space:]]*[\"']?[A-Za-z0-9/+=_-]{20,}"
```
This one is deliberately `grep -l`: it reports *which file* matched and never
the matching line. Keep it that way.

A match is a lead. It becomes a **Critical security finding** when git tracks the file now or ever committed it, whatever `.gitignore` says today: adding a file to `.gitignore` doesn't untrack it, and history keeps every version. These print file names only:

```bash
git -C {repo_path} rev-parse --is-inside-work-tree >/dev/null 2>&1 || echo "NOT A GIT REPO: tracked and committed status was not checked"
git -C {repo_path} ls-files -- '*.env*' ':!*.example' 2>/dev/null
git -C {repo_path} log --all --diff-filter=A --name-only --format= -- '*.env*' ':!*.example' 2>/dev/null | sed '/^$/d' | sort -u
```

Inside a git repository, no output at all means no env file is tracked now or was ever committed. Outside one, the first line reads NOT A GIT REPO and the rest is silent: report that this check didn't run, rather than reading the silence as clean.

A live key in version control is direct evidence against the credential controls SOC 2 and HIPAA both expect. Treat it as a rotation event.

**Source 7: CI/CD pipelines**
```bash
find {repo_path} \( -path "*/.github/workflows/*" -o -path "*/.gitlab-ci*" -o -name "Dockerfile*" \) -type f -print0 2>/dev/null \
  | xargs -0 -r grep -hoE "[A-Z0-9_]*(SECRET|TOKEN|KEY|_URL)[A-Z0-9_]*" | sort -u
```
A hardcoded value in a workflow or Dockerfile is a Critical finding. Report the
file and the variable name. **Never quote the value**, and treat it as a rotation
event under your own incident-response process.

**Source 8: README and documentation references**
- Check `README.md`, `CLAUDE.md`, `AGENTS.md`, any `docs/` directory
- These often mention integrations not yet reflected in env files

**Merge into unified inventory:**

After running all sources, produce a deduped list:

| Vendor | Discovered via | Purpose | Data classification |
|--------|---------------|---------|---------------------|
| {name} | env / package.json / docker / infra / docs | {what it does} | PII / Financial / Public / Internal |

Only THEN proceed to Step 1 (research) for each vendor in the inventory.

### Step 1: Read the project's own spec, scope docs, and status notes for business context

This gives you the regulatory framing (which frameworks apply) and business context (what data flows through the system), but NOT the complete vendor list. That came from Step 0.

### Step 2: Run individual assessments for each vendor against the relevant framework

### Step 3: Produce a summary matrix

```markdown
## Stack Compliance Matrix: {Project}

| Vendor | Purpose | HIPAA | COPPA | SOC 2 | Action Required |
|--------|---------|-------|-------|-------|-----------------|
| {vendor} | {purpose} | ✅ BAA signed | ⚠️ No specific COPPA | ✅ | {action} |
| ... | ... | ... | ... | ... | ... |
```

### Step 4: Credential Hygiene Audit

After vendor discovery, explicitly check:
- Are there `.env` files (non-example) committed to git?
- Are there backup files with credentials (`.env.backup*`, `.env.local`, `.env.dev`)?
- Does `.gitignore` cover ALL env file variants?
- Are there hardcoded API keys in source files?
- Are there secrets in CI/CD config or Dockerfiles?

This is NOT optional. A vendor stack that passes doesn't help if the codebase itself leaks credentials, so include it in every stack assessment.

## Rules

- **Never claim compliance without evidence.** If you can't find documentation, say "insufficient evidence": don't assume.
- **Date everything.** Compliance status is point-in-time. Certifications expire, policies change.
- **Distinguish "eligible" from "compliant."** A cloud provider being HIPAA-eligible doesn't make YOUR deployment HIPAA-compliant until you configure it correctly.
- **Note configuration requirements.** Many services require specific settings to be compliant (e.g., HIPAA-eligible services need a BAA + specific configuration).
- **Flag AI training clauses.** For AI services especially: does the vendor use customer data for model training? This is often a HIPAA/COPPA deal-breaker.
- **Check recency.** A SOC 2 report from two years ago is stale. HIPAA BAAs that reference deprecated services are gaps.
- **Include alternatives.** If a vendor fails, suggest compliant alternatives you could use instead.
- **Make the output shareable.** The assessment document should be professional enough to email to a customer or include in a proposal appendix.

## Staleness Tracking

Assessments get stale. Track freshness:

- **< 90 days:** Current: use as-is
- **90-180 days:** Aging: verify certifications haven't expired
- **> 180 days:** Stale: re-run before using in customer communications

Store the assessment date in the output. Fold a recurring check into whatever review cadence your org already has. See CUSTOMIZE.md.

## Completeness Checklist (Self-Verification)

Before finalizing ANY stack assessment, confirm you checked ALL of these sources. If you skipped one, go back. The ten rows cover the eight sources plus Step 4's `.gitignore` check, with environment files split into example and real files.

| # | What to check | From | Checked? | What it catches |
|---|---------------|------|----------|-----------------|
| 1 | `.env.example` (root AND per-service) | Source 1 | [ ] | Primary vendor list: every API key = a vendor |
| 2 | ALL `.env*` files (`.env.dev`, `.env.local`, `.env.backup*`, `.env.docker`, `.env.production.example`) | Source 1 | [ ] | Additional vendors + **credential exposure finding** |
| 3 | `docker-compose*.yaml` / `docker-compose*.yml` (ALL variants: dev, prod, base) | Source 2 | [ ] | Self-hosted services, service images, env var pass-through |
| 4 | `package.json` / `pyproject.toml` / `requirements.txt` (ALL: root, backend, frontend, services) | Source 3 | [ ] | SDK dependencies that imply vendor relationships |
| 5 | Infrastructure-as-code (`*.tf`, `cdk`, `serverless.yml`, `sam.yaml`) | Source 4 | [ ] | Cloud services, managed resources |
| 6 | CI/CD (`.github/workflows/`, `Dockerfile*`) | Source 7 | [ ] | Build-time secrets, deployment targets |
| 7 | Frontend env vars (`NEXT_PUBLIC_*`, `REACT_APP_*`, `VITE_*`) | Source 5 | [ ] | Client-side integrations (maps, analytics, payment widgets) |
| 8 | `.gitignore` coverage for secrets | Step 4 | [ ] | Whether env files are ACTUALLY ignored (credential hygiene) |
| 9 | Git-committed env files (non-example) | Source 6 | [ ] | **Critical finding** if live credentials are in version control |
| 10 | README / docs / architecture files | Source 8 | [ ] | Mentioned integrations not yet in code |

### Common Misses

These are the vendors most commonly overlooked on first pass:

| Missed Vendor Type | Why It Gets Missed | Where to Find It |
|--------------------|--------------------|------------------|
| LLM routing proxies (OpenRouter, LiteLLM) | Look like "just another API key" | `OPENROUTER_API_KEY`, `LITELLM_*` in env |
| Integration orchestrators (Composio, Zapier, Make) | Abstractly named, not obvious from package name | `COMPOSIO_*`, `ZAPIER_*` in env |
| Data enrichment APIs (people or company lookup) | Industry-specific, not household names | Vendor-specific env var prefixes |
| Domain-specific vertical services | Domain-specific vendor nobody outside that industry knows | Vendor-specific env var prefixes |
| Voice/telephony (beyond primary) | Projects often have TWO voice vendors | e.g. `TELNYX_*` alongside `TWILIO_*` |
| Email senders (Resend, Postmark) | Overshadowed by bigger vendors | `RESEND_*`, `POSTMARK_*` in env |
| Self-hosted open source with cloud tiers | "We self-host it": but does it phone home? | DocuSeal, Supabase, n8n in docker-compose |
| Frontend copilot/AI SDKs | Framework deps, not obvious as "vendors" | `@copilotkit/*`, `@ai-sdk/*` in frontend package.json |
| Marketplace/hub APIs (RapidAPI) | Single key, multiple downstream vendors | `RAPIDAPI_KEY`: must inventory WHICH endpoints |
| Webhook receivers | Not env vars: they receive, not call | Webhook route handlers in code |

### Data Classification Quick Reference

For each discovered vendor, classify the data it touches:

| Classification | Examples | SOC 2 Impact | Action Required |
|----------------|----------|--------------|-----------------|
| **PII** | Names, emails, phones, addresses | In scope: must have SOC 2 or documented controls | Verify vendor compliance |
| **Financial** | Payment data, invoices, account balances | In scope + PCI if card data | Verify PCI (payments) or SOC 2 |
| **Confidential** | Contracts, pricing, internal strategy | In scope: confidentiality criteria | Verify NDAs + SOC 2 |
| **Credentials** | OAuth tokens, API keys, passwords | In scope: security criteria | Verify handling, rotation, storage |
| **Public** | Published content, public company records | Likely out of scope | Document why it's excluded |
| **Internal** | Logs, metrics, feature flags | May be in scope if they contain PII traces | Check for PII leakage |

### Final Verification Question

> "If an auditor asked 'show me every third-party service that touches data in this system,' would my vendor list survive that question?"

If the answer is "maybe not", you missed something. Go back to Step 0.
