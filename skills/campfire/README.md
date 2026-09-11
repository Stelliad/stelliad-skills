# campfire

Interview first, draft second. The stories, numbers, and opinions come out of the
author's head before a word gets written, and the draft is built from those
answers rather than from the topic.

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r campfire /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/campfire

or: "interview me about the migration, then draft a blog post from it"
```

The agent reads [SPEC.md](./SPEC.md) and does the work.

**Working by hand:** read [SPEC.md](./SPEC.md) and follow it directly. Someone
can run the interview off that document with no agent involved, and the result is
usually better.

[CUSTOMIZE.md](./CUSTOMIZE.md) is where you set your formats, your interview
lenses, and the voice profile.

## What a session feels like

Fifteen to twenty minutes, five to eight questions, one at a time.

It is slower than asking for a draft and it will feel like an interruption. That
is the trade. The alternative is a fluent piece that says nothing only you could
have said, which is the thing most AI writing gets wrong and the reason this
skill exists.

Expect to be pushed on vague answers. "It improved a lot" gets asked again as
"by how much, measured how?" If the second answer is also vague, that is worth
knowing before the draft rather than after.

## What it will not do

**It will not invent your material.** If the interview does not produce a story,
the draft does not get one. Where the draft needs something the interview did not
supply, it leaves a visible gap for you to fill rather than writing a plausible
substitute in your voice.

That last part is the whole point. An invented detail written in your voice sits
comfortably beside the true ones and you will not catch it on a read-through.

## Before you rely on it

**Write the voice profile first.** [CUSTOMIZE.md](./CUSTOMIZE.md) explains how to
derive one from a corpus of what you actually said rather than from your
impression of how you sound. Without it the drafts are competent and generic,
which is the failure this skill was built to prevent.

Read the Limitations section in [SPEC.md](./SPEC.md) as well. The honest summary:
this makes a good writer out of your material, not out of nothing.

## When to skip the interview

- Quick replies and short emails. Just write them
- Technical documentation, where precision beats voice
- Rewriting something that already exists in your voice
- You already wrote a draft and want it edited. Go straight to scoring

campfire is for new content where the raw material does not exist yet.

## See Also

- **SPEC.md**: Interview procedure, the six lenses, the source-file contract, the learning loop, limitations
- **CUSTOMIZE.md**: Voice profile authoring, formats, custom lenses, output paths
- **`gauntlet`** in this repository: scores the draft this produces against a stated bar. Give it the source file as well as the draft and it can check every specific against what you actually said, and it treats every `[NEED: ...]` marker as a question for you rather than something to write for you

## License

MIT, from the [LICENSE](../../LICENSE) at the root of `stelliad-skills`. The
install step in this README copies this folder on its own, so the licence does
not travel with it. Keep a copy of the repository, or note the licence where you
store the skill.
