# Rust Learning Plan — Log-Parsing CLI (4h/week, 3 months)

## 0. Diagnosis

- **Goal state (observable):** write and run a working CLI that reads a log file, filters/aggregates lines (e.g. by level, count per source, extract timestamps), and exits 0 with correct output — with unit tests passing via `cargo test`. Modeled on your existing `logscan` project, but in Rust.
- **Current state (assumed):** you already know how to parse logs and structure a small CLI in another language (you built logscan). You have **not** used Rust's ownership/borrowing model. This plan assumes zero Rust but real programming experience — it does not re-teach "what is a loop."
- **Budget:** 4 h/week × ~12 weeks ≈ **48 hours total**. New material 1–2 sessions/week; the rest is review.
- **Failure history:** none reported. The main risk is scheduling (missed weeks), so this plan builds in ~40% slack and a weekly minimum session.

---

## 1. Dependency map

Legend: **[C]** core (on the critical path) · **[S]** supporting (needed by core) · **[P]** peripheral (deferred/cut).

```
N1  Toolchain: rustup, cargo new, cargo build/run/test        [C]  (nothing depends on it; everything depends on it)
N2  Syntax: variables, types, control flow, functions          [C]  ← N1
N3  Ownership & borrowing (the core mental model)              [C]  ← N2
N4  Structs, enums, pattern matching                            [C]  ← N2
N5  Error handling: Result/Option, ? and unwrap                 [C]  ← N3, N4
N6  Traits + std::fs file reading                               [C]  ← N4
N7  String handling: String vs &str, splitting, parsing         [C]  ← N3, N6
N8  CLI: std::env args + basic parsing                          [C]  ← N5, N7
N9  Unit tests (cargo test)                                     [C]  ← N5
N10 Iterators & collections (Vec/HashMap) for aggregation       [C]  ← N4, N7
N11 Build the logscan CLI (the goal itself)                     [C]  ← N8, N9, N10
---
N12 Lifetimes (explicit)                                        [S]  ← N3   (needed to read real errors; NOT a separate deep dive)
N13 Modules & crates                                            [S]  ← N4
N14 Closures / iterators chaining                               [S]  ← N10
---
N15 Async (tokio)                                               [P]  CUT
N16 Macros (derive, custom)                                     [P]  CUT
N17 WebAssembly                                                 [P]  CUT
N18 Traits as generics / trait objects                          [P]  DEFER
N19 Cargo ecosystem (clap, serde)                               [P]  DEFER (use stdlib for the CLI; add later if needed)
```

**Critical path:** N1 → N2 → N3 → N4 → N5 → N7 → N8 → N9 → N10 → N11.
Note: **lifetimes (N12) are supporting, not on the critical path** — you learn enough to read borrow-checker errors, not a full lifetime theory. **Async is cut entirely** — a log-parsing CLI does not need it.

---

## 2. Schedule (12 weeks, review-first)

**Cadence:** 2 sessions/week × 2h. **Session A = review first (30–45 min), then new material. Session B = new material + hands-on project work.** Expanding review intervals: 1d → 3d → 7d → 14d → 30d.

**Weekly minimum viable session:** 15 minutes of due reviews only (keeps the chain alive on bad weeks).

| Week | New material (Session A) | Project work (Session B) | Reviews due |
|---|---|---|---|
| 1 | N1 toolchain + N2 syntax | cargo new; hello + first loop | — |
| 2 | N3 ownership & borrowing | small ownership exercises | N1, N2 |
| 3 | N4 structs/enums/pattern matching | model log line as struct | N2, N3 |
| 4 | N5 error handling (Result/Option) | read a file, handle missing file | N3, N4 |
| 5 | N6 traits + std::fs | read + iterate log lines | N4, N5 |
| 6 | N7 strings (String vs &str) | split lines, extract fields | N5, N6 |
| 7 | N8 CLI args + N9 tests | first `cargo test`; arg parsing | N6, N7 |
| 8 | N10 iterators & collections | aggregate counts per level | N7, N8, N9 |
| 9 | N11 build logscan v1 | implement filter + count | N8, N9, N10 |
| 10 | N11 build logscan v2 | add aggregation + output format | N9, N10 |
| 11 | N11 polish | error paths, exit codes, README | N10, N11 |
| 12 | N11 ship + retrospective | run on real logs; write retrospective | all |

