# compose-score: Content Quality Gate Specification

## The Problem

"Make it better" is not a review. It produces a revised draft nobody can compare
to the old one, and it hides which part was actually weak. A piece either clears
a stated bar or it does not, and the author should be able to see which dimension
is holding it down.

## Core Principle

There are two kinds of problem in a draft, and confusing them is how content
gets worse under review.

| Kind | Examples | Who fixes it |
|---|---|---|
| **Editorial** | Structure, pacing, word choice, hook strength, redundancy, filler | The machine |
| **Information gap** | A missing story, a claim with no evidence, "it depends" with no specific case | **Only the author** |

**Never fill an information gap with generated content.** A model asked to
strengthen a vague claim will invent a specific one, in the author's voice,
indistinguishable on a read-through from the true material around it. That is the
mechanism by which review makes a piece worse while raising its score.

When a dimension is low because something is missing, the output is a question,
not a rewrite.

## Scoring

Seven dimensions, each 1 to 10, except the seventh, which can also score N/A.
**The overall score is the lowest numeric dimension**, not the average. One weak
link means the piece is not ready, and averaging lets five strong dimensions hide
the one that will actually embarrass the author.

Default bar: 9. Configurable, see CUSTOMIZE.md.

### 1. Hook: would a reader continue?

| Score | Meaning |
|---|---|
| 9-10 | Cannot not read the next line. Specific, surprising, stakes clear in the first sentence |
| 7-8 | Pulls you in, could be sharper |
| 5-6 | Functional but generic. Could be anyone's |
| 3-4 | Buries the lead. Gets interesting in paragraph three |
| 1-2 | "I'm excited to announce." "In today's fast-paced world." |

### 2. Specificity: is this grounded in something real?

| Score | Meaning |
|---|---|
| 9-10 | Named examples, real numbers, specific timelines, first-hand detail |
| 7-8 | Mostly specific, one or two generic passages |
| 5-6 | Mixed. Claims appear without evidence |
| 3-4 | Mostly abstract. Could be written by someone who has not done it |
| 1-2 | Pure abstraction |

Low scores here are almost always information gaps, not editorial ones. Route
them.

### 3. Voice: does this sound like the author?

| Score | Meaning |
|---|---|
| 9-10 | Unmistakably them. Their cadence, their vocabulary, their sentence rhythm |
| 7-8 | Mostly right, an occasional generic sentence |
| 5-6 | Inconsistent. Some passages sound like them, others like a model |
| 3-4 | Generic professional voice. Could be anyone |
| 1-2 | Obviously machine-written |

**Cold start.** This dimension requires a voice profile, and there is no useful
default. Where none is configured, do not score it against an imagined voice.
Score internal consistency instead: does the piece sound like one person
throughout, or does the register shift between sections? Then **say so in the
report**, on the line itself:

```
Voice:  7/10  (consistency only, no profile configured)
```

Score it against this instead:

| Score | Meaning |
|---|---|
| 9-10 | One voice throughout. Register, sentence length, and vocabulary hold from first line to last |
| 7-8 | Consistent, with one passage that shifts register |
| 5-6 | Two or more noticeably different voices in the same piece |
| 3-4 | Register changes section by section. Reads as assembled from parts |
| 1-2 | No consistent voice at any length |

A number with no stated reference misleads, because it sits in the column
looking exactly like the five that do have one. CUSTOMIZE.md explains how to
author a profile.

### 4. Value density: can a reader take something from every paragraph?

| Score | Meaning |
|---|---|
| 9-10 | Every paragraph teaches, reveals, or provokes. No filler |
| 7-8 | Tight, one or two paragraphs exist for flow |
| 5-6 | Good ideas diluted by setup and context |
| 3-4 | One idea stretched across ten paragraphs |
| 1-2 | All setup, no payoff |

### 5. Structure: does the format serve the content?

| Score | Meaning |
|---|---|
| 9-10 | Right length, sections earn their place, the ending lands |
| 7-8 | Good flow, one section or the ending could tighten |
| 5-6 | Works but does not elevate. Flat pacing |
| 3-4 | Sections feel arbitrary. The insight is buried. The ending fizzles |
| 1-2 | Stream of consciousness |

### 6. Slop: is any of this machine-generated filler?

Scored by counting tells from the checklist below. The bands are in one place,
the table at the end of the checklist, and this rubric describes what each band
reads like rather than restating the numbers.

| Score | Reads like |
|---|---|
| 9-10 | Varied rhythm, imperfect structure, real personality |
| 7-8 | Clean apart from a couple of borderline phrases |
| 5-6 | Noticeably patterned. A careful reader pauses |
| 3-4 | Multiple paragraphs feel generated |
| 1-2 | A reader would assume a model wrote it |

