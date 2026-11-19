# Claude Code CLI usage examples

Check the installed CLI and loaded configuration before using these examples.

## Read-only review

```bash
claude --print --permission-mode plan --tools "Read,Glob,Grep" \
  --disallowedTools "mcp__*" --output-format json -- \
  "Read the parser and its tests. List untested edge cases by file and line."
```

## Scoped edit

Use when the user has authorized workspace edits. Run any required shell validation in the calling environment.

```bash
claude --print --permission-mode acceptEdits --tools "Read,Glob,Grep,Edit,Write" \
  --disallowedTools "mcp__*" -- \
  "Update the parser usage examples in README.md only."
```

Verify the diff independently and report any tool denial or incomplete work.
