# improve — T2 build trial (what was built)

User's go-ahead (from T1 proposals): **"yes — build the custom tool for the log format, and do the memory writes."**

Per the sandbox rules, the custom tool was registered to `/tmp/creator-sandbox/custom_tools/` (the real `create_custom_tool` registry was NOT called; simulated registration and noted). The memory writes were performed for real via `remember()`.

## Built

### 1. Custom tool: `parse_odd_log` (program-type)

- **Location:** `/tmp/creator-sandbox/custom_tools/parse_odd_log.json` (registry record) + `parse_odd_log.py` (program).
- **Contract:** JSON in / JSON out. Reads `{"log_text": "..."}` OR `{"file_path": "..."}` from stdin; writes `{"records": [...], "record_count": N}` to stdout.
- **Parameters:** `log_text` (string, optional), `file_path` (string, optional) — exactly one required, not both.
- **Tags:** `log,parse,logscan,pipe,key-value`.
- **What it does:** parses the user's odd pipe-separated `key=value` log format (e.g. `2026-09-01T14:22:10Z | level=INFO | msg="job started" | job=nightly`) into structured records, stripping quotes from values.

### 2. Memory writes (real, via `remember()`)

- `user_timezone_preference` → "User wants UTC everywhere in reports and headers — never local time. (From 2026-09-10 session: 'No — use UTC, not local time'; 'I said UTC — the report header still shows local.')"
- `logscan_project` → "logscan project: uses UTC timestamps everywhere; odd pipe-separated log format (key=value, e.g. '2026-09-01T14:22:10Z | level=INFO | msg=\"job started\" | job=nightly'); weekly CSV cleanup (strip header rows, dedupe, reorder columns). From 2026-09-10 session."

## Verification (tool runs, verbatim)

Runner convention matched: `echo '<json>' | python3 parse_odd_log.py`.

**Happy path — log_text:**
```
$ echo '{"log_text":"2026-09-01T14:22:10Z | level=INFO | msg=\"job started\" | job=nightly\n2026-09-01T14:25:00Z | level=ERROR | msg=\"timeout\" | job=nightly"}' | python3 parse_odd_log.py
{"records": [{"timestamp": "2026-09-01T14:22:10Z", "level": "INFO", "msg": "job started", "job": "nightly"}, {"timestamp": "2026-09-01T14:25:00Z", "level": "ERROR", "msg": "timeout", "job": "nightly"}], "record_count": 2}
```

**Happy path — file_path:**
```
$ echo '{"file_path":"/tmp/sample_odd.log"}' | python3 parse_odd_log.py
{"records": [{"timestamp": "2026-09-02T09:00:00Z", "level": "WARN", "msg": "disk full", "job": "backup"}], "record_count": 1}
```

**Failure path — missing param:**
```
$ echo '{}' | python3 parse_odd_log.py
{"error": "missing required parameter: provide 'log_text' or 'file_path'"}   (exit 1)
```

**Failure path — both params:**
```
$ echo '{"log_text":"x","file_path":"/tmp/sample_odd.log"}' | python3 parse_odd_log.py
{"error": "provide only one of 'log_text' or 'file_path'"}   (exit 1)
```

**Failure path — bad file:**
```
$ echo '{"file_path":"/tmp/does-not-exist.log"}' | python3 parse_odd_log.py
{"error": "cannot read file '/tmp/does-not-exist.log': [Errno 2] No such file or directory: '/tmp/does-not-exist.log'"}   (exit 1)
```

**Idempotency (same input twice → identical):**
```
run 1: {"records": [{"timestamp": "2026-09-01T14:22:10Z", "level": "INFO", "msg": "job started", "job": "nightly"}], "record_count": 1}
run 2: {"records": [{"timestamp": "2026-09-01T14:22:10Z", "level": "INFO", "msg": "job started", "job": "nightly"}], "record_count": 1}
```

## Report

- **What was learned:** the user wants UTC everywhere in reports/headers; the logscan project's durable facts (UTC, odd pipe-separated format, weekly CSV cleanup).
- **What was built:** `parse_odd_log` custom tool + two memory writes.
- **Where it lives:** tool at `/tmp/creator-sandbox/custom_tools/` (sandbox; real registry not touched); memories in the persistent memory store.
- **How it shows up next time:** the tool is discoverable for any future odd-log parsing; the memories are recalled automatically so the agent uses UTC and remembers the logscan project context without being re-told.

## Integrity

- Real custom-tools registry dir `/home/omnideck/custom_tools` does NOT exist (verified) — nothing written to live state.
- `/home/omnideck/apps/` = **2** apps (omnideck-refresh, omnideck-ui-refresh) — unchanged.
