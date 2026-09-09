# code-review

> Recovered by extracting embedded prompt strings directly from the `claude`
> binary (`strings`/`grep` + byte-offset `dd` slices), since invoking the
> skill normally forks straight to a background agent without surfacing its
> instructions to the main thread. Reconstructed from real source text found
> in the binary — some plumbing (exact variable names) is paraphrased, but
> every quoted prompt block below is verbatim.

**Description** (as shown to the user/model): "Review the current diff, or a
PR number/branch/path target, for correctness bugs and
reuse/simplification/efficiency cleanups at the given effort level
(low/medium: fewer, high-confidence findings; high→max: broader coverage,
may include uncertain findings; ultra: deep multi-agent review in the cloud
(requires claude.ai account access)); with no level given, it reuses the
level you typed last. Pass `--comment` to post findings as inline PR
comments, or `--fix` to apply the findings to the working tree after the
review. For ultra on a GitHub.com PR target, `--post` asks to post the
finished review's findings to the PR as a single comment from the user's
GitHub account (not a review; the launch dialog still confirms in
interactive sessions, while non-interactive mode posts on the flag alone)
and `--no-post` hides that option."

**Usage**: `/code-review [low|medium|high|xhigh|max|ultra] [--fix] [--comment] [<pr#>|<branch>|<path>]`

## Flags and routing

- **Effort level** (first token): `low`, `medium`, `high`, `xhigh`, `max`, or
  `ultra`. If omitted, it reuses whatever level you typed last time
  (persisted per-session as `codeReviewLastEffort`); if that's also unset it
  defaults to `medium`. An unrecognized level word is ignored with a note,
  falling back the same way.
- **`ultra`**: routes to a *separate* cloud-hosted deep multi-agent review
  (`claude ultrareview` / the `/ultrareview` command), not a local prompt at
  all. Requires claude.ai account access; if unavailable in this session/
  environment, it says so and falls back to a local run at whatever effort
  level was otherwise selected. `--post` (ultra + GitHub PR target only)
  offers to post the finished review as one PR comment from the user's
  GitHub account; `--no-post` suppresses that offer. `--post` is silently
  ignored (with a note) on any local (non-ultra) run.
- **`--fix`**: after producing the findings list, apply each finding directly
  to the working tree — correctness bugs and cleanups alike. Skip anything
  whose fix would change intended behavior, reach well outside the reviewed
  diff, or that looks like a false positive; note the skip instead of arguing
  with it. Verbatim addition to the prompt:

  > ## Applying fixes (--fix)
  >
  > The `--fix` flag was passed. After producing the findings list, apply the
  > findings to the working tree instead of stopping at the report: fix each
  > one directly — correctness bugs and reuse/simplification/efficiency
  > cleanups alike. Skip any finding whose fix would change intended
  > behavior, require changes well outside the reviewed diff, or that you
  > judge to be a false positive — note the skip rather than arguing with it.
  > [Then call ReportFindings with outcomes; after the call, give one line
  > per skipped finding saying why — or, without the tool: finish with a
  > brief summary of what was fixed and what was skipped.]

- **`--comment`**: post each finding as an inline PR comment instead of just
  printing them. Verbatim addition:

  > ## Posting to GitHub (--comment)
  >
  > The `--comment` flag was passed. After producing the findings list, if
  > the review target is a GitHub PR, post each finding as an inline PR
  > comment via `mcp__github_inline_comment__create_inline_comment` (one call
  > per finding; include a suggestion block only when it fully fixes the
  > issue). If that tool is not available in this session, fall back to
  > `gh api` (repos/{owner}/{repo}/pulls/{pr}/comments) or print the findings
  > instead. If the target is not a PR, print the findings to the terminal
  > and note that `--comment` was ignored.

- **Target** (trailing token): a PR number, branch name, or file path to
  review instead of the working diff.
- **Diff-size-scaled finder budget**: for levels/model families with
  `finderBudgetHint` set, it runs `git diff --numstat` against the target
  first, estimates changed-line count, and scales the number of finder
  subagents to roughly `ceil(lines/150)` clamped to `[2, 8]` — "scale your
  investigation depth to the diff size rather than using a fixed large
  fleet."
