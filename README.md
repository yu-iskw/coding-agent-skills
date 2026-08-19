# Coding Agent Skills — Verified Engineering Skills for Agent-Ready Repositories

**Coding Agent Skills** is a curated, cross-agent engineering skillpack built on portable `SKILL.md` packages.

The project focuses on a problem that remains important even as coding agents become more capable: **how to make repeatable engineering workflows discoverable, reviewable, least-privileged, and backed by evidence instead of relying on one-off prompts.**

The canonical product is the skill library under `skills/`. Claude Code, Codex, Cursor, Copilot, Pi, fx, Antigravity, and future hosts are execution surfaces—not the architecture of the skills themselves.

## What makes this different

A valid `SKILL.md` is only the starting point. This repository adds a quality contract around each canonical skill:

- **Outcome-first skills** for repository discovery, planning, CI triage, risk assessment, review, security, maintenance, migration, and release work.
- **Portable packaging** that keeps host-neutral engineering intent in standard Agent Skills packages.
- **Risk metadata** using an R0–R4 capability taxonomy instead of pretending every agent has the same permission model.
- **Routing fixtures** with positive and negative examples for every canonical skill.
- **Behavior assertions** describing required and prohibited behavior that can be scored against host/model observations.
- **Static security checks** for common malicious-skill and supply-chain patterns.
- **Machine-readable discovery** through `catalog/catalog.json` and `llms.txt`.
- **Composition recipes** that describe sequencing and gates without inventing another agent runtime.
- **Optional integration adapters** for explicitly delegating work to other coding-agent CLIs.

## Choose by engineering outcome

| Outcome | Skill | Normal capability |
| --- | --- | --- |
| Understand | [`repository-discovery`](skills/repository-discovery/) | R0 |
| Plan | [`issue-to-implementation-plan`](skills/issue-to-implementation-plan/) | R0 |
| Plan | [`migration-planning`](skills/migration-planning/) | R0 |
| Validate | [`ci-failure-triage`](skills/ci-failure-triage/) | R2 |
| Validate | [`test-gap-analysis`](skills/test-gap-analysis/) | R2 |
| Review | [`change-risk-assessment`](skills/change-risk-assessment/) | R0 |
| Review | [`pull-request-review`](skills/pull-request-review/) | R0 |
| Secure | [`security-review`](skills/security-review/) | R2 |
| Maintain | [`dependency-remediation`](skills/dependency-remediation/) | R3 |
| Maintain | [`documentation-sync`](skills/documentation-sync/) | R1 |
| Operate | [`release-readiness`](skills/release-readiness/) | R2 |
| Orchestrate | [`orchestrating-parallel-tasks`](skills/orchestrating-parallel-tasks/) | R0 |

Risk levels are host-neutral classifications, not authorization boundaries. See [`policies/risk-levels.md`](policies/risk-levels.md).

### Integration and delegation adapters

Use these only when the user or active host explicitly wants another coding agent to perform work:

- [`claude-code-cli`](skills/claude-code-cli/)
- [`codex-cli`](skills/codex-cli/)
- [`cursor-agent-cli`](skills/cursor-agent-cli/)
- [`copilot-cli`](skills/copilot-cli/)
- [`pi-agent-cli`](skills/pi-agent-cli/)
- [`fx-agent-cli`](skills/fx-agent-cli/)
- [`antigravity-cli`](skills/antigravity-cli/)

These adapters preserve each agent's native security model instead of forcing heterogeneous agents into a lowest-common-denominator CLI abstraction. Their project-level capability contracts live in [`policies/skill-contracts.json`](policies/skill-contracts.json) because vendor CLI details change more quickly than canonical engineering procedures.

## Trust and evidence model

The repository deliberately separates three kinds of evidence:

### 1. Conformance

`skills-ref validate` checks Agent Skills package syntax and structure.

### 2. Safety analysis

Repository-local tooling checks declared R0–R4 capability metadata and statically scans skill assets for suspicious patterns such as remote code bootstrapping, decoded payload execution, credential access, destructive commands, approval bypasses, and external uploads.

### 3. Behavioral evidence

[`evals/manifest.json`](evals/manifest.json) contains positive/negative routing cases plus required/prohibited behavior assertions for every canonical skill. Observations from a particular agent host/model/version can be scored with:

```bash
python scripts/score_skill_observations.py path/to/observations.json
```

Behavioral results are **evidence for the evaluated environment, not certification**. Model, host, prompt, tool, and repository changes can change behavior. See [`evals/README.md`](evals/README.md).

