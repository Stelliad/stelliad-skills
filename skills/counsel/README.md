# counsel: AI Tool Compliance Audit

**Audit whether your contracts actually match how your team builds with AI.**

For CTOs, engineering leads, and compliance teams shipping with Claude, OpenAI, Gemini, or any LLM.

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r counsel /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/counsel

or: "audit our contracts against how we actually build with AI"
```

The agent reads [SPEC.md](./SPEC.md) and does the work.

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly.
[CUSTOMIZE.md](./CUSTOMIZE.md) is where you set the thresholds and policy for
your stack.

## What It Does

Walks through six modules to verify that:
- Every AI tool your team uses is disclosed where it should be
- Model training is off where you promised
- Your IP warranties hold for AI-generated code
- Confidentiality terms don't contradict your actual practice
- Your service warranties match your delivery model
- Your regulatory posture is sound

Reports three severity levels:
- 🔴 Exposed: contract says one thing, you're doing another
- ⚠️ Drifting: true today, fragile tomorrow
- ✅ Clean: verified against your actual documents and practices

## Getting Started

1. [Read the SPEC](./SPEC.md): understand the six modules and what they check
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md): adapt for your org's contracts and tooling
3. [See SKILL.md](./SKILL.md): skill invocation and automation
4. Gather your DPA, MSA, and a list of AI tools your team uses
5. Run the audit (use the output format in SPEC.md)
6. Track findings in your issue tracker

## Time Required

- Initial audit: 2-3 hours for a team with 5+ AI tools
- Quarterly re-run: 1 hour
- Per-tool changes: 15 minutes

## Who Should Run This

- **CTO**: Owns the audit, signs off on fixes
- **Engineering lead**: Documents tools and data flows
- **Legal/compliance**: Interprets contract clauses and regulatory scope

## Not Included

- Contract templates (you adapt yours)
- Legal advice (you decide what to fix)
- Insurance assessment (you ask your broker)

## License

MIT. Adapt freely for your org.

---

This is a standalone skill. For other skills in this collection, see the repository README.
