# Check patterns

`check()` is where the model proves it fits. A clean export proves nothing: CadQuery will happily export a lid that passes through its own body. These patterns are what separate a check that can fail from one that only looks like it could.

## The basic measure

Every fit claim is an overlap volume:

```python
VOLUME_TOL = 1e-3   # mm^3

def _overlap(a, b) -> float:
    return a.intersect(b).val().Volume()
```

**Do not wrap it in `try/except`.** An empty intersection returns an empty compound of volume 0.0; it does not raise. Anything that does raise is a kernel failure, and catching it as 0.0 turns "could not measure" into "proven clear".

Report the number in the error: `"The board hits the body (3.641 mm^3)"`. A number tells the user how far off it is; "collision" does not.

## What every model checks

1. **One solid per part.** `len(body.solids().vals()) == 1`, or it has a floating ledge, a detached tab, or a sliver.
2. **Nothing intersects anything** in the assembled state: every pair of printed parts, and every printed part against every stand-in.
3. **Drop-in paths, not just seated positions.** Sweep the part's envelope (plus clearance) from its seat to above the top, and check that against the body. A board that fits once seated can still be impossible to get there.
4. **Wall-line multiples, strain, stack sums** in `layout()`, before any geometry is built.

## Pair every keep-out with a positive assertion

"Nothing is in the way" is true of a hole that is open and of a hole that was never cut. A keep-out alone passes for the wrong reasons. So:

| Keep-out | Positive assertion that goes with it |
|---|---|
| Nothing obstructs the bore | A probe cylinder down the bore overlaps the body by 0 **and** the body has material around it (the wall exists) |
| The lid clears the ledge | A fixed ring just under the lid overlaps the ledge, so the lid actually lands on it |
| The riser does not hit the board | A thin band from the board's top up to the max gap overlaps the riser, so it actually reaches |
| The wheel does not hit its slot | The wheel crosses both the face plane and the back plane, so a finger can reach it |
| The pocket is clear | The **real bought part**, at its datasheet size, sits in the pocket with 0 overlap |
| The snap does not collide | Hook depth minus gap is at least the minimum engagement |
| The cap is not stuck | Pressed by its travel it meets the switch or keeper; pulled outward its flange catches the wall |

## A probe must not move with its subject

If the check measures a ring whose width **is** `LEDGE_WIDTH`, shrinking the ledge shrinks the probe and the check passes at any ledge size, including none. Probes are fixed sizes, or derived from the thing that rests on the feature, never from the feature itself.

## Mutation-test every check

For every check you add, break the model on purpose and confirm the check fires:

| Break | Expect |
|---|---|
| Plug the bore | Bore-open check fires with the plug's volume |
| Shrink the pocket to the old size | Part-fits check fires |
| Drill the isolation wall | Wall-present check fires |
| Plug only the top of a slot | Slot-clear check fires (plugging the whole slot may trip a different check first, and then this one was never exercised) |
| Set the ledge width to 0 | Lid-lands check fires |

Record the break and the number in the commit message ("plugging the bore is caught at 24.544 mm^3"). A check that has never fired is not yet evidence. If the mutation does not trip the check you meant, find out which check did fire before trusting either.

## Try it rather than calculate it

When deciding whether something fits (can a latch go here?), try the position and let `check()` answer, before concluding from arithmetic. Arithmetic on spans in one axis misses that two things adjacent in y can sit at different depths and never touch. Several positions declared impossible by calculation turned out to fit when tried.

## Sweep before committing a value

For a dimension squeezed between two constraints, sweep it (and run both nominal and print for each value) before committing. Record the window: "passes at 2.5 and 3.0, fails at 2.0 and 3.5 under print tolerance". A value committed in the middle of a two-point window will break on the next change nearby, and the README should say so.

## Run at both tolerances

`python <part>.py` runs `check()` at nominal. `python print_<part>.py` applies `PRINT_TOLERANCES` and runs the same `check()` again. Collisions of a few hundredths of a mm^3 routinely appear only at print tolerance. Both must pass.

## What check() cannot tell you

State these in the docstring so nobody reads a pass as more than it is:

- Hooks flexing past tabs on the way in (only the latched state is modelled).
- Anything about bought parts not modelled at their real size.
- Acoustic, thermal, RF and strength behaviour.
- Whether it is comfortable, reachable or legible. Renders help; the print answers.
