---
name: implementing-agent-skills
description: Implements new Agent Skills for the project. Identifies the AI coding tool (Cursor, Claude Code, Codex, Pi, Antigravity), ensures specification compliance, and provides specialized templates. Use when creating, authoring, or adding a new skill, or when the user asks about Agent Skills format or SKILL.md.
---

# Implementing Agent Skills

## Purpose

This skill implements new Agent Skills by identifying the target AI coding tool, ensuring specification compliance, and applying templates and best practices so the created skill is compatible with the user's workflow.

## Implementation Workflow

Copy this checklist and track progress:

```
Implementation Progress:
- [ ] Step 1: Identify AI coding tool
- [ ] Step 2: Choose or create skill directory (name matches frontmatter)
- [ ] Step 3: Select template and adapt frontmatter (name, description)
- [ ] Step 4: Write instructions; keep SKILL.md under 500 lines
- [ ] Step 5: Add references/assets as needed; keep links one level deep
- [ ] Step 6: Validate (YAML, skills-ref if available, keyword-rich description)
```

## 1. Identify AI Coding Tool

Check the project for indicators of AI coding tools:

- **Cursor**: Presence of `.cursor/` directory, `.cursorrules`, or `.cursorignore`.
- **Claude Code**: Presence of `.claude/` directory or Claude Code project settings.
- **Codex**: Presence of `.codex/`, `.agents/`, or Codex plugin configuration.
- **Pi**: Presence of `.pi/` resources or `.agents/skills/` used with Pi.
- **Antigravity**: Antigravity project configuration or an explicitly requested `agy` workflow.

### Logic

1. **Scan** the workspace root for these indicators.
2. **Analyze** the findings:
   - If **one** tool is detected -> Proceed with that tool as the target.
   - If **multiple** tools are detected -> Prefer the shared Agent Skills standard when possible; otherwise ask which tool-specific behavior matters.
   - If **no** tools are detected -> Use the portable Agent Skills structure unless the user specifies a tool.

## 2. Interaction Strategy

When a tool-specific choice is necessary, ask only when the implementations materially differ.

**Example Question:**
"I detected multiple coding-agent environments. Should this skill target the portable Agent Skills format, or rely on a tool-specific capability?"

- [ ] Portable Agent Skills
- [ ] Cursor
- [ ] Claude Code
- [ ] Codex
- [ ] Pi
- [ ] Antigravity

## 3. Implementation Context

Once the tool is identified, tailor the Agent Skill implementation accordingly:

- **Portable Agent Skills**:
  - Target: a repository `skills/<name>/SKILL.md` package or a supported shared `.agents/skills/` location.
  - Keep tool-specific assumptions out of the core instructions where possible.

- **Cursor**:
  - Target: `.cursor/skills/` (project) or `~/.cursor/skills/` (global).
  - Format: Standard `SKILL.md` with YAML frontmatter.

- **Claude Code**:
  - Target: `.claude/skills/` (project) or `~/.claude/skills/` (global).
  - Format: Follow Claude Code skill conventions while retaining Agent Skills compatibility where possible.

- **Codex**:
  - Prefer shared Agent Skills-compatible package structure and Codex plugin metadata when distributing a collection.

- **Pi**:
  - Pi implements the Agent Skills standard and discovers directories containing `SKILL.md` from `.pi/skills/`, `.agents/skills/`, configured package skill directories, and explicit `--skill` paths.
  - Prefer standards-compatible names and portable relative references even though Pi is lenient about some specification violations.

- **Antigravity**:
  - Keep skill content portable when possible.
  - For execution-oriented skills, model safety using Antigravity's current permission resources rather than retired Gemini CLI approval modes.

## 4. Standards & Templates

When implementing a new skill, always follow the established best practices and select the most appropriate template as a starting point.

### Specification Compliance

Ensure the skill follows the [official Agent Skills specification](https://agentskills.io/specification):

- **Naming**: Directory and `name` in frontmatter must match; use **gerund form** (e.g. `processing-pdfs`, `implementing-agent-skills`). Lowercase letters, numbers, and hyphens only; no leading/trailing hyphens or consecutive hyphens.
- **Description**: Write in **third person**; describe what the skill does and when to use it; include keywords for discovery (max 1024 characters).
- **Frontmatter**: Include required `name` and `description`. Add optional `license`, `compatibility`, `metadata`, `allowed-tools` if applicable.
- **Structure**: Keep SKILL.md under 500 lines. Use `scripts/`, `references/`, and `assets/` for progressive disclosure; keep file references **one level deep** from SKILL.md.

### Validation

Before completing the task:

1. **Check Syntax**: Verify YAML frontmatter is valid.
2. **Validate**: If the `skills-ref` tool is available, run `skills-ref validate ./<skill-directory>`.
3. **Manual Review**: Ensure the `description` is keyword-rich for discovery.

### Best Practices

See [references/best-practices.md](references/best-practices.md) for detailed naming, description, and progressive disclosure standards.

### Available Templates

Select the template that best matches the skill's purpose:

| Template                                                    | Purpose                                          |
| :---------------------------------------------------------- | :----------------------------------------------- |
| [generic.md](assets/templates/generic.md)                   | Standard boilerplate for any skill.              |
| [cli-tool-wrapper.md](assets/templates/cli-tool-wrapper.md) | Wrapping CLI tools with help checks and safety.  |
| [sop-workflow.md](assets/templates/sop-workflow.md)         | Checklists and SOPs for hybrid/manual processes. |
| [library-upgrade.md](assets/templates/library-upgrade.md)   | Safe, multi-step dependency upgrades.            |
| [code-review.md](assets/templates/code-review.md)           | Reviewing code against project standards.        |
| [security-audit.md](assets/templates/security-audit.md)     | Systematic vulnerability scanning and reporting. |
| [fixer-loop.md](assets/templates/fixer-loop.md)             | Autonomous "test-analyze-fix" loops (TDD/Lint). |
| [docs-sync.md](assets/templates/docs-sync.md)               | Keeping documentation in sync with source code.  |
