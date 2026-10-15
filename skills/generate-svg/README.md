# Vector Image Generation

**Hand-crafted SVG: a real viewBox, named groups, CSS or SMIL motion and no JavaScript, nothing
embedded that is not vector.**

## Running it

This is a specification an agent executes, not a binary. Install it by copying
this folder into your project's skills directory:

```bash
cp -r generate-svg /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/generate-svg a flat icon of a rocket ship
/generate-svg a geometric wolf head, x5
/generate-svg animate, loop after 8s: a network architecture diagram
```

**Working by hand:** read [SPEC.md](./SPEC.md) for the output contract, and set
your palette and conventions in [CUSTOMIZE.md](./CUSTOMIZE.md).

## What it does

Writes the SVG as code from your description: grouped, named, scalable, and
small enough to review in a diff. With animation requested, it adds CSS
keyframes, including a reveal-then-ambient pattern where the image builds once
and then keeps a little motion going without moving anything.

## Who uses it

- **Product teams** needing icons that match an existing set
- **Engineers documenting systems**, where a diagram in version control beats a
  screenshot of a whiteboard
- **Anyone who wants a vector that can be edited later**, by hand, by someone
  else

## What it will not do

It is not an illustration tool, it produces no raster fallback, and it cannot
tell you the result looks like your brand. Text is left out by default, because
text in a vector is a font dependency. The Limitations section in
[SPEC.md](./SPEC.md) is the full list.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
