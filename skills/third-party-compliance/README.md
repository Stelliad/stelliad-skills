# Third-Party Compliance

**Assess whether a third-party service is safe to use under a regulatory framework, or assess your whole stack at once.**

For engineering leads, CTOs, and compliance teams who need a real answer to "can we use this vendor?", backed by evidence rather than a guess.

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r third-party-compliance /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/third-party-compliance {vendor} --framework {framework}

or: "is Fathom HIPAA compliant", "check every third party our stack talks to", "can we use Firebase with children's data"
```

The agent reads [SPEC.md](./SPEC.md) and does the work.

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly.
[CUSTOMIZE.md](./CUSTOMIZE.md) is where you set your research tooling and where assessments live.

## What It Does

**Single vendor mode:** researches a named vendor's compliance documentation, checks it against a framework-specific checklist (HIPAA, COPPA, GDPR, SOC 2, FERPA), maps how your data would actually flow through it, and produces a client-shareable assessment.

**Stack mode:** discovers every third-party vendor a codebase actually talks to (env files, docker-compose, package manifests, infrastructure-as-code, CI/CD, frontend build vars, eight sources in total), then assesses each one and produces a compliance matrix for the whole stack. The discovery pass doubles as a credential-hygiene audit: it catches committed secrets and env files that should have been gitignored and weren't.

Reports four verdicts:
- ✅ Compliant: vendor explicitly meets the requirement, with evidence
- ⚠️ Conditionally compliant: meets it, but only with specific configuration
- 🔴 Non-compliant: the vendor's own documentation shows it doesn't meet it
- ❓ Insufficient evidence: couldn't confirm either way

## Getting Started

1. [Read the SPEC](./SPEC.md): understand the procedure and the stack-discovery methodology
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md): set your research tooling and where assessments should live
3. [See SKILL.md](./SKILL.md): skill invocation
4. Pick one real vendor (or point it at a real codebase for stack mode)
5. Run the assessment using the templates in `references/`
6. Track findings against whatever compliance backlog you keep

## Time Required

- Single vendor, single framework: 20-30 minutes
- Full stack assessment: 1-3 hours depending on codebase size
- Quarterly re-run: about half the initial time

## Who Should Run This

- **Engineering lead / CTO**: owns the assessment, makes the use-or-don't call
- **Legal / compliance**: reviews before it goes to a customer or regulator
- **Security**: owns the credential-hygiene findings stack mode surfaces

## Not Included

- Legal advice (you decide what risk is acceptable)
- A guarantee (this reads public documentation; verify anything load-bearing directly with the vendor)
- Contract templates or a DPA (you bring your own, or use whatever your legal team provides)

## License

MIT. Adapt freely for your org.

---

This is a standalone skill. For other skills in this collection, see the repository README.
