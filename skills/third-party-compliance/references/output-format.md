# Third-party compliance assessment format

The section-by-section template a third-party compliance assessment is written to. Read at
SPEC.md procedure step 5, once the checklist and data-flow work is done. Status marks, the Score, and the Verdict all follow SPEC.md step 2: ✅ items count as passed, and every item not marked ➖ counts as applicable.

```markdown
# Vendor Compliance Assessment: {Vendor Name}

**Framework:** {HIPAA / SOC 2 / COPPA / GDPR / FERPA}
**Assessed:** {date}
**Assessed by:** {your name or org}
**Context:** {project/client name or "General"}
**Research depth:** {Standard / Deep}

---

## Executive Summary

{2-3 sentences: compliant/partially/non-compliant, key strengths, key gaps, overall recommendation}

**Verdict:** ✅ Compliant | ⚠️ Conditionally Compliant | 🔴 Non-Compliant | ❓ Insufficient Evidence

---

## Vendor Overview

| Item | Detail |
|------|--------|
| Vendor | {name} |
| Service | {what you'd use it for} |
| Trust page | {URL} |
| Certifications | {SOC 2 Type II, HITRUST, ISO 27001, etc.} |
| BAA available | {Yes / No / Upon request} |
| DPA available | {Yes / No / Standard / Custom} |
| Data residency | {Region(s)} |
| Last security audit | {date or "unknown"} |

---

## Framework Compliance Checklist

### {Framework Name} Requirements

| # | Requirement | Status | Evidence | Notes |
|---|-------------|--------|----------|-------|
| 1 | {requirement} | ✅/⚠️/🔴/❓/➖ | {source or "not found"} | {context} |
| 2 | ... | ... | ... | ... |

**Score: {passed}/{applicable} ({percentage}%)**

---

## Data Flow Analysis

### What data enters this vendor?

| Data type | Classification | Example |
|-----------|---------------|---------|
| {type} | PII / PHI / Children's / Financial / Internal | {specific} |

### Storage & Access

| Aspect | Detail |
|--------|--------|
| Storage location | {region, provider} |
| Encryption at rest | {yes/no, method} |
| Encryption in transit | {TLS version} |
| Access controls | {RBAC, SSO, MFA} |
| Vendor employee access | {policy} |
| Subprocessors | {list or link} |

### Retention & Deletion

| Aspect | Detail |
|--------|--------|
| Default retention | {period} |
| Custom retention available | {yes/no} |
| On-demand deletion | {yes/no, SLA} |
| Account termination handling | {what happens to data} |
| Training/model use | {does vendor use data for AI training?} |

---

## Gaps & Mitigations

| # | Gap | Severity | Mitigation | Residual Risk |
|---|-----|----------|-----------|---------------|
| 1 | {what's missing} | High/Med/Low | {what you can do} | {what remains} |

---

## Recommendations

### To use this vendor:
1. {Action required: e.g., "Sign BAA before any PHI enters the system"}
2. {Configuration: e.g., "Enable HIPAA-eligible mode in account settings"}
3. {Architectural: e.g., "Encrypt all PII client-side before API calls"}

### Alternatives to consider:
- {Alternative vendor}: {why it might be better for this framework}

---

## Sources

1. {URL or document title}: accessed {date}
2. ...

---

*This assessment reflects publicly available documentation as of {date}. Certifications and policies change, verify directly with the vendor before making compliance commitments to regulators.*
```
