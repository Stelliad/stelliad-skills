## Objective

The log archive account's bucket cannot have its objects deleted or overwritten
before their retention expires, including by an account administrator.

## Why

Our account layout puts CloudTrail and security logs in a separate account,
and a separate account is not immutability. Without Object Lock the audit trail
is deletable by whoever compromises the account, which is the case the archive
exists for.

## Acceptance Criteria

- [ ] The log archive bucket has Object Lock enabled in compliance mode
- [ ] A default retention period is set and declared in Terraform
- [ ] An attempt to delete an object inside the retention window fails
- [ ] An attempt to overwrite an object inside the retention window fails
- [ ] CloudTrail continues writing to the bucket after the change
- [ ] The change is applied by the pipeline, not by hand, and `terraform plan` is clean afterwards

## Scope

**In:** the log archive bucket in the security OU.
**Out:** application buckets, the retention policy's duration (a separate
decision), and CloudTrail's own configuration.

## Risk

`Critical`. Object Lock in compliance mode is irreversible: the bucket cannot
be un-locked and objects cannot be deleted before expiry by anyone, including
the account root.

## Human Approval

The Terraform apply. Prepare the plan and the PR; a human runs the pipeline
after reading the plan, because this cannot be rolled back.

## Verification

- `aws s3api get-object-lock-configuration` shows compliance mode
- A delete inside the window returns AccessDenied
- CloudTrail delivers a new file after the change

## Dependencies

Depends on the log archive account existing in the Organization.
