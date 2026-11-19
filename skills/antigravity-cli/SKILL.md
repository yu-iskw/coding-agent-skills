---
name: antigravity-cli
description: Executes coding, review, research, and automation tasks using Google Antigravity CLI (`agy`). Uses native fine-grained permission rules for interactive or headless execution.
---

# executing-antigravity

## Purpose

Use this skill to perform coding, review, research, or automation tasks with Google Antigravity CLI (`agy`). Antigravity is the successor to Gemini CLI for consumer workflows and has a different security model; do not translate Gemini CLI `plan`, `auto_edit`, or `yolo` behavior mechanically.

Antigravity represents sensitive operations as permission resources such as `read_file(...)`, `write_file(...)`, `command(...)`, `read_url(...)`, `execute_url(...)`, `mcp(...)`, and `unsandboxed(...)` and evaluates configured rules using `deny > ask > allow` precedence.

## Preflight

Check the installed `agy` version and `agy --help` against the [headless reference](https://antigravity.google/docs/cli/headless/) and [permission rules](https://antigravity.google/docs/cli-permissions). Confirm the active account and effective settings. Preserve native model selection unless the user requests an eligible model. Use `--model "<model>"` only with a verified headless model ID.

## Capability Profiles

These profiles are repository conventions, not Antigravity-native mode names.

| Tier  | Profile                         | Intended capability                                                                                  | Typical tasks                                      |
| :---- | :------------------------------ | :--------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| **0** | Analysis                        | Workspace reading; mutation and external actuation blocked or gated                                  | Code review, audits, architecture analysis         |
| **1** | Workspace development           | Workspace reads/writes; commands, MCP, and web actuation gated                                       | Refactoring, documentation, implementation         |
| **2** | Controlled autonomous execution | Explicit allowlist for necessary commands or integrations; destructive/high-impact operations denied | Tests, builds, dependency work, bounded automation |

## Implementation Workflow

### 1. Analyze required actions

Classify the task by the resources it requires:

- File reads only -> Tier 0.
- Workspace file modifications -> Tier 1.
- Shell commands, MCP calls, web actuation, unsandboxed execution, or other high-impact operations -> Tier 2.

Use the least capable profile that can complete the task.

### 2. Inspect the effective permission boundary

Antigravity permissions are configured in the user's Antigravity CLI settings. Unconfigured workspace reads/writes are normally auto-allowed; web browsing and other unconfigured sensitive actions normally fall back to Ask.

Before launching any scoped task, ensure the effective policy matches it. An analysis request requires explicit enforcement against writes because workspace writes may be allowed by default. Restrict MCP, shell, and browser or network capabilities to the authorized scope. Remember that broader `ask` or `deny` rules can override narrower `allow` rules because precedence is `deny > ask > allow`.

### 3. Prefer explicit resource policies

For controlled automation, prefer narrowly scoped rules. For example:

```json
{
  "permissions": {
    "allow": [
      "command(git status)",
      "command(git diff)",
      "command(npm run (build|lint|test))"
    ],
    "deny": [
      "command(rm -rf)",
      "command(sudo)",
      "write_file(.git/)",
      "write_file(/home/user/.ssh)"
    ]
  }
}
```

Treat this as an example, not a universal policy. Adapt targets to the repository, platform, package manager, and exact task.

### 4. Execute

In an authorized workspace with verified policy, run one headless task:

```bash
agy --prompt "Explain how the parser handles invalid input." --output-format json
```

Check both the JSON status and stderr. Headless mode can skip an action requiring approval and still exit successfully. Use `agy` and `/permissions` to inspect rules and handle approvals interactively when needed.

For autonomous execution, make the requested scope explicit in the prompt: files that may change, commands that may run, validation criteria, and operations that must not occur.

### 5. Validate

After execution:

1. Review changed files and generated artifacts.
2. Review commands or external actions that were performed.
3. Run the minimum required validation.
4. Report unresolved risks or permission requests that were denied.
5. Do not broaden permissions unless the narrower policy demonstrably blocks required work.

## Security Rules

- **ALWAYS** prefer narrowly scoped permission resources over global wildcards.
- **ALWAYS** remember permission precedence: `deny > ask > allow`.
- **DO NOT** reproduce Gemini CLI's `--yolo` mental model as a blanket Antigravity policy.
- **DO NOT** broadly allow `command(*)`, `write_file(*)`, `mcp(*)`, `execute_url(*)`, or `unsandboxed(*)` merely for convenience.
- **KEEP** destructive commands, sensitive credential paths, and privileged operations denied unless the task explicitly and legitimately requires them.
- **GATE** MCP mutations, browser actuation, network side effects, and unsandboxed execution according to their impact.
- **REVIEW** diffs and validation output before treating the task as complete.

## Gemini CLI compatibility

Antigravity has its own permission resources. Use this adapter only for `agy` and consult [Gemini CLI's separate headless reference](https://geminicli.com/docs/cli/headless/) for `gemini`.

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios.
