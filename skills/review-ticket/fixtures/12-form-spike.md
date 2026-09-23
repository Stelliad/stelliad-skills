### Decision needed

Whether to keep the current message queue or move to a managed one.

### Why we need the answer

The current queue drops a message roughly once a week under load and nobody
knows whether the fix is configuration or a different system. Two features are
being designed around a guess.

### Research scope

**In:** measuring current behaviour and evaluating alternatives on paper plus a
throwaway load test.

**Out:** implementing any option and changing production configuration.

### Expected deliverable

An ADR recommending one option, with the measured drop rate behind it.

### Decision criteria

Ordered: durability under load, operational burden, cost at projected volume,
and how far it moves the existing consumer code.

### Effort limit

2 days

### Risk of getting this wrong

Medium

### Why this risk level

_No response_
