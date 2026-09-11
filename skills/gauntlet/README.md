# gauntlet

A quality bar for content, with a number attached. Seven dimensions, a stated
bar, and a clear line between what a machine can fix and what only the author
can answer.

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r gauntlet /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/gauntlet

or: "score this draft and tell me what is holding it down"
```

The agent reads [SPEC.md](./SPEC.md) and does the work.

**Working by hand:** read [SPEC.md](./SPEC.md) and score against the rubrics
directly. [CUSTOMIZE.md](./CUSTOMIZE.md) is where you set the bar and author the
voice profile.

## Reading the report

```
Hook          9/10  Opens on the moment the deadline slipped. Concrete
Specificity   8/10  Strong throughout, but paragraph 4 claims a win with no number
Voice         9/10  Cadence matches the profile. Vocabulary is theirs
Value         7/10  Section 3 is setup. The insight is in section 4
Structure     8/10  Strong open and close. The middle drags
Slop          9/10  Clean. One "it's worth noting" to cut
Visible       6/10  The migration map is the thing readers are asked to trust. Never shown

Overall  6/10  (Visible is the limiter)
```

**The overall score is the lowest numeric dimension, not the average.** Six
strong dimensions do not compensate for a weak one, because a reader meets the
weak one too. Evidence Made Visible can score N/A and is excluded from this
calculation when it does. The limiter is named on the overall line so you know
where to work.

## The part that matters

Every gap gets classified as **editorial** or **information gap**, and they are
handled differently.

Editorial gets fixed. An information gap becomes a question back to you:
"paragraph 4 says the win was significant, what was the number?"

**A gap is never filled with generated content.** A model asked to strengthen a
vague claim will produce a specific one, written in your voice, sitting
comfortably beside the true material. You will not catch it on a read-through.
That is the mechanism by which a review pass makes a piece worse while raising
its score, and refusing it is most of what this skill is for.

If a gap stays unfilled, the report states the ceiling: "this is an 8, and it
stays an 8 until paragraph 4 has a real number."

## Visuals score in both directions

The seventh dimension, Evidence Made Visible, treats a missing diagram and a
padding diagram as the same defect: asking the reader to do work the page
should have done. A screenshot that only repeats the paragraph above it is not
harmless: it scores worse than either the prose or the image alone, because a
reader's confidence that a visual is helping turns out to be no evidence that it
is. Score N/A, not low, for a piece with no mechanism to show, such as an
opinion post or an announcement, and read [references/visuals-evidence.md](./references/visuals-evidence.md)
before arguing with the rubric; most of the popular claims about images are
vendor marketing with no method behind them.

## Before you rely on it

**Write the voice profile.** [CUSTOMIZE.md](./CUSTOMIZE.md) explains how to derive
one from a corpus rather than from impressions. Without it, the Voice dimension
scores internal consistency only and labels itself as such in the report:

```
Voice   7/10  (consistency only, no profile configured)
```

Read the Limitations section in [SPEC.md](./SPEC.md) too. The one worth knowing
up front: this scores the draft, not the truth of it. A confidently wrong piece
with named numbers scores well.

## When to skip review

- Internal notes and specs, where precision beats voice
- Emails under five sentences
- Anything already in the author's natural voice and not going to an audience

gauntlet is for pieces that will be published. Not for everything written.

## See Also

- **SPEC.md**: Seven dimensions and rubrics, the slop checklist, the loop, limitations
- **CUSTOMIZE.md**: The bar, per-format dimensions, voice profile authoring, banned words, the visuals rendering convention
- **references/visuals-evidence.md**: The evidence and sources behind dimension 7, and the named folklore to watch for
- **`campfire`** in this repository: produces the drafts this scores, by interviewing the author first. It also produces a **source file** of the author's stories, quotes, and numbers. Point this skill at it and Specificity stops guessing: every named number and quoted line in the draft either traces to the source or it does not, and the ones that do not are worth asking about

## License

MIT, from the [LICENSE](../../LICENSE) at the root of `stelliad-skills`. The
install step in this README copies this folder on its own, so the licence does
not travel with it. Keep a copy of the repository, or note the licence where you
store the skill.
