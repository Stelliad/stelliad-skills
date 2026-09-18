# Customizing ai-contract-audit for Your Organization

This guide walks you through adapting ai-contract-audit to your org's contracts, tooling, and risk profile.

## 1. Define Your Contracts

**What you have:**
- DPA (Data Processing Agreement) or equivalent privacy terms
- MSA (Master Services Agreement) or core contract terms
- SOW (Statement of Work) or service documentation
- NDA or confidentiality terms
- Security policy or AI tool usage policy

**Customization:**
Save these as your baseline documents. ai-contract-audit will check your actual practice against them.

If you don't have a DPA, consider one. Vendors increasingly require it. A typical DPA should:
- List AI providers and their role (processor, sub-processor, sub-contractor)
- Specify what data reaches each provider
- Define retention and deletion periods
- Call out any no-training commitments (to be confirmed with your counsel)

**For your org:**
- Where do these documents live?
- Who owns them (legal team? CTO?)
- How often are they reviewed? (Suggest: quarterly)

## 2. Map Your AI Tools

Create a table of every tool your team uses:

| Tool | Vendor | Tier/Plan | Purpose | Data Reaching It | Notes |
|---|---|---|---|---|---|
| <Tool A> | <Vendor> | <Tier> | Development | <Data scope> | <Verify training posture> |
| <Tool B> | <Vendor> | <Tier> | Research | <Data scope> | <Verify training posture> |
| <Tool C> | <Vendor> | <Tier> | Production | <Data scope> | <Verify training posture> |

