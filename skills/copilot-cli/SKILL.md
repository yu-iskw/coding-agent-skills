---
name: copilot-cli
description: Delegates one task to GitHub Copilot CLI in prompt mode. Uses a tool availability list and scoped approvals for code review, workspace edits, and targeted validation.
---

# Execute one task with GitHub Copilot CLI

## Preflight

- Check `copilot --version` and `copilot --help` against the [Copilot CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference). Verify that Copilot CLI is enabled for the authenticated account and organization.
- Preserve the user's configured model selection. Use `--model="<confirmed-model>"` for an eligible model, or `--model=auto` if the user chooses Copilot's native model routing. Check model options in the authenticated `/model` picker and verify applicable organization policies.
- Inspect trusted directory settings, enabled plugins, hooks, and MCP servers before prompting. Disable or restrict integrations that are outside scope. The built-in MCP disable flag alone does not cover every server.

## Execute

Use `--available-tools` to restrict which tools the model can call. Use `--allow-tool` only to approve an operation class already authorized by the user. Approval patterns and tool names are different interfaces.

```bash
# Read a known file.
copilot --available-tools=view --prompt "Read README.md and summarize the setup steps."

# Edit files only, after the user authorizes the changes.
copilot --available-tools=view,edit,create,apply_patch --allow-tool='write(README.md)' \
  --prompt "Correct the setup example in README.md."
```

Restrict workspace visibility or writable paths with an enforceable process boundary when required. For validation, prefer running approved commands in the calling environment or use a narrowly scoped command rule from [Allowing and denying tool use](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools). Avoid blanket approvals or automatic escalation when prompt mode cannot obtain permission.

Verify tool denials, exit status, and actual changes. See [usage examples](references/usage-examples.md).
