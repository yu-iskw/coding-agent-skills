# Recipe: Issue to pull request

Recipes describe composition intent; they are not a workflow runtime. Let the active agent host decide how to sequence or delegate work.

## Flow

`repository-discovery` → `issue-to-implementation-plan` → `change-risk-assessment` → implementation by the active host → `test-gap-analysis` → `pull-request-review`

## Gates

1. Discovery must identify repository guidance and validation commands before planning.
2. The plan must have acceptance criteria, non-goals, dependency order, and validation.
3. Medium-or-higher change risk adds explicit rollback/compatibility controls to the plan.
4. Implementation must stay inside approved scope; do not silently expand into cleanup/refactoring.
5. Test-gap analysis runs against the actual diff, not only the original plan.
6. PR review is an independent adversarial pass and may send work back to implementation.

## Optional delegation

Use one of the `*-cli` integration skills only when the user/host explicitly wants another coding agent. The recipe itself is host-neutral.
