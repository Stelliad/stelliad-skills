# campfire: Content Extraction Specification

## The Problem

Most AI content fails at the same place. It goes straight from "write me a post
about X" to a draft, and the draft is fluent, structurally sound, and carries no
information the model did not already have. It reads like everyone else because
it was assembled from everything else.

The missing step is extraction. The stories, the numbers, the moment someone
changed their mind, the thing they believe that their industry does not: none of
that is retrievable. It exists in one person's head and has to be got out before
any drafting happens.

## Core Principle

**The machine never invents the substance.** It researches, structures, drafts,
and edits. The author supplies the stories, the opinions, and the specifics.

This is a hard boundary, not a preference. The moment a model fills a gap in
someone's experience with a plausible invention, the piece is carrying a claim
its author cannot stand behind, and the author usually will not notice, because
the invention is written in their voice and sits comfortably beside the true
parts.

## Procedure

### Stage 1: Format and premise

Establish what is being made and whether the author has the raw material.

| Format | Shape |
|---|---|
| Blog post | 1000 to 2200 words, one thesis |
| Short social post | 150 to 250 words, one idea, hook carries it |
| Thread | 5 to 12 posts, one narrative arc |
| Case study | Problem, approach, result, what I would do differently |
| Long-form article | Multi-section, research-backed |

Formats are configurable. See CUSTOMIZE.md.

If the request is bare ("write about X"), ask two things before anything else:
the format, and whether this is something the author has **done** or something
they are **thinking about**. The answer changes the entire interview. Lived
experience gets a story interview. A developing opinion gets an argument
interview, and the honest framing of the piece is different.

### Stage 2: Research brief

**This stage needs a search tool. Where none is available, skip it and say so.**
An interview-only session still works: the questions are broader, the author does
more of the framing, and the piece is more likely to repeat something already
said elsewhere. That is a real cost and the author should know it was paid.

Before interviewing, build enough context to ask targeted questions:

- What has already been said about this topic, and by whom
- The current facts, and anything that changed recently
- Which contrarian positions are available and who holds them
- **The questions only this author can answer**

That last line is the output that matters. Everything else is preparation for
it. A generic question wastes the author's attention, and their attention is the
scarce input in this whole process.

### Stage 3: The interview

**One question at a time. Wait for the answer. Do not batch.**

Batching questions is the single most common way this stage fails. Six questions
in one message gets six short answers, because the author is managing a list
rather than remembering an event. One question gets a story.

**Lenses.** Pick three to five per session based on the topic. Do not run all
six; the interview should take fifteen minutes, not an hour.

| Lens | What it is after | Opening question |
|---|---|---|
| Story | A specific moment that carries the point | "Walk me through what actually happened. What did you see, hear, do?" |
| Tactics | The part a reader can steal tomorrow | "If someone wanted to do this tomorrow, what is step one? What breaks if they skip it?" |
| Contrarian | The thing the field gets wrong | "What is the conventional wisdom here? Where is it wrong?" |
| Numbers | Metrics, timelines, scale | "How long did it take? What did it cost? What was the before and after?" |
| Stakes | Why it mattered, and to whom | "What was at stake? What happened to the people involved?" |
| Principle | The rule underneath the anecdote | "Boil it to one rule. What is it?" |

**Rules of the interview:**

- **Never accept "it depends".** Follow up: "Give me the case where it does not depend." The specific case is the content; the abstraction is not.
- **Never accept a claim with no evidence behind it.** "It improved a lot" is a prompt for "by how much, measured how?"
- **Push once on a vague answer, then move on.** "That is the general version. What is the specific moment that made you think it?" If the second answer is also vague, the author may not have the material, and that is worth knowing now rather than at the draft.
- **Preserve exact phrasing.** Their words are the raw material. A phrase someone reaches for naturally is worth more than a better phrase you supply.
- **Five to eight questions.** Stop before the author is tired. A short interview with three real stories beats a long one with twelve thin answers.
- **Follow the energy.** If an answer arrives with more force than the others, that is the piece. Abandon the plan and go there.

### Stage 4: The source file

Turn the transcript into a structured source. This file, not the topic, is what
the draft is written from.

| Section | Contents |
|---|---|
| Core stories | Verbatim, with enough context to stand alone |
| Key insights | In the author's words, not paraphrased |
| Quotable lines | Things they said naturally that land as written |
| The stakes | What makes this matter, and to whom |
| Surprises | Things they said that surprised even them. Often the actual piece |
| The "so what" | Why a reader who does not know the author should care |

If a section comes back empty, that is a finding. An empty "so what" means the
piece has no reader yet, and drafting will not create one.

### Stage 5: Draft

Only now. Requirements, all of them binding:

- Every story, number, and claim traces to the source file
- Read the configured voice profile before writing (see CUSTOMIZE.md)
- Follow the format spec for the chosen type
- Apply any accumulated content lessons (see CUSTOMIZE.md)
- **Invent nothing.** No stories, quotes, statistics, or details that are not in the source file

Where the draft needs something the interview did not produce, leave a marked
gap rather than filling it. The marker is `[NEED: {what}]`, configurable but
shared with the scoring pass:

```
We cut deployment time from [NEED: the before number] to [NEED: the after number].
```

A visible marker is a question the author answers in five seconds. An invented
number is a defect that ships, written in their voice, sitting beside the true
ones. `gauntlet` treats any visible marker as an information gap by construction
and will never resolve one for you.

Hand the draft to a scoring pass. `gauntlet` in this repository is built for it.

## Output

Two artifacts:

1. **Interview transcript.** Raw question and answer. Keep it: it is mineable for future pieces, and a story that did not fit this piece often carries the next one.
2. **Draft.** With frontmatter recording the format, the interview date, and the status.

A third artifact, the **source file** from stage 4, is what the scoring pass
reads to tell an author-supplied specific from an invented one. Keep it with the
draft.

Paths, frontmatter fields, and the gap marker are configurable. See CUSTOMIZE.md.

## The Learning Loop

After a piece is finished and published, compare the first draft against what
actually shipped.

1. Diff first draft against final
2. Extract the pattern, not the instance. "Cut the opening paragraph" is an instance. "Cuts abstract openers, starts at the specific moment" is a pattern
3. **Put the pattern to the author before recording it.** A diff shows what changed, not why, and the wrong lesson learned confidently makes every future draft worse in the same direction
4. Record confirmed patterns where future drafts will read them

The point is that first drafts improve. A skill that produces the same quality
of first draft in month six as in week one is not learning, it is just running.

## Limitations

- **It cannot make someone interesting about a topic they have not lived.** If the author has no stories, the interview surfaces that, and the honest output is a shorter and differently framed piece. This is a feature, and it will feel like a failure.
- **It depends on the author actually answering.** A rushed interview with one-line answers produces a thin source file and a thin draft, and no amount of drafting skill recovers it.
- **Voice matching is only as good as the configured profile.** With no profile, the draft will be competent and generic.
- **It does not fact-check the author.** Their numbers go in as given. Verification is a separate pass, and for anything load-bearing it should happen.
- **The learning loop needs volume.** Two pieces will not produce reliable patterns. Expect it to be useful somewhere around ten.

## Cross-File Reference

- **README.md**: Running it, what a session feels like, when to skip the interview
- **CUSTOMIZE.md**: Formats, interview lenses, the voice profile, output paths, content lessons
