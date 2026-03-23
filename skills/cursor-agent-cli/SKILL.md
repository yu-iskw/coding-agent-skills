---
name: cursor-agent-cli
description: Executes tasks using the Cursor Agent CLI (`cursor-agent`). Provides structured modes for planning, Q&A, and full automation with safety guardrails.
---

# executing-cursor-agent

## Purpose

Use this skill to perform coding, research, or automation tasks using the `cursor-agent` CLI. It leverages Cursor's native execution modes to balance autonomy with safety.

## Execution Modes

| Mode        | Flag          | Capability                                  | Approval Required | Typical Tasks                             |
| :---------- | :------------ | :------------------------------------------ | :---------------- | :---------------------------------------- |
| **Plan**    | `--mode plan` | Read-only analysis, research, and planning. | **No**            | Code audits, architectural planning.      |
| **Ask**     | `--mode ask`  | Q&A style for explanations and questions.   | **No**            | Explaining code, searching documentation. |
| **Default** | (none)        | Full access (edits + shell execution).      | **Yes**           | Feature implementation, bug fixes.        |

## Implementation Workflow

### 1. Analyze & Classify

Analyze the user's intent to determine the appropriate mode.

- **Plan Mode**: Does the task only involve analyzing the codebase or proposing a plan without making changes?
- **Ask Mode**: Is the user asking a specific question or seeking an explanation?
- **Default Mode**: Does the task require modifying files or running shell commands?

### 2. Security Protocol

If the task requires **Default Mode**, you **MUST** obtain user approval before execution, as `cursor-agent` has full access to tools like `bash` and `write`.

Use the `AskQuestion` tool to confirm:

> "I've detected that this task requires full agent permissions to modify files and execute commands. OK to proceed with `cursor-agent`?"

### 3. Execution

Execute `cursor-agent` using the determined mode. Use `--print` for non-interactive output suitable for the calling agent.

```bash
# Plan Mode
cursor-agent --print --mode plan "<prompt>"

# Ask Mode
cursor-agent --print --mode ask "<prompt>"

# Default Mode (requires approval)
cursor-agent --print "<prompt>"
```

### 4. Advanced Commands

#### Session Management

- `cursor-agent ls`: List previous conversations.
- `cursor-agent --resume [thread-id]`: Resume a prior conversation by ID. Omit the ID to resume the most recent session.

#### Cloud Handoff

Prefix any interactive message with `&` to push the current conversation to a background Cloud Agent:

```text
& <follow-up prompt>
```

The agent continues running asynchronously. Pick up the conversation at `cursor.com/agents` on the web or mobile app.

#### Context Management

- `@<file-or-folder>`: Select specific files or folders to include in the agent's context.
- `/compress`: Free up context window space by summarizing prior turns.

#### MCP Management

- `cursor-agent mcp list`: View configured MCP servers.
- `cursor-agent mcp list-tools <id>`: Inspect tools available in a specific MCP.
- `/mcp list` (interactive mode): Open an interactive menu to browse, enable, and configure MCP servers.

#### Rule Generation

- `cursor-agent generate-rule`: Create new `.cursorrules` or project-specific rules.

## Configuration

This skill uses native `cursor-agent` flags. Ensure `CURSOR_API_KEY` is set in the environment if required, or run `cursor-agent login` first.

### Model Selection

Cursor supports models from multiple providers. The active model depends on your subscription tier (defaults to Cursor's proprietary **Composer 2 Fast** or GPT-5.3-Codex on most paid plans). Switch models at any time via the in-session model picker, or set `CURSOR_MODEL` in the environment:

```bash
CURSOR_MODEL=claude-sonnet-4-6 cursor-agent --print "<prompt>"
```

Available providers: OpenAI (GPT-5.x), Anthropic (Claude Opus/Sonnet/Haiku 4.x), Google (Gemini 2.5/3), Cursor (Composer 2 Fast), DeepSeek, and local models.

## Automations *(Cloud — GA Mar 2026)*

**Cursor Automations** are always-on cloud agents triggered by external events. They run in an isolated cloud sandbox with your configured MCPs, automatically verify their output, and post results (e.g., comments, PRs).

**Supported triggers:** GitHub PR opened/updated, Slack message, Linear issue created, PagerDuty alert, cron schedule, webhook.

Configure automations at `cursor.com/settings/automations`.

**Example automation uses:**
- Auto-review every PR for security issues and post a summary comment
- Triage Linear issues and assign labels based on content
- On PagerDuty alert: investigate recent commits, identify likely culprit, open a fix PR

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios.
