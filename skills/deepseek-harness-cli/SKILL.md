---
name: deepseek-harness-cli
description: Executes coding, review, research, and automation tasks using DeepSeek Harness CLI (`dsh`) via the headless profile. Uses Harness permission presets and profile composition while requiring external containment for untrusted or unattended work. DeepSeek Harness is in developer preview.
---

# executing-deepseek-harness

## Purpose

Use this skill to delegate coding, review, research, or automation tasks to [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) through the `dsh` CLI.

Harness natively supports Agent Skills. This skill covers the complementary direction: invoking `dsh` as an execution agent from another coding-agent workflow while preserving Harness's profile-based security and skill-discovery model.

Each headless invocation runs **one task** and exits. There is no interactive follow-up in the same process; split multi-step work into separate headless runs or use a different Harness surface (for example Web UI) for multi-turn sessions.

## Security Model

`dsh` runs as a local agent harness with tools that can read files, modify the workspace, execute commands, load plugins, and use network access according to the composed profile. Sandboxing, approval prompts, and permission presets can reduce risk but do not guarantee isolation. Review [SAFETY.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md) before unattended use.

For untrusted repositories, unattended execution, or high-impact tasks, run the entire `dsh` process inside an external containment boundary such as a container, VM, micro-VM, or policy-controlled sandbox. Expose only the required workspace paths, credentials, and network access.

Harness does not offer a single flag equivalent to Pi's `--tools` allowlist. Capability boundaries are expressed through **prompt scope**, **permission presets** (for example the base-backed default `workspace-write`), optional `DSH_PERMISSION_MODE`, and profile or `cordis.patch.yml` overlays. Inspect effective configuration with `dsh --profile headless --dump-config` when tightening automation.

## Capability Tiers

These tiers are repository conventions, not Harness-native mode names. Headless defaults (for example `workspace-write`) still apply unless you tighten presets or patches; use `dsh --profile headless --dump-config` to inspect the effective boundary.

| Tier  | Capability | Harness behavior                                                                            | Approval required              | Typical tasks                                          |
| :---- | :--------- | :------------------------------------------------------------------------------------------ | :----------------------------- | :----------------------------------------------------- |
| **0** | Observe    | Task text requests analysis only; no intentional workspace mutation or command execution    | No workspace mutation intended | Review, architecture analysis, local research          |
| **1** | Edit       | Task permits workspace file changes; prompt limits shell, package managers, and network     | Yes                            | Refactoring, documentation, mechanical fixes           |
| **2** | Execute    | Task permits required commands, tests, builds, or other side effects through composed tools | Yes (High Risk)                | Tests, builds, dependency changes, scripted automation |

## Implementation Workflow

### 1. Analyze the request

Determine the minimum actions required:

- Read/search/list only -> Tier 0.
- Workspace file modifications without command execution -> Tier 1.
- Shell commands, tests, builds, package managers, Git operations, network access, or other side effects -> Tier 2.

If the task can be completed at a lower tier, use the lower tier.

### 2. Approval protocol

Obtain explicit user approval before Tier 1 or Tier 2 execution when the calling environment has not already obtained approval for the requested mutation or command execution.

Do not treat Harness permission presets or approval UI as blanket authorization for unrelated side effects.

### 3. Pre-flight

Before Tier 1 or Tier 2, or before long Tier 0 runs:

1. Confirm the credential your profile expects (for example `DEEPSEEK_API_KEY` for `deepseek-official`, or `OPENROUTER_API_KEY` for the pi-ai `openrouter` route—see [references/cli-reference.md](./references/cli-reference.md)).
2. Confirm `dsh` is available (`command -v dsh`) or pin a version with `npx @deepseek-ai/dsh@<version>` (details in cli-reference).
3. For orchestrated workflows, align with repository resource stewardship; Harness does not expose a universal "remaining quota" CLI—plan task size accordingly.

### 4. Execute a single headless task

Use the `headless` profile for delegated, non-interactive work. The invoking directory is the default workspace root. Prefer one narrowly scoped task per invocation; tier-specific prompt templates are in [references/usage-examples.md](./references/usage-examples.md).

```bash
dsh --profile headless "<scoped task>"
```

**Orchestrator options:**

- `dsh --profile headless --json "<task>"` — newline-delimited JSON events on stdout for supervisors (stderr retains `dsh:` diagnostics).
- `dsh --profile headless --session-id <id> "<task>"` — continue a persisted session only when cwd, preset, and adoption rules match; see [references/cli-reference.md](./references/cli-reference.md).

On success, exit code is `0` and the final assistant text is printed on stdout (default mode). Non-zero exit indicates failure or incomplete turn; check stderr for `dsh:` messages and optional reasoning under `dsh: reasoning:`.

### 5. Validate the result

After `dsh` finishes:

1. Inspect changed files and generated output.
2. Review any commands or external actions that ran.
3. Run only the validation required by the task.
4. Report changes, validation results, and unresolved risks.
5. Escalate capabilities only if the current tier cannot complete the task.

## Native Agent Skills Compatibility

Harness discovers compatible `SKILL.md` packages through layered local roots (nearest git root as project). Shipped local provider rank order:

| Rank | Source           | Root                           |
| ---: | :--------------- | :----------------------------- |
|  100 | `project-dsh`    | `<projectRoot>/.dsh/skills`    |
|  200 | `project-agents` | `<projectRoot>/.agents/skills` |

User-level roots under `$DSH_HOME/skills` and agents home also apply. Harness does **not** load this repository's top-level `skills/` until you mirror packages into `.dsh/skills` or `.agents/skills` (see repository README **DeepSeek Harness Compatibility** and [usage-examples.md](./references/usage-examples.md)).

Subsystem reference: [docs/subsystems/skills.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md).

## Non-Goals

- Do not map retired Gemini CLI approval modes or Antigravity permission resources onto `dsh`.
- Do not use `sdk` or `acp` profiles as the primary delegation path here; use headless for one-shot workers ([references/cli-reference.md](./references/cli-reference.md) for ACP notes).

## Security Rules

Follow the repository **Security Convention for CLI Skills** lifecycle. Additionally for Harness:

- **DO NOT** treat permission presets or approval UI as OS-level isolation or blanket authorization.
- **REVIEW** diffs and command output before treating a task as complete.

Install, preview status, telemetry, and credential layout: [references/cli-reference.md](./references/cli-reference.md).

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios and [references/cli-reference.md](./references/cli-reference.md) for curated upstream links.
