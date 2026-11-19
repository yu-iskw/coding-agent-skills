# GitHub Copilot CLI usage examples

Check the installed version and tool availability before running these examples.

## Read a specific file

```bash
copilot --available-tools=view --prompt "Read README.md and list the installation requirements."
```

## Edit a scoped file

Use when the requested edits are authorized and workspace scope is enforced where required.

```bash
copilot --available-tools=view,edit,create,apply_patch --allow-tool='write(docs/usage.md)' \
  --prompt "Update the parser option example in docs/usage.md and report the change."
```

Verify the diff in the calling environment and run any required validation there. If the CLI reports a denied or unavailable tool, report the limitation.
