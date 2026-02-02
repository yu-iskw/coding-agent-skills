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
5.  **Platform Portability**: Write skills once; run them across **Cursor**, **Claude Code**, **Gemini CLI**, and **Codex**.
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
- **[gemini-cli](skills/gemini-cli/)**: Executes tasks using the Gemini CLI (`gemini`). Automatically determines the safest approval mode (plan, auto_edit, or yolo) based on the task type.
<!-- END-SKILLS -->
