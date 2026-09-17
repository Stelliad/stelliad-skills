# Customizing third-party-compliance for Your Organization

The framework checklists and the stack-discovery methodology are universal. What's yours to set: your research tooling, where assessments live, and how this folds into your existing review cadence.

## 1. Your Research Tooling

SPEC.md's procedure assumes web search access. If your agent environment names its own search tool differently, or you're running this by hand, substitute accordingly. The queries in SPEC.md step 1 are the actual search strings to use, tool-agnostic.

**For your org:**
- What's your standard web search / research tool?
- Do you have a "deep research" mode (multi-source synthesis, longer-running) available, or is standard search all you've got? SPEC.md's deep-mode queries are optional extras, not required.

## 2. Where Assessments Live

The base procedure just says "write the assessment": it doesn't assume a folder structure.

**For your org:**
- Do assessments belong in a client/project-specific folder, a shared compliance doc, or inline wherever the question came up?
- If you run engagements for multiple clients, keep assessments scoped per client/project rather than in one shared pile. A compliance summary written for one customer's stack shouldn't accidentally read as though it applies to another's.
- Naming convention: something like `third-party-compliance-{vendor}-{framework}.md` keeps them greppable later.

## 3. Staleness Tracking

SPEC.md's staleness bands (current under 90 days, aging 90-180, stale over 180) are a reasonable default. Fold the re-check into whatever recurring review process you already run: a quarterly ops review, a security standup, a pre-renewal check for vendor contracts. third-party-compliance doesn't have its own scheduler; it just needs somewhere to be re-invoked from.

## 4. Extending to a New Framework

Not every org needs all five frameworks in `references/framework-checklists.md`. If you need one that isn't there (PCI-DSS, SOX, a state privacy law like CCPA/CPRA, an industry-specific standard), add it following the same shape: a numbered table of concrete, checkable requirements, each with what evidence would satisfy it. Pull from the regulation's own text or an existing compliance framework mapping. Don't invent requirements from memory.

## 5. Fitting Into Your Workflow

Where this skill tends to get used:

| Moment | How it helps |
|---|---|
| Evaluating a new vendor before adoption | Answer "can we use X?" with evidence, not a guess |
| Proposal or SOW drafting | Include compliance posture as part of a technical recommendation |
| Customer security questionnaires | A pre-built answer instead of scrambling when the question lands |
| Periodic stack review | Catch a vendor whose posture changed since you last checked, or one nobody remembered was in the stack |
| Before adding a new integration | Verify before it's wired in, not after |

**For your org:** which of these moments actually happens on your team, and who owns triggering it? A skill nobody remembers to run doesn't help.

## Running third-party-compliance as a Skill

If you're using Claude Code, this folder is already shaped as a skill. Copy it into your project:

```bash
cp -r third-party-compliance /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/third-party-compliance {vendor} --framework {framework}

or: "is Fathom HIPAA compliant", "check every third party our stack talks to", "can we use Firebase with children's data"
```

If running by hand, read SPEC.md and follow the procedure directly.

## Next Steps

1. Confirm your research tooling (§1) and where assessments will be saved (§2)
2. Decide which recurring process staleness re-checks fold into (§3)
3. Add any framework you need beyond the five included (§4)
4. Run it on one real vendor before rolling it out broadly

---

For questions on regulatory interpretation, consult your compliance counsel. This skill surfaces the gaps and the evidence; it doesn't replace legal judgment on what's acceptable risk.
