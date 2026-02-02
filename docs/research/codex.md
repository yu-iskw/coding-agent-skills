# Codex Research

Executive summary (as of January 31, 2026)
• Codex CLI (from OpenAI) is a local coding agent that can read, edit, and run code in your repo, with a configurable sandbox + approval model to control autonomy. ￼
• The most “advanced” power comes from combining: 1. non-interactive automation (codex exec streaming stdout/JSONL), ￼ 2. profiles + layered config (user + project + overrides), ￼ 3. MCP integrations (bring in third-party tools/context safely), ￼ 4. rules/execpolicy (control which commands can run “outside the sandbox”), ￼ 5. skills (packaged, reusable workflows). ￼
• Below you’ll find 10 advanced use cases and a best-practice configuration playbook (security- and team-friendly), grounded in the official docs and the repo’s published defaults. ￼

⸻

What “features, settings, configurations” means in Codex CLI

Core surfaces you can configure 1. CLI flags (one-off behavior) 2. Profiles (named presets) 3. Config layers (user + project + system) 4. Policy files: rules + requirements.toml allow-lists 5. Extensions: MCP servers + skills

Codex resolves config in this precedence order (highest first): CLI overrides → profile → project .codex/config.toml (trusted only) → user ~/.codex/config.toml → system → defaults. ￼

Mermaid: config precedence (mental model)

flowchart TB
A[CLI flags / -c overrides] --> B[--profile values]
B --> C[.codex/config.toml layers<br/>(trusted projects only)]
C --> D[~/.codex/config.toml]
D --> E[/etc/codex/config.toml]
E --> F[Built-in defaults]

⸻

1. Ten advanced use cases of Codex CLI (practical, composable)

Comparison table (what to combine for each use case)

## Advanced use case Key Codex features Most relevant settings / controls

1 CI-style “agent runner” (deterministic automation) codex exec (stdout/JSONL), resume sandbox*mode=read-only, approval_policy=never, rules/allow-lists ￼
2 Safe refactor factory (many edits, constrained execution) interactive TUI + approvals sandbox_mode=workspace-write, approval_policy=untrusted/on-request ￼
3 Cross-repo coordinated change (monorepo-ish) extra write dirs --add-dir (grant additional directories) ￼
4 Governed “outside-sandbox” command control rules + execpolicy tooling .rules + codex execpolicy ￼
5 Integrate 3rd-party tools/context (tickets, docs, SCM) MCP [mcp_servers.*], tool allow/deny lists, OAuth login ￼
6 Institutionalized workflows (team consistency) skills skills.config, SKILL.md format & naming ￼
7 Hardened secret handling (avoid env leakage) environment filtering shell_environment_policy.* include/exclude/inherit ￼
8 Air-gapped / local-model mode (no external API) --oss + local providers oss*provider, local Responses endpoints ￼
9 Org telemetry + audit trails (controlled observability) OpenTelemetry integration otel.\*, keep log_user_prompt=false ￼
10 State isolation per workspace (multiple clients/config sets) alternate CODEX_HOME CODEX_HOME, OPENAI_BASE_URL override ￼

⸻

1. CI-style “agent runner” for PR checks, lint fixes, changelogs

Goal: run Codex in pipelines with minimal nondeterminism and zero risky side effects.
• Use codex exec to run non-interactively and stream output (including JSONL), optionally resuming sessions. ￼
• Recommended posture: --sandbox read-only --ask-for-approval never for “comment-only” outputs. ￼

Example pattern:

codex exec --sandbox read-only --ask-for-approval never \
 "Review the diff; output a markdown checklist of issues + suggested patches."

Edge case: If you want Codex to propose diffs, do it in workspace-write but keep approvals on.

⸻

1. Safe refactor factory (bulk mechanical changes, controlled command runs)

Goal: let Codex rewrite lots of files, but gate command execution and network.

Use workspace-write + a stricter approval policy like untrusted / on-request. ￼
This combination is explicitly recommended as a common “auto edit, but ask before untrusted commands” mode. ￼

⸻

1. Cross-repo coordinated changes with explicit write-scopes

Goal: update multiple repos/libs together without granting blanket filesystem access.

Use --add-dir repeatedly to grant additional directories write access (beyond the main workspace). ￼

⸻

