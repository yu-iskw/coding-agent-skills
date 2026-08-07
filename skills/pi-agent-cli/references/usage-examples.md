# Usage Examples for pi-agent-cli

This reference shows how to invoke Pi with the minimum built-in tool set required for common coding-agent tasks.

## Tier 0: Analysis and Review

**Intent**: Review the repository architecture without making changes.

```bash
pi --tools read,grep,find,ls \
  -p "Review this repository's architecture, identify major risks, and do not modify files."
```

**Intent**: Perform a focused security review.

```bash
pi --tools read,grep,find,ls \
  -p "Inspect the authentication and authorization code for security weaknesses. Do not modify files."
```

If the task needs no local tools at all:

```bash
pi --no-tools -p "Explain the trade-offs of the proposed architecture described in this prompt."
```

## Tier 1: Workspace Editing

**Intent**: Update documentation without running commands.

```bash
pi --tools read,grep,find,ls,edit,write \
  -p "Update the README to document the new configuration option. Do not run shell commands."
```

This tier intentionally excludes `bash`, which prevents Pi's built-in shell tool from being available.

## Tier 2: Controlled Execution

**Intent**: Fix a failing test and validate the change.

```bash
pi --tools read,grep,find,ls,edit,write,bash \
  -p "Run the smallest relevant test target, diagnose the failure, fix it, and rerun that test. Avoid unrelated commands."
```

**Intent**: Perform a build after a code change.

```bash
pi --tools read,grep,find,ls,edit,write,bash \
  -p "Implement the requested change, run the repository's documented formatter and targeted tests, and report the results."
```

## Loading an Explicit Skill

Use `--skill` to load a specific Agent Skill explicitly:

```bash
pi --skill ./skills/orchestrating-parallel-tasks \
  --tools read,grep,find,ls \
  -p "Decompose this implementation into independent work items."
```

Automatic skill discovery can be disabled while keeping explicitly supplied skills:

```bash
pi --no-skills \
  --skill ./skills/orchestrating-parallel-tasks \
  --tools read,grep,find,ls \
  -p "Plan this migration."
```

## Untrusted or Unattended Work

Pi project trust is not a sandbox. For untrusted repositories or unattended execution, place the entire `pi` process inside an external containment boundary and expose only the required workspace, credentials, and network access.
