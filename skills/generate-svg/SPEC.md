# Vector Image Generation Specification

## System Overview

An SVG is code. Written by hand it stays small, scales cleanly, diffs in review,
and can be edited six months later by someone who was not there. Traced from a
raster, or generated as a pile of absolute coordinates, it is none of those
things.

This skill writes SVGs as code from a description, and the output contract below
is what separates a file a team can keep from a file that merely renders today.

## The output contract

Every file this produces:

- **Has a `viewBox`** and no fixed pixel width or height, so it scales
- **Groups logically** with `<g>`, and names groups and shapes with `id` or
  `class` that describe the thing, not the geometry
- **Keeps paths readable**: relative commands, no redundant precision
- **Uses no JavaScript.** Animation is CSS or SMIL, inside the file
- **Embeds no raster image.** If something can only be a bitmap, this is the
  wrong tool
- **Adds no text** unless text was asked for, because text in a vector becomes a
  font dependency

## Procedure

### Step 1: Read the request

| Parameter | Where it comes from | Default |
|---|---|---|
| Subject | The description | required |
| Count | A number, `x3`, "three variations" | 1 |
| Animation | "animate", "animated", "motion" | off |
| Reveal length | "loop after 8s" and similar | none |
| Output directory | Stated, or asked for | ask |

**Ask where the files go** unless it was stated. Writing several files into a
directory the person did not choose is the one failure here that costs them
cleanup.

### Step 2: Draw

Compose from primitives rather than one long path where the shape allows it: a
diagram is a set of named rectangles and connectors, not a single outline. For
several variations, give each a distinct angle rather than nudging the same
drawing, and name the files so the set is obvious.

### Step 3: Animate, if asked

CSS keyframes in a `<style>` block inside the SVG. Animate `transform`,
`opacity` and `stroke-dashoffset`, which composite cheaply; avoid animating
layout or geometry properties.

**The reveal-then-ambient pattern**, for a request like "loop after 8s":

1. **Reveal, once.** Elements fade or draw in, staggered, over the stated
   duration, and freeze in their final state. This never repeats.
2. **Ambient, forever.** After the reveal, a small number of indefinite
   animations keep the image alive: a pulsing border, a dot travelling a
   connector, a marching dashed line, a gentle opacity drift.

The rule that keeps it tasteful: ambient motion may only reinforce the idea the
image is about, usually flow or hierarchy. It never moves an element from its
final position and never animates text.

### Step 4: Report

List each file with its path, say what it depicts, and name any animation. For a
batch, number them.

## Quality checks before handing it over

- Does it render at 16 px and at 1000 px?
- Does it survive being recoloured by CSS, or are colours hardcoded where a
  `currentColor` would do?
- Is the file under a few tens of kilobytes? A large SVG is usually a traced one.
- Does every animation stop being interesting after one loop, and is that fine?
- Would someone reading the markup understand what the image is?

## Limitations

- **This is not illustration.** Icons, marks, diagrams and simple scenes are in
  scope; a painted or photographic image is not.
- **No raster fallback is produced.** If the target cannot take SVG, this is the
  wrong step in the pipeline.
- **Brand judgment is not included.** It can follow a palette and a stroke
  weight you give it; it cannot tell you the result looks like your company.
- **Complex text layout is fragile.** Text needs a font that exists wherever the
  file is rendered, which is why the default is to leave it out.
- **Animation taste is subjective**, and the ambient pattern is deliberately
  conservative. A brief with a strong motion idea deserves a designer.