1. Governed “outside-sandbox” commands via Rules + execpolicy

Goal: prevent accidental “real world” commands (e.g., gh, kubectl, prod deploys) from being run outside the sandbox.
• Rules are defined in .rules files and can prompt/allow/block based on prefixes. ￼
• codex execpolicy helps evaluate those rule files. ￼

This is ideal when paired with workspace-write (fast local edits) but strict command governance.

⸻

1. MCP: bring in third-party tools/context (docs, tickets, SCM)

Goal: let Codex call external tools through the Model Context Protocol.

Codex stores MCP configuration in config.toml and supports:
• STDIO servers with command, args, env, and env_vars allow-listing
• HTTP servers with bearer tokens / OAuth (codex mcp login) ￼

Example: adding an MCP server via CLI (supports env injection). ￼

⸻

1. Skills: codify “how your org writes software”

Goal: turn best practices into reusable agent workflows (architecture docs, ADRs, migration runbooks, etc.).

Skills package instructions/resources/scripts, and Codex uses name + description as primary signals to invoke them reliably. ￼

This is the most scalable way to keep Codex consistent across developers and repos.

⸻

1. Hardened secret handling (don’t leak your terminal env into subprocesses)

Goal: prevent accidental propagation of sensitive env vars when Codex runs tools/commands.

Use shell_environment_policy to constrain inheritance (inherit = all|core|none) and apply include/exclude patterns. ￼

This matters even more if you allow MCP servers or enable network.

⸻

1. Air-gapped / local-model mode (--oss)

Goal: run Codex against local Responses endpoints (e.g., Ollama / LM Studio) in restricted networks.

The Codex agent loop uses the Responses API, and the endpoint is configurable; when running with --oss, Codex can default to a local endpoint (example given: localhost /v1/responses). ￼

⸻

1. Org telemetry + audit trails (controlled observability)

Goal: observe agent performance and failures without capturing sensitive prompts.

Codex exposes OpenTelemetry settings (otel.\*) and explicitly calls out keeping log_user_prompt=false unless your policy allows prompt storage. ￼

⸻

1. State isolation per workspace (multiple configs, ephemeral dev envs)

Goal: separate Codex state/config across different machines, containers, or repos.

Codex stores local state under CODEX_HOME (defaults to ~/.codex). ￼
Also, you can override the OpenAI provider’s endpoint via OPENAI_BASE_URL without changing config.toml. ￼

This is useful for:
• devcontainer dotfiles setups
• “client A vs client B” segregation
• different data residency/proxy endpoints

⸻

1. Settings with best practices (secure-by-default, team-friendly)

A. Pick a sandbox + approval posture (the biggest lever)

Codex documents common safe combinations and what they imply. ￼

Comparison table: sandbox modes (recommended mental model)

Mode What it enables Best for Main risks / notes
read-only read files, answer questions audits, code review, CI commenting no edits; safest default ￼
workspace-write edit within workspace; optional network in sandbox day-to-day dev with guardrails still gate “untrusted” commands; consider disabling network unless needed ￼
danger-full-access / --yolo full access, no sandbox controlled containers only explicitly “use caution / not recommended” ￼

Best-practice default (most teams):
• sandbox_mode = "workspace-write"
• approval_policy = "on-request" or "untrusted"
• network off unless truly required (sandbox_workspace_write.network_access=false) ￼

⸻

B. Use profiles to make “safe vs fast” a one-word switch

Security docs show saving presets as profiles and selecting via codex --profile <name>. ￼

Typical profiles:
• readonly_quiet (CI / audit)
• full_auto (local dev with guardrails)
• net_on (only when you need outbound network)

⸻

C. Layer config correctly: user defaults + project overrides (trusted only)

Use project .codex/config.toml only for repos you trust; untrusted projects skip project-scoped layers. ￼

Best practice:
• Put personal preferences in ~/.codex/config.toml
• Put repo conventions in .codex/config.toml
• Check in rules / requirements allow-lists for teams (enforceable posture)

⸻

D. Control model + reasoning intentionally (cost / latency vs capability)

Defaults (from the official sample config):
• model = "gpt-5.2-codex"
• model_provider = "openai" ￼

