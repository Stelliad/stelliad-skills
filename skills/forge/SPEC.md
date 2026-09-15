# forge: Technical Document Quality Framework

Score technical documents against a quality bar. Fix what the machine can fix. Route knowledge gaps back to the author. Loop until it hits 9/10 or the author says ship.

## Philosophy

Technical writing has a different failure mode than content writing. Content fails by being boring or generic. Technical writing fails by being incomplete, vague, or indefensible.

A patent disclosure that a lawyer can't write claims from is a waste. An ADR that doesn't list alternatives isn't a decision record. A design doc without a migration plan is a wish list. This framework makes those gaps visible and measurable.

Two kinds of problems in a technical document:
1. **Editorial**: structure, precision, redundancy, ordering, clarity. The machine fixes these.
2. **Knowledge gaps**: missing embodiments, unquantified claims, undocumented tradeoffs, absent prior art. Only the author can fill these.

Never let the machine fill a knowledge gap with generated content. A patent claim based on invented details is worse than no claim at all.

## Scoring Dimensions

Each dimension scored 1-10. Overall score is the lowest dimension. One weak link means not ready.

### 1. Claim Clarity (can someone act on this without a follow-up?)

| Score | Meaning |
|-------|---------|
| 9-10 | A reader can implement from this doc alone. Claims are specific and traceable to architecture. |
| 7-8 | Clear with 1-2 areas needing elaboration. |
| 5-6 | Core idea is there but multiple sections require interpretation. |
| 3-4 | Ambiguous. Reader would need a 30-min call to understand intent. |
| 1-2 | Unclear what's being proposed or claimed. |

**Per document type:**
- Patent: Could a patent attorney draft formal claims without a follow-up call?
- ADR: Could a new team member understand the decision and its rationale in one read?
- Design doc: Could an engineer implement this without asking clarifying questions?
- Whitepaper: Could a technical reader replicate or evaluate the approach?
- Spec: Could QA write tests from this alone?

### 2. Structural Completeness (are all required sections present and substantive?)

| Score | Meaning |
|-------|---------|
| 9-10 | Every section from the template is present, substantive, and earns its space. |
| 7-8 | Complete with 1 section that's thin or could be expanded. |
| 5-6 | Missing 1-2 required sections or 3+ sections are stubs. |
| 3-4 | Major structural gaps. Key sections missing or placeholder only. |
| 1-2 | Doesn't follow any recognizable structure for its type. |

**Required sections by type** (adapt these — see CUSTOMIZE.md):
- Patent: Problem, Prior Art, Novel Approach, Claims, Embodiments, Figures, Advantages
- ADR: Context, Decision, Rationale, Alternatives Considered, Consequences
- Design: Goal, Non-Goals, Background, Proposed Design, Risks, Open Questions, Timeline
- Whitepaper: Abstract, Introduction, Architecture, Implementation, Evaluation, Related Work
- Spec: Overview, Data Model, API Surface, Logic/Rules, Dependencies, Testing, Ops

### 3. Precision (is every statement load-bearing and verifiable?)

| Score | Meaning |
|-------|---------|
| 9-10 | Every claim has evidence. Numbers are quantified. No hand-waving. |
| 7-8 | Mostly precise with 1-2 vague claims that could be tightened. |
| 5-6 | Mix of precise and vague. "Significantly faster" without numbers. |
| 3-4 | Mostly vague. Claims without evidence. Adjectives doing the work of data. |
| 1-2 | Pure assertion. No evidence, no specifics, no traceability. |

**Red flags:**
- "Significantly" / "substantially" / "dramatically" without a number
- "Various" / "multiple" / "several" without naming them
- "Improves performance" without saying from what to what
- Architecture described without data flow
- Claims that can't be traced to a specific component

### 4. Defensibility (would this survive review by a hostile reader?)

| Score | Meaning |
|-------|---------|
| 9-10 | Every claim defended. Limitations acknowledged. Alternatives honestly dismissed. |
| 7-8 | Strong with 1 area where a reviewer would push back. |
| 5-6 | Some claims asserted without defense. Missing "why not X" for obvious alternatives. |
| 3-4 | Major gaps a reviewer would attack. Cherry-picked evidence. Missing counterarguments. |
| 1-2 | Indefensible. Claims asserted as fact without evidence or reasoning. |

**Per document type:**
- Patent: Would the examiner find prior art that invalidates a claim?
- ADR: Would an engineer on the team challenge "why not Option B"?
- Design: Would a reviewer find an unaddressed failure mode?
- Whitepaper: Would a peer reviewer find the evaluation flawed?
- Spec: Would QA find behaviors not covered?

### 5. Novelty / Value (does this say something that isn't already obvious?)

| Score | Meaning |
|-------|---------|
| 9-10 | Clear novel contribution. Distinct from prior art. Non-obvious combination of techniques. |
| 7-8 | Mostly novel with 1 section that restates common knowledge without advancing it. |
| 5-6 | Mix of novel and well-known. Hard to tell what's the actual contribution. |
| 3-4 | Largely restates existing approaches with minor tweaks. |
| 1-2 | Nothing new. Could be a summary of existing documentation. |

