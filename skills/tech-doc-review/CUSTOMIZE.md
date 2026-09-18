# Customizing tech-doc-review for Your Organization

tech-doc-review's six scoring dimensions and the editorial-vs-knowledge-gap split are universal. What's yours to set: the bar, the document types, and where this fits in your own writing workflow.

## 1. Set Your Bar

The default bar is 9/10. That's calibrated for documents that get filed as IP, referenced as architectural source of truth, or shared outside the team.

**For your org:**
- Patents / IP filings: keep the bar high (9-10). The cost of a weak claim is real.
- Internal ADRs: 7-8 may be enough. The goal is a legible decision record, not a legal document.
- Design docs before a build: 8 is a reasonable gate before code starts.
- Whitepapers / anything public-facing: 9+, since a defensibility gap here is a credibility gap.

Pick a bar per document type rather than one number for everything.

## 2. Adjust Required Sections

SPEC.md's "Required sections by type" table is a starting point, not a fixed template. If your org's design doc template has a section tech-doc-review doesn't check for (e.g., "Cost Impact," "Security Review," "Rollback Plan"), add it to the completeness rubric for that type.

**For your org:**
- Do you have a standard template per document type already? Use its section list, not the one in SPEC.md.
- Is there a section your team always skips? That's either a sign the template is wrong, or a sign tech-doc-review should flag it as a completeness gap every time until you fix one or the other.

## 3. Add or Remove Document Types

SPEC.md covers five types: patent, ADR, design doc, whitepaper, spec. If your org has a type that doesn't fit (a postmortem, a proposal, an architecture review writeup), define its own rubric:

- What does a 9/10 version of this document type look like?
- What sections are required?
- What's the type-specific defensibility question? ("Would this survive review by a hostile reader?" needs a concrete answer per type; see SPEC.md's per-type breakdowns for the pattern.)

## 4. Fold Into Your Own Workflow

In this repository, `compose-from-interview` drafts from an author interview and `compose-score` scores non-technical writing. tech-doc-review runs once a draft exists, whoever or whatever wrote it, and it is deliberately not `compose-score`: it's for documents that live or die on precision and defensibility, not voice or hook.

**For your org:**
- What produces your first drafts? (A person, an agent, a template.) tech-doc-review runs after that, not instead of it.
- Do you have a separate quality gate for non-technical writing (blog posts, marketing copy)? Keep that separate: tech-doc-review's rubric is wrong for content that's supposed to be persuasive rather than precise.
- Where do documents go once approved? (A wiki, a repo, a patent docket.) Have tech-doc-review's "recommend where this document should live" step point there.

## 5. Decide Who Can Override the Bar

"Author says ship" is an explicit override in the base procedure: someone can ship below the bar on purpose (a draft ADR that needs a team discussion before it's final, a spec that's intentionally incomplete pending a decision). Decide who holds that authority for each document type: the author alone, or the author plus a reviewer.

## Running tech-doc-review as a Skill

If you're using Claude Code, this folder is already shaped as a skill. Copy it into your project:

```bash
cp -r tech-doc-review /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/tech-doc-review

or: "score this design doc", "is this patent ready", "review this tech doc"
```

If running by hand, read SPEC.md and follow the procedure directly.

## Next Steps

1. Set your bar per document type (§1)
2. Confirm or replace the required-sections list for each type you use (§2)
3. Add any document types SPEC.md doesn't cover (§3)
4. Try it on one real document before rolling it out broadly

---

For questions on what counts as "defensible" for your specific field (patent claims especially), consult the relevant specialist. tech-doc-review finds the gaps; it doesn't replace expert judgment on how to close them.
