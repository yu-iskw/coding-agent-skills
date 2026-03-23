# GitHub Copilot CLI Research

Executive summary (as of March 2026)
• GitHub Copilot CLI became generally available in February 2026. It is a terminal-native AI agent that can read, edit, and run code in your repository, featuring both an interactive conversational mode and a non-interactive automation mode (`-p/--prompt`).
• The core power of Copilot CLI stems from its granular tool-permission system and extensibility: 1. **Non-interactive automation**: Use `-p/--prompt` for one-shot tasks and CI/CD integration. 2. **Tool permission flags**: `--allow-tool`, `--deny-tool`, and `--allow-all-tools` give precise control over what the agent can do. 3. **MCP (Model Context Protocol)**: Integrate external data sources and tools via `~/.copilot/mcp-config.json`. 4. **Skills**: Reusable, specialized workflows loaded from `.github/skills/` or `~/.copilot/skills/`. 5. **Hooks**: Enforce policy at lifecycle points (preToolUse, postToolUse) via `.github/hooks/hooks.json`. 6. **Custom Instructions**: Natural language Markdown files automatically included in all prompts.
• Below you'll find advanced use cases and a configuration playbook focused on security, team collaboration, and automation.

⸻

## What "features, settings, configurations" means in Copilot CLI

Core surfaces you can configure:
1. **CLI flags**: One-off overrides (e.g., `--allow-all-tools`, `--deny-tool`, `--model`).
2. **Config file**: Persistent configuration in `~/.copilot/config.json` (override with `COPILOT_HOME`).
3. **MCP servers**: External tool providers configured in `~/.copilot/mcp-config.json`.
4. **Skills**: Packaged workflows (e.g., `SKILL.md` format) discoverable from `.github/skills/` or `~/.copilot/skills/`.
5. **Hooks**: Shell commands in `.github/hooks/hooks.json` that fire at key lifecycle events.
6. **Custom Instructions**: Markdown files that are automatically prepended to every prompt.

⸻

## 1. Three execution modes

| Mode | How to invoke | Behavior | Best for |
|------|--------------|----------|---------|
| **Interactive (Plan)** | `copilot` (no flags) | Asks clarifying questions, builds a plan before acting | Daily development, complex multi-step tasks |
| **Programmatic** | `copilot -p "<prompt>"` | One-shot; returns response inline; ideal for scripts | CI/CD pipelines, scripting, agent orchestration |
| **Autopilot** | `copilot -p "<prompt>" --allow-all-tools` | Executes end-to-end without prompting for approvals | Trusted environments, fully automated workflows |

⸻

## 2. Tool permission flags

Copilot CLI uses tool-permission flags to control what the agent may do without prompting:

| Flag | Effect |
|------|--------|
| `--allow-all-tools` | Bypass all approval prompts for every tool |
| `--allow-tool='write'` | Auto-approve file edit operations only |
| `--allow-tool='shell'` | Auto-approve shell command execution only |
| `--allow-tool='url'` | Auto-approve outbound network/URL fetch operations |
| `--allow-tool='<mcp-server-id>'` | Auto-approve tools from a specific MCP server |
| `--deny-tool='<tool>'` | Block a specific tool for the entire session |
| `--model <model-id>` | Override the default AI model |

Flags accept a permission pattern in the format `Kind(argument)` for fine-grained scoping.

Best practice: **Never** use `--allow-all-tools` in production environments or against repositories with sensitive secrets. Prefer `--allow-tool='write'` for edit-only tasks.

⸻

## 3. Skills

Copilot CLI discovers and loads skills automatically when relevant to the current task.

**Locations:**
- Project skills: `.github/skills/` (per repository)
- Personal skills: `~/.copilot/skills/` (shared across projects)

**Structure:** A skill is a folder containing at minimum a `SKILL.md` file, optionally with supporting scripts and Markdown references.

**Activation:** Copilot selects skills based on semantic relevance to the user's request. No explicit invocation is required.

⸻

## 4. Hooks

Hooks execute custom shell commands at key agent lifecycle points, enabling policy enforcement.

**Location:** `.github/hooks/hooks.json`

**Supported events:**
- `preToolUse`: Runs before a tool call; can deny or modify the call.
- `postToolUse`: Runs after a tool call; enables custom post-processing or logging.

Hooks are the recommended mechanism when policy must be **enforced** rather than just suggested. Unlike custom instructions (which are advisory), hooks can block tool execution outright.

⸻

## 5. Custom Instructions

Custom instructions are natural language Markdown files that are automatically included in all prompts within a repository. They are ideal for:
- Coding standards and style guides
- Project-specific context (e.g., "This project uses pnpm, not npm")
- Architectural constraints

**When to use what:**
- **Custom Instructions**: Simple rules needed for almost every task.
- **Skills**: Detailed SOPs that Copilot should only load when relevant.
- **Hooks**: Where policy must be enforced programmatically, not just suggested.

⸻

## 6. MCP (Model Context Protocol)

MCP servers expose additional tools to the Copilot CLI agent (databases, APIs, documentation systems).

**Configuration:** `~/.copilot/mcp-config.json`

```json
{
  "mcpServers": {
    "documentation": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

Grant a specific MCP server's tools without blanket `--allow-all-tools`:
```bash
copilot -p "<prompt>" --allow-tool='documentation'
```

⸻

## 7. Advanced use cases

| # | Use Case | Key Flags / Features |
|---|----------|---------------------|
| 1 | CI/CD automation runner | `-p`, no allow flags (read-only analysis) |
| 2 | Bulk file refactoring | `-p`, `--allow-tool='write'` |
| 3 | Governed command execution | `preToolUse` hooks in `hooks.json` |
| 4 | Cross-service context | MCP servers in `mcp-config.json` |
| 5 | Institutionalized workflows | Skills in `.github/skills/` |
| 6 | Autonomous build & test loop | `-p`, `--allow-all-tools` (sandboxed env) |
| 7 | Fine-grained tool control | `--allow-tool='shell' --deny-tool='url'` |
| 8 | Custom agent integrations | Copilot SDK (Node.js, Python, Go, .NET) |

⸻

## 8. Authentication

```bash
# Interactive login (opens browser)
copilot auth login

# Environment-variable-based (for CI)
export GITHUB_TOKEN=<pat-or-app-token>
```

⸻

## 9. Configuration hygiene

**Recommended `~/.copilot/config.json` structure:**

```json
{
  "model": "gpt-4o",
  "allowedTools": ["write"],
  "trustedDirectories": ["/home/user/projects"]
}
```

**Best practices:**
- Never store secrets in `config.json`; use environment variables for MCP tokens.
- Scope `trustedDirectories` to only the paths you work in.
- Use `--deny-tool='url'` in airgapped or sensitive environments.

⸻

## How this was validated

- Command flags and behaviors extracted from the GitHub Copilot CLI official documentation (docs.github.com/en/copilot/how-tos/copilot-cli).
- Permission model verified against the CLI reference and best-practices pages.
- Hooks and skills model cross-referenced with the customize-copilot documentation section.
