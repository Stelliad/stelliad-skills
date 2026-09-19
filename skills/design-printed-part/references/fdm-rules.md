# FDM rules

Defaults for a 0.4mm nozzle at 0.2mm layers. Every number here is a **design-time rule**: it came from a slicer warning, a review, or geometry, not from calipers on a printed part. Where `measured.md` has a number for the same thing, it wins, and this file should be corrected to point at it.

## Walls and the extrusion line

**Make every outer wall a whole number of extrusion lines, and slice at that width.**

At Bambu Studio's default 0.42mm line width, a 2mm wall is 4.76 lines: four perimeters and a ~0.3mm void down the middle that shows on the outside as gaps between the printed lines. At 0.5mm the same wall is exactly four lines and fuses into one skin.

- `LINE_WIDTH = 0.5`, and `layout()` refuses any visible wall, floor, cover or rim that is not a multiple of it.
- Slicer: Prepare tab, Expert mode, Quality > Line width for outer and inner wall = 0.5; Strength > Wall loops = wall / 0.5 (4 for a 2mm wall).
- The 3MF carries geometry only, so this is set by hand every time. Say so in the README and the print script docstring.
- **Internal ribs are exempt.** A gap-filled rib is invisible, and forcing ribs to the rule thickens them into things they then collide with.

Typical sections: wall and floor 2.0, cover 2.0 (1.0 is flexible enough to bow off its latches), rim 1.0.

## Clearances: nominal vs print

The model carries the nominal (machined) value; the print script opens it. Radial means per side.

| Fit | Nominal | Print | Note |
|---|---|---|---|
| Shaft turning in a printed bore (radial) | 0.15–0.20 | 0.25–0.35 | 0.20 is a machined fit; printed, it binds |
| Disc or wheel in a pocket | 0.5 | 0.6 | More if a lip or hook is nearby |
| Button cap in its aperture | 0.2 | 0.3 | |
| Lid or cover in its seat | 0.05 | 0.15 | |
| Snap tab gap | 0.10 | 0.15 | Re-check the engagement still clears its minimum |
| Snap pocket clearance | 0.15 | 0.20 | |
| Board dropping into a bay | 0.5 | 0.5 | Check the drop-in path, not just the seated position |
| Riser stopping short of a board | 0.1 | 0.15 | Grips without clamping |
| Flange in a slot | total, not per face | | A 0.9mm slot on a 0.8mm flange is 0.1 total. Use 1.1, print at 1.2 |

Stacks of small gaps (cap + switch + board + backer in a pocket) must be summed in `layout()` and refused if the remaining clearance drops under ~0.3mm. A pass that depends on `>` rather than `>=` is not a pass.

## Holes

- **Printed holes come out undersize.** Open them in the print profile: 2.0 → 2.2, 2.4 → 2.6.
- **Nothing under ~1.5mm through a 2mm wall.** A 1.2mm hole through 2mm is a tube, not a port, and the nozzle half closes it on the way.
- **Acoustic ports and grilles: 2.0–2.4mm holes on a 4mm pitch**, which leaves a ~1.6mm web that prints as solid extrusions. Open area follows the driver.
- **Screw heads** counterbore flush from the side that is not handled.
- **USB-C openings** size to the cable's overmold, not the receptacle.

## Detail the nozzle cannot draw

- **Webs under ~0.8mm** (two lines) do not print reliably. A 0.2mm web between holes is air.
- **Knurls:** 48 grooves of 0.5mm on a 9–11mm wheel are below a 0.4mm nozzle's resolution. Use about 20 grooves of 0.9mm (radius 0.45).
- **Logos and windows** in a face: keep strokes and the web between windows at or above ~0.7mm and check the part stays one solid.
- **Fillets on thin parts:** the radius cannot approach the part's thickness, or it rounds it to a knife edge. A 1.2mm radius on a 2mm cover, not 2.0.

## Orientation

Decide orientation per part, write it in the print script, and **check the script actually applies it**. READMEs saying "flat, bosses up" while the script exported the part standing on its bosses has happened.

- Largest flat face on the bed; bosses, posts and tabs growing upward.
- **No large bridges.** A 54 x 48mm recess printed face down is bridged over air; face up it is an open recess. Turn the part, or turn the recess into a window on a ledge.
- **Load along the layers, not across them.** A loop whose underside is flush with the back prints without support and a pull runs along the layers. A hook hanging off a thin cover bends across its layers at a root too thin to strengthen, so put the flexing member on the body.
- Face-down parts read mirrored on the plate. If that matters to the person looking at the plate, name the object "(face down)" or print face up.
- Parts meant for a different filament colour export as separate STLs, so no one has to split them in the slicer.

