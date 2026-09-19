"""Print-ready parts for <part name>, for an FDM printer.

Template from the design-printed-part skill. Builds the same model as
model_template.py with FDM tolerances applied, re-runs its fit checks at
those tolerances, lays each part flat in its print orientation, writes one
STL per part to print/, and arranges them on one plate as plate.3mf.

WHAT THIS PRINT IS FOR: <size and feel | a mechanism | a fit against the
real part | a working device>. Say which, and what to look at first.

SET THE WALL LINE WIDTH TO 0.5mm IN THE SLICER. Every visible wall is a
whole number of 0.5mm lines; at Bambu's default 0.42mm they do not divide
and the slicer leaves a void down the middle of each wall. Bambu Studio:
Prepare tab, Expert mode, Quality > Line width (outer and inner wall) 0.5,
Strength > Wall loops 4. The 3MF carries geometry only, so Bambu Studio
asks to "load geometry only"; that is expected, and these are set by hand.

Material: <PLA for a bench fit check | PETG if it hangs or is worn>.

Run:
    uv run python <option>/print_<part>.py
"""

import pathlib
import struct
import zipfile
from xml.sax.saxutils import escape

import cadquery as cq

import model_template as m

# Only the values printing changes. Every name must exist in the model, or
# the override raises rather than silently toleranceing nothing.
PRINT_TOLERANCES = {
    "COVER_FIT_GAP": 0.15,        # 0.05 is a machined fit
    "USB_OVERMOLD": (12.2, 7.2),  # printed openings come out undersize
}

BED_SIZE = (220.0, 220.0)         # smallest common bed; the largest part must fit it
PLATE_BED = (256.0, 256.0)        # Bambu X1 / P1 / A1. A1 mini is 180
PLATE_GAP = 8.0
PLATE_COLUMNS = (("body",), ("lid",))

# Parts built for check() and never printed.
STAND_INS = ("board",)

# Print orientation per part: "" as modelled, or a named flip. Check the
# result, not the intent: a README saying "bosses up" does not make it so.
ORIENTATION = {
    "lid": "face_down",           # the visible face on the bed, for the best surface
}
EXPECTED_SOLIDS = {}              # parts that are deliberately more than one solid

OUT = pathlib.Path(__file__).parent / "print"


def apply_print_tolerances() -> None:
    for name, value in PRINT_TOLERANCES.items():
        if not hasattr(m, name):
            raise AttributeError(f"The model has no {name}; the print profile is out of date.")
        setattr(m, name, value)


def lay_flat(shape: cq.Workplane, flip: str = "") -> cq.Workplane:
    """Rotate into print orientation, then sit it on z=0 centred on the origin."""
    if flip == "face_down":
        shape = shape.rotate((0, 0, 0), (1, 0, 0), 180)
    elif flip == "on_side_x":
        shape = shape.rotate((0, 0, 0), (0, 1, 0), 90)
    elif flip == "on_side_y":
        shape = shape.rotate((0, 0, 0), (1, 0, 0), 90)
    elif flip:
        raise ValueError(f"Unknown orientation {flip!r}.")
    bb = shape.val().BoundingBox()
    return shape.translate((-(bb.xmin + bb.xmax) / 2, -(bb.ymin + bb.ymax) / 2, -bb.zmin))


# ── Plate 3MF ───────────────────────────────────────────────────────────
# Copied, not imported, between options, so one option never loads another.

def _read_binary_stl(path: pathlib.Path) -> list:
    data = path.read_bytes()
    (n,) = struct.unpack_from("<I", data, 80)
    if len(data) != 84 + 50 * n:
        raise ValueError(f"{path.name} isn't a binary STL.")
    return [struct.unpack_from("<12f", data, 84 + 50 * i)[3:12] for i in range(n)]


def _weld(tris: list, name: str) -> tuple:
    """Share vertices, then prove the mesh is closed and consistently wound
    (every edge traversed exactly once in each direction), and that the
    winding faces outward (positive signed volume). Volume alone is not
    enough: one reversed triangle barely moves the total."""
    index, verts, faces = {}, [], []
    for t in tris:
        f = []
        for v in (t[0:3], t[3:6], t[6:9]):
            key = tuple(round(c, 4) for c in v)
            if key not in index:
                index[key] = len(verts)
                verts.append(key)
            f.append(index[key])
        if len(set(f)) == 3:
            faces.append(f)
    directed: dict = {}
    for a, b, c in faces:
        for e in ((a, b), (b, c), (c, a)):
            directed[e] = directed.get(e, 0) + 1
    if any(n != 1 for n in directed.values()):
        raise ValueError(f"{name} has an edge used twice in one direction: inconsistent winding "
                         f"or non-manifold.")
    if any((b, a) not in directed for a, b in directed):
        raise ValueError(f"{name} isn't a closed mesh after welding.")
    volume = 0.0
    for a, b, c in faces:
        (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = verts[a], verts[b], verts[c]
        volume += x0 * (y1 * z2 - z1 * y2) - y0 * (x1 * z2 - z1 * x2) + z0 * (x1 * y2 - y1 * x2)
    if volume <= 0:
        raise ValueError(f"{name}'s faces point inward.")
    return verts, faces


CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
    "</Types>"
)
RELS = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
    'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
    "</Relationships>"
)


