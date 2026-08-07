# Usage Examples for antigravity-cli

This reference shows how to apply least privilege when using Google Antigravity CLI (`agy`). The tiers are conventions of this repository; Antigravity itself evaluates fine-grained `allow`, `ask`, and `deny` resource rules.

## Tier 0: Analysis

**Intent**: Review a repository without changing files or running commands.

Keep workspace reads available while denying mutation and command execution for the task. A restrictive policy may include rules such as:

```json
{
  "permissions": {
    "deny": [
      "write_file(*)",
      "command(*)",
      "execute_url(*)",
      "unsandboxed(*)"
    ]
  }
}
```

Then launch:

```bash
agy
```

Prompt example:

> Review the architecture and security boundaries of this repository. Do not modify files or perform external side effects.

## Tier 1: Workspace Development

**Intent**: Implement a code or documentation change while keeping process execution and external side effects gated.

Antigravity normally auto-allows reads and writes inside the active workspace, while unconfigured commands and other sensitive operations fall back to Ask. Preserve that boundary unless the task requires more.

Prompt example:

> Update the README and implementation for the requested feature. Do not run package-manager, Git mutation, network, or deployment commands without approval.

## Tier 2: Controlled Autonomous Execution

**Intent**: Implement a change and autonomously run a bounded validation set.

Prefer explicit command patterns rather than a blanket command wildcard. For a Node.js project, for example:

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

Prompt example:

> Implement the requested change. Run only the allowed formatter, lint, build, and test commands necessary to validate it. Do not push, publish, deploy, or alter credentials.

## MCP and Web Actuation

Treat MCP mutations and browser/web actuation as separate capabilities from ordinary repository editing. Keep them on Ask or Deny unless required.

Examples of high-impact resources that should normally remain gated:

```text
mcp(database/execute_mutation)
execute_url(example.com)
unsandboxed(git push)
```

## Permission Precedence Pitfall

Antigravity evaluates conflicting rules using:

```text
deny > ask > allow
```

Therefore a broad rule such as `ask: ["command(*)"]` will still require approval even if a narrower command is also placed in `allow`. Design the policy deliberately instead of assuming the narrow allow rule wins.

## Migration Example from Gemini CLI

Do not convert this old pattern:

```text
Gemini CLI "yolo" -> allow everything in Antigravity
```

Instead enumerate the actual operations required by the task, allow only those operations, keep dangerous capabilities denied, and let remaining sensitive operations fall back to Ask.
