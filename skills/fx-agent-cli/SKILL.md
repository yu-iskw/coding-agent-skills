---
name: fx-agent-cli
description: Executes coding, review, research, and automation tasks using the Vercel Labs fx coding-agent CLI (`fx`). Uses fx's native permission review, Agent Skills support, and single-request `fx ask` workflow while requiring external containment for untrusted or unattended work.
---

# executing-fx-agent

## Purpose

Use this skill to delegate coding, review, research, or automation tasks to the `fx` coding-agent CLI.

fx natively supports Agent Skills. This skill covers the complementary direction: invoking fx as an execution agent from another coding-agent workflow while preserving fx's own permission and skill-discovery model.

## Security Model

fx runs as a local coding agent with tools that can read files, modify the workspace, execute commands, and use configured external capabilities. Its native permission system reviews sensitive actions, but it is not a substitute for operating-system isolation.

For untrusted repositories, unattended execution, or high-impact tasks, run the entire `fx` process inside an external containment boundary such as a container, VM, micro-VM, or policy-controlled sandbox. Expose only the required workspace paths, credentials, and network access.

## Capability Tiers

| Tier | Capability | fx behavior | Approval required | Typical tasks |
| :--- | :--------- | :---------- | :---------------- | :------------ |
| **0** | Observe | Request analysis only; do not authorize mutations | No workspace mutation | Review, architecture analysis, local research |
| **1** | Edit | Permit the requested workspace changes through fx's permission flow | Yes | Refactoring, documentation, mechanical fixes |
| **2** | Execute | Permit required commands or external side effects through fx's permission flow | Yes (High Risk) | Tests, builds, dependency changes, scripted automation |

## Implementation Workflow

### 1. Analyze the request

Determine the minimum actions required:

- Read/search/list only -> Tier 0.
- Workspace file modifications without command execution -> Tier 1.
- Shell commands, tests, builds, package managers, Git operations, network access, or other side effects -> Tier 2.

If the task can be completed at a lower tier, use the lower tier.

### 2. Approval protocol

Obtain explicit user approval before Tier 1 or Tier 2 execution when the calling environment has not already obtained approval for the requested mutation or command execution.

Do not treat fx's native permission reviewer as blanket authorization for unrelated side effects. Persistent permission rules should remain narrow and task-specific.

### 3. Execute a single request

Use `fx ask` for delegated, non-interactive work:

```bash
# Tier 0: analysis only
fx ask "Review this repository and report the requested findings. Do not modify files or run commands that create side effects."

# Tier 1: bounded workspace editing
fx ask "Implement the requested workspace-only change. Do not run tests, package managers, Git commands, or other external side effects."

# Tier 2: controlled execution
fx ask "Implement the requested change, run only the smallest relevant validation commands, and report every command and result. Avoid unrelated side effects."
```

Prefer one narrowly scoped request per `fx ask` invocation. Split unrelated work into separate invocations rather than granting one session an unnecessarily broad mandate.

### 4. Validate the result

After fx finishes:

1. Inspect changed files and generated output.
2. Review any commands or external actions that ran.
3. Run only the validation required by the task.
4. Report changes, validation results, and unresolved risks.
5. Escalate capabilities only if the current tier cannot complete the task.

## Native Agent Skills Compatibility

fx discovers compatible `SKILL.md` packages from workspace and compatibility roots, including:

- `skills/`
- `.agents/skills/`
- `.claude/skills/`
- `.codex/skills/`
- `.opencode/skills/`
- `.claw/skills/`

fx also provides a managed installer through the interactive `/skills` command. To install this collection from GitHub:

```text
/skills add https://github.com/yu-iskw/coding-agent-skills
```

To install only this delegation skill:

```text
/skills add https://github.com/yu-iskw/coding-agent-skills --skill fx-agent-cli
```

Use `/skills list` to inspect discovered skills and `/skills path` to see the managed install root and compatibility roots.

## Operational Checks

Before relying on fx in automation:

- Confirm authentication/configuration with the repository's documented `fx login` or `fx setup` flow.
- Use `fx status` and `fx doctor` when validating local configuration or integrations.
- Review persistent permission rules before unattended runs.
- Treat fx as experimental software and pin/verify the version used in production-like automation.

## Security Rules

- **ALWAYS** request only the minimum scope needed for the task.
- **DO NOT** authorize workspace mutation for analysis-only requests.
- **DO NOT** authorize command execution or external side effects unless required.
- **DO NOT** treat native permission review as a sandbox.
- **DO NOT** expose broad credentials, host filesystem mounts, or unrestricted network access to unattended fx sessions unless required.
- **PREFER** external containment for untrusted repositories and unattended automation.
- **REVIEW** diffs and command output before treating a task as complete.

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios.
