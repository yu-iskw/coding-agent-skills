# Recipe: Failing CI to validated fix

## Flow

`ci-failure-triage` → implementation by the active host → targeted validation → `change-risk-assessment` when CI/workflow semantics changed → `pull-request-review`

## Gates

1. Identify the first actionable failure and exact failing command before editing.
2. Reproduce narrowly when possible; record environmental limitations when not possible.
3. Apply the smallest root-cause fix. Do not disable or weaken required checks.
4. Re-run the narrow failure, then broader relevant validation.
5. If the fix changes CI configuration, permissions, caching, matrix semantics, or release behavior, assess change risk before merge.