## The Slop Checklist

**It is the accumulation, not any single tell.** One em dash is punctuation. An
em dash in every paragraph, next to perfect triads and frictionless transitions,
is what a reader registers as machine-written before they can say why.

**Read this before using the checklist.** These tells describe a register, not a
failing. Plenty of careful writers use em dashes, triads, and measured hedges by
choice. Several of the tells also over-fire on people writing English as a second
language, where careful parallel structure, hedging openers, and even sentence
length are marks of learned precision rather than of a model. The checklist is
for finding accumulation in a draft. **Never turn it on a person, and never treat
a high tell count as evidence about who wrote something.** The list also ages:
it describes machine prose as of the time it was written, and it should be
re-read and revised yearly.

| Tell | What to look for | Fix |
|---|---|---|
| Em dash overuse | More than one per 500 words, used for rhetorical pause rather than grammar | A comma, or a full stop and two sentences |
| "It's not X, it's Y" | Contrastive constructions restating the obvious | Cut. State the point directly |
| Triadic lists | Groups of exactly three everywhere | Use two, or four, or one |
| Hedging openers | "It's worth noting", "Generally speaking", "It's likely that" | Delete the preamble. Start at the claim |
| Artificial profundity | Sounds deep, says nothing checkable | Replace with a number, a name, or an example |
| Passive clusters | "Mistakes were made." The actor is hidden | Name who did it |
| Frictionless transitions | Every section bridges perfectly into the next | Real writing is choppier. Leave seams |
| Perfect parallelism | Every bullet the same length, grammar, and rhythm | Vary. Mix fragments and full sentences |
| Low burstiness | Every sentence 12 to 18 words | Mix three-word sentences with 25-word ones |
| Compulsory balance | Equal weight to every perspective | Have an opinion. Be lopsided where you hold one |
| Negative parallelism | "No X, no Y, no Z, just W" | Say it a different way |
| Filler transitions | "Let's dive in", "Without further ado", "In conclusion" | Cut entirely |
| Over-generous setup | A paragraph introducing a point that needs a sentence | Make the point. Trust the reader |
| Vocabulary tells | "delve", "landscape", "paradigm", "leverage", "holistic", "resonate" | The plain word |
| Signposted insight | An emoji and a bold label announcing the point that follows | Delete the label. The point should carry itself |

**Tell count to score.** This table is authoritative for the Slop dimension.

| Distinct tells firing | Slop score |
|---|---|
| 0 to 1 | 9-10 |
| 2 to 3 | 7-8 |
| 4 to 6 | 5-6 |
| 7 or more | 3 or below |

**The unit is a checklist row, not an instance.** A row fires once for the piece
however many times it occurs. Four em dashes are one tell, not four. This is
deliberate: the checklist measures how many *different* machine habits are
present, because that is what a reader registers. A single habit repeated is a
stylistic quirk, and quirks are what voices are made of.

The banned-word list in CUSTOMIZE.md is part of the Vocabulary tells row. Any
number of banned words, in any combination, fires that one row.

**The read-aloud test.** If it sounds like a conference talk transcript or a
well-meaning corporate blog, it is slop. If it sounds like someone talking at a
whiteboard, uneven and opinionated and occasionally blunt, it is not.

A caveat worth holding: these tells describe machine-written prose *as of the
time this was written*, and they describe a register, not a moral failing. Plenty
of careful human writers use em dashes and triads. The checklist catches
accumulation in a draft, and should never be turned on a person.

### 7. Evidence made visible: does the reader have to take the mechanism on trust?

Dimensions 1-6 all score prose. This one scores what the piece **shows**:
diagrams, screenshots, real tool output, tables, artifacts. It is scored in both
directions: a missing visual and a padding visual are the same defect, which is
asking the reader to do work the page should have done.

| Score | Meaning |
|---|---|
| 9-10 | Every claim the reader must trust has its artifact on the page, and nothing is illustrated that the prose already carries |
| 7-8 | Right instinct, one gap or one visual that duplicates its paragraph |
| 5-6 | The central mechanism is described but never shown, or shown exactly once more than needed: a single diagram repeating what one paragraph already carries |
| 3-4 | Visuals are decorative, or a wall of screenshots stands in for an argument |
| 1-2 | Redundant or decorative visuals throughout, not an isolated lapse: stock imagery, a diagram of a bulleted list, screenshots of text quoted two lines above |

The 5-6 and 1-2 bands are the same defect at different scale. 5-6 is one
otherwise-strong piece with one redundant diagram on its central point. 1-2 is
the piece's default mode: redundant capture repeated enough times that it reads
as how the author works, not as a slip.