Recommended approach:
• Keep default for normal coding
• Raise model_reasoning_effort for hard debugging/design tasks (trade latency for deeper reasoning) ￼
• Use review_model to run /review with a different model if desired. ￼

⸻

E. Web search: choose freshness vs safety

web_search supports disabled | cached | live and defaults to "cached"; if you run full-access sandbox settings, it defaults to "live". ￼

Best practice:
• "cached" for most coding (less exposure + still helpful)
• "live" only when you truly need latest info (security advisories, API changes)
• "disabled" in sensitive environments

⸻

F. Governance: allow-lists via requirements.toml

Security docs give an example of using requirements.toml to block risky combinations (e.g., disallow approval_policy=never and disallow danger-full-access). ￼

This is your “org policy lock.”

⸻

G. MCP hygiene: allow-list tools and credentials paths

From config reference + MCP docs:
• Use enabled_tools / disabled_tools per MCP server
• Prefer bearer tokens sourced from env var names for HTTP servers
• Use OAuth login flow where supported ￼

Best practice:
• Default-deny high-risk tools (anything that can mutate prod systems)
• Use env_vars allow-list for STDIO servers
• Keep secrets out of checked-in config

⸻

H. Secrets: reduce environment inheritance in subprocesses

Use shell_environment_policy:
• inherit = all|core|none
• include_only, exclude, and set for explicit control ￼

Best practice baseline:
• inherit = "core" (or "none" in higher-assurance environments)
• explicitly set only what you need for build tools

⸻

I. History and local state: know what’s stored and where

Codex state lives under CODEX_HOME (defaults ~/.codex) and can include history.jsonl if persistence is enabled. ￼

Best practice:
• Turn off history persistence in regulated contexts (history.persistence = "none") ￼
• Prefer OS keychain/keyring storage for credentials (cli_auth_credentials_store). ￼

⸻

A concrete “best-practice” config.toml starter (adapt as needed)

################################################################################

## Baseline: safe-by-default daily driver

################################################################################

## Model defaults (sample config indicates gpt-5.2-codex is default)

model = "gpt-5.2-codex"
model_provider = "openai"

## Guardrails

approval_policy = "on-request" # or "untrusted" for stricter command gating
sandbox_mode = "workspace-write"

## Keep network off by default; enable only in a dedicated profile

[sandbox_workspace_write]
network_access = false

## Web search: prefer cached; disable entirely in sensitive environments

web_search = "cached"

## Secrets: reduce env leakage into subprocesses

[shell_environment_policy]
inherit = "core"

## include*only = ["PATH", "HOME", "LANG", "LC*\*"] # tighten further if needed

## Don’t keep transcripts in regulated contexts

[history]
persistence = "save-all" # set to "none" when required

## max_bytes = 5000000

################################################################################

## Profiles

################################################################################

[profiles.readonly_ci]
sandbox_mode = "read-only"
approval_policy = "never"
web_search = "disabled"

[profiles.net_on]
[sandbox_workspace_write]
network_access = true
web_search = "live"

All keys shown above are documented in the config reference (and the sandbox/approval combos are explicitly described in the security guide). ￼

⸻

How I validated this (so you can trust it)
• Cross-checked feature surfaces (interactive, resume, exec) in the official CLI feature/reference docs. ￼
• Used the official Configuration Reference for authoritative key names and allowed values. ￼
• Used the official Security guide for recommended sandbox/approval combinations and governance patterns (requirements.toml). ￼
• Used the MCP guide for integration configuration and credential handling. ￼
• Used the Jan 23, 2026 engineering post to confirm architecture details (Responses API endpoints, --oss/local endpoints). ￼

⸻

Three next actions (to go from “knowing” → “operationalizing”) 1. Decide your default posture: pick 2–3 profiles (e.g., readonly_ci, daily, net_on) and enforce them with requirements.toml allow-lists. ￼ 2. Create 1–2 skills for your highest-frequency workflows (e.g., “migration PR template”, “secure dependency bump”) using crisp name + description so they trigger reliably. ￼ 3. Add one MCP server for your “source of truth” (docs or issue tracker) and strictly allow-list tools—then test in read-only first before enabling edits/commands. ￼

If you tell me your environment constraints (solo vs team, compliance level, whether outbound network is allowed, CI system), I can propose a tight policy set (profiles + requirements + rules) tailored to that.
