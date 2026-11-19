---
name: cursor-agent-cli
description: Delegates one task to Cursor CLI in print mode. Uses Ask or Plan mode for analysis and native permissions and sandbox controls for authorized edits and command execution.
---

# Execute one task with Cursor CLI

## Preflight

- Find the installed Cursor binary. Current [Cursor CLI documentation](https://cursor.com/docs/cli/overview) uses `agent`. If the installation exposes `cursor-agent`, use that binary only when its `--version` and `--help` confirm the same options. Review [CLI parameters](https://cursor.com/docs/cli/reference/parameters) and [headless behavior](https://cursor.com/docs/cli/headless).
- Use `agent status` where supported to check authentication. Preserve the native model selection unless the task specifies an eligible model. Check `agent --list-models` before passing `--model "<confirmed-model>"`. Confirm the effective provider and account when the task restricts them.
- Review project trust, the effective [permission rules](https://cursor.com/docs/cli/reference/permissions), sandbox and configured integrations. In print mode, operations already allowed by policy can run, including workspace edits in default agent mode.

## Execute

```bash
agent --print --mode ask --sandbox enabled "Explain how the parser handles invalid input."
agent --print --mode plan --sandbox enabled "Propose a migration plan for src/parser.py."
```

Use Ask for read-only exploration and Plan for analysis and planning. Confirm effective tool and integration restrictions where shell, network access, or reads outside scope must be blocked.

For changes, use default agent mode only with the user's authorization and effective write and command rules that fit the task. Print mode cannot pause for approvals. When an operation requires one, report it and continue only through the native approval workflow. Keep `--force`, `--yolo`, trust bypasses, and blanket MCP approval out of routine delegation.

Capture output with `--output-format` if needed. Check the exit status and result, then inspect the diff and validation independently. See [usage examples](references/usage-examples.md).

For hosted execution, use the separate [Cursor Cloud Agents workflow](https://cursor.com/docs/cloud-agent) after confirming the destination and repository access.