**Slack:** weeks 9–12 are deliberately light on new material — if weeks 2–8 slip, the project weeks absorb the catch-up. ~40% of the 48h is review + slack, not new content.

---

## 3. Card deck (atomic, tagged)

Tags: `rust/<node>`. ~20 new cards/day cap; this deck is ~60 cards across the plan (≈5/week), well under the cap.

**N1 Toolchain**
- Q: What command creates a new Rust binary project in the current dir? → `cargo new <name>` (creates a binary crate). [rust/n1]
- Q: What's the difference between `cargo build` and `cargo run`? → `build` compiles; `run` compiles and executes. [rust/n1]

**N2 Syntax**
- Q: What is the default integer type in Rust? → `i32`. [rust/n2]
- Q: Which keyword declares a constant? → `const`. [rust/n2]

**N3 Ownership**
- Q: What happens to a value when it's assigned to a new variable? → The binding moves; the old variable is no longer usable. [rust/n3]
- Q: Which operator creates a shared (read-only) reference? → `&`. [rust/n3]
- Q: How many owners can a value have at once? → Exactly one. [rust/n3]

**N4 Structs/enums**
- Q: How do you define a struct with three fields? → `struct Name { field: Type, ... }`. [rust/n4]
- Q: What keyword introduces an enum variant? → `enum` with `Variant` cases. [rust/n4]

**N5 Error handling**
- Q: What does `Result<T, E>` represent? → A value of type T on success, or an error E. [rust/n5]
- Q: What does the `?` operator do inside a function returning Result? → Unwraps Ok or returns early with the Err. [rust/n5]

**N6 Traits + fs**
- Q: What is a trait in Rust? → A set of method signatures a type can implement. [rust/n6]
- Q: Which function reads a whole file into a String? → `std::fs::read_to_string(path)`. [rust/n6]

**N7 Strings**
- Q: What is the difference between `String` and `&str`? → `String` is owned/mutable; `&str` is a borrowed view of a string. [rust/n7]
- Q: Which method splits a string on a delimiter? → `.split(delim)`. [rust/n7]

**N8 CLI**
- Q: How do you read command-line arguments in stdlib? → `std::env::args()`. [rust/n8]

**N9 Tests**
- Q: What command runs the test suite? → `cargo test`. [rust/n9]
- Q: Which attribute marks a test function? → `#[test]`. [rust/n9]

**N10 Collections**
- Q: Which collection maps keys to values? → `HashMap`. [rust/n10]
- Q: What does `.iter()` give you over a Vec? → An iterator over the elements. [rust/n10]

**N11 Project**
- Q: What exit code should a CLI return on success? → 0. [rust/n11]

---

## 4. Resources (real, named)

| Node | Primary resource | Role |
|---|---|---|
| N1–N4 | **The Rust Book** (doc.rust-lang.org/book) — ch. 1–6 | primary |
| N3 | **Rustlings** (github.com/rust-lang/rustlings) — ownership exercises | primary (practice) |
| N5–N7 | **The Rust Book** ch. 7–10, 12 | primary |
| N8–N11 | **Rust by Example** (doc.rust-lang.org/rust-by-example) — CLI + file I/O examples | primary |
| N12 | The Rust Book ch. 10 (lifetimes) — read only the "borrow checker" parts | reference |

All three are real, free, official resources. No fabrication.

---

## 5. Operating rules

- **Session 1 (concrete kickoff):** install rustup, `cargo new logscan-rs`, write a hello-world, do the first 3 Rustlings ownership exercises, make the first 4 cards.
- **Review-first:** every session starts with due reviews. New material only after.
- **If behind:** cut scope (drop N13/N14, trim polish) before cutting reviews. Reviews are the asset.
- **Weekly checkpoint:** what was due, what was recalled, what lapsed (lapsed cards go back to the new-material lane).
- **Retrospective at week 12:** what made Rust learnable/hard for you; record it for the next plan.