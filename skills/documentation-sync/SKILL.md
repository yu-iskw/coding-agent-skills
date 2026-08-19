---
name: documentation-sync
description: Synchronizes repository documentation with verified code, configuration, CLI, API, or workflow behavior by finding stale claims and making narrowly scoped documentation updates. Use after behavior changes, when README/reference docs disagree with implementation, or before release when user-facing documentation must match the repository.
license: Apache-2.0
compatibility: Works in Agent Skills hosts that can read and edit repository documentation and implementation files.
metadata:
  maturity: beta
  risk: R1
  category: maintain
  network: "false"
  side-effects: repository-write
---

# Documentation Sync

## Purpose

Keep documentation truthful to current repository behavior without broad copy-editing or speculative documentation redesign.

## Workflow

1. Identify the changed behavior or documentation claim that needs synchronization.
2. Verify behavior from source code, configuration, generated interfaces, tests, or repository-native command help.
3. Search for duplicate/stale references across README, docs, examples, comments, templates, and release guidance.
4. Update only claims affected by verified behavior.
5. Preserve repository terminology and documentation structure unless it is itself the problem.
6. Validate links, command examples, generated markers, and formatting with repository-native checks.
7. Report what source evidence was used for each material documentation change.

## Required behavior

- Treat implementation/configuration as evidence, not assumptions.
- Keep examples executable or clearly illustrative.
- Update all materially inconsistent user-facing references found in scope.
- Preserve generated sections and use their generator when one exists.
- Separate factual synchronization from optional editorial improvements.

## Do not

- Invent unsupported features or options.
- Rewrite unrelated prose during a synchronization task.
- Hand-edit generated documentation when a repository generator exists.
- Change implementation merely to make stale documentation true unless explicitly requested.

## Success criteria

Documentation in scope accurately reflects verified repository behavior, examples and links remain valid, and unrelated content is left unchanged.
