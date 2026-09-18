---
name: ai-contract-audit
description: Audit whether your contracts match how your team builds with AI, disclosure, training posture, IP assignment, confidentiality, warranties, regulatory.
license: MIT
compatibility: Run against your org's contracts and tooling. No external dependencies.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
type: skill
scope: all
status: active
---

# ai-contract-audit

Audit the gap between what your contracts say about AI tools and how your team actually uses them.

## Quick start

1. [Read SPEC.md](./SPEC.md) to understand the six modules and what they check
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to adapt for your org's contracts and tooling  
3. Gather your DPA, MSA, and SOW
4. Run through Modules A–F using the framework in SPEC.md
5. Report findings using the output format provided

## Modules

- **A**: AI provider disclosure
- **B**: Model training posture
- **C**: IP assignment over generated code
- **D**: Confidentiality vs. delivery reality
- **E**: Delivery warranties
- **F**: Regulatory posture

## Output

Three severity levels:
- 🔴 **Exposed**: contract says one thing, you're doing another
- ⚠️ **Drifting**: true today, fragile tomorrow
- ✅ **Clean**: verified against your actual documents

## Time required

- Initial audit: 2–3 hours
- Quarterly re-run: 1 hour
- Per-tool changes: 15 minutes

## Who runs this

- **CTO/Engineering lead**: owns the audit
- **Legal/Compliance**: interprets contract clauses
- **Product**: documents tooling and data flows

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
