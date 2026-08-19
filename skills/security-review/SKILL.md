---
name: security-review
description: Performs a repository-scoped security review of a change or component by identifying trust boundaries, attacker-controlled inputs, authorization and secret handling, dangerous execution paths, dependency exposure, and realistic abuse cases. Use for security-sensitive changes, pre-release review, or focused investigation of a suspected weakness.
license: Apache-2.0
compatibility: Works in Agent Skills hosts with repository read access; optional local security tools require command execution.
metadata:
  maturity: beta
  risk: R2
  category: secure
  network: "false"
  side-effects: local-execution
---

# Security Review

## Purpose

Produce high-signal security findings grounded in reachable code paths and explicit trust boundaries.

## Workflow

1. Define assets, entry points, identities, trust boundaries, and attacker-controlled inputs relevant to the requested scope.
2. Inspect authentication, authorization, validation, serialization, command/process execution, filesystem access, network calls, secret handling, and dependency boundaries.
3. Trace realistic abuse paths from attacker influence to security impact.
4. Inspect existing mitigations and tests before declaring a finding.
5. Use repository-native static/security tooling when available and proportionate.
6. Rank findings by exploitability and impact; separate confirmed defects from defense-in-depth suggestions.
7. Recommend the smallest remediation and a regression test or verification method.

## Required behavior

- Include a concrete threat/abuse scenario for each vulnerability finding.
- Distinguish confidentiality, integrity, availability, and privilege impacts.
- Treat generated scanner output as evidence to investigate, not automatically as a vulnerability.
- Call out secret exposure or unsafe external execution immediately.
- Keep analysis within the requested/repository-visible scope.

## Do not

- Exfiltrate, print, or copy real credentials while reviewing.
- Run destructive exploitation against external systems.
- Inflate severity without a reachable threat path.
- Hide a security failure by disabling validation or policy.

## Success criteria

Findings are reproducible or plausibly reachable, prioritized by security impact, and paired with practical remediation/verification steps.
