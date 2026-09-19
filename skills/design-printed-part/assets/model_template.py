"""<Part name>: <one line on what it is and what it holds>.

Template from the design-printed-part skill. A board in a rounded box, on
posts, with a lid resting on a ledge and a USB-C opening in one end wall. It
runs as is; rename it, replace the constants, and keep the shape:

    constants   named, commented where the value is not obvious
    layout()    derives every size and position into one dict, and REFUSES
                with a sentence when something does not fit
    build_*()   one per physical part, stand-ins for bought parts included
    check()     proves the assembled state by measured overlap, pairing
                every keep-out with a positive assertion

WHAT IS MEASURED AND WHAT IS ESTIMATED. Say it here, per bought part:
    board        <datasheet | calipers | ESTIMATE>
    connector    <datasheet | calipers | ESTIMATE>

WHAT THE LID DOES NOT DO: it rests on its ledge and nothing holds it down.
Add snap latches (see references/fdm-rules.md, Snap fits) or screws.

Run:
    uv run python <option>/<part>.py
"""

import pathlib

import cadquery as cq

# ── Bought parts ────────────────────────────────────────────────────────
BOARD_WIDTH = 30.0               # ESTIMATE until measured
BOARD_LENGTH = 50.0
BOARD_THICKNESS = 1.6
COMPONENT_HEIGHT = 3.0           # tallest part on the board's top side
USB_WIDTH = 9.0                  # USB-C receptacle
USB_DEPTH = 7.5
USB_HEIGHT = 3.2
USB_OVERHANG = 0.3               # how far the receptacle sits past the board edge
USB_OVERMOLD = (12.0, 7.0)       # the cable's plug body, which the opening must pass

# ── Shell ───────────────────────────────────────────────────────────────
LINE_WIDTH = 0.5                 # slice at this; every visible section is a multiple
WALL_THICKNESS = 2.0
FLOOR_THICKNESS = 2.0
COVER_THICKNESS = 2.0
CORNER_RADIUS = 4.0
HEADROOM = 1.0                   # above the tallest component, under the lid

# ── Fits ────────────────────────────────────────────────────────────────
POST_HEIGHT = 2.0
POST_DIAMETER = 4.0
POST_INSET = 3.0                 # post centre from the board's edges
BOARD_EDGE_CLEARANCE = 0.5       # board edge to the ledge's inner edge, all round
LEDGE_WIDTH = 1.0                # what the lid rests on
LEDGE_DEPTH = 1.0
COVER_FIT_GAP = 0.05             # lid to wall, per side. The print profile opens it
OPENING_MARGIN = 0.2             # opening above the ledge's underside

VOLUME_TOL = 1e-3                # mm^3
LEDGE_PROBE = 0.6                # FIXED width, not derived from LEDGE_WIDTH (see check)

OUT = pathlib.Path(__file__).parent / "out"


def layout() -> dict:
    """Every derived dimension, or a ValueError that says what does not fit."""
    for name, value in (("WALL_THICKNESS", WALL_THICKNESS), ("FLOOR_THICKNESS", FLOOR_THICKNESS),
                        ("COVER_THICKNESS", COVER_THICKNESS)):
        lines = value / LINE_WIDTH
        if abs(lines - round(lines)) > 1e-6:
            raise ValueError(f"{name} is {value}mm, {lines:.2f} lines at a {LINE_WIDTH}mm extrusion.")

    # The cavity has to pass the board past the ledge on the way down, so the
    # ledge sits outside the board's drop-in envelope, not over it.
    inner_w = BOARD_WIDTH + 2 * (BOARD_EDGE_CLEARANCE + LEDGE_WIDTH)
    inner_l = BOARD_LENGTH + 2 * (BOARD_EDGE_CLEARANCE + LEDGE_WIDTH)
    outer_w = inner_w + 2 * WALL_THICKNESS
    outer_l = inner_l + 2 * WALL_THICKNESS
    if CORNER_RADIUS <= WALL_THICKNESS:
        raise ValueError(f"CORNER_RADIUS {CORNER_RADIUS} leaves no inner radius inside a "
                         f"{WALL_THICKNESS}mm wall.")
    if CORNER_RADIUS >= min(outer_w, outer_l) / 2:
        raise ValueError("CORNER_RADIUS is half the width or more. Build a stadium with slot2D instead; "
                         "a fillet at exactly half width fails in OCC.")

    pcb_bottom = FLOOR_THICKNESS + POST_HEIGHT
    pcb_top = pcb_bottom + BOARD_THICKNESS
    usb_zc = pcb_top + USB_HEIGHT / 2
    opening_top = usb_zc + USB_OVERMOLD[1] / 2
    opening_bottom = usb_zc - USB_OVERMOLD[1] / 2
    if opening_bottom < FLOOR_THICKNESS:
        raise ValueError(f"The USB-C opening reaches z {opening_bottom:.2f}, into the floor. "
                         f"Raise POST_HEIGHT.")

    # Height is whichever is taller: what the board stack needs, or what the
    # opening needs to stay under the ledge. Say which one governs.
    by_stack = pcb_top + COMPONENT_HEIGHT + HEADROOM + COVER_THICKNESS
    by_opening = opening_top + OPENING_MARGIN + LEDGE_DEPTH + COVER_THICKNESS
    outer_h = max(by_stack, by_opening)
    governs = "the board stack" if by_stack >= by_opening else "the USB-C opening under the ledge"

    # A rounded inner corner eats clearance at a square part's corner: the
    # arc comes closer along the diagonal than the side does. Cap the ledge's
    # inner radius so the board keeps its clearance there too.
    c = BOARD_EDGE_CLEARANCE - 0.05
    ledge_r = min(max(CORNER_RADIUS - WALL_THICKNESS - LEDGE_WIDTH, 0),
                  (2**0.5 * BOARD_EDGE_CLEARANCE - c) / (2**0.5 - 1))

    cover_z0 = outer_h - COVER_THICKNESS
    posts =[(sx * (BOARD_WIDTH / 2 - POST_INSET), sy * (BOARD_LENGTH / 2 - POST_INSET))
             for sx in (-1, 1) for sy in (-1, 1)]
    return {
        "inner_w": inner_w, "inner_l": inner_l, "outer_w": outer_w, "outer_l": outer_l,
        "outer_h": outer_h, "governs": governs, "cover_z0": cover_z0,
        "ledge_z0": cover_z0 - LEDGE_DEPTH, "ledge_r": ledge_r,
        "pcb_bottom": pcb_bottom, "pcb_top": pcb_top, "usb_zc": usb_zc,
        "usb_y": -BOARD_LENGTH / 2 - USB_OVERHANG,   # the receptacle's mating face
        "posts": posts,
    }


