# Skill capability and risk levels

Risk metadata gives humans and agent hosts a fast, host-neutral summary of the maximum capability a skill normally needs. It is classification evidence, not an authorization mechanism.

| Level  | Capability boundary                                                 | Examples                                                           |
| ------ | ------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **R0** | Read/reason only                                                    | repository discovery, planning, review                             |
| **R1** | Repository writes                                                   | documentation edits, source changes without command execution      |
| **R2** | Local command execution                                             | tests, builds, package-manager remediation, local scanners         |
| **R3** | Network or external systems                                         | remote agent delegation, API calls, fetching remote state          |
| **R4** | Credentials, deployment, destructive or high-impact external writes | production deploys, secret rotation, irreversible remote mutations |

## Required metadata

New canonical outcome and orchestration skills under `skills/` declare these string-valued metadata fields directly in `SKILL.md`:

```yaml
metadata:
  maturity: stable
  risk: R0
  category: review
  network: "false"
  side-effects: none
```

`maturity` is one of `experimental`, `beta`, or `stable`. `network` describes whether the skill normally requires network access. `side-effects` is a short human-readable summary, for example `none`, `repository-write`, `local-execution`, or `external-agent`.

Legacy vendor-specific delegation adapters are intentionally treated as compatibility shims. Their project-level risk contracts live in `policies/skill-contracts.json` so frequently changing vendor documentation does not need to be rewritten merely to update repository governance metadata. Generated catalog surfaces merge those sidecar contracts with skill frontmatter.

## Rules

1. Classify the normal maximum capability, not the most dangerous action an agent could theoretically invent.
2. Escalation beyond the declared level requires explicit host/user approval and must not be hidden inside a workflow.
3. A skill should prefer the lowest capability that can achieve the task.
4. Vendor-specific permission modes belong in integration adapters; canonical outcome skills remain host-neutral.
5. Behavioral evaluation and static security scanning complement this metadata but do not turn it into a security boundary.
6. Sidecar contract overrides are reserved for legacy integration adapters; new outcome skills must carry native frontmatter metadata.
