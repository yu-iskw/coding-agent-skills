# Usage Examples for deepseek-harness-cli

This reference shows how to invoke `dsh` with the headless profile for common delegated tasks. Replace `<pinned-version>` with the Harness release you validated in automation.

## Tier 0: Analysis and Review

**Intent**: Review architecture without making changes.

```bash
dsh --profile headless "Review this repository's architecture, identify major risks, and do not modify files or run shell commands."
```

**Intent**: Review a diff supplied on stdin (task omitted; pipe is the prompt).

```bash
{ echo "Summarize these changes and list risks:"; git diff; } | dsh --profile headless
```

## Tier 1: Workspace Editing

**Intent**: Update documentation without running commands.

```bash
dsh --profile headless "Update the README to document the new configuration option. Do not run tests, package managers, or Git commands."
```

## Tier 2: Controlled Execution

**Intent**: Fix a failing test and run minimal validation.

```bash
dsh --profile headless "Fix the failing test in tests/auth_test.py, run only that test file, and report every command you executed."
```

**Intent**: Pinned CI step.

```bash
npx --yes @deepseek-ai/dsh@<pinned-version> --profile headless "Run the project's lint script and fix only auto-fixable issues it reports."
```

## Orchestrator: Machine-Readable Progress

**Intent**: Supervisor parses NDJSON events on stdout while diagnostics stay on stderr.

```bash
dsh --profile headless --json "Implement the requested change in src/api.ts and report completion."
```

Expect a stream that opens with a `session` event and closes with `final` on success. Treat exit code `1` and `turn_end` reason as failure signals even when the stream is well formed.

## Session Continuation (Advanced)

**Intent**: Second headless run continues the same persisted session id from a prior `--json` run.

```bash
dsh --profile headless --session-id session-abc123 "Continue: add tests for the change you just made."
```

Adoption fails if cwd, preset, subagent/fork state, or in-process ownership does not match Harness rules. Prefer fresh sessions for parallel orchestrator workers unless you deliberately serialize work in one workspace directory.

## Failure Handling

| Signal                          | Meaning                                        |
| :------------------------------ | :--------------------------------------------- |
| Exit `0`                        | Completed turn (`turn/end` reason `completed`) |
| Exit `1`                        | Aborted, errored, or empty assistant output    |
| stderr `dsh: reasoning:`        | Provider reasoning deltas (default mode)       |
| stderr `dsh: <code>: <message>` | Runner or turn failure diagnostic              |

After a non-zero exit, inspect stderr, workspace state, and partial files before retrying with a narrower task.

## Installing skills inside Harness

From the repository root, mirror into a discovery root (adjust paths if you copied only this skill directory):

```bash
mkdir -p .dsh/skills
ln -s ../../skills/deepseek-harness-cli .dsh/skills/deepseek-harness-cli
```

See repository README **DeepSeek Harness Compatibility** for discovery order. Verify the skill appears in the Harness catalog before relying on it in interactive sessions.
