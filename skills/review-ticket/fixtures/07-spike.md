## Decision Needed

Whether to keep the current message queue or move to a managed one.

## Why

The current queue drops a message roughly once a week under load and nobody
knows whether the fix is a configuration change or a different system. Two
features are waiting on the answer and both are being designed around a guess.

## Scope

**In:** measuring the current behaviour under a reproducible load, and
evaluating alternatives on paper plus a throwaway load test.

**Out:** implementing any option, migrating data, and changing production
configuration.

## Expected Deliverable

An ADR recommending one option, with the measured drop rate and the cause (or
an explicit statement that the cause was not identified) behind it, and a
follow-up implementation ticket filed for whichever option wins.

## Decision Criteria

Ordered: message durability under load, operational burden, cost at projected
volume, and how far it moves the existing consumer code.

## Risk

`Medium`. Getting the recommendation wrong costs a migration later, but the
spike itself changes nothing in production.

## Follow-up

The implementation ticket for whichever option wins.