def write_plate_3mf(out: pathlib.Path, filename: str = "plate.3mf") -> dict:
    """Arrange the STLs in columns centred on one plate, each a separate
    object so material and supports can be set per part in the slicer."""
    names = [n for col in PLATE_COLUMNS for n in col]
    meshes = {n: _weld(_read_binary_stl(out / f"{n}.stl"), n) for n in names}

    def extent(n: str) -> tuple:
        vs = meshes[n][0]
        return (max(v[0] for v in vs) - min(v[0] for v in vs), max(v[1] for v in vs) - min(v[1] for v in vs))

    widths = [max(extent(n)[0] for n in col) for col in PLATE_COLUMNS]
    depths = [sum(extent(n)[1] for n in col) + PLATE_GAP * (len(col) - 1) for col in PLATE_COLUMNS]
    total_w = sum(widths) + PLATE_GAP * (len(PLATE_COLUMNS) - 1)
    if total_w > PLATE_BED[0] - 2 * PLATE_GAP or max(depths) > PLATE_BED[1] - 2 * PLATE_GAP:
        raise ValueError(f"Parts need {total_w:.0f} x {max(depths):.0f}mm; the plate is {PLATE_BED[0]:.0f}mm.")

    placed, x = {}, (PLATE_BED[0] - total_w) / 2
    for col, w, d in zip(PLATE_COLUMNS, widths, depths):
        y = (PLATE_BED[1] - d) / 2
        for n in col:
            ed = extent(n)[1]
            placed[n] = (x + w / 2, y + ed / 2)
            y += ed + PLATE_GAP
        x += w + PLATE_GAP

    objects, items = [], []
    for i, n in enumerate(names, start=1):
        verts, faces = meshes[n]
        cx = placed[n][0] - (max(v[0] for v in verts) + min(v[0] for v in verts)) / 2
        cy = placed[n][1] - (max(v[1] for v in verts) + min(v[1] for v in verts)) / 2
        vx = "".join(f'<vertex x="{v[0] + cx:.4f}" y="{v[1] + cy:.4f}" z="{v[2]:.4f}"/>' for v in verts)
        tr = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in faces)
        label = f"{n} (face down)" if ORIENTATION.get(n) == "face_down" else n
        objects.append(f'<object id="{i}" name="{escape(label)}" type="model"><mesh>'
                       f"<vertices>{vx}</vertices><triangles>{tr}</triangles></mesh></object>")
        items.append(f'<item objectid="{i}"/>')
    model = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        f'<resources>{"".join(objects)}</resources><build>{"".join(items)}</build></model>'
    )
    with zipfile.ZipFile(out / filename, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("3D/3dmodel.model", model)
    return placed


def main() -> None:
    apply_print_tolerances()
    L, body, parts = m.build_all()

    # The same fit checks as the model, re-run at print tolerances. Nominal
    # and print must both pass.
    m.check(L, body, parts)

    for name in STAND_INS:
        parts.pop(name)
    to_print = {"body": body} | parts

    OUT.mkdir(exist_ok=True)
    print(f"{'part':16s} {'x':>7s} {'y':>7s} {'z':>6s} {'cm3':>6s}  solids")
    for name, shape in to_print.items():
        n = len(shape.solids().vals())
        if n != EXPECTED_SOLIDS.get(name, 1):
            raise ValueError(f"{name} is {n} solids; expected {EXPECTED_SOLIDS.get(name, 1)}.")
        flat = lay_flat(shape, ORIENTATION.get(name, ""))
        bb = flat.val().BoundingBox()
        if bb.xlen > BED_SIZE[0] or bb.ylen > BED_SIZE[1]:
            raise ValueError(f"{name} ({bb.xlen:.0f} x {bb.ylen:.0f}mm) doesn't fit a {BED_SIZE[0]:.0f}mm bed.")
        cq.exporters.export(flat, str(OUT / f"{name}.stl"), tolerance=0.02, angularTolerance=0.1)
        print(f"{name:16s} {bb.xlen:7.1f} {bb.ylen:7.1f} {bb.zlen:6.1f} {flat.val().Volume() / 1000:6.2f}  {n}")
    print(f"Wrote {len(to_print)} STLs to {OUT}")

    placed = write_plate_3mf(OUT)
    print(f"Wrote {OUT / 'plate.3mf'} ({len(placed)} parts on a {PLATE_BED[0]:.0f}mm plate)")


if __name__ == "__main__":
    main()