def _outline(w: float, l: float, r: float, z0: float, h: float) -> cq.Workplane:
    wp = cq.Workplane("XY").workplane(offset=z0).rect(w, l).extrude(h)
    return wp.edges("|Z").fillet(r) if r > 0 else wp


def _box(x0: float, x1: float, y0: float, y1: float, z0: float, h: float) -> cq.Workplane:
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, h, centered=False).translate((x0, y0, z0))


def _usb_path(L: dict, shrink: float, y0: float, y1: float) -> cq.Workplane:
    w, h = USB_OVERMOLD
    return _box(-w / 2 + shrink, w / 2 - shrink, y0, y1,
                L["usb_zc"] - h / 2 + shrink, h - 2 * shrink)


def build_body(L: dict) -> cq.Workplane:
    r_in = CORNER_RADIUS - WALL_THICKNESS
    body = _outline(L["outer_w"], L["outer_l"], CORNER_RADIUS, 0, L["outer_h"])
    body = body.cut(_outline(L["inner_w"], L["inner_l"], r_in, FLOOR_THICKNESS, L["outer_h"]))
    # The ledge starts AT the wall's inner face, so it fuses to the wall
    # rather than floating as a second solid.
    ledge = (_outline(L["inner_w"], L["inner_l"], r_in, L["ledge_z0"], LEDGE_DEPTH)
             .cut(_outline(L["inner_w"] - 2 * LEDGE_WIDTH, L["inner_l"] - 2 * LEDGE_WIDTH,
                           L["ledge_r"], L["ledge_z0"], LEDGE_DEPTH)))
    body = body.union(ledge)
    for x, y in L["posts"]:
        body = body.union(cq.Workplane("XY").workplane(offset=FLOOR_THICKNESS - 0.01)
                          .center(x, y).circle(POST_DIAMETER / 2).extrude(POST_HEIGHT + 0.01))
    # Cuts that must go all the way through come LAST, after every union,
    # or an interior feature refills them.
    body = body.cut(_usb_path(L, 0, -L["outer_l"] / 2 - 1, -L["inner_l"] / 2 + 0.01))
    return body


def build_lid(L: dict) -> cq.Workplane:
    r = max(CORNER_RADIUS - WALL_THICKNESS - COVER_FIT_GAP, 0)
    return _outline(L["inner_w"] - 2 * COVER_FIT_GAP, L["inner_l"] - 2 * COVER_FIT_GAP, r,
                    L["cover_z0"], COVER_THICKNESS)


def build_board(L: dict) -> cq.Workplane:
    """Stand-in, not printed: the board, its tallest component, and USB-C."""
    board = _box(-BOARD_WIDTH / 2, BOARD_WIDTH / 2, -BOARD_LENGTH / 2, BOARD_LENGTH / 2,
                 L["pcb_bottom"], BOARD_THICKNESS)
    parts = _box(-BOARD_WIDTH / 2 + 2, BOARD_WIDTH / 2 - 2, -BOARD_LENGTH / 2 + USB_DEPTH,
                 BOARD_LENGTH / 2 - 2, L["pcb_top"], COMPONENT_HEIGHT)
    usb = _box(-USB_WIDTH / 2, USB_WIDTH / 2, L["usb_y"], L["usb_y"] + USB_DEPTH,
               L["pcb_top"], USB_HEIGHT)
    return board.union(parts).union(usb)