## Snap fits

Size snap arms by root strain for a straight cantilever:

```
strain = 1.5 * t * deflection / L**2
```

`t` arm thickness, `deflection` how far the hook has to move to pass (hook depth + gap), `L` arm length from root to hook. `layout()` computes it and **refuses above the allowance**.

- **Allowance: 0.8% for PLA** flexing repeatedly (a working allowance, not a datasheet value; tighten it in `measured.md` once a latch has been cycled). A design at 0.4–0.75% has margin.
- **Length is what buys it.** A split peg with 3mm halves needing 0.4mm of deflection is 8% strain. An arm rooted at the floor, 7.35mm long, costs 0.76% for the same deflection. Root arms low.
- **Asymmetric hook faces:** ~40° lead on the face the lid rides down, ~60° hold on the face a pull loads. Matched faces release exactly as easily as they engage, which reads as weak.
- **Engagement:** 0.45mm bite, never under 0.25 at print tolerance.
- **Flex the body, not the cover.** The thin part should be the rigid one.
- **A long lid needs latches along its long sides**, or it is held at its ends and bows in the middle. Five on the ends of a 105mm lid was not enough.
- **Latches hold down; a ledge holds up.** Give the lid a ledge to rest on, broken at every latch, and joined to the wall so it is not a separate floating solid.
- Provide a pry notch so it can come off again without a tool.
- Nothing here simulates the hook flexing past the tab on the way in. That is the first thing to look at on a print.

## Captive parts

- A part that drops in "from above" through a solid wall cannot get there. Check the insertion path, not just the seated position.
- Buttons go in from inside, flange behind the wall, backed by something that loads the body (a rib from the floor), not the cover.
- For worn devices, small loose caps are a hazard; prefer a TPU keymat captured by the structure.

## Materials

| Use | Material |
|---|---|
| Coupons, gauges, fixtures, anything on a bench | PLA |
| Anything that hangs, is worn, or takes a pull | PETG, with a bench pull test (e.g. 30N) before it is trusted |
| Keymats, gaskets, bumpers | TPU 95A, fed direct to the extruder rather than through an AMS |
| Light pipes / diffusers for LEDs | Translucent filament, the part itself as the diffuser |

**A printed part is not a breakaway or a safety device.** Its break force moves with layer direction, age and pull angle, and it can leave sharp edges. Safety releases belong in a bought, rated component.

## CadQuery gotchas

- **A fillet at exactly half the width fails in OCC.** Build a stadium from `slot2D`, or a rectangle plus two discs, not `rect().fillet(w/2)`.
- **A zero-radius fillet throws.** Guard every optional fillet with `if r > 0`, so "square" is expressible.
- **Cut after you union.** Interior features unioned after a bore is cut refill it. Do the cuts that must go all the way through last.
- **A cut can remove nothing.** Measure the volume a cut removed when it matters; a slot cut upward from the top of a wall removes air.
- **A feature that does not touch the body exports as a second solid.** Refuse anything but one solid per part.
- **Rename carefully.** When a name like `outer_h` stops meaning what twenty call sites assume, split it into names that say what they are (`face_z`, `cover_z0`) and grep for every variant, including ones with a trailing underscore.
- **Rounded pocket corners eat clearance at a square part's corners.** The arc comes closer along the diagonal than the straight side does, so a board with 0.5mm clearance on its sides can hit a filleted corner. For clearance `e` on the sides and `c` required at the corner, the pocket's corner radius must be at most `(sqrt(2)*e - c) / (sqrt(2) - 1)`, about 0.6mm for e=0.5, c=0.45. Round the part's own envelope by its clearance when sweeping it.
- **Measure along the right axis.** On an arc, x understates radial distance. A probe in the wrong axis passes or fails for the wrong reason.
- Export STLs with `tolerance=0.02, angularTolerance=0.1`.

## Beds

| Printer | Plate |
|---|---|
| Bambu X1 / P1 / A1 | 256 x 256mm |
| Bambu A1 mini | 180 x 180mm |
| Smallest common bed to design the body for | 220 x 220mm |
