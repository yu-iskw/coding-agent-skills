---
name: change-risk-assessment
description: Assesses the blast radius and operational risk of a proposed or completed code change by tracing interfaces, data and control flows, compatibility boundaries, security implications, rollback paths, and validation gaps. Use before high-impact implementation, during review, or when deciding how much testing and rollout protection a change needs.
license: Apache-2.0
compatibility: Works in Agent Skills hosts that can inspect repository files, diffs, tests, and configuration.
metadata:
  maturity: stable
  risk: R0
  category: review
  network: "false"
  side-effects: none
---

# Change Risk Assessment

## Purpose

Estimate engineering and operational risk from repository evidence so implementation, testing, review, and rollout effort match the actual blast radius.

## Workflow

1. **Define the change boundary** from the request, plan, or diff.
2. **Trace affected contracts** including public APIs, schemas, configuration, events, persistence, CLI behavior, and shared utilities.
3. **Identify consumers and coupling** across packages, services, tests, deployment artifacts, and external integrations visible in the repository.
4. **Evaluate risk dimensions**: correctness, backward compatibility, data integrity, security/privacy, performance, operability, and reversibility.
5. **Inspect safeguards** such as tests, feature flags, migrations, validation, observability, rollback, and staged rollout mechanisms.
6. **Classify risk** as low, medium, high, or critical and explain the evidence behind the classification.
7. **Recommend proportionate controls** rather than generic process.

## Required behavior

- Tie every material risk to an affected contract, path, or missing safeguard.
- Distinguish likelihood from impact.
- Treat data/schema migrations and irreversible external effects as higher-risk unless proven otherwise.
- Include rollback/reversibility analysis for medium-or-higher risk changes.
- Identify the smallest additional evidence that could materially lower uncertainty.

## Do not

- Inflate risk because a diff is large when changes are mechanical and isolated.
- Understate risk because a diff is small when it changes shared contracts or production state.
- Invent consumers or infrastructure not evidenced by the repository.
- Modify files while performing assessment.

## Success criteria

Reviewers receive an evidence-backed risk level, the dominant failure modes, missing safeguards, and a proportionate validation/rollout recommendation.
