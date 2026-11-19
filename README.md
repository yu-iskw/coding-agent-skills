# Coding Agent Skills

Configure which coding agent, provider, and model to use for a task. The plugin ships a setup skill, a routing skill, and CLI adapters that preserve each tool's native permission and approval workflow.

## Configure agent routing

1. Ask your host to use `setup-agent-routing`. In Claude Code, run `/coding-agent-skills:setup-agent-routing`. Choose the tools and models you can access, then review the proposed `.agents/coding-agent-routing.yaml` in your project.
2. Ask `route-coding-task` for a dry run, for example, “Which configured agent would review this diff?” It shows the selected target, model, matching rule, and any known blockers without launching another CLI.
3. Request delegation when you want the selected adapter to run the task. The router checks the destination, installed invocation, authentication, workspace permissions, and required integrations before sending the task. You can also invoke any CLI adapter directly.

The policy uses your own task descriptions as ordered rules. The first match wins, and you can define a default for unmatched tasks. You can choose a different target for an individual request. Keep credentials in each CLI's native authentication flow. For the policy format and a working example, see [Route one coding task](skills/route-coding-task/SKILL.md#policy-format). To check a host's routing behavior, use the [manual routing cases](docs/evals/routing-cases.md).

When upgrading from a version with the parallel orchestration skills, update prompts that referenced those skills or the coding-orchestrator subagent. Use `route-coding-task` when you want to select a tool and delegate one task.

## Available Skills

<!-- START-SKILLS -->

- **[antigravity-cli](skills/antigravity-cli/)**: Executes coding, review, research, and automation tasks using Google Antigravity CLI (`agy`). Uses native fine-grained permission rules for interactive or headless execution.
- **[claude-code-cli](skills/claude-code-cli/)**: Delegates one task to Claude Code in print mode. Uses native permission modes and tool restrictions for scoped code review, editing, or validation.
- **[codex-cli](skills/codex-cli/)**: Delegates one task to the OpenAI Codex CLI using codex exec and the narrowest supported sandbox and approval policy. Use for scoped code review, implementation, or validation.
- **[copilot-cli](skills/copilot-cli/)**: Delegates one task to GitHub Copilot CLI in prompt mode. Uses a tool availability list and scoped approvals for code review, workspace edits, and targeted validation.
- **[cursor-agent-cli](skills/cursor-agent-cli/)**: Delegates one task to Cursor CLI in print mode. Uses Ask or Plan mode for analysis and native permissions and sandbox controls for authorized edits and command execution.
- **[deepseek-harness-cli](skills/deepseek-harness-cli/)**: Executes coding, review, research, and automation tasks using DeepSeek Harness CLI (`dsh`) via the headless profile. Uses Harness permission presets and profile composition while requiring external containment for untrusted or unattended work. DeepSeek Harness is in developer preview.
- **[fx-agent-cli](skills/fx-agent-cli/)**: Executes coding, review, research, and automation tasks using the Vercel Labs fx coding-agent CLI (`fx`). Uses fx's native permission review, Agent Skills support, and single-request `fx ask` workflow while requiring external containment for untrusted or unattended work.
- **[pi-agent-cli](skills/pi-agent-cli/)**: Executes coding, review, research, and automation tasks using the Pi coding agent CLI (`pi`). Uses explicit tool allowlists to apply least privilege and distinguishes project trust from sandboxing.
- **[route-coding-task](skills/route-coding-task/)**: Selects one coding agent CLI and model using project routing rules. Use when the user asks which agent or model should handle a coding task, requests a dry run, or asks to delegate one task.
- **[setup-agent-routing](skills/setup-agent-routing/)**: Configures project-local rules for choosing a coding agent CLI, provider, and model. Use when the user asks to set up or update coding-agent routing, record available subscriptions or models as routing preferences, or customize which agent handles a type of task.
<!-- END-SKILLS -->

## Security Convention for CLI Skills

Each execution skill follows the same conceptual lifecycle while preserving the native security model of its agent:

```text
Analyze requested actions
        |
        v
Select minimum capability boundary
        |
        v
Map to native agent controls
        |
        v
Execute -> Validate -> Report
        |
        v
Escalate only if required
```

For example, Pi uses explicit `--tools` allowlists, fx uses native permission review and persistent permission rules, Antigravity uses fine-grained permission resources, and DeepSeek Harness uses profile permission presets plus prompt scope (inspect with `dsh --profile headless --dump-config`). This repository does not force heterogeneous agents into a lowest-common-denominator CLI abstraction.