## Quality gate

Run the complete deterministic quality gate with:

```bash
make check
```

It covers:

1. Agent Skills conformance.
2. Repository quality-contract validation.
3. Static security scanning.
4. Generated catalog freshness.

Additional useful commands:

```bash
make catalog          # regenerate catalog/catalog.json, llms.txt, docs/compatibility.md
make security-report  # write a machine-readable catalog/security-report.json
make contracts        # validate risk + eval contracts
make validate         # run skills-ref validation
```

Pull requests run the same checks in `.github/workflows/skill_quality.yml`.

## Installation

The canonical skills are plain Agent Skills packages, so prefer the host's native installation/discovery mechanism when available.

### GitHub CLI Agent Skills

Install the collection using the GitHub CLI Agent Skills command:

```bash
gh skill install yu-iskw/coding-agent-skills --all
```

Or install one skill:

```bash
gh skill install yu-iskw/coding-agent-skills repository-discovery
```

### Claude Code plugin

Add this repository as a marketplace and install the plugin:

```text
/plugin marketplace add yu-iskw/coding-agent-skills
/plugin install coding-agent-skills@coding-agent-skills
```

Direct installation is also supported by the existing Claude plugin package:

```text
/plugin install yu-iskw/coding-agent-skills
```

### Codex plugin

```bash
codex marketplace add https://github.com/yu-iskw/coding-agent-skills
codex plugins install coding-agent-skills
```

### fx

fx can install the Agent Skills collection directly:

```text
/skills add https://github.com/yu-iskw/coding-agent-skills
```

Or install only the fx delegation adapter:

```text
/skills add https://github.com/yu-iskw/coding-agent-skills --skill fx-agent-cli
```

See [`docs/compatibility.md`](docs/compatibility.md) for the distinction between package/format compatibility and behavioral evidence.

## Composition recipes

Recipes express useful sequencing and gates while leaving execution and delegation to the active agent host:

- [`issue-to-pr`](recipes/issue-to-pr.md)
- [`failing-ci-to-fix`](recipes/failing-ci-to-fix.md)
- [`dependency-advisory-to-remediation`](recipes/dependency-advisory-to-remediation.md)
- [`library-upgrade`](recipes/library-upgrade.md)
- [`pr-risk-review`](recipes/pr-risk-review.md)

For example:

```text
repository-discovery
        ↓
issue-to-implementation-plan
        ↓
change-risk-assessment
        ↓
implementation by active host
        ↓
test-gap-analysis
        ↓
pull-request-review
```

A recipe is intentionally **not** a custom scheduler or workflow language.

## Machine-readable discovery

Humans and agents do not need to parse every skill directory to discover capabilities:

- [`catalog/catalog.json`](catalog/catalog.json) — canonical generated catalog including risk/category metadata.
- [`llms.txt`](llms.txt) — compact agent-readable skill index.
- [`docs/compatibility.md`](docs/compatibility.md) — packaging and evidence model across supported surfaces.
- [`evals/manifest.json`](evals/manifest.json) — routing and behavioral test fixtures.

Generated discovery files are checked in CI to prevent drift from `SKILL.md` source metadata.

## Adding a skill

New outcome skills should be small, reusable, and host-neutral. A new canonical skill must define:

```yaml
metadata:
  maturity: beta
  risk: R0
  category: review
  network: "false"
  side-effects: none
```

It must also add positive and negative routing fixtures plus required/prohibited behavior assertions to `evals/manifest.json` and pass `make check`.

Do not add a new vendor adapter merely because a new coding-agent CLI exists. Prefer a standard outcome skill unless explicit cross-agent delegation provides distinct user value.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the complete contribution contract and [`SECURITY.md`](SECURITY.md) for private vulnerability-reporting guidance.

## Project design principles

1. **Skills are the source of truth.** Plugin and host packaging must remain thin.
2. **Engineering outcomes beat vendor wrappers.** A skill should solve a recurring task independent of the executing model when possible.
3. **Least capability by default.** R0–R4 metadata makes expected side effects visible before execution.
4. **Evidence over badges.** Conformance and static safety checks are deterministic; model behavior is measured, contextual evidence.
5. **Composition without lock-in.** Recipes describe intent while native host runtimes handle orchestration.
6. **Small curated catalog over prompt quantity.** New skills should earn their maintenance and routing cost.
7. **No custom package manager or runtime dependency.** Installation, sandboxing, credentials, and scheduling remain responsibilities of the surrounding ecosystem.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