**Per document type:**
- Patent: Is the novel element clearly distinguished from prior art?
- ADR: Is the decision non-trivial? (If there's only one option, it's not an ADR.)
- Design: Does this propose a real change or just document the obvious next step?
- Whitepaper: What does this show that hasn't been shown?
- Spec: Is there non-trivial logic that needs specifying? (Trivial CRUD doesn't need a spec.)

### 6. Slop Detection (is any of this AI-generated filler?)

| Score | Meaning |
|-------|---------|
| 9-10 | Zero AI tells. Reads like an engineer who's built this system wrote it. |
| 7-8 | 1-2 phrases that scan as AI-ish. Quick fix. |
| 5-6 | Noticeable AI patterns. Generic sections that could apply to any project. |
| 3-4 | Multiple sections feel generated: not grounded in the actual system. |
| 1-2 | Obvious AI output. Template filled in without real architectural knowledge. |

**Technical Document Slop Checklist:**

| Tell | What to look for | Fix |
|------|-----------------|-----|
| Generic architecture | "The system uses a microservices architecture with event-driven communication" without naming the actual services | Name the services. Describe the actual data flow. |
| Ungrounded claims | "This approach scales horizontally" without proving which component and how | Identify the specific scaling mechanism and its limits |
| Template sentences | "This section describes the..." / "In this document, we will..." | Cut preamble. Start with the content. |
| Exhaustive-but-shallow | Lists 15 alternatives considered but dismisses each in one sentence | Fewer alternatives, deeper analysis on the real contenders |
| Symmetric bullet points | Every pro has a con, every section same length, suspiciously balanced | Real tradeoffs are asymmetric. Some options have 5 cons and 1 pro. |
| Hedging clusters | "It could potentially be argued that this might..." | State the claim. If uncertain, say why specifically. |
| Filler figures | "Figure 1 shows the system architecture" [describes what the reader can see] | Figures should reveal non-obvious relationships. Captions explain why, not what. |
| Missing specifics | Component names are generic ("the processing service", "the data layer") | Use actual names from the codebase |
| Over-broad claims | "This invention applies to any distributed system" | Narrow to what was actually built and tested |
| Context-free evaluation | "Results show improved performance" without baseline or methodology | State what was measured, how, against what baseline |

**Scoring:**
- 0-1 tells → 9-10
- 2-3 tells → 7-8
- 4-6 tells → 5-6
- 7+ tells → 3 or below

## Procedure

### 1. Identify document type

Determine the type from context or ask:
- Patent / invention disclosure
- ADR (architecture decision record)
- Design document / RFC
- Whitepaper
- Technical spec

This determines which sections are required and which rubrics to weight.

### 2. Score the document

```
🔨 Forge Review: "Invention Disclosure. Cognitive Shard System"
Type: Patent / Invention Disclosure

Claim Clarity:    8/10. Claims are specific but Claim 3 needs tighter language on the trigger mechanism.
Completeness:     7/10. Missing one embodiment variant (edge deployment). Figures section is thin.
Precision:        9/10. Latency numbers grounded, architecture traces to actual code.
Defensibility:    8/10. Prior art section is honest. One claim overlaps with [specific existing patent].
Novelty:          9/10. The combination of session-scoped retrieval + shard routing is non-obvious.
Slop:             9/10. Clean. One generic sentence in the Advantages section to tighten.

Overall: 7/10 (Completeness is the limiter)
Bar: 9/10

Verdict: NOT READY, 1 dimension below bar.
```

### 3. Classify fixes

| Fix type | Who handles | Example |
|----------|-------------|---------|
| Editorial | Machine | "Tighten Claim 3 language, cut generic sentence in Advantages" |
| Knowledge gap | Author | "What happens in the edge deployment case? Is the shard system viable without persistent connectivity?" |

### 4. Fix or route

- **Editorial fixes:** Apply them. Produce a revised document.
- **Knowledge gaps:** Present targeted questions. Author answers get inserted, then re-score.

### 5. Loop

Re-score after fixes. Max 3 editorial loops. Knowledge gaps require author input, can't be brute-forced.

### 6. Approve

At the bar (default 9/10) or the author says "ship":
- Mark as approved
- Note any residual limitations (things that would push it higher but aren't blockers)
- Recommend where this document should live

## Type-Specific Checks

### Patent / Invention Disclosure

- [ ] Novelty distinguishable from prior art in first 2 paragraphs of Novel Approach
- [ ] Every claim traces to a specific architectural component
- [ ] 3+ embodiment variants covering different deployment/data/trigger models
- [ ] 2+ figures with substantive captions
- [ ] Prior art honestly assessed (not strawmanned)
- [ ] Claims are broad enough to be defensible but specific enough to be non-obvious
- [ ] Method claims AND system claims present
- [ ] Defensive breadth: implementations NOT being built but worth covering

### ADR

- [ ] One decision per record (not bundled)
- [ ] Alternatives section has 2+ real options (not strawmen)
- [ ] Each alternative has honest pros AND cons
- [ ] Consequences include both positive and negative
- [ ] Trigger for revisiting is specific (condition, not calendar)
- [ ] Context includes constraints that drove the decision

### Design Document / RFC

- [ ] Non-Goals section present and substantive
- [ ] At least one diagram in Detailed Design
- [ ] Migration/rollout plan for anything touching production
- [ ] Open Questions section (empty = suspicious)
- [ ] Risks table with mitigations (not just risks listed)
- [ ] Timeline is realistic given stated constraints

### Whitepaper

- [ ] Quantified results (not just "improved")
- [ ] Comparison to at least one alternative with numbers
- [ ] Related Work is honest about competitors
- [ ] Under 5000 words (unless genuinely warranted)
- [ ] 1+ architecture diagram AND 1+ results table/chart
- [ ] Limitations section present

### Technical Spec

- [ ] Data model is explicit (tables, schemas, access patterns)
- [ ] API surface fully defined (endpoints, request/response, errors)
- [ ] Business rules are unambiguous (testable assertions)
- [ ] Testing strategy maps to business rules
- [ ] Operational concerns addressed (monitoring, failure modes)

## When to Skip

- README files (informational docs don't need this level of rigor)
- Code comments and inline docs
- Meeting notes and communications
- Status updates

forge is for documents that will be shared externally, filed as IP, or referenced as architectural source of truth. Not for everything that gets written.