def _overlap(a: cq.Workplane, b: cq.Workplane) -> float:
    # An empty intersection comes back as an empty compound of volume 0.0,
    # not an exception. So nothing is caught here: a kernel failure must
    # stop the check, never read as proven clearance.
    return a.intersect(b).val().Volume()


def check(L: dict, body: cq.Workplane, parts: dict) -> None:
    """Fit checks a clean export would hide. They prove the assembled state
    only; nothing here simulates a part being pushed home."""
    n = len(body.solids().vals())
    if n != 1:
        raise ValueError(f"Body is {n} disconnected solids; expected 1.")
    lid, board = parts["lid"], parts["board"]

    # Nothing intersects anything, assembled.
    for a_name, b_name in (("body", "lid"), ("body", "board"), ("lid", "board")):
        a = body if a_name == "body" else parts[a_name]
        vol = _overlap(a, parts[b_name])
        if vol > VOLUME_TOL:
            raise ValueError(f"The {b_name} hits the {a_name} ({vol:.3f} mm^3).")

    # The board can get there: its footprint, plus clearance, swept from its
    # seat to above the top, must clear the body. Seated is not enough.
    # Rounded by c, so it is the board grown by c in every direction.
    c = BOARD_EDGE_CLEARANCE - 0.05
    sweep = (_box(-BOARD_WIDTH / 2 - c, BOARD_WIDTH / 2 + c, -BOARD_LENGTH / 2 - c, BOARD_LENGTH / 2 + c,
                  L["pcb_bottom"] + 0.01, L["outer_h"] + 2 - L["pcb_bottom"])
             .edges("|Z").fillet(c))
    vol = _overlap(body, sweep)
    if vol > VOLUME_TOL:
        raise ValueError(f"The board can't drop in past the ledge ({vol:.3f} mm^3).")

    # POSITIVE: every post reaches the board. A post that stops short and a
    # post that touches are both "not intersecting".
    for x, y in L["posts"]:
        band = (cq.Workplane("XY").workplane(offset=L["pcb_bottom"] - 0.2)
                .center(x, y).circle(POST_DIAMETER / 2 - 0.05).extrude(0.2))
        if _overlap(body, band) < VOLUME_TOL:
            raise ValueError(f"The post at ({x:.1f}, {y:.1f}) doesn't reach the board.")

    # POSITIVE: the lid lands on the ledge. The probe is a FIXED-width ring
    # under the lid's edge. If it were LEDGE_WIDTH wide, shrinking the ledge
    # would shrink the probe and the check would pass with no ledge at all.
    r = max(CORNER_RADIUS - WALL_THICKNESS - COVER_FIT_GAP, 0)
    w, l = L["inner_w"] - 2 * COVER_FIT_GAP, L["inner_l"] - 2 * COVER_FIT_GAP
    ring = (_outline(w, l, r, L["cover_z0"] - 0.1, 0.1)
            .cut(_outline(w - 2 * LEDGE_PROBE, l - 2 * LEDGE_PROBE, max(r - LEDGE_PROBE, 0),
                          L["cover_z0"] - 0.1, 0.1)))
    under = _overlap(body, ring)
    if under < 0.5 * ring.val().Volume():
        raise ValueError(f"The lid isn't resting on the ledge: {under:.3f} of "
                         f"{ring.val().Volume():.3f} mm^3 under its edge is supported.")

    # The plug reaches the receptacle: its overmold, slightly shrunk, from
    # outside the wall to the mating face, is clear of the body...
    path = _usb_path(L, 0.1, -L["outer_l"] / 2 - 2, L["usb_y"])
    vol = _overlap(body, path)
    if vol > VOLUME_TOL:
        raise ValueError(f"The USB-C plug can't reach the receptacle ({vol:.3f} mm^3).")
    # ...and POSITIVE: there is wall round the opening, so "clear" means an
    # opening was cut, not that the wall is missing.
    w, h = USB_OVERMOLD
    frame = _box(-w / 2 - 1, w / 2 + 1, -L["outer_l"] / 2, -L["inner_l"] / 2,
                 L["usb_zc"] - h / 2 - 1, h + 2).cut(_usb_path(L, 0, -L["outer_l"] / 2 - 1,
                                                               -L["inner_l"] / 2 + 1))
    if _overlap(body, frame) < 0.9 * frame.val().Volume():
        raise ValueError("The wall round the USB-C opening is missing.")


def build_all() -> tuple:
    L = layout()
    body = build_body(L)
    parts = {"lid": build_lid(L), "board": build_board(L)}
    return L, body, parts


def main() -> None:
    L, body, parts = build_all()
    check(L, body, parts)
    OUT.mkdir(exist_ok=True)
    cq.exporters.export(body.union(parts["lid"]), str(OUT / "assembly.step"))
    print(f"Envelope {L['outer_w']:.1f} x {L['outer_l']:.1f} x {L['outer_h']:.1f}mm "
          f"(height set by {L['governs']})")
    print("All fit checks pass at nominal.")


if __name__ == "__main__":
    main()
