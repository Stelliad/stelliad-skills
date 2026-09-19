# Vector Image Generation: Customization Guide

## Before you start

Two decisions make the output usable rather than merely valid: what your images
must look like, and where they belong. Both are house style, and neither can be
inferred from a description.

## Customization 1: Palette and stroke

**Where it is used:** SPEC.md, step 2, and the quality checks.

```
Primary colours:     <hex values, or "use currentColor">
Neutrals:            <hex values>
Stroke weight:       <e.g. 1.5 at a 24 unit viewBox>
Corner radius:       <e.g. 2>
Grid:                <e.g. 24x24 for icons, 1200x630 for diagrams>
```

Say whether colour is hardcoded or inherited. Icons that inherit
`currentColor` theme themselves; diagrams usually cannot.

**If you skip it:** the output is plausible and off-brand.

## Customization 2: Output conventions

**Where it is used:** SPEC.md, steps 1 and 4.

```
Directory:     <where files land>
Naming:        <e.g. icon-{subject}.svg, diagram-{topic}-{n}.svg>
One per file:  <yes, or a sprite sheet>
Optimisation:  <whether an SVG optimiser runs afterwards, and its settings>
```

**If you skip it:** the skill asks every time, which is correct and slow.

## Customization 3: The animation budget

**Where it is used:** SPEC.md, step 3.

Motion is the easiest thing to overdo. Write down the limit:

```
Maximum simultaneous animations:  <e.g. 3>
Reveal duration default:          <e.g. 8s>
Ambient loop: allowed elements    <e.g. connectors and borders only>
Never animate:                    <e.g. text, anything that moves layout>
Reduced motion:                   <whether to wrap in prefers-reduced-motion>
```

**Accessibility is a real decision here.** If your audience includes anyone who
has asked their system for less motion, the ambient phase belongs inside a
`prefers-reduced-motion` guard.

**If you skip it:** the defaults are conservative, and still not yours.

## Customization 4: Where the output is used

**Where it is used:** SPEC.md, *Quality checks*.

An icon in a component library, a diagram in documentation and a graphic in an
email have different constraints. Name the destinations and their rules:

```
Component library:  <sizes, inherits colour, no animation>
Documentation:      <max width, light and dark backgrounds>
Slides:             <bleed, fixed colours>
Email:              <SVG often unsupported: what happens instead>
```

**If you skip it:** files that render beautifully in a browser and break in the
destination.

## Customization 5: Review

**Where it is used:** the whole skill.

- Who checks the result against brand, and before or after it is committed
- Whether generated images are reviewed like code, in a pull request
- What happens to variations that were not chosen

**If you skip it:** generated images accumulate and nobody can say which is
canonical.

## Final checklist

- [ ] Palette, stroke weight, radius and grid are written down
- [ ] Output directory and naming are set
- [ ] The animation budget names a maximum and a reduced-motion rule
- [ ] Each destination's constraints are listed
- [ ] Someone owns the brand check

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | The trigger and the one-line rule |
| `SPEC.md` | The output contract, the procedure, animation patterns, limitations |
| `CUSTOMIZE.md` | This file: palette, conventions, motion budget, review |
