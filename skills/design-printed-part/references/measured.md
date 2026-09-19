# Measured results

**This file is a template. Copy it into your own project before writing a row.**
If it ships as part of an installed plugin, it sits in a package cache and the
next update overwrites it, which is the one thing a measurement log must never
do. `CUSTOMIZE.md` binds where yours lives.

What real prints showed. **A number here beats a default in `fdm-rules.md`.** Append a row after every print that tested a fit, a mechanism or a setting, including the ones that worked as designed: a confirmed default is worth recording too.

When a row contradicts `fdm-rules.md`, update the rule to point here.

## Printers and profiles in use

| Printer | Nozzle | Layer | Line width | Notes |
|---|---|---|---|---|
| | | | | |

## Results

| Date | Printer | Material | What was tested | Designed | What worked | Verdict | Source |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

No rows yet. Everything in `fdm-rules.md` is design-time until this file has
some. The first tests worth running are all cheap, and each one settles a number
the rules can only estimate:

- **A stepped gauge** for whatever dimension a bought part has to close on, a
  series of bars or bores a few tenths apart, read by which step fits.
- **A fit coupon** for each bay or pocket: a floorless slice of just that
  feature, set over the real part.
- **Bore and shaft clearance**: whether the radial clearance in `fdm-rules.md`
  turns freely or rattles on this printer.
- **Hole shrink**: what a hole of a given nominal diameter actually measures
  once printed.
- **Snap latch**: engagement feel at the designed bite, and whether the designed
  strain survives the cycle count the part will see, in each material.
- **Line width**: whether the outer skin closes on a wall at the width you slice
  at.
