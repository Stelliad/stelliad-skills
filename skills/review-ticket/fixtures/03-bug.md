## Summary

The customer list overflows horizontally on a phone, so the rightmost column
and the row actions are unreachable.

## Impact

Every mobile user of the customer list. It has been reported by two people this
week and there is no workaround short of rotating to landscape.

## Current Behavior

At viewport widths below 420px the table extends past the viewport. The page
body scrolls horizontally and the sticky header detaches from the rows.

## Expected Behavior

The table scrolls inside its own container. The page body never scrolls
horizontally and the header stays aligned to the rows.

## Reproduction

1. Open the customer list on a 390px viewport
2. Scroll right
3. Observe the header separating from the rows and the page itself panning

## Acceptance Criteria

- [ ] At 390px the page body does not scroll horizontally
- [ ] The table scrolls within its own container at 390px
- [ ] The header row stays aligned with the body rows while scrolling
- [ ] The row action control is reachable at 390px
- [ ] A regression test covers the 390px layout

## Scope

**In:** the customer list table on viewports under 768px.
**Out:** the desktop layout, the table's column set, and every other table in
the app.

## Risk

`Low`. Presentation only, contained to one component, revert is a single commit.

## Evidence

Reported 2026-08-24 and 2026-08-25. Screenshots attached.
