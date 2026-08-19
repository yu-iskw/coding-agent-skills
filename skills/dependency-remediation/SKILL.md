---
name: dependency-remediation
description: Remediates a known vulnerable or broken dependency with the smallest supported dependency-file change, using the repository's native package manager and existing lockfile policy. Use when a dependency advisory, audit result, broken transitive dependency, or explicitly identified package version requires a targeted fix rather than a general upgrade campaign.
license: Apache-2.0
compatibility: Works in Agent Skills hosts with repository access, local command execution, and package-registry network access for the detected package manager.
metadata:
  maturity: beta
  risk: R3
  category: maintain
  network: "true"
  side-effects: repository-write-and-local-execution
---

# Dependency Remediation

## Purpose

Resolve a concrete dependency problem conservatively without turning remediation into an unrelated dependency refresh.

## Workflow

1. Detect package managers and authoritative manifest/lock files from repository evidence.
2. Identify the affected direct or transitive dependency, vulnerable range, fixed range, and relevant ecosystem constraints from the supplied advisory/audit evidence.
3. Choose the narrowest native remediation mechanism supported by the package manager.
4. Preserve declared versioning policy, lockfile format, workspace boundaries, and existing package-manager configuration.
5. Apply only dependency-file changes needed for remediation.
6. Run the narrow dependency audit/resolution check and repository-native validation relevant to the affected package.
7. Summarize changed dependency edges, remaining advisories, and compatibility risk.

## Required behavior

- Detect the package manager rather than assuming one.
- Prefer patched versions within existing compatibility constraints.
- Explain any major-version or broad transitive movement before applying it.
- Keep manifest and lockfile changes consistent.
- Distinguish unresolved advisories from accepted/not-applicable findings.

## Do not

- Run broad upgrade-all commands for a targeted advisory.
- Disable audit tooling or suppress an advisory without documented justification.
- Delete/recreate lockfiles merely to make resolution easier.
- Change unrelated dependencies opportunistically.
- Commit credentials or registry tokens.

## Success criteria

The targeted dependency issue is resolved or narrowly bounded, dependency files remain consistent, and relevant validation passes without unrelated upgrades.
