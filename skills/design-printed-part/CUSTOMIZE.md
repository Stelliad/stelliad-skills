# Printed Part Design: Customization Guide

## Before you start

Every number in [references/fdm-rules.md](./references/fdm-rules.md) came off a
particular machine with a particular nozzle and a particular filament. They are
a reasonable starting point and they are not your printer. The first thing to
customize is the measurement log, because a single row in it outranks the whole
rules file.

## Customization 1: The measurement log

**Where it is used:** SPEC.md step 9, and every tolerance decision.

[references/measured.md](./references/measured.md) ships as a template with two
empty tables. **Copy it into your own project.** If this skill is installed as a
plugin, the copy inside it sits in a package cache and the next update
overwrites it, which is the one thing a measurement log must never do.

```
Log lives at:   <e.g. docs/print-log.md, a row per print in the part's README>
Who appends:    <whoever ran the print, same day>
What a row carries: date, printer, nozzle, material, what was tested,
                    the dimension designed, the dimension that worked
```

**If you skip it:** every tolerance stays an estimate forever, and the skill
never gets better than the day you installed it.

## Customization 2: Printer and profile

**Where it is used:** SPEC.md steps 1, 4 and 5, and the rules file throughout.

```
Printer(s):       <model, bed size>
Nozzle:           <default 0.4mm>
Layer height:     <default 0.2mm>
Line width:       <what you actually slice outer and inner walls at>
Slicer:           <name, and where the wall and line-width settings live in its UI>
Plate format:     <3MF, or whatever your slicer takes as multi-object>
```

The click path matters more than the number. A handover that says "0.5mm outer
wall line width" and does not say where that setting lives gets applied wrong or
not at all.

**If you skip it:** the shipped defaults apply, which suit a 0.4mm nozzle at
0.2mm layers.

## Customization 3: Materials

**Where it is used:** SPEC.md steps 1 and 5, and the snap-fit rules.

Write your house defaults and, more importantly, what each one is *for*:

```
Coupons and fixtures:     <e.g. PLA>
Anything loaded or worn:  <e.g. PETG>
Flexible parts:           <e.g. TPU 95A>
Strain limit per material: <the number the layout refuses above>
Anything you will not print: <and why>
```

**If you skip it:** the rules file's material table applies.

## Customization 4: Project layout

**Where it is used:** SPEC.md step 2.

```
One directory per:   <part / design option>
Model file:          <e.g. <part>.py>
Print script:        <e.g. print_<part>.py>
Tracked output:      <e.g. print/  holds STLs and the plate>
Scratch output:      <e.g. out/    gitignored: STEP and experiments>
Environment:         <uv at the repo root, or per directory>
```

**If you skip it:** the layout in SPEC.md step 2 applies, which the two templates
already assume.

## Customization 5: The CAD kernel

**Where it is used:** SPEC.md step 2.

This skill is written against CadQuery, and so are the check helpers, the
templates and every code sample in the references. Swapping to build123d,
OpenSCAD, FreeCAD scripting or a mesh library is not a find-and-replace: the
interference checks are the substance of the skill and they are kernel APIs.

If your organization has already standardized elsewhere, the honest options are
to keep CadQuery for this workflow or to port the check helpers deliberately and
re-prove each one by deliberate breakage.

```
Kernel:   <CadQuery, or the one you ported to and the date it was re-proved>
```

**If you skip it:** CadQuery, as shipped.

## Customization 6: What a handover contains

**Where it is used:** SPEC.md step 8.

```
Goes to:         <a colleague / a print bureau / a client>
Format:          <README in the repo / a PDF / a ticket>
Always includes: <slicer click paths, material per part, orientation per part,
                  what to inspect first, what is not modelled>
Who prints:      <you / them>
```

Where the handover leaves your organization, decide separately what the README
may name. It is a shareable document, and part names, project names and
customer names all end up in it by default.

**If you skip it:** the README carries everything in SPEC.md step 8.

## Customization 7: Safety posture

**Where it is used:** SPEC.md rule 7.

The shipped rule is that a printed part is not a safety device. If your parts go
near people, write what that means concretely for you:

```
Never printed:     <breakaway links, retention against a pull, battery protection>
Bought and rated:  <the part, the rating, who signs off>
Review before print: <which categories need a second person>
```

**If you skip it:** rule 7 applies as written, which is conservative.

## Final checklist

- [ ] Measurement log copied into the project, with an owner
- [ ] Printer, nozzle, layer height, line width and slicer click paths recorded
- [ ] Material defaults and strain limits set
- [ ] Project layout agreed and reflected in the templates
- [ ] Kernel decision made and dated
- [ ] Handover format and audience decided
- [ ] Safety categories named

## Cross-file reference

| File | What it carries |
|---|---|
| `SKILL.md` | Triggers and the reading table |
| `SPEC.md` | The nine steps, the rules, the limitations |
| `CUSTOMIZE.md` | This file: log, printer, materials, layout, kernel, handover, safety |
| `references/fdm-rules.md` | Tolerances, walls, holes, orientation, snap fits, materials |
| `references/check-patterns.md` | How to write a check that can fail |
| `references/measured.md` | The measurement log template |
| `assets/model_template.py` | The model skeleton, runnable as is |
| `assets/print_template.py` | The print pipeline skeleton |
