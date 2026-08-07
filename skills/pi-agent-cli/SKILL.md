---
name: pi-agent-cli
description: Executes coding, review, research, and automation tasks using the Pi coding agent CLI (`pi`). Uses explicit tool allowlists to apply least privilege and distinguishes project trust from sandboxing.
---

# executing-pi-agent

## Purpose

Use this skill to perform coding, review, research, or automation tasks through the `pi` CLI. Prefer explicit tool allowlists so each invocation receives only the capabilities required for the task.

Pi implements the Agent Skills standard and can also consume compatible `SKILL.md` files directly. This skill covers the other direction: invoking Pi as an execution agent from another coding-agent workflow.

## Security Model

Pi runs with the operating-system permissions of the user that launches it. Project trust controls whether project-local settings, skills, extensions, and related resources are loaded; it is **not** a sandbox and does not restrict what enabled tools can do.

For untrusted repositories, unattended execution, or high-impact tasks, run Pi inside an external containment boundary such as a container, VM, micro-VM, or policy-controlled sandbox. Mount only the required workspace paths and pass only the minimum credentials and network access needed.

## Capability Tiers

| Tier | Capability | Pi tools | Approval required | Typical tasks |
| :--- | :--------- | :------- | :---------------- | :------------ |
| **0** | Observe | `read,grep,find,ls` | No | Code review, audits, architecture analysis, local research |
| **1** | Edit | `read,grep,find,ls,edit,write` | Yes | Refactoring, documentation, mechanical fixes |
| **2** | Execute | Add `bash` only when required | Yes (High Risk) | Tests, builds, dependency changes, scripted automation |

## Implementation Workflow

### 1. Analyze the request

Determine the minimum actions required:

- Read/search/list only -> Tier 0.
- Workspace file modifications without shell execution -> Tier 1.
- Shell commands, tests, builds, package managers, Git operations, or other process execution -> Tier 2.

If the task can be completed at a lower tier, use the lower tier.

### 2. Approval protocol

Obtain explicit user approval before Tier 1 or Tier 2 execution when the calling environment has not already obtained approval for the requested mutation or command execution.

Do not interpret Pi project trust as approval to modify files, execute commands, access secrets, or perform external side effects.

### 3. Execute with an explicit allowlist

```bash
# Tier 0: read-only analysis
pi --tools read,grep,find,ls -p "<prompt>"

# Tier 1: workspace editing without shell execution
pi --tools read,grep,find,ls,edit,write -p "<prompt>"

# Tier 2: shell execution explicitly enabled
pi --tools read,grep,find,ls,edit,write,bash -p "<prompt>"
```

Prefer `--tools` over relying on the default built-in tool set. If no tools are required, use `--no-tools`.

### 4. Validate the result

After Pi finishes:

1. Inspect changed files or generated output.
2. Run only the validation commands required by the task.
3. Report changes, validation results, and any unresolved risks.
4. Escalate capabilities only if the current tier cannot complete the task.

## Skill Discovery Compatibility

Pi discovers Agent Skills from locations including:

- `~/.pi/agent/skills/`
- `~/.agents/skills/`
- `.pi/skills/`
- `.agents/skills/`
- package-provided `skills/` directories or `pi.skills` package metadata
- explicit `--skill <path>` arguments

Use `--skill <path>` when a workflow should load a specific skill explicitly. Use `--no-skills` when automatic skill discovery is undesirable; explicit `--skill` arguments remain additive.

## Security Rules

- **ALWAYS** select the minimum required tool allowlist.
- **DO NOT** enable `bash` for analysis-only or edit-only tasks.
- **DO NOT** treat project trust as a sandbox or execution authorization boundary.
- **DO NOT** expose broad credentials or host filesystem mounts to unattended Pi sessions unless required.
- **PREFER** external containment for untrusted repositories, generated code that will not be closely monitored, and unattended automation.
- **REVIEW** diffs and command output before treating a task as complete.

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios.
