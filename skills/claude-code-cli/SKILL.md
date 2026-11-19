---
name: claude-code-cli
description: Delegates one task to Claude Code in print mode. Uses native permission modes and tool restrictions for scoped code review, editing, or validation.
---

# Execute one task with Claude Code

## Preflight

- Check `claude --version` and `claude --help` against the [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference). Use `claude auth status --text` where supported and confirm the actual provider and workspace configuration.
- Leave the model unset for the user's configured default. Use `--model "<confirmed-alias-or-id>"` only for a verified model. A model alias can resolve differently depending on provider or account.
- Review loaded settings, hooks, plugins, and MCP servers before launching in a trusted workspace. Claude's [Bash sandbox](https://code.claude.com/docs/en/sandboxing) is configured in settings. Verify it independently when the task requires shell isolation.

## Execute

For read-only analysis, combine plan mode with a restricted built-in tool list and explicitly deny MCP tools. For authorized file changes, use an edit-only tool list.

```bash
claude --print --permission-mode plan --tools "Read,Glob,Grep" \
  --disallowedTools "mcp__*" -- "Review the parser implementation."

claude --print --permission-mode acceptEdits --tools "Read,Glob,Grep,Edit,Write" \
  --disallowedTools "mcp__*" -- "Correct the usage example in README.md."
```

Plan and tool controls apply to agent tools. Use a sandbox or isolated workspace when the task requires an enforceable boundary around the whole process, including hooks or other loaded code. Where supported, `--safe-mode` can disable customizations when they are outside task scope.

For authorized validation commands, prefer running them in the calling environment. If Claude must run them, confirm that its Bash sandbox and permission rules enforce the command scope, or use an authorized interactive session for approvals. If a print-mode run cannot obtain a required approval, report it and stop. Preserve native safeguards.

Use `--output-format json` when structured results are useful. Check the exit status, output and any permission denials, then inspect changes and verify the result. See [usage examples](references/usage-examples.md).

For an explicitly requested hosted run or control of an existing session, use the native [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) or [Remote Control](https://code.claude.com/docs/en/remote-control) workflow.
