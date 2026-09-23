## Objective

Users receive a notification when an invoice becomes overdue.

## Why

Overdue invoices are currently only visible if someone opens the dashboard, and
nobody does. Collections are slipping because of it.

## Acceptance Criteria

- [ ] An invoice crossing its due date generates one notification
- [ ] A notification is sent once and not repeated daily
- [ ] Delivery failure is recorded and visible

## Scope

**In:** overdue detection and the notification send.
**Out:** the notification's copy, in-app notifications, and reminders before
the due date.

## Risk

`Medium`

## Dependencies

Depends on #999

## Assumptions

None recorded. The repo has no email, SMS, or push provider today, so the
delivery channel is undecided.
