# TODOS — Dev A (Token Machinery & Tooling)

**Role:** Developer A
**Phase:** Build 1 — post-research
**Last updated:** 8 Oct 2026
**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE

---

## Status legend

- ☑ Done
- ◐ In progress
- ☐ Todo
- ⛔ Blocked / needs a decision

---

## Next up

| # | Task | GAP id | Why now |
|---|---|---|---|
| 1 | `pyproject.toml` + test config so `pytest` works repo-root | G8 | Unblocks the "25 tests" repro claim; bluntest "does it even run" probe |
| 2 | Seeded generator module + provenance sheet | G1 | Everything depends on it; dev_B's twin needs it |
| 3 | Live-classifier runner + 15 s watchdog → video | G2 | The single "live" beat we promise; without it the honesty story breaks |
| 4 | P1/P2/P3 provider dimensions in `_DIMENSIONS` + coverage counts | G9 | "Where is the provider ledger?" has no cell in the show-me-the-code matrix |
| 5 | Coverage-report entrypoint decision | G7 | Blocked on no-CLI tension (see below) |

---

## Backlog

| # | Task | Spec anchor | GAP id | Status |
|---|---|---|---|---|
| 1 | Packaging (pyproject + test config) | — | G8 | ☐ |
| 2 | Seeded generator + provenance sheet | §4.4, §10 | G1 | ☐ |
| 3 | Live-classifier runner + watchdog | §10 | G2 | ☐ |
| 4 | P1/P2/P3 provider fields in code | §3.1 | G9 | ☐ |
| 5 | Coverage-report entrypoint | §3.1 | G7 | ⛔ |

---

## Done

| Item | Evidence |
|---|---|
| Taxonomy (stdlib-only) | `cadence/cadence/taxonomy.py` — `classify()` returns exactly one code; 98,304-state partition |
| CoverageReport + coverage_report() | `taxonomy.py:302`, `taxonomy.py:331` |
| 25/25 tests | `cadence/tests/test_taxonomy.py` (24) + `test_toolchain.py` (1) |
| W1–W9 exhaustive, exclusive, reachable | `test_taxonomy.py` — all 98,304 states enumerated, 0 uncovered |
| W5 ≠ W6 distinct | Pinned by test (fatal A1) |
| No dead codes | Every code fires on ≥1 state |
| Data gap → no ledger row | Pinned by test |
| Docstring truth (G6) | `taxonomy.py:277` reads 98,304 (not 32,768) |

---

## Blocked / needs a decision

| Item | Blocker | Needed from |
|---|---|---|
| Coverage-report entrypoint (G7) | ADVERSARIAL §5 says "no CLI, no CSV repo"; G7 proposes `python -m cadence.report` | Team decision: re-word §5 or mark G7 as deliberate supersession |

---

## Standing rule

Every item will be presented on stage as either **implemented** (with a file:line), **specified** (B), or the exact sentence **"Not currently supported by the implementation."** No item crosses from "to build" to "built" inside a demo without a test run beside it.
