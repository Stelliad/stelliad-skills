---
name: design-printed-part
description: Design a parametric CadQuery part or enclosure meant to be FDM printed, and hand over print-ready output. The model proves its own fit by measured interference before any filament is spent, and the print differs from it only where printing demands.
license: MIT
compatibility: Requires Python 3.11+, uv and CadQuery 2.8+. Printer, materials, tolerances and directory layout adapt via CUSTOMIZE.md.
metadata:
  version: "1.0"
  author: Sanvio Labs, Agentience
  source: https://github.com/Stelliad/stelliad-skills
type: skill
scope: all
status: active
---

# design-printed-part

Parametric CAD for parts that come off an FDM printer, written so the model
proves its own fit before any filament is spent.

This is a design skill, not a printer driver. It does not slice, send jobs or
talk to a printer. Its output is a CadQuery model, print-ready STLs, a plate
3MF, and the slicer settings the 3MF cannot carry.

## Quick start

1. [Read SPEC.md](./SPEC.md) for the procedure, the rules and what it will not do
2. [Follow CUSTOMIZE.md](./CUSTOMIZE.md) to bind your printer, materials and layout
3. Copy [assets/model_template.py](./assets/model_template.py) and
   [assets/print_template.py](./assets/print_template.py) and rename them

## Trigger phrases

- "design an enclosure for X" / "model a case for this board"
- "make this printable" / "print-ready STLs" / "put it on one plate"
- "add a snap fit" / "make the lid clip on"
- "print a fit coupon" / "a gauge for the clip"
- "why did this print badly" / "the walls have gaps"

## What to read

| File | When |
|---|---|
| [references/fdm-rules.md](./references/fdm-rules.md) | Before drawing anything. Tolerances, walls, holes, orientation, snap fits, materials |
| [references/check-patterns.md](./references/check-patterns.md) | Before writing `check()`. How to make a fit check that can actually fail |
| [references/measured.md](./references/measured.md) | Before choosing a tolerance. What real prints measured, which beats any default |
| [assets/model_template.py](./assets/model_template.py) | Starting a part: constants, `layout()`, `build_*()`, `check()`. Runs as is |
| [assets/print_template.py](./assets/print_template.py) | Starting the print pipeline: tolerance override, lay flat, STL, plate 3MF |

## Before you rely on it

Read the Limitations section in [SPEC.md](./SPEC.md). The short version: a model
that passes every check has still never been printed, and this skill will not
say otherwise.

---

See [CUSTOMIZE.md](./CUSTOMIZE.md) to adapt this skill for your organization.
