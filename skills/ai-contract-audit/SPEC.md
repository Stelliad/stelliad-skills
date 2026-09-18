# AI Contract Audit: Specification

**Audit the gap between what your contracts say about AI tools and how your team actually uses them.**

For engineering leaders and compliance teams building with Claude, OpenAI, Gemini, or any LLM. Runs against your own org's contracts and practices.

## The Problem

You have a DPA, an MSA, an SOW, and a security policy. You're also using AI tools to build. Claude Code for development, ChatGPT for research, maybe a fine-tuned model in production.

Three weeks later, your team adds a new tool. Or a tool changes its training defaults. Or your data handling widened to include customer data where before it was just internal.

**Did anyone update the paper?**

This skill checks. It does not edit contracts, it reports the gap and you decide.

## The Core Question

> Do our contracts, disclosures, and warranties match how we actually build with AI?

## What This Audits

| Module | What it checks | Scope |
|---|---|---|
| **A** | AI provider disclosure | Is every inference provider and dev tool listed where it should be? Does the disclosure match actual usage? |
| **B** | Model training posture | What data does each tool train on? What's our tier (API, business, consumer)? Is it actually off where we claim? |
| **C** | IP assignment | Can we actually assign AI-generated code to our client/customer? Does the warranty hold? |
| **D** | Confidentiality | Our contract can't bar AI tools if we use them. Does it? Does the carve-out match what we actually send? |
| **E** | Delivery warranties | If humans don't review every line, do our contracts promise it anyway? |
| **F** | Regulatory | GDPR, CCPA, EU AI Act: does our posture match our process? |

## How It Works

