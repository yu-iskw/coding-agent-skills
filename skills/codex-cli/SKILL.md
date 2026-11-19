---
name: codex-cli
description: Delegates one task to the OpenAI Codex CLI using codex exec and the narrowest supported sandbox and approval policy. Use for scoped code review, implementation, or validation.
---

# Execute one task with Codex

## Preflight

- Check `codex --version`, `codex --help`, and `codex exec --help`. Use the [Codex command reference](https://developers.openai.com/codex/cli/reference) for flag placement and [sandbox and approval guidance](https://developers.openai.com/codex/agent-approvals-security) for policy behavior. `codex login status` checks native login when applicable.
- Run from the authorized Git workspace. Review the effective user and trusted project configuration, including model provider, MCP servers, additional writable roots, and network access. A project configuration can affect which service receives the task.
- Use the configured model when the user accepts it. To pin an eligible model, use `codex exec --model "<model>"`. For a requested provider, confirm the effective `model_provider` or an explicitly selected, verified native profile. A model ID alone does not select a provider.

## Execute

Choose the narrowest sandbox that supports the authorized task. Set the approval policy at the top level, before `exec`.

```bash
# Review: shell commands can run within the read-only sandbox.
codex --ask-for-approval never exec --sandbox read-only "Review the current diff."

# Scoped edits or validation commands, when authorized.
codex --ask-for-approval never exec --sandbox workspace-write "Update docs/usage.md only."
```

- `read-only` limits filesystem writes by sandboxed commands. For a task requiring no command execution or narrower file visibility, use a verified tool or process boundary that enforces it.
- `workspace-write` can run commands and write to the workspace, temporary directories, and other configured writable roots. If the task authorizes only editing and the effective boundary cannot prevent command execution, use a more restrictive adapter or add containment.
- `never` disables requests to run a command outside the sandbox. Keep required network controls and external tool restrictions in place and stop if the requested capability is unavailable.
- Use `--ephemeral` when supported to omit persisted session files, or `--json` for JSONL events. Cloud execution changes the execution environment and requires its own authorization.

Check the exit status and final result, inspect the actual changes, and verify the requested acceptance checks. See [usage examples](references/usage-examples.md).

For a requested hosted run, see the [Codex Cloud documentation](https://developers.openai.com/codex/cloud) and confirm the separate destination and workspace.
