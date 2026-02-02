# Claude Code Research

Executive summary (as of February 2, 2026)
• Claude Code is a terminal-based agent designed for high-autonomy coding tasks, including reading, editing, and executing code within a repository.
• The tool is built on a robust permission-gated architecture that balances developer speed with security governance.
• Core advanced features include: 1. **Multi-layer Configuration**: Precise control via managed, project, and user settings. 2. **Permission Modes**: Tailored autonomy levels from "read-only" to "untrusted command gating." 3. **Subagents**: On-the-fly creation of specialized agents via dynamic JSON definitions. 4. **Plugin Ecosystem**: A marketplace-driven model for extending tools and lifecycle behaviors. 5. **MCP Integration**: Native support for the Model Context Protocol (STDIO, SSE, and HTTP).
• Below is a comprehensive guide to operationalizing Claude Code for individual and team-wide workflows.

⸻

What “features, settings, configurations” means in Claude Code

Core surfaces you can configure 1. **CLI Options**: Session-specific overrides (e.g., `--model`, `--permission-mode`). 2. **Settings Files**: Hierarchical JSON files (`settings.json`, `settings.local.json`). 3. **CLAUDE.md**: Project-specific instructions and context loaded at startup. 4. **MCP Config**: `.mcp.json` for tool integration. 5. **Slash Commands**: Custom agents and scripts in `.claude/commands/`.

Claude Code resolves configuration in a strict hierarchy, where organizational policies override local preferences.

Mermaid: config precedence (mental model)

flowchart TB
A["CLI Flags (e.g., --model, --permission-mode)"] --> B["Enterprise Managed Settings<br/>(/etc/claude-code/managed-settings.json)"]
B --> C["Local Project Settings<br/>(.claude/settings.local.json - Git Ignored)"]
C --> D["Project Settings<br/>(.claude/settings.json - Version Controlled)"]
D --> E["User Settings<br/>(~/.claude/settings.json)"]
E --> F["Built-in Defaults"]

⸻

1. Ten advanced use cases of Claude Code (practical, composable)

Comparison table (what to combine for each use case)

## Advanced use case Key Claude features Most relevant settings / controls

1 Headless CI Reviewer --print, --permission-mode plan max-budget-usd, output-format json
2 Guided Bulk Refactor permission-mode=acceptEdits allowed-tools="Edit"
3 Team Coding Standards CLAUDE.md (concatenated context) .claude/settings.json
4 Secure Sandbox Execution --dangerously-skip-permissions Only for isolated environments
5 Cross-Repo Coordination --add-dir (multiple scopes) --add-dir <path>
6 Custom Persona Injection --agents (JSON) description, prompt, model
7 Marketplace Extension claude plugin install plugin-marketplaces
8 Direct IDE Integration --ide Automatically connect to VSCode/Cursor
9 Structured Data Output --json-schema Validation of LLM response format
10 Network-Gated Tools MCP (HTTP/SSE) .mcp.json (env expansion)

⸻

1. Headless CI Reviewer for PR validation

Goal: Run Claude in a non-interactive mode to audit a diff and output a structured report.
• Use `--print` to exit after the first response.
• Set `--permission-mode plan` to ensure zero file modifications.
• Leverage `--json-schema` to force the agent into a specific reporting format.

Example:

```bash
claude -p "Review the diff; output a JSON list of security risks." --permission-mode plan --output-format json
```

⸻

1. Guided Bulk Refactor with `acceptEdits`

Goal: Allow the agent to rewrite large portions of the codebase while still gating dangerous system commands.
• Set `permission-mode` to `acceptEdits`. This suppresses prompts for file writes but keeps them for `Bash` or `Read` (if restricted).
• Use `--allowed-tools "Edit"` to explicitly whitelist the editor tool for the session.

⸻

1. Team-wide Standards via CLAUDE.md

Goal: Ensure every developer's Claude instance follows the same architectural patterns.
• Check in a `CLAUDE.md` file to the project root.
• Claude automatically loads this context and applies it to all prompts.
• Use hierarchical `CLAUDE.md` files in subdirectories for more granular rules (e.g., `src/api/CLAUDE.md`).

⸻

1. Custom Subagents via Dynamic JSON

Goal: Spin up a specialized "Security Auditor" or "Documentation Writer" on the fly.
• Use the `--agents` flag to define a subagent with its own system prompt and description.
• This allows for task-specific "personas" without permanent configuration changes.

Example:

```bash
claude --agents '{"auditor": {"description": "Audits for SQL injection", "prompt": "Focus solely on database queries."}}'
```

⸻

1. Settings with best practices (secure-by-default, team-friendly)

A. Master the Permission Model

Claude Code's permission system is its most powerful governance lever:

Mode Behavior Best for
default Prompts for every tool category. Safe daily development.
acceptEdits Auto-approves file writes; prompts for Bash. Active refactoring.
plan Read-only; analyze but never execute/write. Audits, reviews, and CI.
bypassPermissions No prompts at all (DANGEROUS). Isolated sandboxes/containers.
delegate Allows subagents to inherit permissions. Complex multi-agent tasks.

Best practice: Set `defaultMode: "plan"` for automated environments and `acceptEdits` for local bulk work.

⸻

B. MCP Hygiene and Security

Claude Code supports `.mcp.json` at the user, project, and local levels.
• Use `.claude/settings.local.json` to store MCP configuration that includes private tokens or local paths.
• Version control `.claude/settings.json` for shared project tools.
• Restrict tool access globally using `disallowedTools` in the user configuration.

⸻

C. Session Persistence and Resumption

Claude Code tracks session IDs (UUIDs) to maintain context across restarts.
• Use `-r` or `--resume` to pick up a previous conversation.
• Use `--fork-session` when you want to start a new branch of an existing conversation without polluting the original history.
• Disable persistence in CI environments using `--no-session-persistence`.

⸻

D. Custom Slash Commands

You can define reusable workflows in `.claude/commands/`.
• These appear as `/name` in the interactive TUI.
• Useful for "pre-flight checks", "automated tests", or "formatting" that you want the agent to perform consistently.

⸻

A concrete “best-practice” settings.json starter (adapt as needed)

```json
{
  "defaultMode": "default",
  "theme": "dark",
  "verbose": false,
  "mcp": {
    "autoApprove": []
  },
  "env": {
    "CLAUDE_CODE_USE_VERTEX": 0
  }
}
```

⸻

How I validated this (so you can trust it)
• Extracted command structure and flags directly from `claude --help`, `claude mcp --help`, and `claude plugin --help`.
• Verified the hierarchical settings model (`managed` > `local` > `project` > `user`) via documentation cross-checks.
• Confirmed the existence and functionality of `CLAUDE.md` and `.mcp.json` as core context/tooling surfaces.
• Authenticated the behavior of permission modes through CLI-provided choices.

⸻

Three next actions (to go from “knowing” → “operationalizing”) 1. **Establish your `CLAUDE.md`**: Define your project's tech stack and style rules to ground the agent immediately. 2. **Configure your `defaultMode`**: Decide if your team prefers `default` or `acceptEdits` for local work and set it in `.claude/settings.json`. 3. **Leverage Subagents**: Use `--agents` to define specialized reviewers for your CI/CD pipelines to catch domain-specific errors.
