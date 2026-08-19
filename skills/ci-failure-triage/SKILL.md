---
name: ci-failure-triage
description: Diagnoses failing continuous-integration jobs by isolating the first actionable failure, reproducing it with repository-native commands when safe, and proposing or applying the smallest evidence-backed fix. Use when CI is red, checks fail after a change, or multiple downstream failures obscure the root cause.
license: Apache-2.0
compatibility: Works in Agent Skills hosts with repository read access; local reproduction requires command execution.
metadata:
  maturity: stable
  risk: R2
  category: validate
  network: "false"
  side-effects: local-execution
---

# CI Failure Triage

## Purpose

Turn a failing CI run into a root-cause hypothesis and the smallest validated remediation without unrelated cleanup.

## Workflow

1. **Inventory failing checks** and identify which failures are primary versus likely downstream/cancelled noise.
2. **Read the failing workflow/configuration** and determine the exact command, environment, matrix entry, or prerequisite that failed.
3. **Inspect the first actionable error** rather than starting from the final cascade of failures.
4. **Correlate with the change** using the diff and nearby code/configuration. Do not assume the current change caused a pre-existing failure.
5. **Reproduce narrowly** with the repository-native command when the environment permits it. Prefer a single test/lint/build target before running the whole suite.
6. **Fix minimally** only when evidence is strong enough; otherwise report the likely root cause and the missing evidence.
7. **Re-run the narrow reproduction**, then the broader relevant validation if necessary.

## Required behavior

- Identify the specific failing job/step/command before editing.
- Preserve CI semantics unless the workflow itself is the demonstrated defect.
- Separate primary failures from cascaded failures.
- State what was reproduced locally and what was only observed remotely.
- Keep fixes scoped to the failure.

## Do not

- Disable or skip a failing test merely to make CI green.
- Remove required security, lint, type, or test checks without explicit justification.
- Rewrite unrelated code while triaging.
- Claim a fix is validated when the failing command could not be reproduced or rerun.

## Success criteria

The root cause is identified with evidence, the minimal remediation is applied or clearly proposed, and the relevant validation command passes or the remaining limitation is explicit.
