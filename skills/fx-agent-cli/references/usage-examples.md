# Usage Examples for fx-agent-cli

This reference shows how to delegate common coding-agent tasks to fx while keeping each invocation narrowly scoped.

## Tier 0: Analysis and Review

**Intent**: Review repository architecture without making changes.

```bash
fx ask "Review this repository's architecture, identify major risks, and do not modify files or perform side effects."
```

**Intent**: Perform a focused security review.

```bash
fx ask "Inspect the authentication and authorization code for security weaknesses. Do not modify files or run commands that create side effects."
```

For review tasks, reject or avoid any permission request that would mutate the workspace or perform unrelated external actions.

## Tier 1: Workspace Editing

**Intent**: Update documentation without running validation commands.

```bash
fx ask "Update the README to document the new configuration option. Limit changes to workspace files and do not run tests, package managers, Git commands, or external side effects."
```

Inspect the diff after completion before accepting the result.

## Tier 2: Controlled Execution

**Intent**: Fix a failing test and validate the change.

```bash
fx ask "Run the smallest relevant test target, diagnose the failure, fix it, rerun only that test, and report the commands and results. Avoid unrelated changes or external side effects."
```

**Intent**: Perform a build after a code change.

```bash
fx ask "Implement the requested change, run the repository's documented formatter and targeted tests only, and report every validation result."
```

## Installing Agent Skills into fx

From an interactive fx session, install this repository's skills:

```text
/skills add https://github.com/yu-iskw/coding-agent-skills
```

Install only the fx delegation skill:

```text
/skills add https://github.com/yu-iskw/coding-agent-skills --skill fx-agent-cli
```

Inspect discovered skills and paths:

```text
/skills list
/skills path
```

fx also discovers compatible skills from workspace roots such as `skills/` and `.agents/skills/`, so a project can vendor or link selected skills there when repository-local skill configuration is preferred.

## Untrusted or Unattended Work

Native permission review does not provide process isolation. For untrusted repositories or unattended execution, run the entire `fx` process inside an external containment boundary and expose only the workspace, credentials, and network access required for the task.
