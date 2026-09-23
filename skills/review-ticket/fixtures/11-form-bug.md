### Summary

The customer list overflows horizontally on a phone, so the rightmost column
and the row actions are unreachable.

### Impact

Every mobile user of the customer list. Reported twice this week with no
workaround short of rotating to landscape.

### Current behaviour

At viewport widths below 420px the table extends past the viewport and the
sticky header detaches from the rows.

### Expected behaviour

The table scrolls inside its own container and the page body never scrolls
horizontally.

### Reproduction

1. Open the customer list on a 390px viewport
2. Scroll right
3. Observe the header separating from the rows

### Acceptance criteria

- [ ] At 390px the page body does not scroll horizontally
- [ ] The table scrolls within its own container at 390px
- [ ] The header row stays aligned with the body rows while scrolling
- [ ] A regression test covers the 390px layout

### Risk of the fix

Low

### Why this risk level

_No response_

### Evidence and suspected scope

Screenshots attached from 2026-08-24 and 2026-08-25.
