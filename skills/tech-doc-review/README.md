# Technical Document Review

**Score a technical document against a quality bar. Loop revisions until it's ready, or until the author explicitly says ship.**

For anyone filing a patent disclosure, writing an ADR, shipping a design doc, publishing a whitepaper, or specifying a feature.

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r tech-doc-review /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/tech-doc-review

or: "score this design doc", "is this patent ready", "review this tech doc"
```

The agent reads [SPEC.md](./SPEC.md) and does the work.

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly.
[CUSTOMIZE.md](./CUSTOMIZE.md) is where you set your bar and document types.

## What It Does

Scores a document on six dimensions (claim clarity, structural completeness, precision, defensibility, novelty, and AI-slop detection), each 1-10. Overall score is the lowest dimension: one weak link means not ready.

Splits every problem into two kinds:
- **Editorial** (structure, vague phrasing, filler): the agent fixes these directly
- **Knowledge gaps** (missing embodiments, unquantified claims, absent prior art): routed back to the author as specific questions, never invented

Loops revise-and-rescore (capped at 3 editorial passes) until the document hits the bar or the author says ship.

## Getting Started

1. [Read the SPEC](./SPEC.md): understand the six dimensions and the procedure
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md): set your bar per document type
3. [See SKILL.md](./SKILL.md): skill invocation
4. Pick one real document (a design doc waiting for review is a good first target)
5. Run it, apply the editorial fixes, answer the knowledge-gap questions
6. Re-score until it ships

## Document Types Supported

- Patent / invention disclosures
- Architecture decision records (ADRs)
- Design documents / RFCs
- Whitepapers
- Technical specs

Each has its own required sections and type-specific defensibility question. Add your own type by following the pattern in CUSTOMIZE.md §3.

## Who Should Run This

- **Author**: answers the knowledge-gap questions, makes the final ship call
- **Reviewer / tech lead**: can run it standalone as a pre-review pass

## Not Included

- Legal review (a patent scoring 9/10 on tech-doc-review still needs an attorney)
- Content/voice scoring for non-technical writing (marketing copy, blog posts: different rubric, different tool)
- A house style guide (tech-doc-review checks defensibility and completeness, not tone)

## License

MIT. Adapt freely for your org.

---

This is a standalone skill. For other skills in this collection, see the repository README.
