# Usage Examples for copilot-cli

This reference provides concrete examples of how to apply the permission tiers when using the `copilot` CLI through this skill.

## Tier 0: Analysis & Research (Plan Mode)

**Intent**: "Summarize the architecture of this project."
**Logic**: No changes or commands needed. Safe read-only analysis.
**Command**:

```bash
copilot -p "Summarize the project architecture based on the directory structure and key source files."
```

**Intent**: "Review this pull request for security vulnerabilities."
**Logic**: Requires reading code but no file system changes.
**Command**:

```bash
copilot -p "Review the changes in src/auth/ for potential security vulnerabilities such as injection flaws or insecure token handling."
```

## Tier 1: Workspace Modification (Editor Mode)

**Intent**: "Fix all typos in the documentation files."
**Logic**: Modifies files automatically but does not run external shell commands without approval.
**Approval Required**: Yes.
**Command**:

```bash
copilot -p "Find and fix spelling and grammar errors in all .md files in the docs/ directory." --allow-tool='write'
```

**Intent**: "Rename the 'User' class to 'Account' across the whole repo."
**Logic**: Requires writing to multiple files but no shell execution.
**Approval Required**: Yes.
**Command**:

```bash
copilot -p "Rename the 'User' class to 'Account' across all source files, updating all imports and references." --allow-tool='write'
```

## Tier 2: Autonomous Execution (Autopilot Mode)

**Intent**: "Update dependencies and ensure the build still passes."
**Logic**: Modifies files AND executes build/test commands without interruption.
**Approval Required**: Yes (High Risk).
**Command**:

```bash
copilot -p "Update all dependencies to their latest compatible versions and run 'make build' to verify the build still passes." --allow-all-tools
```

**Intent**: "Identify and fix the failing unit test in tests/test_api.py."
**Logic**: Needs to run tests to identify the failure and then edit the code to fix it autonomously.
**Approval Required**: Yes (High Risk).
**Command**:

```bash
copilot -p "Run tests/test_api.py, analyze the failure output, and apply a fix to the underlying source code." --allow-all-tools
```

## Advanced: Fine-Grained Tool Control

**Intent**: "Run the linter and apply auto-fixes, but do not make any network calls."
**Logic**: Allow shell (to run linter) and write (to apply fixes), but explicitly deny URL access.
**Approval Required**: Yes.
**Command**:

```bash
copilot -p "Run 'make lint' and apply all auto-fixable issues." --allow-tool='shell' --allow-tool='write' --deny-tool='url'
```
