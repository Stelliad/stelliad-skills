---
name: generate-svg
description: Hand-craft production-ready SVG images and animations from a description: clean paths, a real viewBox, CSS-only motion, and no embedded rasters.
license: MIT
compatibility: Any project. Output conventions, animation budget and house style adapt via CUSTOMIZE.md. No external dependencies.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
type: skill
scope: all
status: active
---

# generate-svg

Write the SVG by hand, as code: a real `viewBox`, grouped and named elements,
CSS-only animation, nothing embedded that is not vector.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the output contract and the animation patterns
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to set your palette, sizes, naming and where files land
3. Ask for one image first, then batch once the style matches

## What it does

1. Reads the description, the count, and whether motion was asked for
2. Writes each file as clean, semantic SVG rather than tracing a raster
3. Adds CSS keyframes when animation is wanted, including a reveal-then-ambient pattern
4. Reports what it produced and where

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). This draws diagrams,
icons and marks; it is not an illustration tool, and it cannot judge whether the
result is on brand.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
