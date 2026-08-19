# Recipe: Dependency advisory to remediation

## Flow

`repository-discovery` (dependency boundaries only) → `dependency-remediation` → targeted audit/tests → `change-risk-assessment` when resolution crosses major versions or moves broad transitive graphs → `pull-request-review`

## Gates

1. Confirm the affected package, vulnerable/fixed range, package manager, and authoritative lockfile.
2. Prefer the narrowest native remediation; no upgrade-all behavior.
3. Review manifest/lockfile diff for unrelated movement.
4. Run the relevant audit/resolution command and repository validation.
5. Escalate for explicit review when remediation requires a major version, registry/source change, or broad dependency churn.
