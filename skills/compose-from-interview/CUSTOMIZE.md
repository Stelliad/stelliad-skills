# Customizing compose-from-interview

Four things to set up. The voice profile is the one that matters most and the
one most people skip.

## 1. The voice profile

This skill drafts in someone's voice. Without a description of that voice it
drafts competently and generically, which is the failure it exists to prevent.

**Where it lives.** Both skills in this pair read the same file. Put it at
`content/voice-profile.md` unless you have a reason not to, and use the same path
in both configurations:

```yaml
voice_profile: "content/voice-profile.md"
```

### Do not write it from impressions

The instinct is to write down what you think you sound like. That produces a
document full of adjectives ("direct", "warm", "no-nonsense") which is unfalsifiable
and does not constrain a draft.

**Derive it from a corpus instead.** Gather 5,000 to 15,000 words the person
actually produced, unedited: call transcripts, voice notes, sent emails, Slack
messages they wrote quickly. Transcripts are the best source because nobody
performs in a meeting.

Then measure:

| What to measure | How | Why it constrains a draft |
|---|---|---|
| Load-bearing vocabulary | The 10 to 15 concept words they reach for repeatedly, with counts | These are theirs. Using them reads as authentic; substituting synonyms reads as translation |
| Sentence length | Mean, median, and the share under 8 words | "Short sentences" is not actionable. "30% under 8 words" is |
| Pronoun balance | Counts of you, we, I | Someone who says "you" three times per "I" writes at the reader. A draft that inverts that sounds like a different person |
| Question rate | Questions per speaking turn or per paragraph | Some people are dialogic and end on questions. Most drafts end on summaries |
| Banned words | Terms they never use, and terms they would wince at | Easier to enforce than a positive style rule |

### Separate speech tics from voice

The most common mistake in a corpus-derived profile is transcribing speech into
prose. "Kind of", "you know", "right?", and "basically" are frequent in anyone's
talking and wrong on the page. Take the vocabulary, the rhythm, and the
orientation. Leave the filler.

Be equally careful about the reverse. A phrase that appears twice in 11,000 words
is an impression, not a pattern, and a profile built on it produces an
impersonation. Count before you record.

### Suggested shape

```markdown
# Voice profile: [name]

Derived from [N] words of [source], [date].

## Load-bearing vocabulary
| Term | Uses | How it is used |

## Rhythm
Mean sentence [N] words, median [N], [N]% under 8 words.

## Orientation
"you" [N], "we" [N], "I" [N]. [What that implies for drafting.]

## Never
[Banned words and constructions, with the replacement for each.]

## Reference pieces
[2 to 4 finished things that represent the voice. Match their energy.]
```

Re-derive it annually, or after anything that changes how someone writes.

## 2. Formats

The formats in SPEC.md are a starting set. Replace them with yours, and give
each one a length and a shape rather than a name only. A format entry that does
not constrain the draft is decoration.

```yaml
formats:
  blog:        {words: [1000, 2200], shape: "one thesis, opens on the problem"}
  short_social:{words: [150, 250],   shape: "one idea, hook in the first line"}
  case_study:  {words: [1000, 1500], shape: "problem, approach, result, what I would do differently"}
  newsletter:  {words: [600, 900],   shape: "one story, one takeaway, one link"}
```

## 3. Interview lenses

The six in SPEC.md cover most topics. Add lenses specific to what you write
about. A few that earn their place in particular fields:

| Lens | Field | Question |
|---|---|---|
| Failure | Engineering, operations | "What broke? What did you learn that you could not have learned any other way?" |
| Decision | Leadership, strategy | "What were the options, and why did you pick that one over the runner-up?" |
| Before and after | Consulting, product | "What did the situation look like the week before? The week after?" |
| Objection | Sales, advocacy | "What is the strongest argument against your position? Why does it not change your mind?" |

Keep the ceiling at five per session regardless of how many you define.

## 4. Output paths and content lessons

```yaml
output:
  transcripts: "content/interviews/{date}-{slug}.md"
  drafts:      "content/drafts/{date}-{slug}.md"
  source:      "content/sources/{date}-{slug}.md"

lessons_file: "content/content-lessons.md"

gap_marker: "[NEED: {what}]"

draft_frontmatter:
  - title
  - format
  - status          # draft | in-review | approved | published
  - interview_date
  - source          # path to the source file the draft was written from
```

`compose-score` reads `lessons_file` under the same key and writes to it after
approval. There is one learning loop across the pair, not one per skill.

**`source` is what makes the pair a pair.** When `compose-score` scores a draft and
the source file is reachable, it checks every named number, date, and quoted line
against it. A specific that does not trace is either material the author supplied
outside the interview or invented content, and those are worth telling apart.

**`gap_marker` is shared too.** `compose-from-interview` writes it where the interview did not
produce something the draft needs. `compose-score` treats any visible marker as an
information gap by construction and never resolves one by writing the missing
thing. If you change the format, change it in both configurations, or the second
skill stops recognising the first skill's gaps.

`content-lessons.md` starts empty. That is the correct state on day one and it
stays empty until the learning loop has run on real pieces and the author has
confirmed the patterns. Do not seed it with guesses. A file of unconfirmed
lessons steers every future draft in a direction nobody chose.

Expect it to be worth reading somewhere around the tenth piece.

## Questions to answer before first use

1. **Whose voice is this drafting in?** One person, or a house voice several people write in? A house voice needs a corpus from all of them and will be less distinctive. That is a real cost and worth deciding deliberately.
2. **Who conducts the interview?** The author talking to an agent is the common case. An interviewer talking to the author while an agent listens produces better material and costs a second person's time.
3. **Where does an unfilled gap go?** SPEC.md says leave a marked gap rather than invent. Decide what the marker looks like and who is responsible for clearing it before publication.
4. **What is the review path after the draft?** `compose-score` in this repository scores against a bar. If you use something else, say so in the draft stage so the handoff is explicit.

## Cross-File Reference

- **SPEC.md**: The interview procedure, the source-file contract, the learning loop, limitations
- **README.md**: Running it, what a session feels like, when to skip the interview
