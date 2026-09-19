# Printed Part Design Specification

## System Overview

A CAD model that exports cleanly proves nothing. The kernel will happily export
a lid that passes through its own body, a pocket with no part in it, and a wall
one tenth of a millimetre thinner than the printer can draw. All three look
identical in a render, and all three are found the same way: on the bed, an hour
in.

This skill closes that gap. The model computes its own dimensions and refuses
the ones that cannot work, proves fit by measured interference rather than by
eye, and then re-proves it at the tolerances the print will actually have. What
gets handed over is print-ready output plus the settings a 3MF cannot carry.

Two ideas carry most of the weight:

- **Refuse, do not clamp.** A layout that quietly shrinks a gap to make things
  fit has hidden the cost the designer needed to see.
- **A check that has never fired is not evidence.** Every check gets broken on
  purpose once, and the number it printed goes in the commit message.

## Procedure

### 1. Pin the inputs, and mark each one measured or estimated

Before any geometry:

- **What the part holds.** Every bought part with its dimensions and where the
  number came from: a datasheet, calipers on the part in hand, or an estimate.
  Estimates are labelled as estimates in the docstring. An enclosure built
  around an unmeasured board is a guess with a nice render.
- **What this print is for.** Size and feel, a mechanism, a fit against a real
  part, or a working device. Each print answers one question. Say which in the
  print script's docstring.
- **The printer.** Bed size, nozzle, layer height, and material per part.
- **What is decided and what is open.** Decisions go in the docstring with a
  date. Open questions stay visibly open.

If a bought part has not been chosen, say so and model a stand-in with a clearly
named constant. An empty pocket is equally consistent with a part that fits and
one that never will.

### 2. Lay the project out

**Use CadQuery.** The templates, the check helpers and every rule in
`references/` are written against CadQuery's `Workplane` API. Mixing kernels
means the checks stop proving anything. If a project already uses something
else, say so and ask before converting it.

One environment at the root, one directory per part or per design option, each
carrying the model, the print script, an optional render script, a tracked
output directory for STLs and the plate 3MF, a scratch directory that is not
tracked, and a README. `CUSTOMIZE.md` binds the names.

Options compared side by side stay independent: copy shared code rather than
importing across options, so one option never loads another's model.

### 3. Model it

- **Constants** at the top, named for what they are, each with a comment where
  the value is not obvious. Every outer wall a whole multiple of the line width.
- **`layout()`** derives every position and size from the constants into one
  dict, and **raises with a sentence naming what does not fit and which constant
  to change**.
- **`build_*()`**, one per physical part, all built from that dict. Stand-ins for
  bought parts are built the same way, so `check()` can test against them.
- **`check()`** proves the assembled state. Write it to `check-patterns.md`.
- **`__main__`** builds everything, runs `check()`, exports a STEP for scratch,
  and prints the envelope plus anything the user will ask about.

Where a reference is given as a render, a photo or a sketch, measure it rather
than eyeballing it. Where two instructions seem to contradict, look for the
reading where both are true before picking one: a section sketch and a photo
often describe different places on the same part.

### 4. Apply the FDM rules

Read `references/fdm-rules.md` and `references/measured.md`. The rules that bite
most often: outer walls a whole number of extrusion lines, printed holes coming
out undersize, nothing finer than the nozzle can draw, snap arms sized by strain
rather than by feel, and a print orientation per part that needs no support.

### 5. Build the print pipeline

The print script:

1. Overrides the model's constants from a tolerance dict, and **raises if a name
   no longer exists in the model**, so a renamed constant cannot be silently
   toleranced as nothing.
2. Re-runs `check()` at print tolerances. **Nominal and print must both pass.**
   Collisions routinely appear only at print tolerance.
3. Lays each part flat in its print orientation, sits it on the bed, and refuses
   a part that is not exactly the expected number of solids.
4. Removes stand-ins after the check and before export. They are in the model so
   their fit is checked, not so they print.
5. Writes one file per part and a plate with each part as a separate object, so
   material and supports can be set per part in the slicer. Verifies each mesh
   is closed and outward-facing, and refuses a layout that overflows the plate.
6. Keeps test pieces and different-material parts off the main plate.

### 6. Prove every new check fails when it should

Break the model deliberately: plug the hole, shrink the pocket, move the part.
Confirm the check fires with a number, and record that number in the commit
message.

### 7. Print test pieces before the body

Where a dimension depends on something physical that has not been measured,
print the smallest thing that answers it first: a fit coupon, which is a
floorless slice of just that feature set over the real part; a stepped gauge,
which answers a question without calipers; or a material coupon at the device's
own size. Say in the README which gauge gates which print, and in what order.

### 8. Hand over

The README and the print script's docstring carry what the 3MF cannot:

- **Slicer settings by click path**, not just numbers. A geometry-only file
  makes the slicer ask what to do with it; say that this is expected.
- **Material per part**, and which parts want a different filament or colour.
- **Orientation per part** and why.
- **What to look at first**: the weakest predicate, the check that passed with
  the least margin, and the mechanism never exercised in CAD. A hook flexing
  past its tab on the way in is never simulated.
- **What is not modelled**: stand-ins, seals, fasteners.

Then state plainly: modelled and checked, not printed.

### 9. Close the loop after a print

When a print comes back, ask for the numbers that matter: what bound, what was
loose, what closed up, what the calipers said, which printer and filament. Then:

1. Append the result to your project's measurement log, with printer, nozzle,
   material, the dimension designed and the dimension that worked.
2. Update the part's print tolerances and say what changed.
3. Where a measured value contradicts a default in `fdm-rules.md`, the
   measurement wins. Note the contradiction in the rules file.

This step is what turns rules of thumb into a calibrated profile. It is also the
step that gets skipped, because by then the part works and the question feels
answered. It is worth more than any other step in this list.

## Rules

1. **Refuse, do not clamp.** The layout raises when something does not fit.
2. **Nominal and print tolerance both pass**, or it is not done.
3. **Measured interference, not eyeballed renders.** Every fit claim is an
   overlap volume.
4. **Every check has fired at least once**, by deliberate breakage.
5. **Estimates are labelled as estimates** everywhere they appear.
6. **Say what it costs.** Where a change grows the envelope, state the before and
   after; do not bury it.
7. **A printed part is not a safety device.** Breakaways, retention against a
   pull, and battery protection are specified with bought, rated parts. A
   printed part's break force varies with layer direction, age and pull angle.
8. **Never claim printed, fitted or working** for anything only modelled.

## Limitations

- **It does not simulate.** No FEA, no thermal, no drop. Snap arms are sized by
  a strain formula and a material constant, which is a design-time estimate and
  not a prediction of fatigue life.
- **It does not simulate assembly motion.** A part can pass every seated check
  and still be impossible to get into place. The swept-path check in
  `check-patterns.md` covers the straight-in case and nothing else.
- **Every default is printer-specific.** Line width, hole shrink and clearances
  come from one class of machine and one set of materials. Until the measurement
  log has rows, treat every number as a starting point.
- **It does not slice.** Anything the slicer decides, such as support placement,
  seam position, infill and cooling, is outside it, and those decide a surprising
  amount of how a part comes out.
- **Checked is not printed.** This is the one that matters. A model that passes
  everything here has never touched a bed.
