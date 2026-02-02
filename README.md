# Coding Agent Skills

This repository contains a collection of coding agent skills that can be used to perform tasks such as coding, research, and automation.

## Available Skills

This repository includes the following coding agent skills:

<!-- START-SKILLS -->

- **[claude-code-cli](skills/claude-code-cli/)**: Executes tasks using the Claude Code CLI (`claude`). Automatically determines the safest permission mode (plan, acceptEdits, or bypassPermissions) based on the task type.
- **[codex-cli](skills/codex-cli/)**: Executes tasks using the Codex CLI (`codex`). Automatically determines the least privilege required (Read-Only, Editor, or Autonomous) based on the user's request and handles security approvals.
- **[gemini-cli](skills/gemini-cli/)**: Executes tasks using the Gemini CLI (`gemini`). Automatically determines the safest approval mode (plan, auto_edit, or yolo) based on the task type.
<!-- END-SKILLS -->
