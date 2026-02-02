# Gemini CLI Research

Executive summary (as of February 2, 2026)
• Gemini CLI is a powerful interactive coding agent that can read, edit, and run code in your repository, featuring both a conversational TUI and a non-interactive automation mode.
• The core power of Gemini CLI stems from its extensibility and governance model: 1. **Non-interactive automation**: Use `-p/--prompt` for one-shot tasks and CI/CD integration. 2. **Extensions**: Package prompts, MCP servers, custom commands, hooks, sub-agents, and agent skills into shareable units. 3. **MCP (Model Context Protocol)**: Integrate external data sources and tools (databases, APIs, documentation) safely. 4. **Agent Skills**: Reusable, specialized workflows that are activated on-demand (e.g., security audits, PR reviews). 5. **Lifecycle Hooks**: Intercept and customize agent behavior at key events (BeforeTool, AfterTool, SessionStart).
• Below you’ll find advanced use cases and a configuration playbook focused on security, team collaboration, and automation.

⸻

What “features, settings, configurations” means in Gemini CLI

Core surfaces you can configure 1. **CLI flags**: One-off overrides (e.g., `-m` for model, `-y` for YOLO mode). 2. **Settings files**: JSON files for persistent configuration across user and project scopes. 3. **Extensions**: External modules providing tools, prompts, and logic. 4. **Skills**: Packaged workflows (e.g., `SKILL.md` format). 5. **Hooks**: Executables that run at specific agent lifecycle points.

Gemini CLI resolves configuration in this precedence order (highest first): CLI flags → Environment variables → Project `.gemini/settings.json` → User `~/.gemini/settings.json` → System settings (`/etc/gemini-cli/settings.json`) → System defaults (`/etc/gemini-cli/system-defaults.json`) → Built-in defaults.

Mermaid: config precedence (mental model)

flowchart TB
A["CLI flags (-m, -p, -y, etc.)"] --> B["Environment variables"]
B --> C[".gemini/settings.json<br/>(Project scope)"]
C --> D["~/.gemini/settings.json<br/>(User scope)"]
D --> E["/etc/gemini-cli/settings.json<br/>(System scope)"]
E --> F["/etc/gemini-cli/system-defaults.json<br/>(System default)"]
F --> G["Built-in defaults"]

⸻

1. Ten advanced use cases of Gemini CLI (practical, composable)

Comparison table (what to combine for each use case)

## Advanced use case Key Gemini features Most relevant settings / controls

1 CI/CD Automation Runner --prompt, --output-format json approval-mode=plan, --sandbox true
2 Bulk Refactoring Engine auto_edit mode, skills approval-mode=auto_edit, -s
3 Shared Team Standards Extensions (git/local), GEMINI.md gemini extensions install, GEMINI.md
4 Governed Command Execution BeforeTool Hooks, allowed-tools gemini hooks migrate, --allowed-tools
5 Cross-Service Context MCP (STDIO/HTTP) gemini mcp add, settings.json (mcpServers)
6 Institutionalized Workflows Skills (installable/discoverable) gemini skills install, SKILL.md
7 Interactive Rapid Prototyping Interactive TUI, resume session -i, --resume latest
8 Accessibility-First Dev Screen reader mode --screen-reader
9 Safe "Read-Only" Audit Plan mode (read-only) approval-mode=plan, --sandbox true
10 Experimental Feature Testing Preview features / experimental-acp --experimental-acp

⸻

1. CI/CD Automation Runner for quality checks

Goal: Use Gemini as a headless agent to perform code reviews or generate changelogs in a pipeline.
• Use `--prompt` for non-interactive execution.
• Set `--output-format json` or `stream-json` for machine-readable results.
• Recommended posture: `approval-mode=plan` to ensure it only reads and reports without making changes.

Example:

```bash
gemini -p "Review the latest changes in src/ and generate a security report in JSON." --output-format json --approval-mode plan
```

⸻

1. Bulk Refactoring Engine with auto-approvals

