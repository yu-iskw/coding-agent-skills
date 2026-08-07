# Coding Agent Skills: The Orchestration Framework for Industrial-Grade AI Workflows

Standard coding agents are powerful but often hit a **"Complexity Ceiling"** in long-horizon tasks. As conversations grow, context decays, hallucinations increase, and reliability drops.

**Coding Agent Skills** transform your repository from a collection of code into an **Agent-Ready Environment**. By codifying workflows into deterministic, reusable skills, you enable agents to work with higher autonomy, precision, and parallelism.

## Why Coding Agent Skills?

Standard agents operate in a single-session vacuum. Coding Agent Skills provide:

- **Orchestration**: Decouple planning from execution for complex tasks.
- **Reliability**: Replace vague prompts with structured, executable SOPs.
- **Efficiency**: Parallelize work that would take a single agent hours to complete.

## Key Advantages for Advanced Users

1.  **Multi-Agent Parallelism**: Break monolithic tasks into sub-tasks and execute them simultaneously across multiple agent instances.
2.  **Deterministic SOPs**: Standardize complex workflows (e.g., security audits, library upgrades) as executable SOPs that ensure zero steps are skipped.
3.  **Context Hygiene**: Use progressive disclosure to feed agents only the data they need, maintaining high reasoning quality.
4.  **Autonomous Fixer Loops**: Encapsulate `Test -> Analyze -> Fix` loops so agents self-correct without human intervention.
5.  **Platform Portability**: Write skills once; run them across **Claude Code**, **Codex**, **Cursor**, **GitHub Copilot CLI**, **Pi**, and **Google Antigravity CLI**.
6.  **Safety Governance**: Define granular permission modes per skill to manage risk in autonomous executions.
7.  **Institutional Memory**: Codify "Tribal Knowledge" into skills so every agent (and human) operates at an expert level.
8.  **Sub-Agent Specialization**: Spin up micro-personas (e.g., "SQL Optimizer") for domain-specific precision.
9.  **Headless CI/CD**: Trigger skills in pipelines for automated PR validation and structured reporting.
10. **Low-Code Customization**: Add new capabilities by simply adding a `SKILL.md` file—no extension development required.

## Building an Agent-Ready Repository

An Agent-Ready repository isn't just about good code; it's about **explicit intent**. By providing `SKILL.md` files, you give AI agents a clear "map" of how to interact with your codebase, what tools to use, and how to validate their own work.

## Available Skills

This repository includes the following coding agent skills:

<!-- START-SKILLS -->

- **[orchestrating-parallel-tasks](skills/orchestrating-parallel-tasks/)**: Decomposes complex or large-scale requirements into discrete, mutually exclusive sub-tasks that can be executed in parallel by multiple agents. Use when a task is described as an "epic", spans multiple architectural layers, or would benefit from concurrent development to reduce time-to-completion.
- **[claude-code-cli](skills/claude-code-cli/)**: Executes tasks using the Claude Code CLI (`claude`). Automatically determines the safest permission mode (plan, acceptEdits, or bypassPermissions) based on the task type.
- **[codex-cli](skills/codex-cli/)**: Executes tasks using the Codex CLI (`codex`). Automatically determines the least privilege required (Read-Only, Editor, or Autonomous) based on the user's request and handles security approvals.
- **[cursor-agent-cli](skills/cursor-agent-cli/)**: Executes tasks using the Cursor Agent CLI with structured planning, Q&A, and automation modes.
- **[copilot-cli](skills/copilot-cli/)**: Executes tasks using the GitHub Copilot CLI (`copilot`). Automatically determines the safest permission mode (plan, editor, or autopilot) based on the task type.
- **[pi-agent-cli](skills/pi-agent-cli/)**: Executes tasks using the Pi coding agent CLI (`pi`) with explicit tool allowlists and least-privilege capability tiers. Pi also natively implements the Agent Skills standard.
- **[antigravity-cli](skills/antigravity-cli/)**: Executes tasks using Google Antigravity CLI (`agy`) with native fine-grained `allow` / `ask` / `deny` permission resources.
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

For example, Pi uses explicit `--tools` allowlists while Antigravity uses fine-grained permission resources. This repository does not force heterogeneous agents into a lowest-common-denominator CLI abstraction.

## Pi Compatibility

Pi implements the Agent Skills standard and discovers compatible `SKILL.md` packages from standard skill locations, including `.agents/skills/`. It can also load a specific skill explicitly with `--skill <path>`.

The `pi-agent-cli` skill is complementary: it describes how another agent or workflow can invoke Pi as a delegated execution agent with a least-privilege tool set.

## Gemini CLI Retirement

Gemini CLI support has been removed. Google transitioned consumer Gemini CLI workflows to Antigravity CLI; use the `antigravity-cli` skill for Google coding-agent CLI execution.

The migration is intentionally not a command rename: Gemini CLI approval modes such as `plan`, `auto_edit`, and `yolo` do not map directly to Antigravity's fine-grained permission engine.

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

### Option 1: Via Custom Marketplace (Recommended)

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
/coding-agent-skills:orchestrating-parallel-tasks
/coding-agent-skills:claude-code-cli
/coding-agent-skills:codex-cli
/coding-agent-skills:cursor-agent-cli
/coding-agent-skills:copilot-cli
/coding-agent-skills:pi-agent-cli
/coding-agent-skills:antigravity-cli
```