- **Output mechanism**: when the `ReportFindings` tool is available (gated by
  an env flag and non-text/json output mode), findings are reported by
  calling it with `{level, findings}` — never printed as text, never
  published as an artifact. Otherwise it falls back to a plain-text list.
  Each finding carries `file`, `line`, `summary`, `short_summary` (≤60 chars,
  no rationale), `failure_scenario`, `category` (a kebab-case slug —
  `correctness`, `simplification`, `efficiency`, `reuse`, `altitude`,
  `conventions`, or a more specific one like `test-coverage`), and `verdict`
  when a verify pass produced one.

## Local review pipeline (shared shape across all levels)

### Phase 0 — Gather the diff

> Run `git diff @{upstream}...HEAD` (or `git diff main...HEAD` / `git diff
> HEAD~1` if there's no upstream) to get the unified diff under review. If
> there are uncommitted changes, or the range diff is empty, also run `git
> diff HEAD` and include the working-tree changes in scope — the review
> often runs before the commit. If a PR number, branch name, or file path was
> passed as an argument, review that target instead. Treat this diff as the
> review scope.

### Phase 1 — Find candidates (parallel finder agents, one per "angle")

Every angle produces candidates with `file`, `line`, `summary`, and a
concrete `failure_scenario`. There are two families of angle:

**Correctness angles** (bug-hunting):

- **Angle A — line-by-line diff scan**: read every hunk, then the enclosing
  function for each (bugs in unchanged lines of a touched function are in
  scope). Look for inverted/wrong conditions, off-by-one, null/undefined
  deref, missing `await`, falsy-zero checks, wrong-variable copy-paste, error
  swallowed in a catch, unescaped regex metacharacters.
- **Angle B — removed-behavior auditor**: for every line the diff deletes or
  replaces, name the invariant it enforced and check the new code re-
  establishes it. A removed guard, dropped error path, narrowed validation,
  or deleted test covering a real case is a candidate.
- **Angle C — cross-file tracer**: for each changed function, find callers
  (and callees) and check whether the change breaks any call site — new
  precondition, changed return shape, new exception, timing/ordering
  dependency.
- **Angle D — language-pitfall specialist** (xhigh/max only): scans for
  classic per-language footguns — JS falsy-zero/`==` coercion/closure-
  captured loop var; Python mutable default args/late-binding closures; Go
  nil-map write/range-var capture; SQL injection; timezone/DST drift; float
  equality.
- **Angle E — wrapper/proxy correctness** (xhigh/max only): when the diff
  adds/modifies a type that wraps another (cache, proxy, decorator, adapter),
  check every method routes to the wrapped instance and not back through a
  registry/session/global, and that the wrapper forwards every method
  callers actually use.

**Cleanup angles** (quality, not bugs — same `file`/`line`/`summary` shape,
but `failure_scenario` states a cost instead of a crash: "correctness bugs
always outrank cleanup, altitude, and conventions findings when the output
cap forces a cut"):

- **Reuse**: new code re-implementing something the codebase already has —
  name the existing helper to call instead.
- **Simplification**: redundant/derivable state, copy-paste with slight
  variation, deep nesting, dead code left behind.
- **Efficiency**: redundant computation/repeated I/O, sequential independent
  operations, blocking work on hot paths/startup; long-lived closures that
  keep a whole scope alive (memory-leak-shaped) — prefer a class/struct that
  copies only what it needs.
- **Altitude**: special cases layered on shared infra instead of generalizing
  the underlying mechanism.
- **Conventions (CLAUDE.md)**: find every CLAUDE.md/CLAUDE.local.md
  governing the changed files (user-level, repo-root, and any ancestor
  directory of a changed file) and flag only violations you can quote both
  the rule and the breaking line for — no vague "spirit of the doc"
  inferences.

If the Agent tool isn't available in context, every angle runs sequentially
in the same context instead of fanning out — the review still covers every
angle, just without parallelism, and the report says so explicitly so
readers aren't misled about what actually ran.

### Phase 2 — Verify

Two verify modes, depending on level:

- **Precision mode** (medium): dedup, then run exactly **one verifier** per
  remaining candidate, returning one of three states:

  > - **CONFIRMED** — can name the inputs/state that trigger it and the wrong
  >   output or crash. Quote the line.
  > - **PLAUSIBLE** — mechanism is real, trigger is uncertain (timing, env,
  >   config). State what would confirm it.
  > - **REFUTED** — factually wrong (code doesn't say that) or guarded
  >   elsewhere. Quote the line that proves it.

  Keep CONFIRMED and PLAUSIBLE; drop REFUTED.

- **Recall-biased mode** (high, xhigh, max): same one-vote CONFIRMED/
  PLAUSIBLE/REFUTED verdict, but with an explicit bias:

  > **PLAUSIBLE by default** — do not refute a candidate for being
  > "speculative" or "depends on runtime state" when the state is realistic:
  > concurrency races, nil/undefined on a rare-but-reachable path (error
  > handler, cold cache, missing optional field), falsy-zero treated as
  > missing, off-by-one on a boundary the code does not exclude, retry
  > storms / partial failures, regex/allowlist that lost an anchor. These are
  > PLAUSIBLE.
  >
  > **REFUTED** only when constructible from the code: factually wrong (quote
  > the actual line); provably impossible (type/constant/invariant — show
  > it); already handled in this diff (cite the guard); or pure style with no
  > observable effect.

  "This is recall mode — a single non-REFUTED vote carries the finding. Do
  NOT drop on uncertainty." Every finder is warned separately: "finders that
  silently drop half-believed candidates bypass the verify step and are the
  dominant cause of misses."

### Phase 3 — Sweep for gaps (xhigh/max only)

> Run **one more finder** as a fresh reviewer who has the verified list.
> Re-read the diff and enclosing functions looking ONLY for defects not
> already listed. Do not re-derive or re-confirm anything already there — the
> job is gaps. Focus on what the first pass tends to miss: moved/extracted
> code that dropped a guard or anchor; second-tier footguns (dataclass
> default evaluated once, `hash()` non-determinism, lock-scope shrink,
> predicate methods with side effects); setup/teardown asymmetry in tests;
> config defaults flipped.
>
> Surface **up to 8 additional candidates**, each naming a defect not already
> on the list. If nothing new, return an empty sweep — do not pad.

## The effort ladder

| Level | Angles run | Candidates/angle | Verify | Extra pass | Finding cap | Framing |
|---|---|---|---|---|---|---|
| **low** | none (single inline pass over the raw diff hunks only — no Phase 1/2 machinery) | — | none | — | 4 (or `min(files_changed, 4)` in one variant, with a "do one more pass" retry if short) | Fast, hunk-only: inverted/wrong conditions, off-by-one, null deref, removed guard, falsy-zero, missing `await`, copy-paste, swallowed errors — plus dupes/dead-code visible in the hunk. Explicitly skips test/fixture files and anything outside the hunk (style, naming, perf, missing tests). |
| **medium** | 8 (Angles A–C + Reuse/Simplification/Efficiency + Altitude + Conventions) | up to 6 each | precision (1-vote, 3-state, keep CONFIRMED+PLAUSIBLE) | none | 8 | "You are reviewing for **precision**: every finding you surface should be one a maintainer would act on." |
| **high** | same 8 as medium | up to 6 each | recall-biased (1-vote, keep non-REFUTED) | none | 10 | "You are reviewing for **recall**: catch every real bug a careful reviewer would catch in one sitting. Catching real bugs matters more than avoiding false positives. Err on the side of surfacing." |
| **xhigh** | 10 (Angles A–E + Reuse/Simplification/Efficiency + Altitude + Conventions) | up to 8 each | recall-biased | Phase 3 sweep | 15 | "reviewing for **recall** at extra-high effort... a missed bug ships." |
| **max** | same 10 as xhigh | up to 8 each | recall-biased | Phase 3 sweep | 15 | Same as xhigh but framed "maximum effort" |
| **ultra** | *(not a local prompt)* — hands off to a cloud-hosted deep multi-agent review via `claude ultrareview` | — | — | — | — | Requires claude.ai account access; falls back to a local run at the otherwise-selected level if unavailable. |

When the Agent tool isn't available at all, every level collapses to a
single-pass inline review done by the main thread itself, working through
every angle in one context — the report says explicitly that this was a
single-pass review without the fan-out, "so whoever reads it isn't misled
about what actually ran."

Internally there are also alternate prompt variants keyed by model family
(e.g. distinct low/medium/high/xhigh phrasing for `claude-sonnet-5` vs
`claude-opus-4-8` vs a generic default, plus older `o48-*` legacy variants) —
the ladder above describes the default/current-generation shape; the
model-family variants tweak wording and the diff-size finder-budget hint but
keep the same phase structure.
