# Contributing

Contributions should improve reliable engineering outcomes rather than maximize the number of prompts or agent integrations in the repository.

## Before proposing a skill

A canonical outcome skill should:

- solve a recurring engineering outcome that is not already covered by a more general skill;
- remain host-neutral and use standard `SKILL.md` packaging;
- have a routing description specific enough to distinguish when it should and should not activate;
- declare maturity, R0-R4 risk, category, network requirement, and side effects in frontmatter metadata;
- use the lowest capability needed for its normal workflow;
- include at least two positive and two negative routing fixtures plus required/prohibited behavior assertions in `evals/manifest.json`;
- pass static supply-chain/security checks;
- avoid embedding volatile vendor/model details unless the skill is explicitly an integration adapter.

Vendor-specific delegation adapters are intentionally a small compatibility surface. New adapters need evidence that the target agent provides distinct user value beyond generic Agent Skills installation/discovery.

## Local validation

```bash
make validate
make contracts
make security
make catalog
make security-report
make check
```

Generated files under `catalog/`, `llms.txt`, and `docs/compatibility.md` must be regenerated when canonical skill metadata changes.

## Behavioral evidence

Behavioral observations are welcome, but must identify the evaluated repository/fixture, skill commit, agent host/version, and model/version. Results are evidence for that environment, not certification. See `evals/README.md`.

## Security

Do not add remote bootstrap patterns, credential harvesting, hidden network uploads, destructive commands, or privilege escalation. Security-sensitive reports should follow `SECURITY.md` rather than public contribution discussion.

## Pull requests

Keep skill changes reviewable. Explain the user outcome, routing boundaries, capability level, evaluation fixtures, security impact, compatibility impact, and generated-file updates. Existing repository CI must remain green.
