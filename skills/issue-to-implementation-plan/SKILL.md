---
name: issue-to-implementation-plan
description: Converts a concrete issue or feature request into a repository-informed implementation plan with scope, affected contracts, staged tasks, acceptance criteria, validation, dependencies, and explicit non-goals. Use when work is understood well enough to plan but should not yet be implemented, especially before delegating tasks to one or more coding agents.
license: Apache-2.0
compatibility: Works in Agent Skills hosts that can inspect repository files and the supplied issue or requirements.
metadata:
  maturity: stable
  risk: R0
  category: plan
  network: "false"
  side-effects: none
---

# Issue to Implementation Plan

## Purpose

Produce an implementation-ready plan grounded in the actual repository, avoiding both vague task lists and premature code changes.

## Workflow

1. Restate the requested user outcome, constraints, acceptance criteria, and non-goals from the issue.
2. Discover the relevant repository architecture, conventions, existing abstractions, and validation commands.
3. Identify affected interfaces, data/configuration, tests, documentation, deployment/release behavior, and compatibility requirements.
4. Challenge whether the proposed mechanism is the smallest path to the desired outcome; record a better path when repository evidence supports it.
5. Decompose work into ordered, independently verifiable tasks. Separate prerequisites/shared-interface changes from parallelizable leaves.
6. Define acceptance criteria and validation for each task, including negative/edge cases where material.
7. Record risks, rollout/rollback needs, unknowns, and explicitly excluded scope.

## Required behavior

- Reference concrete repository paths and existing patterns.
- Keep tasks outcome-oriented rather than splitting blindly by frontend/backend/file type.
- Identify dependency ordering and safe parallelism.
- Include tests/validation in the plan rather than as a final generic step.
- Distinguish facts, assumptions, and unresolved questions.

## Do not

- Modify repository files during planning-only work.
- Produce pseudo-code when architecture and acceptance criteria are sufficient.
- Expand scope with unrelated refactors.
- Assume a requested implementation mechanism is optimal when repository evidence suggests a simpler route.

## Success criteria

A coding agent can pick up the plan and implement it with minimal rediscovery, while reviewers can evaluate scope, risk, acceptance criteria, and validation before code is written.
