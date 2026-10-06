# DeepSeek Harness CLI Reference (curated)

Authoritative upstream documentation changes frequently during developer preview. Prefer these links over paraphrased flag lists when details matter.

## Official sources

| Resource                         | URL                                                                                            |
| :------------------------------- | :--------------------------------------------------------------------------------------------- |
| Repository README                | https://github.com/deepseek-ai/deepseek-harness/blob/master/README.md                          |
| User documentation site          | https://deepseek-harness.github.io/deepseek-harness/                                           |
| Safety notice                    | https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md                          |
| `dsh` CLI overview               | https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/README.md                 |
| CLI behavior reference           | https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/reference/README.md       |
| Headless bundle (`dsh-headless`) | https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/bundle/headless/README.md |
| Skills subsystem                 | https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md          |

## npm package

Install or run without a global install:

```bash
npx @deepseek-ai/dsh web
npx @deepseek-ai/dsh --profile headless "task text"
```

Pin versions in automation: `npx --yes @deepseek-ai/dsh@<version> ...`.

## Profiles relevant to delegation

| Profile               | Role                                                                                    |
| :-------------------- | :-------------------------------------------------------------------------------------- |
| `headless`            | One task, final answer on stdout, then exit — **primary worker surface for this skill** |
| `web`                 | Interactive Web UI (default `http://127.0.0.1:3080`)                                    |
| `acp`                 | Agent Client Protocol on stdio until disconnect — not covered by this skill             |
| `sdk` / `sdk-minimal` | JSON-RPC SDK server on stdio — not covered by this skill                                |

Shorthand: `dsh web` boots the Web profile; `dsh --profile headless "job"` runs headless.

## Headless invocation contract (summary)

- **Task**: positional argument, or stdin when omitted (see headless README for pipe and blank-argument rules).
- **stdout (default)**: final assistant text only; reasoning streams to stderr when present.
- **Exit codes**: `0` on completed turn; `1` otherwise.
- **`--json`**: NDJSON event stream on stdout; diagnostics remain on stderr.
- **`--session-id`**: adopt persisted session; strict cwd, preset, and ownership checks.
- **`--help`**: profile app help; does not run a task.

Full event vocabulary and truncation limits: headless bundle README.

## Environment and credentials

Typical real-API configuration (see CLI reference "Shared deployment behavior"):

- `DEEPSEEK_API_KEY` — provider credential
- `DEEPSEEK_BASE_URL` — optional gateway base URL
- Project `.env` and `$DSH_HOME/.env` may layer into the launch environment

Never commit credentials. CI jobs should inject secrets through the platform secret store.

### OpenRouter (not `DEEPSEEK_BASE_URL` alone)

The default headless stack uses **`deepseek-official`** (`dsh-llm-deepseek`, Anthropic Messages at `https://api.deepseek.com/anthropic`). An [OpenRouter](https://openrouter.ai/docs/api-reference/authentication) key in `DEEPSEEK_API_KEY` fails with `AUTH` because that key is not a DeepSeek Platform key.

Use the **`llm-pi-ai`** `openrouter` catalog route and point the default model at OpenRouter. Prefer **`OPENROUTER_API_KEY` in the launch environment** or `$DSH_HOME/.env` (loaded at startup); set `apiKeyEnv: OPENROUTER_API_KEY` in the profile patch. The `refs:` section in `.credentials.yaml` holds **literal** values, not env indirection—do not duplicate the secret there if you want env-only storage. Example for `$DSH_HOME/profiles/headless/cordis.patch.yml`:

```yaml
- id: llm-pi-ai
  config:
    providers:
      openrouter:
        apiKeyEnv: OPENROUTER_API_KEY

- id: agent-default-model
  config:
    provider: openrouter
    model: deepseek/deepseek-v4.1-flash
```

Use a model slug from [openrouter.ai/models](https://openrouter.ai/models). Confirm routing with `dsh --profile headless --dump-config` (look for `provider: openrouter`). Upstream guide: [Configure models](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md).

## Permissions (base-backed profiles)

Base-backed surfaces (including headless over `dsh-base`) default new sessions to the `workspace-write` permission preset unless configured otherwise. Process-wide fallback may be influenced by `DSH_PERMISSION_MODE`. This is not equivalent to a fixed read-only CLI flag—combine prompt constraints, presets, and patches for least privilege.

Inspect composition without booting:

```bash
dsh --profile headless --dump-config
```

## Optional: Harness-hosted subagents

Harness can install optional bundles that delegate to other CLIs (for example Codex or Claude Code) via `dsh plugin --profile <name> add ...`. That path is orthogonal to invoking headless `dsh` as the worker from an external orchestrator. See plugin management in the CLI behavior reference.

## Telemetry and session logs

The base bundle enables DeepSeek session-log contribution and feedback-gated telemetry by default. Sensitive workspaces may require disabling or routing exports through organizational policy. Details and opt-out configuration live in the upstream CLI reference and package READMEs linked above.

## Future: ACP workers (phase 2)

When an orchestrator needs a **persistent** stdio worker with reconnect semantics, evaluate `dsh --profile acp` only after a concrete ACP client exists (no separate skill in this collection yet).

| Surface    | Lifetime                  | Typical use                                       |
| :--------- | :------------------------ | :------------------------------------------------ |
| `headless` | One task per process exit | Parallel sub-tasks, CI steps, scripted delegation |
| `acp`      | Until disconnect          | Long-lived automation clients speaking ACP        |

Do not substitute `acp` for headless in simple "run this sub-task and exit" orchestration without an ACP client implementation.
