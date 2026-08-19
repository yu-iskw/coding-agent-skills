---
name: migration-planning
description: Designs a safe, reversible migration plan for APIs, schemas, dependencies, infrastructure, or application architecture by inventorying current consumers, compatibility constraints, sequencing, rollout, rollback, and validation. Use when a change cannot be safely completed as a single atomic edit or must preserve compatibility during transition.
license: Apache-2.0
compatibility: Works in Agent Skills hosts that can inspect repository code, configuration, schemas, and tests.
metadata:
  maturity: stable
  risk: R0
  category: plan
  network: "false"
  side-effects: none
---

# Migration Planning

## Purpose

Turn a risky one-step replacement into a staged migration with explicit compatibility, validation, and rollback boundaries.

## Workflow

1. Define source and target states and the reason for migration.
2. Inventory consumers, persisted data, schemas, public interfaces, deployment units, and operational dependencies visible in the repository.
3. Identify incompatibilities and determine whether expand/contract, dual-read/write, adapters, feature flags, backfills, or versioned interfaces are needed.
4. Break the migration into independently verifiable stages with explicit entry/exit criteria.
5. Define rollback for each stage and identify irreversible points.
6. Define validation: tests, data checks, compatibility checks, observability, and rollout signals.
7. Document cleanup criteria so temporary compatibility code is removed after migration completes.

## Required behavior

- Preserve compatibility until all identified consumers can move or explicitly document a breaking-change boundary.
- Separate schema/data migration from application cutover when their rollback properties differ.
- Identify irreversible operations and backup/recovery requirements.
- Minimize periods of dual behavior and define how temporary state ends.
- State assumptions and unknown consumers explicitly.

## Do not

- Treat a destructive schema change as an atomic deploy without evidence that it is safe.
- Assume all consumers deploy simultaneously.
- Omit rollback because the target state is considered better.
- Modify files while the task is planning-only.

## Success criteria

The migration can be executed as a sequence of bounded steps with known dependencies, validation, rollback, and cleanup conditions.