**Score N/A and exclude it from the overall** when the piece has no mechanism to
show: a short opinion post, a personal essay, an announcement. This dimension
applies to pieces that ask the reader to believe something works.

**Two findings should govern how you score this.** First, a visual duplicating
prose is not neutral: it scores **worse than either alone**. Second, readers
rate the redundant version as their *best understood* while comprehending it
worst, so your confidence that a diagram is helping is evidence of nothing. The
effect is strongest for expert readers, which is who reads most published
technical and business writing.

**The test is self-sufficiency, not overlap.** Ask whether the prose alone works,
and whether the visual alone works. If **both** do, delete one, preferring to
keep the prose, which is searchable and does not go stale. If **neither** does,
that is a different defect: the two are mutually incomplete, and the fix is to
integrate them (put the label on the node, not in a legend) rather than to cut.

**Then count the parts.** Fewer than about four items, or anything purely
sequential, has too little going on for a diagram to pay for itself.
Simultaneous, mutually-constraining relationships are what a diagram is for.

**The decision rule.** Apply it to each candidate visual, and to each claim that
has none:

> **Show it when the reader is being asked to trust something they cannot verify
> from the prose**: a sign-off artifact, real tool output, a state a screenshot
> proves and a sentence only asserts, a number whose shape matters more than its
> value.
>
> **Cut it when the prose already carries it**: a diagram of a list, a concept
> with a canonical external explainer, a screenshot of a command already quoted,
> a second diagram of a thing diagrammed once.
>
> **Behaviour earns a diagram; static structure usually does not.** A funnel, a
> pipeline, a state machine, or a branching flow earns one. A list, or a
> configuration of "A talks to B talks to C," does not: either medium alone
> conveys that.

**Anti-patterns, by name:**

| Anti-pattern | What it looks like | Fix |
|---|---|---|
| Decorative imagery | A stock photo, or an abstract graphic, above the fold | Cut. It costs load time and signals marketing |
| Diagram of a list | Four boxes in a row reproducing four bullets | Keep the bullets |
| Screenshot wall | Six consecutive screenshots walking a UI | Apply the omission test to each: can the reader follow the prose without it? Then cut it |
| Redundant capture | A screenshot of text quoted in the paragraph above | Cut the screenshot, keep the quote: text is searchable and ages better |
| The invisible artifact | "This is the thing you sign off on," and it is never shown | Show it. This is the most common miss |
| Undated screenshot | A UI capture with no version or date, in a piece that will outlive the UI | Date it in the caption, or use text output instead |

**Captions state the takeaway: a house choice, not a settled rule.** Say what
the image *shows*, not what it *is*. This is contested: the controlled evidence
for claim-style headlines is about spoken slides, and Nature's figure policy
requires the opposite. What is not contested is that **a caption cannot carry
the figure**: readers given only a legend miss 39-68% of the information, so the
prose has to do the work regardless of which caption style you pick.

**Alt text: identify the image and point at the prose.** WCAG's own sanctioned
pattern for anything complex is a short alt that signals a description follows,
with the description in the body where everyone can read it, not a paragraph
stuffed into an attribute. A decorative image, if one survives the rule above,
takes `alt=""`; omitting the attribute is not an option, because some screen
readers then read the filename aloud. There is no 125-character limit; that
number is folklore.

**Never screenshot text, code, or terminal output.** Quote it. Every major
documentation style guide says this independently, and quoted text is
searchable, translatable, and does not rot.

**Check the render, not the source.** A diagram that reads fine as source can
render as an unusable strip, and a background choice that looks fine in a light
editor can invert or vanish in a reader's dark-mode client. Point this at your
own rendering convention via CUSTOMIZE.md; without one, at least eyeball the
rendered output before calling a visual done, not just its source.

**Evidence, sources, and the named folklore** are in
[references/visuals-evidence.md](references/visuals-evidence.md). Read it before
arguing with any line above, and before quoting a statistic about images: the
popular ones are almost all vendor marketing with no method behind them.

## Procedure

### 1. Score

Read the draft. Score all seven (six numeric, one possibly N/A) with a one-line
justification each.

```
compose-score: "Why the migration took nine months"

Hook          9/10  Opens on the moment the deadline slipped. Concrete
Specificity   8/10  Strong throughout, but paragraph 4 claims a win with no number
Voice         9/10  Cadence matches the profile. Vocabulary is theirs
Value         7/10  Section 3 is setup. The insight is in section 4
Structure     8/10  Strong open and close. The middle drags
Slop          9/10  Clean. One "it's worth noting" to cut
Visible       6/10  The migration map is the thing readers are asked to trust. Never shown

Overall  6/10  (Visible is the limiter)
Bar      9/10
Verdict  NOT READY. Four dimensions below bar
```

