# Codex CLI usage examples

Run examples from the authorized Git workspace after checking the installed CLI and effective configuration.

## Review

```bash
codex --ask-for-approval never exec --sandbox read-only \
  "Review the current diff and report findings by file and line."
```

The sandbox restricts writes. Codex can still run permitted read-only shell commands.

## Edit and run a targeted test

Use when the user has authorized workspace edits and command execution.

```bash
codex --ask-for-approval never exec --sandbox workspace-write \
  "Fix the regression in src/parser.py, run pytest tests/test_parser.py, and report the result."
```

Review the actual diff and check the reported test result.

## Capture structured output

```bash
codex --ask-for-approval never exec --sandbox read-only --ephemeral --json \
  "Summarize the project layout from the README and top-level directory."
```

Check the exit status and terminal event before using the result. JSONL can contain sensitive task or tool data, so handle it under the same policy as the task.
