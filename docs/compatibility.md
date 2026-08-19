# Compatibility

The canonical artifacts are standard `SKILL.md` packages. This matrix describes packaging/discovery evidence; it is not a claim that every model/host version has passed behavioral evaluation.

| Surface                                   | Status                | Notes                                                                                                                         |
| ----------------------------------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Agent Skills specification                | Canonical             | `skills/*/SKILL.md` is the source of truth.                                                                                   |
| Claude Code plugin                        | Packaged              | `.claude-plugin` points at the canonical `skills/` directory.                                                                 |
| Codex plugin                              | Packaged              | `.codex-plugin` points at the canonical `skills/` directory.                                                                  |
| Cursor                                    | Compatible collection | Repository also carries maintainer-only Cursor skills under `.cursor/skills/`; canonical product skills stay under `skills/`. |
| Pi                                        | Compatible collection | Pi can discover Agent Skills from standard locations.                                                                         |
| fx                                        | Compatible collection | fx can install/discover Agent Skills and also has a delegation adapter in this collection.                                    |
| GitHub Copilot / other Agent Skills hosts | Format-compatible     | Behavioral evidence should be recorded per host/model/version using the eval harness.                                         |

## Evidence model

- **Conformance:** deterministic Agent Skills syntax validation.
- **Safety:** deterministic static security findings and declared R0-R4 capability metadata.
- **Behavior:** observations scored against `evals/manifest.json`; results are evidence for a particular host/model/version, not certification.
- **Integration adapters:** vendor-heavy legacy CLI skills use `policies/skill-contracts.json` for risk classification so volatile vendor documentation does not need to be rewritten merely to update project metadata.
