## Objective

Date handling in the invoice module goes through one utility instead of four
divergent local implementations, with no change to any produced invoice.

## Why

Four call sites parse and format dates independently and two of them disagree
about timezone handling, which is why the same invoice renders a different due
date in the PDF than in the API response. Every new invoice feature has to pick
one of the four and gets it wrong roughly half the time.

## Acceptance Criteria

- [ ] All four call sites use a single date utility
- [ ] The PDF due date and the API due date match for an invoice created at 23:30 UTC
- [ ] Existing invoice output is byte-identical for the golden fixture set
- [ ] The three superseded local implementations are removed
- [ ] The utility has tests covering the timezone boundary case

## Scope

**In:** date parsing and formatting inside the invoice module.
**Out:** date handling elsewhere in the app, the invoice PDF layout, and the
API response schema.

## Risk

`Medium`. Touches invoice output, which customers see, but the golden fixture
set makes a regression visible and the revert is one commit.

## Verification

- The golden fixture set produces byte-identical output before and after
- An invoice created at 23:30 UTC shows the same due date in both surfaces
