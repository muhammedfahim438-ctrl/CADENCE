# TODOS — Research (Evidence & Claims Owner)

**Role:** Research member
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

| # | Task | Why now |
|---|---|---|
| 1 | Reconcile no-CLI/CSV tension (ADVERSARIAL §5 vs G7/G11) | Blocks dev_A's report-entrypoint decision; must be resolved before any "what we ship" claim |
| 2 | Re-verify all source URLs pre-stage | A precise judge catches a citation error; the entire "we read the sources" credibility is one line away |
| 3 | Keep sync log current | Spec `:667` six→seven gates; bible `:372` 858→860 — both report-only, both must stay logged |

---

## Backlog

| # | Task | Spec anchor | GAP id | Status |
|---|---|---|---|---|
| 1 | Reconcile no-CLI/CSV tension | ADVERSARIAL §5 vs G7/G11 | — | ☐ |
| 2 | Re-verify source URLs (LASI, CAG, Kemdirim, HMIS) | §0.1, §5.3 | G5 | ☐ |
| 3 | Confirm booked-share measurement phrasing (unknown #6) | §9.2 | — | ☐ |
| 4 | Sign off on G7/G11 no-CLI reconciliation | — | G7, G11 | ☐ |
| 5 | Pre-stage adversarial re-review | — | — | ☐ |

---

## Done

| Item | Evidence |
|---|---|
| Spec v4.0 locked | `PROJECT_SOLUTION_FINAL.md` — 860 lines, repo URL stamped |
| Adversarial review V4 | `ADVERSARIAL_REVIEW_V4.md` — 165 lines, §5 appended |
| QA workbook | `HACKATHON_JUDGE_QA.md` — Q4/Q9 consistent; "two taps" only in guard rows |
| Demo pack drafted | `DEMO_AND_JUDGE_PACK.md` — superseded by member4's G3 rebuild |
| Build-gaps catalogue | `HACKATHON_BUILD_GAPS.md` — G1–G20, P0/P1/P2 |
| Tech stack doc | `TECH_STACK.md` — build reference |
| Repo URL stamp | 9/9 files stamped |
| 25/25 tests verified | `cadence/tests/` — taxonomy + toolchain |
| Bible sync | `PROJECT_BIBLE.md` — §14 pointer, §5.1/§5.2, stale flags cleared |

---

## Blocked / needs a decision

| Item | Blocker | Needed from |
|---|---|---|
| No-CLI/CSV tension | ADVERSARIAL §5 says "no CLI, no CSV repo"; G7 proposes `python -m cadence.report`; G11 proposes MIS CSV/JSON export | Team decision: either re-word §5 or mark G7/G11 as deliberate supersessions |
| Clinical sponsorship | Not yet secured — project's largest risk (relationship, not technical) | User / team |

---

## Standing rule

Every item will be presented on stage as either **implemented** (with a file:line), **specified** (B), or the exact sentence **"Not currently supported by the implementation."** No item crosses from "to build" to "built" inside a demo without a test run beside it.
