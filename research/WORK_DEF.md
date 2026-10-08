# WORK_DEF — Research (Evidence & Claims Owner)

**Role:** Research member
**Phase:** Build 1 — post-research
**Last updated:** 8 Oct 2026
**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE

---

## Mission

Own the evidence base, the honesty spine, and the judge-ready story — so that every claim on stage is traceable, every unknown is named, and no document drifts from the canonical spec.

---

## In-scope responsibilities

1. **Canonical spec** — `PROJECT_SOLUTION_FINAL.md` v4.0 is the authority. Research owns it; nobody edits it beyond the repo line.
2. **Claim-class tags** — every claim carries a class (A–E). Research assigns and audits them.
3. **Unknowns ledger** — unknowns #1–#7, each with an owner. Research tracks and updates.
4. **Source verification** — LASI, CAG, Kemdirim, HMIS, Nigerian comparator. Every headline number traceable to a named source with URL.
5. **Sync log** — spec-vs-doc drift (e.g., spec `:667` "six gate thresholds" vs seven gates; bible `:372` "858 lines" vs 860). Research logs and flags.
6. **Judge QA** — `HACKATHON_JUDGE_QA.md` is the audit workbook. Research answers and maintains it.
7. **Adversarial review** — `ADVERSARIAL_REVIEW_V4.md`. Research re-runs the adversarial pass before stage.
8. **Demo pack** — `DEMO_AND_JUDGE_PACK.md` drafted at research handoff; superseded by member4's 8-beat rebuild (G3).

---

## Out of scope

- Writing code (dev_A / dev_B own that).
- Building the deck (member4 owns that).
- Answering unknowns #4 / #5 / #6 without measurement — research never fills a gap with an assumption.

---

## Definition of Done

| Responsibility | DoD |
|---|---|
| Spec canon | v4.0 locked; repo URL stamped on all 9 files; no edits beyond repo line |
| Claim classes | Every claim in every doc tagged A–E; untagged claims flagged |
| Unknowns | #1–#7 each have an owner and a status (open / measured / resolved) |
| Sources | Every headline number has a named source + URL; re-verified pre-stage |
| Sync log | All known drift items logged with file:line and resolution status |
| Judge QA | Q4 (if-else/ML) and Q9 (SMS) carry no raw tap-claims; "two taps" only in guard rows |
| Adversarial | V4 review complete; §5 "What actually ships" appended; no-CLI/no-CSV tension logged |

---

## Handoffs

| Direction | What | To/From |
|---|---|---|
| → | Source card (corrected, verbatim) | member4 |
| → | Seven-gate card | member4 |
| → | Claim-class audit of deck | member4 |
| ← | Model results + gate pass/fail | dev_B |
| ← | Generator + taxonomy test results | dev_A |
| ← | Deck for claim-check | member4 |

---

## Guardrails

- **Banned phrases:** never "six causes" (nine codes W1–W9); never "two taps per patient" (seven taps on counter→clinician path); never claim CLI/API/CSV dependence.
- **No fabrication:** no invented studies, no reused retracted stats, no "share of voice" claims.
- **SIMULATED labelling:** every demo number labelled `SIMULATED`; twin marked `UNGATED`.
- **Gate can fail:** if any §6.4 threshold fails, CADENCE ships Phase 1 only. Research never softens this.
- **Ethics spine:** no clinical function, no individual scoring, no clinician name in SMS, DPDP consent architecture.

---

## References

- `PROJECT_SOLUTION_FINAL.md` v4.0 — canonical spec (860 lines)
- `TECH_STACK.md` — build reference
- `HACKATHON_BUILD_GAPS.md` — G1–G20 backlog
- `HACKATHON_JUDGE_QA.md` — audit workbook
- `ADVERSARIAL_REVIEW_V4.md` — adversarial review (165 lines)
- `PROJECT_BIBLE.md` — constraints and guardrails
- `DEMO_AND_JUDGE_PACK.md` — demo pack (drafted, superseded by G3)
