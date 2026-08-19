# Recipe: Library upgrade and migration

## Flow

`repository-discovery` → `migration-planning` → implementation by the active host → `test-gap-analysis` → `documentation-sync` → `release-readiness`

## Gates

1. Inventory current library usage, wrappers, generated artifacts, public APIs, and version constraints.
2. Plan compatibility stages when the upgrade is breaking or spans multiple consumers.
3. Prefer adapter/interface-first migration when old and new versions must coexist temporarily.
4. Validate changed behavior at the narrowest reliable test layer, then run repository-required checks.
5. Synchronize user/operator migration docs from verified implementation behavior.
6. Do not release until temporary compatibility assumptions and rollback conditions are explicit.
