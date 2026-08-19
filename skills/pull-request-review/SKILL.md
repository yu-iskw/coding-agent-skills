---
name: pull-request-review
description: Reviews a pull request or local diff for correctness, regressions, security issues, broken contracts, missing tests, and maintainability risks while prioritizing actionable findings over stylistic noise. Use when asked to review code changes, validate a PR before merge, or perform an adversarial second pass on an implementation.
license: Apache-2.0
compatibility: Works in Agent Skills hosts that can inspect repository files and a diff or pull-request patch.
metadata:
  maturity: stable
  risk: R0
  category: review
  network: "false"
  side-effects: none
---

# Pull Request Review

## Purpose

Find defects that materially affect users, operators, security, data, or future maintenance. Optimize for signal, evidence, and precise remediation rather than comment volume.

## Workflow

1. **Understand intent** from the request, issue, PR description, and relevant repository guidance.
2. **Read the diff in context**, opening surrounding implementation, tests, schemas, and configuration rather than reviewing patch fragments in isolation.
3. **Trace changed behavior** through callers, shared contracts, persistence, error paths, authorization boundaries, and compatibility surfaces.
4. **Challenge assumptions** with adversarial examples, edge cases, partial failures, concurrency, invalid input, and rollback behavior where relevant.
5. **Inspect validation coverage** and identify material behavior that changed without corresponding tests or checks.
6. **Rank findings** by impact and confidence. Prefer a few high-confidence findings to speculative style feedback.
7. **Summarize residual risk** when no blocking finding exists.

## Required behavior

- Provide a concrete failure scenario for each defect finding.
- Point to the affected code/path and explain why existing validation does not prevent the failure.
- Separate blocking defects, non-blocking risks, and optional improvements.
- Check backward compatibility when public interfaces or persisted formats change.
- Avoid duplicating automated lint/format feedback unless it reveals a semantic issue.

## Do not

- Approve based solely on passing CI.
- Request broad refactoring unrelated to the change.
- Treat personal style preference as a defect.
- Modify repository files during a review-only request.
- Claim a vulnerability without a plausible attack or failure path.

## Success criteria

The review surfaces actionable, evidence-backed defects and risks in priority order, or explicitly states that no material findings were found while noting residual uncertainty.