Goal: Perform large-scale mechanical changes (e.g., renaming a property across 100 files) without manual clicking.
• Use `approval-mode=auto_edit`. This allows the agent to apply file edits automatically while still prompting for risky tools (like shell execution).
• Pair with a specific Skill or Extension that contains the refactoring logic.

⸻

1. Shared Team Standards via Extensions

Goal: Enforce coding styles or architectural patterns across a team.
• Create a Gemini Extension containing a `GEMINI.md` file with your team's standards.
• Distribute the extension via a Git repository.
• Developers run `gemini extensions install <git-url>` to load the standards into their context.

⸻

1. Governed Command Execution via Lifecycle Hooks

Goal: Prevent the agent from running dangerous commands (e.g., `rm -rf`, `docker push`) or log every tool usage.
• Implement a `BeforeTool` hook that inspects the tool name and arguments.
• The hook can return a signal to block execution or require additional user confirmation.

⸻

1. Cross-Service Context with MCP

Goal: Allow Gemini to query Jira tickets, search internal Wiki docs, or fetch database schemas.
• Use `gemini mcp add <name> <command>` to register a Model Context Protocol server.
• This grants Gemini CLI access to a suite of new tools defined by the MCP server.

⸻

1. Settings with best practices (secure-by-default, team-friendly)

A. Choose the right Approval Mode

Gemini CLI offers four distinct modes to balance speed and safety:

Mode Behavior Best for
default Prompts for every tool (edit, shell, etc.) General development
auto_edit Auto-approves file edits; prompts for shell Bulk refactoring / drafting
yolo Auto-approves ALL tools Trusted scripts / sandboxed envs
plan Read-only; no tools that modify state Audits, reviews, analysis

Best practice: Use `default` for daily work and `plan` for CI/CD or sensitive analysis.

⸻

B. Managing Extensions and Skills

Gemini CLI treats Extensions as the primary unit of distribution for complex logic.
• Use `gemini extensions list` to audit what's installed.
• Use `gemini skills list` to see what workflows are currently discoverable in your workspace.
• Baseline: Only install extensions from trusted internal or verified sources.

⸻

C. Configuration Hygiene in settings.json

Avoid putting secrets (API keys, tokens) directly in `settings.json`.
• Use environment variables for sensitive MCP configuration.
• Leverage `oauth-personal` for secure authentication where available.

Example `~/.gemini/settings.json` structure:

```json
{
  "ui": {
    "theme": "GitHub",
    "screenReader": false
  },
  "security": {
    "approvalMode": "default",
    "allowedTools": ["ls", "git status"]
  },
  "mcpServers": {
    "documentation": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

⸻

D. Leveraging Session History

Gemini CLI saves session history, allowing you to resume context without re-explaining the problem.
• `gemini --list-sessions` to see available history.
• `gemini --resume latest` to pick up where you left off.
• `gemini --delete-session <index>` to clean up sensitive or irrelevant context.

⸻

A concrete “best-practice” settings.json starter (adapt as needed)

```json
{
  "security": {
    "approvalMode": "default"
  },
  "ui": {
    "theme": "GitHub"
  },
  "mcpServers": {
    "vibe_kanban": {
      "command": "npx",
      "args": ["-y", "vibe-kanban@latest", "--mcp"]
    }
  }
}
```

⸻

How I validated this (so you can trust it)
• Extracted command usage and options directly from `gemini --help` and subcommand help (`mcp`, `extensions`, `skills`, `hooks`).
• Verified configuration precedence and settings file structure through web search and local inspection of `~/.gemini/settings.json`.
• Analyzed the Extension and Hook models based on official documentation links found during research.

⸻

Three next actions (to go from “knowing” → “operationalizing”) 1. **Audit your MCP servers**: Run `gemini mcp list` and ensure only necessary tools are enabled. 2. **Create a Team Extension**: Package your project's `GEMINI.md` and custom scripts into a local extension using `gemini extensions new`. 3. **Setup CI Reviews**: Integrate Gemini into your PR flow using `gemini -p "..." --approval-mode plan`.
