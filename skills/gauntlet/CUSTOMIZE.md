# Customizing gauntlet

Three things to set, and one to deliberately leave empty.

## 1. The bar

Default is 9. It is high on purpose: the overall score is the lowest dimension,
so a 9 means every dimension cleared 9.

```yaml
bar:
  default: 9
  by_format:
    blog:         9
    short_social: 9
    case_study:   8   # accuracy matters more than hook here
    internal_memo: 7  # precision over voice
```

Lower the bar for a format rather than switching to an average. The
lowest-dimension rule is what keeps a single weak dimension visible, and
averaging is how a piece ships with an embarrassing hook and a good score.

## 2. Dimensions per format

Not every dimension applies to everything. Turn them off explicitly rather than
tolerating a score you have decided to ignore, or the report trains people to
ignore reports.

```yaml
dimensions:
  short_social:
    structure: off             # 200 words has no structure to speak of
    evidence_made_visible: off # a screenshot rarely fits a 200-word post
  case_study:
    hook: off           # a reader arriving here is already convinced
  internal_memo:
    voice: off
    hook: off
```

**What `off` means:** the dimension is excluded from the overall score entirely.
It does not score zero, and it does not score ten. It is left out of the
lowest-dimension calculation and printed as `off` in the report so a reader can
see it was a decision rather than an omission:

```
Structure   off   (disabled for short_social)
```

`voice: off` and the no-profile cold start in SPEC.md are different things. `off`
removes the dimension. The cold start keeps it, scores internal consistency, and
labels the line. Use `off` when you do not care about voice for a format. Use the
cold start when you care and have not written the profile yet.

`evidence_made_visible: off` and the dimension's own N/A are also different
things, in the same shape as the voice example above. `off` is a per-format
decision you make once, here. N/A is a per-piece judgment the skill makes every
time it scores a draft that has no mechanism to show. Turn the dimension off for
a format that structurally never has visuals (a five-tweet thread); let it score
N/A, piece by piece, for a format that sometimes does (a case study is not
always about a mechanism, but often is).

## 3. The voice profile

Dimension 3 needs a reference. Without one it scores internal consistency and
says so, which is honest but narrower than the dimension name suggests.

### Derive it, do not describe it

Writing down what you think you sound like produces adjectives, and adjectives
do not constrain a score. Build it from a corpus instead: 5,000 to 15,000 words
the person actually produced unedited. Call transcripts are the best source,
because nobody performs in a meeting.

Measure, and record the measurements:

| Measure | Why it constrains a score |
|---|---|
| The 10 to 15 concept words they reach for, with counts | Their vocabulary. A synonym reads as translation |
| Mean and median sentence length, and the share under 8 words | "Short sentences" is not scoreable. "30% under 8 words" is |
| Counts of you, we, I | Someone who writes at the reader scores differently from someone who writes about themselves |
| Questions per paragraph | Dialogic writers end on questions. Most drafts end on summaries |
| Banned words, with the replacement for each | Easier to score than a positive rule |
| Two to four reference pieces | The energy to match |

Strip speech tics before recording. "Kind of", "you know", "right?" are frequent
in talking and wrong on the page. And count before you record: a phrase that
appears twice in 11,000 words is an impression, not a pattern, and a profile
built on impressions produces an impersonation.

**Where it lives.** Both skills in this pair read the same file. Put it at
`content/voice-profile.md` unless you have a reason not to, and use the same path
in both configurations:

```yaml
voice_profile: "content/voice-profile.md"
```

Re-derive it annually, or after anything that changes how someone writes.

## 4. Banned words

The slop checklist in SPEC.md is general. This list is yours, and it should
include the terms specific to your field that have gone hollow.

```yaml
banned:
  - leverage        # use
  - cutting-edge
  - empower
  - synergy
  - holistic
  - paradigm
  - unlock value
  - game-changer
  - in today's fast-paced world
  - at the end of the day
```

A banned term in a draft is a Slop tell, counted with the rest.

## 5. The lessons file: leave it empty

```yaml
lessons_file: "content/content-lessons.md"
```

`campfire` reads and writes the same file under the same key. There is one
learning loop across the pair, not one per skill: `campfire` applies the lessons
when drafting, `gauntlet` records them after approval.

It starts empty and stays empty until the learning loop has run on real pieces
and the author has confirmed the patterns.

**Do not seed it with guesses.** A file of unconfirmed lessons steers every
future draft in a direction nobody chose, and because the drafts get more
consistent, it looks like it is working. Expect it to be worth reading around
the tenth piece.

## 6. Inputs from the drafting stage

Two optional inputs change what this skill can see. Both come from `campfire` in
this repository, and both work with anything else that produces the same shape.

```yaml
inputs:
  source: "content/sources/{date}-{slug}.md"   # what the author actually said
  gap_marker: "[NEED: {what}]"                 # must match the drafting stage
```

**`source`** is the file of stories, quotes, and numbers as the author gave them.
With it, Specificity checks every named number, date, and quoted line against
what was actually said. Without it, Specificity scores what is on the page and
cannot tell an author-supplied fact from an invented one, and the report should
not imply otherwise.

**`gap_marker`** must be byte-identical to whatever the drafting stage writes. A
mismatch means this skill stops recognising the other's gaps and starts
classifying them as editorial, which is the one classification error that lets
invented content into a finished piece.

Neither is required. gauntlet scores a draft from anywhere.

## 7. Visuals: rendering convention

Dimension 7 (Evidence Made Visible) assumes a diagram or screenshot that reads
fine as source will also read fine wherever it lands: GitHub, a CMS, a dark-mode
mail client. That is often not true, and the fix is house-specific: your own
color palette, your own light/dark background choice, your own SVG-vs-PNG rule
per destination.

```yaml
visuals:
  render_style_guide: "docs/style-guide.md#diagrams"
```

Point this at wherever your team's rendering convention already lives. Without
one, this skill can only check what the source communicates, not what the
rendered artifact will actually look like. Say so in the report rather than
assuming the two match.

## Questions to answer before first use

1. **What happens at the bar?** Does clearing it mean publish, or publish after a human read? Scoring is not approval, and a skill that reads as approval will eventually be treated as one.
2. **Who answers the information-gap questions?** If the author is not reachable within the publishing window, decide now whether the piece ships below bar with the gap named, or waits. Deciding under deadline is how invented content gets in.
3. **Which dimension is your team actually weakest on?** Whichever it is, expect the first month of reports to be monotonous about it. That is the tool working.
4. **Do you want the loop at all?** The learning loop needs volume and an author willing to confirm patterns. Below roughly ten pieces a year it will not pay for itself, and turning it off is a legitimate configuration.

## Cross-File Reference

- **SPEC.md**: The seven dimensions and rubrics, the slop checklist, the loop, limitations
- **README.md**: Running it, reading the report, when to skip review
- **references/visuals-evidence.md**: The evidence behind dimension 7