### Input
You provide:
- Your contracts (DPA, MSA, SOW, NDA, security policy)
- Your actual tooling config (what you use, where, and what data reaches it)
- Your data carve-outs (what data is in-scope, what's excluded)

### Process
The skill walks through Modules A–F, checking each contract statement against reality.

### Output
Three severity levels:
- 🔴 **Exposed**: your contract says one thing, you're doing another. Fix this now.
- ⚠️ **Drifting**: true today, but resting on a condition that just changed. Check it.
- ✅ **Clean**: verified against your actual documents and practices.

---

## The Six Modules

### Module A: AI Provider Disclosure (per contract)

**For every tool your team uses, is it disclosed where it should be?**

Two categories:
- **Inference providers**: AI services your product/deliverable calls at runtime (TTS, LLM, embedding service). *Always* disclosed.
- **Development tooling**: Assistants that write code (e.g., Claude Code, ChatGPT, Copilot). Disclosed *if* customer/user data reaches them; can be excluded if your data carve-out is narrow enough.

| ID | Check | What to verify |
|---|---|---|
| A-1 | Inference providers enumerated | Every AI service your product calls appears in your subprocessor disclosure. Derive the list from your SOW's architecture and your actual approved systems, not from the disclosure itself: reading the disclosure to check the disclosure proves nothing. |
| A-2 | Transfer mechanism named | Each provider's disclosure cites the agreement that governs it. A provider you contract with directly is not covered by a reseller's agreement, even if you reach it through that reseller. |
| A-3 | Category assignment defensible | Each tool sits in a category whose purpose matches what it does. If multiple categories apply, the disclosure states which one explicitly so it doesn't turn on taxonomy alone. |
| A-4 | Dev tooling status justified | If development tools are absent from your disclosure, a note records *why*. Check that the reason still holds against your current data scope. |
| A-5 | Carve-out width | Read your SOW or DPA's data-to-tooling clause. Does it admit only business contact data (e.g., employee emails), or has it widened to admit customer/user/production data? A widened carve-out silently turns every dev tool into an undisclosed subprocessor. |
| A-6 | Disclosed tools reconciled | Your DPA's tooling list, your SOW's systems section, and your subprocessor disclosure all name the same set. Drift between them is the most common defect. |
| A-7 | Retired tools removed | Tools you no longer use are struck, not left standing. A stale authorization is a live authorization. |
| A-8 | Comms tooling | Meeting recording, transcription, and summarization tools capture names, voices, emails. These are personal data and frequently missed. |

**Reporting rule:** Name the specific provider, the specific disclosure row (or its absence), and the specific contract clause that governs it. "Subprocessor disclosure may be incomplete" is not a finding, "[Provider] (inference provider) is not listed in your subprocessor disclosure, but your SOW's architecture section names it" is.

#### Authorized ≠ Used

Configuration and steering files establish what a tool is *permitted* to do. They do not establish what it *does*. A configured tool may never touch customer data; a contract may authorize a capability nobody exercises.

**Never report an authorization as a defect.** Before flagging a tool as an undisclosed subprocessor, establish that customer/user data actually reaches it. If you can't establish that from the documents, mark it unverified and ask, an assumption is not a finding.

### Module B: Model Training and Plan Tier

The most under-checked area, because the answer changes with a billing tier, not a contract.

| ID | Check | What to verify |
|---|---|---|
| B-1 | Tier confirmed, not assumed | Is your Claude plan an API key (Processor role, no training)? Is your OpenAI account on business tier (no training) or consumer (training on by default)? The tier must be established as fact, not assumed from the vendor's data sheet. |
| B-2 | SOW language matches tier | If your SOW or contract asserts "no training," that assertion must be true for the tier you actually use. A correct sentence about the wrong tier is a misrepresentation to your customer/partner. |
| B-3 | Training toggles off where they exist | If a vendor offers a model-improvement or data-retention setting, confirm it is off. Record when you checked it so you know when it needs re-checking. |
| B-4 | Retroactivity acknowledged | Turning a training toggle off is *not* retroactive. Data sent while training was on cannot be recalled from models already trained. Where that window existed, record it rather than quietly closing over it. |
| B-5 | Vendor DPAs on file | The governing DPA for each AI provider is obtained and kept on file, not merely cited by name. You need the actual terms. |
| B-6 | Zero-retention where promised | If your SOW promises deletion within a stated window (e.g., 30 days), the vendor's actual retention setting supports it. |

### Module C: IP Assignment over AI-Generated Code

Your contracts probably say you own or can assign the code you deliver. Purely AI-generated output has contested copyright status in the US, so that warranty may not hold.

| ID | Check | What to verify |
|---|---|---|
| C-1 | Assignment warranty scope | What does your MSA warrant about your right to assign IP? An unqualified warranty that you own all deliverables is stronger than the law supports when models generated them. |
| C-2 | Reusable tooling carve-out intact | Reusable code and tools you build stay yours; only client/customer-specific output is assigned. Check that your deliverable definition keeps that line clear even when the tooling was AI-generated. |
| C-3 | Open-source contamination | LLMs can emit code derived from copyleft-licensed training data (GPL, AGPL, etc.). Is there a license-scanning step before delivery? Does your indemnity cover a third-party claim arising from generated code? |
| C-4 | Third-party IP indemnity exposure | If an IP claim lands on AI-generated code, who bears it under your contract? Compare that exposure to your liability cap. |
| C-5 | Provenance record | For deliverables where IP ownership matters commercially, is there a record of what was generated versus written by humans? Absent one, your warranty rests on memory. |

### Module D: Confidentiality vs. Delivery Reality

| ID | Check | What to verify |
|---|---|---|
| D-1 | No self-contradicting clauses | Your contract can't bar entry of customer data into external AI tools if you use those tools to build. Does it? Does your client-facing contract have a carve-out matching your actual practice? |
| D-2 | Client-side symmetry | If you propose a clause barring your customer from using AI tools, can you meet that same standard yourself? |
| D-3 | Customer code in AI tools | Customer source code is confidential. Does your NDA and SOW together permit it reaching a disclosed AI provider without training? |
| D-4 | Secrets discipline | Credentials, keys, tokens, passwords: these must never reach an AI provider under any tier or training posture. This is a hard line. |

### Module E: Delivery Warranties

If humans don't review every line of code, your contract can't promise they do.

| ID | Check | What to verify |
|---|---|---|
| E-1 | Professional care standard | What standard of care do your contracts promise? Is it consistent with human + AI review, or does it imply human review only? |
| E-2 | QA floor preserved | With AI writing code and team reviews, how much time is allocated to testing and QA? Ensure QA is a distinct line item. |
| E-3 | Validation responsibility | AI outputs are probabilistic. Does your SOW explicitly allocate validation responsibility to the customer, not just to you? |
| E-4 | Key-person exposure | Do your contracts promise continuity or capacity you can't actually field? |
| E-5 | Insurance fit | Does your errors & omissions policy cover defects in AI-generated deliverables? If uncertain, flag it for your broker. |

### Module F: Regulatory Posture

| ID | Check | What to verify |
|---|---|---|
| F-1 | EU AI Act reach | If your product serves EU users or your team is EU-based, do you act as a provider or deployer under the EU AI Act? Do any deliverables fall in a high-risk category? |
| F-2 | Client-facing AI disclosure | Where your deliverable's users interact with AI, is the disclosure obligation allocated to whoever operates it in writing? |
| F-3 | Subprocessor change notice | Your DPA (if you have one) requires notice before subprocessor changes. Do you have a process for notifying when a new AI tool joins? |
| F-4 | Cross-border processing | If your AI provider processes data outside your country/region, is that recorded in your disclosures? |

---

## Severity Levels

| Level | Meaning | Action |
|---|---|---|
| 🔴 Exposed | Your contract says one thing and you're doing another, or an obligation is unmet. Includes any undisclosed AI provider receiving customer/user data. | Fix immediately. Update the contract or change the practice. |
| ⚠️ Drifting | Accurate today but resting on a condition that just weakened: a widened data carve-out, an unconfirmed vendor tier, a feature that just shipped. | Re-test the assumption or update the contract. |
| ✅ Clean | Verified against your actual documents and current practices this run. | No action required. Retest quarterly or when tooling changes. |

---

## How to Run It

### Step 1: Gather Your Documents
Collect:
- Your DPA (or the DPA you offer customers)
- Your MSA/SOW template (or MSAs with customers)
- Your security policy or AI tool usage policy
- Any compliance questionnaires you've filled out

### Step 2: Document Your Tooling
List every AI tool your team uses:
- What is it? (Claude, ChatGPT, custom fine-tuned model, etc.)
- Why? (development, testing, production inference, research)
- What data reaches it? (business contact data only, customer data, production data)
- What tier/plan are you on?

### Step 3: Run the Audit
For each module, check your tools and contracts against the verifications above. Record:
- What you found
- What contract/section governs it
- Severity (Exposed, Drifting, Clean)

### Step 4: Report
Document findings with:
- Specific provider name
- Specific contract section
- The gap between what the contract says and what you're doing
- Your fix

---

## Output Format

```
⚖️  AI Contract Audit: Your Organization Compliance Posture
Generated: [date] · Scope: [all engagements | specific customer]

┌──────────────────────────────────────┐
│ Findings reviewed: N                 │
│ 🔴 Exposed: N  ⚠️ Drifting: N  ✅ Clean: N │
└──────────────────────────────────────┘

## 🔴 Exposed: Fix These Now

{Customer/Product} · Module A-2 · Transfer mechanism
  Your subprocessor disclosure names [provider] under [agreement], but you contract with them directly.
  That agreement does not cover this transfer.
  → Update your disclosure to cite the actual governing agreement, or change to an intermediary.

## ⚠️ Drifting: Re-test These

{Customer/Product} · Module A-5 · Dev tooling carve-out
  Development tooling sits outside your disclosure because only business contact data
  reaches it. Your recent amendment now admits customer/user data to [scope category].
  → Re-test whether the exclusion still holds, or disclose the tooling.

## Per-Product/Customer AI Disclosure

| Tool | Category | Status | Notes |
|---|---|---|---|
| <your-inference-tool> | Inference | Disclosed | Transfer via <provider-dpa> |
| Development tooling | Dev tools | Excluded | Business contact data only; widening would trigger disclosure |

## Company-Level Findings

[Findings from Modules C–F that apply across all products/customers]

## Open Questions for Counsel

- Does your E&O policy cover AI-generated deliverables?
- Are you in EU AI Act scope?
```

---

## Rules

1. **Read the actual documents.** Never assess from memory or previous runs.
2. **Verify by derivation.** Build your own list of AI tools from your SOW and actual practice, then test your contracts against it. Reading the contract to validate the contract proves nothing.
3. **Name the clause.** Every finding cites a specific document, section, and provider. Findings that can't be traced to a clause are not findings.
4. **Distinguish inference from tooling** before assessing any disclosure gap.
5. **A tier is a fact.** When you can't establish it from your billing or tool settings, say so and mark dependent findings unverified.
6. **Usage is a fact too.** Configuration proves availability, never use. Ask before flagging a tool as receiving customer data.
7. **State the boundary.** Copyrightability of AI-generated work and insurance coverage are unsettled. Frame them as exposure to be decided, not settled law.
8. **Escalate rather than opine** on: insurance coverage disputes, a live IP claim, regulator contact, or anything where being wrong costs more than asking.

---

## When to Run

- Before onboarding any new AI tool into your workflow: this is when the paper goes stale
- Before issuing a new DPA or SOW that authorizes AI processing
- When your data scope widens (e.g., you start handling customer data with a tool previously excluded)
- When a vendor changes its terms, tiers, or training defaults
- Quarterly across all active products/customers
- Before any customer security review or compliance questionnaire

---

## Customization

See [CUSTOMIZE.md](./CUSTOMIZE.md) for how to adapt this framework for your organization, contracts, and tools.

---

---

**Not legal advice.** This framework is for audit and analysis. For coverage of unsettled questions (AI copyright, insurance), consult your legal counsel.
