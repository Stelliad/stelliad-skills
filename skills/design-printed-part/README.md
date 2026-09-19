# Printed Part Design

**Parametric CAD for FDM, written so the model proves its own fit before any
filament is spent.**

## Running it

This is a specification an agent executes, plus two Python templates you copy.
Install it by copying this folder into your project's skills directory:

```bash
cp -r design-printed-part /path/to/your-project/.claude/skills/
```

Then invoke it:

```
/design-printed-part

or: "design an enclosure for this board", "make this printable",
    "add a snap fit", "why did this print badly"
```

**Working by hand:** [SPEC.md](./SPEC.md) is the procedure.
[assets/model_template.py](./assets/model_template.py) and
[assets/print_template.py](./assets/print_template.py) run as they are, so you
can start from a thing that works rather than a blank file. Requires Python
3.11+, `uv` and CadQuery 2.8+.

## What it does

A CAD model that exports cleanly proves nothing. The kernel will export a lid
that passes through its own body, a pocket with no part in it, and a wall
thinner than the nozzle can draw. All three look fine in a render.

So the model computes its dimensions from constants and **refuses** the ones
that cannot work rather than quietly shrinking a gap. It proves fit as an
overlap volume in cubic millimetres, not by eye. Then the print script re-runs
those same checks at printed tolerances, because collisions routinely appear
only there, lays each part flat, and writes one file per part plus a plate.

It carries the FDM rules that cost people a print to learn: walls as whole
multiples of the line width, holes that come out undersize, nothing finer than
the nozzle, snap arms sized by strain rather than by feel.

## Who uses it

- **Hardware and product teams** iterating enclosures against boards that keep
  changing
- **Anyone printing a part that has to fit something bought**, where the fit is
  the whole job
- **Teams handing a print to someone else**, since the settings a plate file
  cannot carry are half of what makes it come out right

## The part people skip

Step 9: after the print, write down what actually measured. That is what turns
the shipped rules of thumb into a profile calibrated to your machine. It gets
skipped because by then the part works and the question feels answered.

## What it will not do

It does not slice, send jobs or talk to a printer. It does not simulate: no FEA,
no thermal, no fatigue life. It does not simulate assembly motion beyond a
straight-in path, so a part can pass every check and still be impossible to fit.
And a model that passes everything here has never touched a bed. The Limitations
section in [SPEC.md](./SPEC.md) is the full list.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
