# Cursor CLI usage examples

Use the installed name and check its flags against the current CLI reference.

## Read-only explanation

```bash
agent --print --mode ask --sandbox enabled --output-format text \
  "Explain how the parser validates user input. Cite the relevant files."
```

## Plan an implementation

```bash
agent --print --mode plan --sandbox enabled --output-format json \
  "Propose a refactor of src/parser.py and list the tests to run."
```

## Edit with verified permissions

Use only after authorizing edits and verifying the effective file, shell and integration rules for this workspace.

```bash
agent --print --sandbox enabled --output-format json \
  "Update docs/usage.md for the existing parser option and report the changes."
```

Inspect the actual diff and check for rejected operations before treating the task as complete.
