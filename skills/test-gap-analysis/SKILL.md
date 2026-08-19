---
name: test-gap-analysis
description: Identifies material behavior and failure modes that are insufficiently tested by mapping changed or critical code paths to existing test coverage and validation layers. Use before merging meaningful changes, after a regression, or when deciding which tests provide the highest confidence instead of maximizing test count.
license: Apache-2.0
compatibility: Works in Agent Skills hosts with repository read access; running tests or coverage tools requires local command execution.
metadata:
  maturity: beta
  risk: R2
  category: validate
  network: "false"
  side-effects: local-execution
---

# Test Gap Analysis

## Purpose

Find missing tests that materially reduce confidence, emphasizing behavior and risk rather than raw coverage percentages.

## Workflow

1. Identify the changed or critical behavior, contracts, branches, error paths, and state transitions.
2. Locate existing unit, integration, end-to-end, contract, migration, and static validation that exercise those behaviors.
3. Map important behaviors to evidence and identify untested or weakly asserted paths.
4. Prioritize gaps by failure impact, likelihood, regression history, and difficulty of detecting failures elsewhere.
5. Recommend the smallest test level that validates the behavior reliably.
6. Run targeted existing tests/coverage commands when useful and available.
7. Report high-value gaps separately from optional coverage improvements.

## Required behavior

- Tie each proposed test to a concrete behavior or failure mode.
- Prefer observable outcomes over implementation-detail assertions.
- Recognize when type checks, schema validation, or contract tests already cover a risk.
- Call out flaky or non-deterministic test dependencies when relevant.
- Avoid treating line coverage as a sufficient quality measure.

## Do not

- Recommend tests solely to increase a percentage.
- Duplicate existing equivalent coverage.
- Overfit tests to private implementation details without a regression reason.
- Modify production behavior during an analysis-only request.

## Success criteria

The report identifies the few missing tests that most improve confidence and explains why each one matters and at what test layer it belongs.
