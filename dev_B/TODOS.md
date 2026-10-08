# TODOS — Dev B (Models, Twin, RSR & MIS)

**Role:** Developer B
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
| 1 | Gate harness vs synthetic held-out ledger | G10 | Build before demoing the twin — it is what makes the twin claimable |
| 2 | Arrival-rate + no-show models + calibration curve | G10, G12 | No-show calibration gate is part of the harness |
| 3 | DES twin + reconfiguration search + net_value + refusal path | G13 | Beats 3–5 must otherwise be pure narration |
| 4 | RSR bipartite matching + walk-in P90 non-regression | — | Requires Phase 0(b) booked-share measurement |
| 5 | MIS export schema + CAG mapping table | G11 | Downstream "what does the hospital export" is vague |
| 6 | No-show decision-record lane fixture | G12 | The corrected Q3 answer has no artefact behind it |

---

## Backlog

| # | Task | Spec anchor | GAP id | Status |
|---|---|---|---|---|
| 1 | Gate harness (7 thresholds + no-show calibration) | §6.4 | G10 | ☐ |
| 2 | Arrival-rate model (HistGradientBoosting, 15-min bins) | §6.1 | — | ☐ |
| 3 | No-show model (calibrated; ECE < 0.05) | §6.1, §6.4 | — | ☐ |
| 4 | DES twin + net_value + refusal path | §3.2 | G13 | ☐ |
| 5 | RSR bipartite matching + P90 non-regression | §3.3 | — | ☐ |
| 6 | MIS export schema + CAG mapping table | §4.1 | G11 | ☐ |
| 7 | No-show decision-record lane fixture | §13.2 | G12 | ☐ |

---

## Done

| Item | Evidence |
|---|---|
| (Nothing yet — build phase starting) | — |

---

## Blocked / needs a decision

| Item | Blocker | Needed from |
|---|---|---|
| Gate harness | Twin must be fitted on days 1–7 and scored on held-out days 8–14; needs dev_A's generator (G1) | dev_A |
| RSR | Requires Phase 0(b) booked-share measurement; if booked share is small, RSR is deprioritised | research / team |
| MIS export (G11) | ADVERSARIAL §5 says "no CSV repo"; G11 proposes documented CSV/JSON export surface | Team decision: re-word §5 or mark G11 as deliberate supersession |

---

## Standing rule

Every item will be presented on stage as either **implemented** (with a file:line), **specified** (B), or the exact sentence **"Not currently supported by the implementation."** No item crosses from "to build" to "built" inside a demo without a test run beside it.