## Pi Compatibility

Pi implements the Agent Skills standard and discovers compatible `SKILL.md` packages from standard skill locations, including `.agents/skills/`. It can also load a specific skill explicitly with `--skill <path>`.

The `pi-agent-cli` skill is complementary: it describes how another agent or workflow can invoke Pi as a delegated execution agent with a least-privilege tool set.

## fx Compatibility

fx natively discovers Agent Skills from workspace and compatibility roots including `skills/`, `.agents/skills/`, `.claude/skills/`, `.codex/skills/`, `.opencode/skills/`, and `.claw/skills/`.

From an interactive fx session, install this collection directly from GitHub:

```text
/skills add https://github.com/yu-iskw/coding-agent-skills
```

Or install only the fx delegation skill:

```text
/skills add https://github.com/yu-iskw/coding-agent-skills --skill fx-agent-cli
```

The `fx-agent-cli` skill is complementary: it describes how another agent or workflow can invoke fx as a delegated execution agent through narrowly scoped `fx ask` requests while preserving fx's native permission model.

## DeepSeek Harness Compatibility

DeepSeek Harness (`dsh`) discovers Agent Skills under **`.dsh/skills`** and **`.agents/skills`**, not this repo's top-level `skills/` until you mirror packages there. Setup and symlink examples: [skills/deepseek-harness-cli/references/usage-examples.md](skills/deepseek-harness-cli/references/usage-examples.md).

The `deepseek-harness-cli` skill is complementary: it describes how another agent or workflow invokes `dsh` through narrowly scoped `dsh --profile headless` runs while preserving Harness's profile and permission model.

## Google Antigravity CLI and Gemini CLI

The bundled `antigravity-cli` skill targets `agy`. Google moved individual Google AI Pro, Google AI Ultra, and free-tier Gemini CLI users to Antigravity CLI in June 2026. Gemini CLI remains available through supported enterprise licenses and API-key authentication. See [Google's announcement](https://github.com/google-gemini/gemini-cli/discussions/28017) and the [Gemini CLI headless reference](https://geminicli.com/docs/cli/headless/).

## Codex Plugin

This repository is published as a Codex plugin. Install it to use the skills
directly from within any Codex session.

### Option 1: Via Custom Marketplace (Recommended)

Add this repository as a custom marketplace, then install the plugin:

```
codex marketplace add https://github.com/yu-iskw/coding-agent-skills
codex plugins install coding-agent-skills
```

### Option 2: Project Settings

To enable the plugin for all members of a project, add the custom marketplace
to `.agents/plugins/marketplace.json` in your repository:

```json
{
  "name": "Coding Agent Skills Marketplace",
  "entries": [
    {
      "name": "coding-agent-skills",
      "source": "https://github.com/yu-iskw/coding-agent-skills",
      "policy": "AVAILABLE",
      "category": "productivity"
    }
  ]
}
```

## Claude Code Plugin

This repository is published as a Claude Code plugin. Install it to use the skills
directly from within any Claude Code session.

### Option 1: Claude Code Marketplace (Recommended)

Add this repository as a custom marketplace, then install the plugin:

```
/plugin marketplace add yu-iskw/coding-agent-skills
/plugin install coding-agent-skills@coding-agent-skills
```

### Option 2: Direct Install

Install the plugin directly from GitHub without adding the marketplace:

```
/plugin install yu-iskw/coding-agent-skills
```

### Option 3: Project Settings

To enable the plugin for all members of a project, add the following to
`.claude/settings.json` in your repository:

```json
{
  "extraKnownMarketplaces": {
    "coding-agent-skills": {
      "source": {
        "source": "github",
        "repo": "yu-iskw/coding-agent-skills"
      }
    }
  },
  "enabledPlugins": ["coding-agent-skills@coding-agent-skills"]
}
```

### Invoking Skills

Once installed, skills are available under the `coding-agent-skills` namespace:

```
/coding-agent-skills:setup-agent-routing
/coding-agent-skills:route-coding-task
/coding-agent-skills:claude-code-cli
/coding-agent-skills:codex-cli
/coding-agent-skills:cursor-agent-cli
/coding-agent-skills:copilot-cli
/coding-agent-skills:pi-agent-cli
/coding-agent-skills:fx-agent-cli
/coding-agent-skills:antigravity-cli
/coding-agent-skills:deepseek-harness-cli
```