Lead with the limiter. An author reading a seven-line report should know in one
glance what to work on. When two or more dimensions tie for lowest, name all of
them on the overall line rather than picking one arbitrarily.

A piece with no mechanism to show scores Visible as N/A, printed on its own line
and left out of the overall:

```
compose-score: "Why I'm leaving my role at the end of the quarter"

Hook          8/10  Opens on the decision, not the backstory
Specificity   9/10  Named dates, named projects, no hedging
Voice         9/10  Cadence matches the profile
Value         8/10  One paragraph of thanks could be trimmed
Structure     9/10  Right length for the format, ending lands
Slop          9/10  Clean
Visible       N/A   No mechanism to show; personal announcement

Overall  8/10  (Hook and Value are tied limiters; Visible excluded)
Bar      9/10
Verdict  NOT READY. Two dimensions below bar
```

Visible is skipped in the lowest-dimension calculation the same way an `off`
dimension is (CUSTOMIZE.md), but the report still prints the line and the
reason, so a reader can tell a scored omission from a configured one.

### 2. Classify every gap

For each dimension under the bar, decide: editorial, or information gap? Say
which. This classification is the skill's actual output, and getting it wrong in
the direction of "editorial" is how invented content enters a draft.

**A visible gap marker is an information gap by construction.** `compose-from-interview` writes
`[NEED: ...]` where the interview did not produce something the draft needs.
Never classify one as editorial, never resolve one by writing the missing thing,
and never quietly delete one to raise a score. Each marker becomes a question in
step 3, verbatim.

**Where a source file exists, check the specifics against it.** `compose-from-interview`
produces one: stories, quotes, and numbers as the author gave them. When it is
available, every named number, date, and quoted line in the draft should trace to
it. Anything specific that does not trace is either the author supplying material
outside the interview, which is fine and worth confirming, or invented content,
which is the failure this pair exists to catch. Say which you found. Without a
source file, Specificity scores what is on the page and cannot tell the two
apart, and the report should not imply otherwise.

### 3. Fix or route

- **Editorial:** apply the fix, produce a revised draft
- **Information gap:** ask one to three targeted questions. Not "add more detail" but "paragraph 4 says the win was significant. What was the number?"

### 4. Loop

Re-score after each pass. Cap at three editorial loops. If the score is not
moving after two, the problem is not editorial and further passes will only sand
the piece down.

At the cap, stop and report the ceiling the same way an unfilled information gap
is reported:

```
Stopped at 3 editorial passes. Structure held at 7/10.
The middle section does not tighten because there are two arguments in it.
That is a decision about the piece, not an edit. Which one is it about?
```

An editorial stall is a signal about the piece's shape, and it goes back to the
author as a question rather than as a fourth pass.

If information gaps stay unfilled, **stop and report the ceiling**: "This is an
8, and it stays an 8 until paragraph 4 has a real number." Do not fill the gap to
clear the bar.

### 5. Finish

At the bar, or when the author says ship, mark it approved and run the learning
loop.

## The Learning Loop

After approval, compare the first draft with the final:

1. Diff first against final
2. Extract the pattern rather than the instance
3. **Put it to the author before recording it.** A diff shows what changed, not why
4. Record confirmed patterns where future drafts will read them

Lessons file starts empty and should stay empty until real pieces have run
through. See CUSTOMIZE.md.

## Limitations

- **It scores the draft, not the truth of it.** A confidently wrong piece with named numbers scores well on Specificity. Fact-checking is a separate pass.
- **Voice without a profile is consistency only.** Stated on the line, not hidden.
- **The slop checklist ages.** It describes a register that shifts as models shift. Re-read it yearly and expect to add and retire tells.
- **The lowest-dimension rule is deliberately harsh.** A 9-9-9-9-9-4 piece scores 4. That is intended, and it will be annoying when the 4 is a dimension you do not care about for this format. Turn dimensions off per format rather than switching to an average.
- **Three loops is a real ceiling.** A piece that will not clear the bar in three passes usually has a problem no editor can fix.
- **It cannot tell you whether the piece should exist.** It scores execution against a bar, and a well-executed piece nobody needed still scores 9.
- **Evidence Made Visible is directional, not additive.** A missing visual and a padding visual are the same defect. Do not reward a piece for including diagrams regardless of whether they earn their place, and do not let this dimension's N/A become a default: most published technical and business writing has a mechanism to show.

## Cross-File Reference

- **README.md**: Running it, reading the report, when to skip review
- **CUSTOMIZE.md**: The bar, dimension weighting per format, the voice profile, banned words, the lessons file
- **references/visuals-evidence.md**: The evidence and sources behind dimension 7, and the named folklore to watch for
