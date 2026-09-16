# Third-party compliance framework checklists

The per-framework requirement checklists: HIPAA, COPPA, GDPR, SOC 2, FERPA.
Read only the one the run is assessing against, at SPEC.md procedure step 2.

To add a framework your org needs (SOX, PCI-DSS, a state privacy law), follow
this same shape: a numbered list of concrete, checkable requirements, each
with a one-line description of what evidence would satisfy it.

## HIPAA Checklist

| # | Requirement | What to check |
|---|-------------|---------------|
| 1 | Business Associate Agreement (BAA) | Will they sign one? Is it standard or negotiable? |
| 2 | Encryption at rest | AES-256 or equivalent on all PHI storage |
| 3 | Encryption in transit | TLS 1.2+ for all data transmission |
| 4 | Access controls | Role-based, MFA available, audit logs |
| 5 | Audit logging | All access to PHI logged with identity and timestamp |
| 6 | Breach notification | ≤60 days (regulatory), ideally ≤72 hours (best practice) |
| 7 | Data disposal | Secure deletion on termination, documented process |
| 8 | Employee training | Vendor staff trained on HIPAA handling |
| 9 | Physical safeguards | Data center security (usually covered by cloud provider) |
| 10 | Minimum necessary | Can access be scoped to only needed data? |
| 11 | De-identification | Can data be de-identified for analytics/reporting? |
| 12 | Subprocessor management | List available, notification on changes |

## COPPA Checklist

| # | Requirement | What to check |
|---|-------------|---------------|
| 1 | Parental consent mechanism | Supports verifiable parental consent flow |
| 2 | Data minimization | Collects only what's necessary for the service |
| 3 | No behavioral advertising | No ad targeting using children's data |
| 4 | Parental access/deletion | Parents can review and delete child's data |
| 5 | Data retention limits | Clear retention policy, not indefinite |
| 6 | Security safeguards | Reasonable security for children's data |
| 7 | No conditioning on disclosure | Service isn't contingent on providing excess data |
| 8 | Age gating | Mechanism to identify users under 13 |
| 9 | Third-party sharing | Clear policy on whether children's data is shared |
| 10 | Safe harbor program | Participation in FTC-approved safe harbor (bonus) |

## GDPR Checklist

| # | Requirement | What to check |
|---|-------------|---------------|
| 1 | Data Processing Agreement (DPA) | Available, covers Article 28 requirements |
| 2 | Lawful basis | Clear basis for processing (consent, legitimate interest, contract) |
| 3 | Data subject rights | Supports access, rectification, erasure, portability |
| 4 | Data residency | Can guarantee EU storage or has adequate transfer mechanism |
| 5 | Transfer mechanisms | SCCs, adequacy decisions, or binding corporate rules |
| 6 | Breach notification | Notifies the controller without undue delay after becoming aware of a breach (Art. 33(2)). A stated hour count is a plus: the controller itself has 72 hours to notify the supervisory authority |
| 7 | Data Protection Impact Assessment | DPIA available or supported |
| 8 | Privacy by design | Default privacy settings, data minimization |
| 9 | Subprocessor management | List available, notification + objection right on changes |
| 10 | Records of processing | Maintains Article 30 records |
| 11 | DPO appointed | Has a Data Protection Officer (required for large-scale) |
| 12 | Consent management | Supports granular consent collection and withdrawal |

## SOC 2 Checklist

| # | Requirement | What to check |
|---|-------------|---------------|
| 1 | SOC 2 Type II report | Current (within 12 months), covers relevant trust criteria |
| 2 | Trust criteria covered | Security (required) + which optional: Availability, Confidentiality, Processing Integrity, Privacy |
| 3 | Penetration testing | Annual pen test with remediation |
| 4 | Vulnerability management | Regular scanning, patch SLAs |
| 5 | Incident response | Documented plan, tested regularly |
| 6 | Change management | Formal change control process |
| 7 | Access management | Provisioning, deprovisioning, periodic reviews |
| 8 | Encryption | At rest and in transit, key management |
| 9 | Business continuity | DR plan, tested, RPO/RTO defined |
| 10 | Vendor management | Third-party risk program for their vendors |
| 11 | Employee security | Background checks, security training, offboarding |
| 12 | Monitoring & alerting | SIEM or equivalent, 24/7 monitoring |

## FERPA Checklist

| # | Requirement | What to check |
|---|-------------|---------------|
| 1 | "School official" exception | Vendor can operate under school official designation |
| 2 | Legitimate educational interest | Clear purpose limitation |
| 3 | Direct control | School maintains control over data use |
| 4 | No re-disclosure | Vendor won't share student records with third parties |
| 5 | Data disposal on termination | Returns or destroys records when contract ends |
| 6 | Directory information handling | Clear on what's directory vs. non-directory |
| 7 | Parent/student access rights | Supports access requests |
| 8 | Annual notification support | Helps schools meet notification obligations |
| 9 | De-identification | Supports safe de-identification for research |
| 10 | Security safeguards | Reasonable security measures documented |
