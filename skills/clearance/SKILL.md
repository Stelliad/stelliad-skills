---
name: clearance
description: Vendor compliance checkpoint. Assess whether a third-party app or service is safe to use under a regulatory framework (HIPAA, SOC 2, COPPA, GDPR, FERPA, SOX), or assess your whole stack at once by discovering every vendor a codebase actually talks to. Produces a client-shareable compliance summary.
license: MIT
compatibility: Web search access (or equivalent research tooling) for vendor research. No other external dependencies.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
type: skill
scope: all
status: active
---

# clearance

Evaluate a third-party app, service, or platform against a regulatory framework and produce a structured compliance summary suitable for customer conversations, proposals, and engagement deliverables.

## Quick start

1. [Read SPEC.md](./SPEC.md) to understand the procedure, the framework checklists, and the stack-discovery methodology
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to adapt for your research tooling and where assessments live
3. Name a vendor and a framework, or point it at a whole codebase for a stack assessment
4. Run the procedure in SPEC.md
5. Report findings using the output format in `references/output-format.md`

## Supported frameworks

HIPAA, COPPA, GDPR, SOC 2, FERPA. Extend to others (SOX, PCI-DSS, state privacy laws) by following the checklist pattern in `references/framework-checklists.md`.

## Output

Four verdicts:
- ✅ **Compliant**: vendor explicitly meets the requirement, with evidence
- ⚠️ **Conditionally compliant**: meets it, but only with specific configuration or a signed addendum
- 🔴 **Non-compliant**: doesn't meet it, or no evidence exists
- ❓ **Insufficient evidence**: couldn't find documentation either way

## Time required

- Single vendor, single framework: 20-30 minutes
- Full stack assessment: 1-3 hours depending on codebase size
- Quarterly re-run: half the initial time, mostly re-verifying what changed

## Who runs this

- **Engineering lead / CTO**: owns the assessment, makes the use-or-don't call
- **Legal/Compliance**: reviews before it goes to a customer or regulator
- **Security**: owns the credential-hygiene findings that fall out of stack discovery

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
