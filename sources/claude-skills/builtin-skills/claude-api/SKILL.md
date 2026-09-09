# Building LLM-Powered Applications with Claude

This skill helps you build LLM-powered applications with Claude. Choose the right surface based on your needs, detect the project language, then read the relevant language-specific documentation.

## Before You Start

Scan the target file (or, if no target file, the prompt and project) for non-Anthropic provider markers — `import openai`, `from openai`, `langchain_openai`, `OpenAI(`, `gpt-4`, `gpt-5`, file names like `agent-openai.py` or `*-generic.py`, or any explicit instruction to keep the code provider-neutral. If you find any, stop and tell the user that this skill produces Claude/Anthropic SDK code; ask whether they want to switch the file to Claude or want a non-Claude implementation. Do not edit a non-Anthropic file with Anthropic SDK calls. (Exception: the `prompt-audit` subcommand is non-interactive and does not stop here — it records non-Anthropic provider markers in its report's stated assumptions and never proposes switching a non-Anthropic file to the Anthropic SDK.)

## Output Requirement

When the user asks you to add, modify, or implement a Claude feature, your code must call Claude through one of:

1. **The official Anthropic SDK** for the project's language (`anthropic`, `@anthropic-ai/sdk`, `com.anthropic.*`, etc.). This is the default whenever a supported SDK exists for the project.
2. **Raw HTTP** (`curl`, `requests`, `fetch`, `httpx`, etc.) — only when the user explicitly asks for cURL/REST/raw HTTP, the project is a shell/cURL project, or the language has no official SDK.

Never mix the two — don't reach for `requests`/`fetch` in a Python or TypeScript project just because it feels lighter. Never fall back to OpenAI-compatible shims.

**Never guess SDK usage.** Function names, class names, namespaces, method signatures, and import paths must come from explicit documentation — either the `{lang}/` files in this skill or the official SDK repositories or documentation links listed in `shared/live-sources.md`. If the binding you need is not explicitly documented in the skill files, WebFetch the relevant SDK repo from `shared/live-sources.md` before writing code. Do not infer Ruby/Java/Go/PHP/C# APIs from cURL shapes or from another language's SDK.

**If WebFetch or repository access fails** (network restricted, timeouts, clone blocked): do not keep retrying — write code from the patterns and namespace/package tables in the `{lang}/` file, run the compiler or interpreter on it, and iterate on the error output. For statically-typed SDKs (C#, Java, Go) a compile-fix loop against local errors reaches working code faster than blocked network research.

## Defaults

Unless the user requests otherwise:

For the Claude model version, please use Claude Opus 5, which you can access via the exact model string `claude-opus-5`. Please default to using adaptive thinking (`thinking: {type: "adaptive"}`) for anything remotely complicated. And finally, please default to streaming for any request that may involve long input, long output, or high `max_tokens` — it prevents hitting request timeouts. Use the SDK's `.get_final_message()` / `.finalMessage()` helper to get the complete response if you don't need to handle individual stream events.

## API Drift — model prior may be stale

Several common Claude API shapes changed in 2025–2026:

| Area | Stale prior | Current API |
|---|---|---|
| Extended thinking | `thinking: {type: "enabled", budget_tokens: N}` | On Claude 4.6+ models: `thinking: {type: "adaptive"}`. `budget_tokens` is deprecated on Opus 4.6 / Sonnet 4.6 and **rejected with a 400** on Fable 5 / Sonnet 5 / Opus 5 / 4.8 / 4.7. Pre-4.6 models still use `budget_tokens`. |
| Web search / web fetch tool type | `web_search_20250305`, `web_fetch_20250910` | `web_search_20260209`, `web_fetch_20260209` (dynamic filtering) on Opus 5/4.8/4.7/4.6, Sonnet 5, and Sonnet 4.6. Older models keep the basic variants; on Vertex AI only basic `web_search_20250305` is available (web fetch is not on Vertex). |
| PHP parameter names | snake_case wire names as named args (`max_tokens`) | Top-level named args are camelCase (`maxTokens`). Nested array keys vary by feature — copy the exact key from the documented example; do not bulk-convert. |
| Managed Agents credentials | Keep secrets host-side via custom tools | Vault `environment_variable` credentials — stored by Anthropic, substituted at egress, never visible in the sandbox. Host-side custom tools remain the fallback for self-hosted sandboxes. |

## Subcommands

| Subcommand | Action |
|---|---|
| `migrate` | Migrate existing Claude API code to a newer model. Read `shared/model-migration.md`: confirm scope, classify each file, apply per-target breaking changes, then audit prompts against `shared/prompt-audit.md`. |
| `prompt-audit` | Audit existing prompts/skills/tool descriptions for dated patterns written for older models. Read `shared/prompt-audit.md`: establish scope/target, inventory, provenance, pattern scan, then produce a report + proposed diff. |
| `upgrade` | Upgrade the project's Anthropic SDK dependency across a major version (currently Python `anthropic` 0.x → 1.x). Read `python/claude-api/sdk-upgrade.md`. |

## Language Detection

- `*.py`, `requirements.txt`, `pyproject.toml` → Python → `python/`
- `*.ts`/`*.tsx`, `package.json` → TypeScript → `typescript/` (plain `.js` uses the same)
- `*.java`, `pom.xml`, `build.gradle`, `.kt`/`.scala` → Java (Kotlin/Scala use the Java SDK) → `java/`
- `*.go`, `go.mod` → Go → `go/`
- `*.rb`, `Gemfile` → Ruby → `ruby/`
- `*.cs`, `*.csproj` → C# → `csharp/`
- `*.php`, `composer.json` → PHP → `php/`
- Ambiguous / empty project → ask via AskUserQuestion (Python, TypeScript, Java, Go, Ruby, cURL, C#, PHP)
- Unsupported language (Rust, Swift, etc.) → suggest cURL examples

Every SDK language supports the beta Tool Runner and Managed Agents (beta).

## Which Surface Should I Use?

Start simple: single API calls and workflows handle most use cases; only reach for agents when the task genuinely needs open-ended, model-driven exploration.

| Use Case | Tier | Surface |
|---|---|---|
| Classification/summarization/extraction/Q&A | Single call | Claude API |
| Batch processing / embeddings | Single call | Claude API |
| Multi-step pipelines, code-controlled logic | Workflow | Claude API + tool use |
| Custom agent, your own tools | Agent | Claude API + tool use |
| Server-managed stateful agent with workspace | Agent | Managed Agents |
| Persisted, versioned agent configs | Agent | Managed Agents |
| Long-running multi-turn agent with file mounts | Agent | Managed Agents |
| Agent that runs on a schedule | Agent | Managed Agents — scheduled deployments |

### Four approaches to building an agent

1. **Claude API — manual loop**: you write the `while stop_reason == "tool_use"` loop; you host.
2. **Claude API — Tool Runner** (`client.beta.messages.tool_runner`): SDK supplies the loop; you host; only tools you define.
3. **Managed Agents** (beta): Anthropic supplies the harness AND hosts a per-session sandbox.
4. **Claude Agent SDK** (separate product, `claude-agent-sdk`): Claude Code packaged as a library — full harness with built-in tools; you host. This skill does NOT generate Claude Agent SDK code — point users at `code.claude.com/docs/en/agent-sdk` for that.

Tool Runner ≠ Claude Agent SDK: Tool Runner is a thin loop helper over tools you define (no built-in tools, no sandbox); Claude Agent SDK is the full Claude Code harness with built-in Read/Write/Edit/Bash/etc.

### Should I build an agent?

Check complexity, value, viability, and cost-of-error. If "no" to any, stay at a simpler tier.

## Architecture

Everything goes through `POST /v1/messages`. User-defined tools use the SDK's tool runner or a manual loop. Server-side tools (web search, web fetch, code execution) run on Anthropic's infra. Structured outputs use `output_config.format` and/or `strict: true`. Supporting endpoints: Batches, Files, Token Counting, Models.

## Current Models (cached: 2026-06-24)

| Model | Model ID | Context | Input $/1M | Output $/1M |
|---|---|---|---|---|
| Claude Fable 5 | `claude-fable-5` | 1M | $10.00 | $50.00 |
| Claude Mythos 5 (Project Glasswing only) | `claude-mythos-5` | 1M | $10.00 | $50.00 |
| Claude Opus 5 | `claude-opus-5` | 1M | $5.00 | $25.00 |
| Claude Opus 4.8 | `claude-opus-4-8` | 1M | $5.00 | $25.00 |
| Claude Opus 4.7 | `claude-opus-4-7` | 1M | $5.00 | $25.00 |
| Claude Opus 4.6 | `claude-opus-4-6` | 1M | $5.00 | $25.00 |
| Claude Sonnet 5 | `claude-sonnet-5` | 1M | $3.00 (intro $2.00 thru 2026-08-31) | $15.00 (intro $10.00) |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M | $3.00 | $15.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | $1.00 | $5.00 |

**ALWAYS use `claude-opus-5` unless the user explicitly names a different model.** Use exact model ID strings only — never append date suffixes. Claude Fable 5 / Mythos 5 is Anthropic's most capable widely released model: 1M context (also default), 128K max output, thinking always on (omit the `thinking` param or send `{type:"adaptive"}`; explicit disable/budget_tokens returns 400), raw chain of thought never returned, same tokenizer as Opus 4.8, has a `refusal` stop reason (check `stop_reason` before reading `content`; enable server-side `fallbacks` by default), no assistant prefill, 30-day data retention required, longer turns possible.

## Thinking & Effort

Use adaptive thinking (`thinking: {type: "adaptive"}`) on every current model. Effort (`output_config: {effort: "low"|"medium"|"high"|"xhigh"|"max"}`, default `high`) controls thinking depth/spend — `xhigh` is best for most coding/agentic use on Fable 5/Opus 4.7/4.8/Sonnet 5. Thinking display defaults to `"omitted"` on Fable 5/Mythos 5/Opus 5/4.8/4.7/Sonnet 5 — set `display: "summarized"` explicitly to stream a readable summary. `budget_tokens` is deprecated/removed except as a transitional escape hatch on Opus 4.6 / Sonnet 4.6 only.

## Other Quick-Reference Topics (see shared/*.md for full detail)

- **Compaction** (beta, `compact-2026-01-12`): server-side summarization for long conversations; always append `response.content` back, not just text.
- **Prompt caching**: prefix match; render order `tools`→`system`→`messages`; max 4 breakpoints; ~1024 token minimum; verify with `usage.cache_read_input_tokens`. Mid-conversation system messages (Opus 5/4.8, Fable 5/Mythos 5; not Sonnet 5) append `{role:"system",...}` to `messages[]`.
- **Fast Mode** (research preview, Opus 5/4.8 only): beta `fast-mode-2026-02-01` + `speed: "fast"` on `client.beta.messages`, 2.5x throughput at $10/$50 per MTok.
- **Task Budgets** (beta, Opus 5/Fable 5/Sonnet 5/Opus 4.8/4.7): `output_config.task_budget` with beta `task-budgets-2026-03-13`, min total 20,000 tokens, advisory token ceiling for agentic loops.
- **Provider clients**: dedicated classes per platform — `AnthropicBedrockMantle` (AWS Bedrock), `AnthropicFoundry` (Microsoft Foundry), `AnthropicVertex` (Google Cloud, no model-ID prefix, GCP ADC auth).
- **Context editing** (beta `context-management-2025-06-27`): clears old tool results/thinking, distinct from compaction.
- **Managed Agents** (beta `managed-agents-2026-04-01`): persisted versioned Agent configs + Sessions with Anthropic-hosted container workspace. Reading guide: `shared/managed-agents-overview.md` then topical `shared/managed-agents-*.md` files. Subcommand `managed-agents-onboard` walks a from-scratch setup interview.
- **Server tools**: web search (`web_search_20260209`), web fetch (`web_fetch_20260209`), code execution (`code_execution_20260521`), tool search (regex/BM25) — no beta header needed for most; declare in `tools`, results arrive as content blocks.
- **Document/file input**: base64 PDF or Files API (beta `files-api-2025-04-14`); citations via `citations: {enabled: true}`.
- **Tool use patterns**: strict tool use (`strict: true` on the tool def), parallel tool use (return all `tool_result`s in one message), Tool Runner beta helper, programmatic tool calling (Claude calls your tool from inside code execution).
- **Workload Identity Federation** (GA): auto-detected via `ANTHROPIC_FEDERATION_RULE_ID` etc. env vars, no explicit client config needed.

## Authentication

An unset `ANTHROPIC_API_KEY` does not mean no credentials exist — resolution order is `ANTHROPIC_API_KEY` → `ANTHROPIC_AUTH_TOKEN` → active OAuth profile (`ant auth login`) → WIF env vars → default profile on disk. Check `ant auth status` before asking the user for a key.

## Common Pitfalls (abridged — see live skill output for the full list)

- Don't truncate inputs; notify the user instead of silently truncating.
- Assistant prefill is removed on Fable 5/Mythos 5/Opus 5/Sonnet 5/the 4.6-4.8 family — use structured outputs instead.
- Confirm migration scope before editing when no specific file/directory is named.
- `max_tokens` defaults: ~16000 non-streaming, ~64000 streaming; don't lowball.
- Disabling thinking on Opus 5 has two failure modes (tool calls leaking into visible text, `<thinking>` tag leakage) — prefer low/medium effort instead of disabling.
- Parse tool call JSON with `json.loads()`/`JSON.parse()`, never raw string matching.
- Use `output_config: {format: {...}}`, not the deprecated `output_format`.
- Don't reimplement SDK helpers (`stream.finalMessage()`, typed exception classes, SDK types).
- Catch a most-specific-first exception chain, not one broad class.
- Don't research SDK types before writing — write from the namespace tables, let the compiler point to the right name.
- Bash/text-editor tools are Anthropic-defined and schema-less (`bash_20250124`, `text_editor_20250728`).
- Advisor tool's model must be at least as capable as the top-level request model.
- Agent Skills ≠ Managed Agents — different API surfaces (`container: {skills:[...]}` + code execution tool vs. `client.beta.agents/sessions/environments`).
- MCP connector needs both `mcp_servers` and a `mcp_toolset` tool entry.
- `inference_geo` is a top-level request param, not nested in `extra_body`.
- Memory tool type is `memory_20250818`.
- Use a model the feature actually supports (fast mode, task budgets, advisor pairing all have model-tier restrictions).

## Reading Guide (pointers into shared/, {lang}/, curl/ subdirectories — all present alongside this file)

Every SDK language uses `{lang}/claude-api/` (README.md, tool-use.md, streaming.md, batches.md, files-api.md) and `{lang}/managed-agents/README.md`; cURL uses `curl/examples.md` and `curl/managed-agents.md`. Topical deep-dives live in `shared/`: agent-design.md, anthropic-cli.md, claude-platform-on-aws.md, error-codes.md, live-sources.md, model-migration.md, models.md, platform-availability.md, prompt-audit.md, prompt-caching.md, token-counting.md, tool-use-concepts.md, and the managed-agents-*.md family (core, environments, tools, events, outcomes, multiagent, webhooks, memory, scheduled-deployments, client-patterns, onboarding, api-reference, self-hosted-sandboxes, overview).
