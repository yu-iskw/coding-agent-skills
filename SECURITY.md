# Security Policy

## Reporting a vulnerability

Please do not disclose suspected vulnerabilities, malicious skill behavior, credential exposure, or supply-chain issues in a public issue before maintainers have had a chance to investigate.

Use GitHub's private vulnerability reporting / Security Advisory flow for this repository when available. Include:

- the affected skill, script, workflow, or commit;
- a minimal reproduction or proof of concept;
- the capability or data at risk;
- whether exploitation requires user approval, network access, credentials, or external systems;
- any suggested mitigation.

If private vulnerability reporting is unavailable, open a public issue that contains only non-sensitive coordination details and explicitly request a private follow-up. Do not post secrets, exploit payloads, private repository data, or credentials.

## Scope

Security reports may include traditional code vulnerabilities as well as agent-specific risks such as:

- prompt injection embedded in skills or bundled resources;
- unexpected network access or data exfiltration;
- credential or sensitive-file access;
- unsafe shell execution or remote-code bootstrap patterns;
- privilege escalation beyond the declared skill risk level;
- provenance, dependency, or marketplace supply-chain compromise.

## Security model

Skill metadata is descriptive evidence, not an authorization boundary. Agent hosts and users remain responsible for enforcing sandboxing, approvals, credentials, and network policies. See `policies/risk-levels.md` for the repository's capability-risk taxonomy.