**For each tool, verify:**
- **Tier/plan:** Is training on or off? Is this documented?
- **Data flow:** What actually reaches this tool? (Not what's *allowed*, but what *does*.)
- **Contract coverage:** Is this tool named in your DPA or SOW?

**Red flags:**
- Consumer tier where you need business tier
- Training toggles not confirmed off
- Tools you've added since your contracts were signed

## 3. Check Disclosure Status

For each tool, determine if it needs to be disclosed:

### Inference Providers (Always disclose)
Models your product/deliverable calls at runtime:
- LLM APIs powering a feature
- TTS or transcription service
- Embedding service
- Computer vision service

**Disclosure lives in:** Your subprocessor exhibit, data processing disclosure, or privacy policy.

### Development Tooling (Disclose if data reaches it)
Tools your team uses to build:
- Claude Code / GitHub Copilot / Cursor
- ChatGPT for research
- Internal AI assistants
- LLMs for code generation

**Disclose if:** Customer/user/production data reaches it
**Exclude if:** Only business contact data (employee emails, internal docs) reaches it

**Verify the carve-out:**
Read your SOW or contract. Does it say something like:
- "Development tooling may process business contact data only" ✅ (Allows exclusion)
- "Development tooling may process any data needed to build the product" ❌ (Requires disclosure)

**Customization question:**
What data does your team actually send to dev tools? 
- If it's only internal/business contact: you can exclude those tools
- If it includes customer/user data: you must disclose them

## 4. Document Your Data Scopes

Define what kinds of data your org handles. This determines which AI tools need disclosure.

Example scopes:
- **Business contact data:** Employee names, emails, titles
- **Customer data:** Customer-provided documents, code, configuration
- **User data:** End-user personal information (names, emails, engagement)
- **Production data:** Live customer data, transaction records, PII
- **Health/regulated data:** PHI, financial records, government IDs

**For your org:**
- Which data reaches AI tools?
- Which data is in-scope for your customer contracts?
- Which data is restricted by law (HIPAA, PCI-DSS, GDPR)?

## 5. Run the Audit

### Module A: Disclosure
For each AI tool, check:
- Is it listed in your DPA/disclosure?
- If not, should it be?
- If it should be and isn't, mark as 🔴 Exposed.

### Module B: Training
For each tool:
- What tier are you on? (Confirm it, don't assume.)
- Is training on or off?
- Where? (Vendor's account settings, not product docs.)
- When was this last checked?

### Module C: IP Assignment
Review your MSA:
- Does it warrant you own all deliverables?
- Does it account for AI-generated code?
- Do you have a license-scanning step before delivery?

### Module D: Confidentiality
Review your contract:
- Does it bar you from using AI tools?
- Does it match your actual practice?
- Does it bar customers from using AI? Can you enforce it?

### Module E: Warranties
Check:
- What standard of care do you promise?
- Is QA time allocated in your pricing?
- Who validates AI-generated output?

### Module F: Regulatory
If applicable:
- GDPR: Are you a processor or controller?
- EU AI Act: Do you serve EU users? High-risk category?
- CCPA: How do you handle consumer data requests?
- HIPAA/PCI-DSS: Data restrictions?

## 6. Document Findings

For each defect you find, record:

**🔴 Exposed example:**
```
Product: Internal code generation tool
Module: A-2 (Transfer mechanism)
Tool: <inference_tool>
Issue: SOW names <inference_tool> but DPA <exhibit_name> doesn't.
Fix: Add <provider> to <exhibit_name>, cite <provider>'s DPA as governing agreement.
Owner: Legal team
Deadline: <agreed_upon_date>
```

**⚠️ Drifting example:**
```
Product: Customer dashboard
Module: A-5 (Carve-out width)
Tool: Development assistant
Issue: Initial SOW excluded this tool ("development only, no customer data").
      Tooling use has expanded to include customer-facing feature research.
Fix: Re-test whether the data carve-out still holds, or disclose the tool.
Owner: [Product lead] + [Legal]
Deadline: [Before next security review]
```

## 7. Set a Review Cadence

**Initial audit:** In next planning cycle (establish baseline of current tooling disclosure)

**Ongoing:**
- **Quarterly:** Re-run full audit (Module A-B for all tools)
- **On change:** When adding a new AI tool, when a vendor changes terms, when your data scope widens
- **Before customer reviews:** Before any security questionnaire or compliance audit

**Owner:** CTO or engineering lead + Legal

**Escalation:** Any 🔴 findings go to leadership immediately; ⚠️ findings get added to the backlog.

## 8. Customize the Framework

The SPEC.md modules are universal, but adapt these to your org:

**Modules A-F apply universally.** Customize:

| Element | Adapt for your org |
|---|---|
| Tool list | List your actual tools, not the examples above |
| Contract names | Replace DPA/MSA with your contract names |
| Data types | Replace "customer data" with your data categories |
| Regulatory scope | Add HIPAA, PCI-DSS, SOC 2 if applicable |
| Severity thresholds | 🔴 Exposed = breaking a material contract promise; ⚠️ Drifting = assumption just weakened |
| Review cadence | Suggest quarterly, but your risk tolerance may differ |

## Running ai-contract-audit as a Skill

If you're using Claude Code:

**In your `.claude/skills/` directory, add:**

```
your-org/
├── ai-contract-audit-spec.md (this SPEC.md, customized)
├── ai-contract-audit-customize.md (this CUSTOMIZE.md, customized)
├── README.md (vendor-neutral overview)
└── examples/
    ├── contract-dpa.md (template/example, replace with yours)
    ├── contract-msa.md (template/example, replace with yours)
    └── tool-inventory.md (template/example, replace with yours)
```

If running as a Claude Code skill, create a SKILL.md that references your org's contracts and policies.

**Trigger:** `ai-contract-audit`, `AI compliance check`, `audit our AI tools`, etc.

## Next Steps

1. Share this guide with your CTO and legal team
2. Gather your actual contracts (DPA, MSA, SOW, NDA)
3. Map your AI tools using the table in §2
4. Run Modules A-B first (disclosure and training status)
5. Schedule a follow-up to cover Modules C-F (IP, confidentiality, warranties, regulatory)
6. Set a quarterly calendar reminder to re-run the audit

---

For questions on legal interpretation or contract language, consult your counsel.
