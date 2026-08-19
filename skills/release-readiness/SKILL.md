---
name: release-readiness
description: Evaluates whether a repository change or release candidate is ready to ship by checking required validation, compatibility, migrations, security, documentation, packaging, rollback, and release automation. Use before a release, tag, deployment handoff, or merge that is intended to become a release candidate.
license: Apache-2.0
compatibility: Works in Agent Skills hosts with repository access; executing validation/build/package commands requires local command execution.
metadata:
  maturity: beta
  risk: R2
  category: operate
  network: "false"
  side-effects: local-execution
---

# Release Readiness

## Purpose

Provide a release go/no-go assessment based on repository evidence rather than a generic checklist.

## Workflow

1. Identify the repository's release mechanism, required checks, versioning, packaging, changelog/release-note conventions, and deployment artifacts.
2. Review changes since the relevant baseline for compatibility, migration, security, and operational risk.
3. Run or inspect required tests, type/lint checks, builds, package validation, and release-specific checks that are safe locally.
4. Verify required documentation, migration instructions, configuration changes, and breaking-change communication.
5. Confirm rollback/recovery expectations and any irreversible migration gates.
6. Classify blockers, warnings, and informational release notes.
7. Give an explicit go/no-go/conditional-go recommendation with evidence.

## Required behavior

- Derive release criteria from repository configuration before adding generic criteria.
- Treat failing required checks as blockers unless explicitly waived by project policy.
- Surface breaking changes and migration requirements prominently.
- Distinguish locally validated evidence from CI/production evidence not available to the agent.
- Avoid creating tags or deployments unless separately authorized.

## Do not

- Declare readiness solely because tests pass.
- Ignore packaging, schema, configuration, or documentation changes relevant to users/operators.
- Bypass required checks to produce a green result.
- Perform external release/deployment writes during assessment.

## Success criteria

Maintainers receive a concise evidence-backed readiness decision, blockers and warnings, and the exact remaining actions needed before release.
