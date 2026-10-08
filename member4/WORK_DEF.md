# WORK_DEF — Member 4 (Delivery & Demo)

**Role:** Member 4
**Phase:** Build 1 — post-research
**Last updated:** 8 Oct 2026
**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE

---

## Mission

Own the stage story — the 4:30 / 3-minute deck, the judge cards, and the fail-safes that survive live — so that the demo matches the spec beat-for-beat, every number is labelled, and the worst case is still 4:30.

---

## In-scope responsibilities

1. **8-beat deck rebuild** (G3) — rebuild to the 8 specified beats (0–7) with per-beat windows and SIMULATED labels. Current `DEMO_AND_JUDGE_PACK.md` has 7 beats, no beat 0, mismatched timings.
2. **Corrected seven-gate card** (G4) — print the seven §6.4 thresholds everywhere: median < 20%, P90 < 30%, ±3 pp abandonment, W9 < 2% + coverage, stage-order < 1%, short-idle < 10%, first-tap P95 < 10 min. Flag the spec `:667` "six" line in the sync log.
3. **Corrected source card** (G5) — rewrite the judge-card sources block verbatim per QA file §17 row 2 + §25 item 9. CAG "Chapter IV" → III; LASI "best domain" → worst (4.6%); Kemdirim "2022" → 2021; "87.30% walk-ins" → visited directly.
4. **Version banner sweep** (G14) — sweep every deck/QA/card to v4.0. Current pack header/footer say "v2".
5. **Pre-rendered demo video + offline LAN duplicate** — 4:30 MP4 in a second tab, plus offline LAN duplicate.
6. **One genuinely live computation** — wire dev_A's live-classifier runner (G2) to the slide. Re-running W1–W9 attribution live over the day's token log (fast, deterministic, non-Monte-Carlo).
7. **Three-minute variant** — beats 0, 1, 2, 4, 7 re-timed to 12 + 60 + 55 + 25 + 28 = 180 s.
8. **Printed judge card** — seven thresholds, seven unknowns with owners, sources with URLs, regeneration command.
9. **15-second fail-safe rule** — if not working within 15 seconds, cut to pre-rendered video. The 15 seconds are drawn from beat 0's allocation, not added to it.

---

## Out of scope

- Writing code (dev_A / dev_B own that).
- Models, twin, RSR (dev_B owns those).
- Taxonomy, generator (dev_A owns those).
- Editing the canonical spec.

---

## Definition of Done

| Responsibility | DoD |
|---|---|
| 8-beat deck (G3) | Matches §10 beat table exactly; per-beat windows; SIMULATED labels; no beat 0 missing |
| Seven-gate card (G4) | Seven thresholds printed everywhere; spec `:667` "six" flagged in sync log |
| Source card (G5) | Verbatim per QA §17/§25; CAG III; LASI worst 4.6%; Kemdirim 2021; "visited directly" |
| Version sweep (G14) | All deck/QA/card footers say v4.0 |
| Pre-rendered video | 4:30 MP4 in second tab; offline LAN duplicate |
| Live computation | W1–W9 re-run live over day's token log; deterministic; non-Monte-Carlo |
| 3-min variant | Beats 0,1,2,4,7 = 180 s |
| Printed judge card | Thresholds, unknowns, sources, regeneration command |
| Fail-safe | 15 s watchdog; worst case still 4:30 |

---

## Handoffs

| Direction | What | To/From |
|---|---|---|
| → | Deck + cards | Stage |
| → | Claim-check request | research |
| ← | Live runner | dev_A |
| ← | Source card + seven-gate card | research |
| ← | Twin + RSR fixtures | dev_B |

---

## Guardrails

- **No slide claims anything the ledger cannot reproduce.**
- **SIMULATED labelling.** Every demo number labelled `SIMULATED`; twin marked `UNGATED`.
- **Worst case still 4:30.** The 15 s fail-safe is drawn from beat 0, not added.
- **No banned phrases.** Never "six causes"; never "two taps per patient"; never claim CLI/API/CSV dependence.
- **No apology.** Keep talking.
- **Sources with URLs.** Every headline number traceable.

---

## References

- `PROJECT_SOLUTION_FINAL.md` v4.0 — §10 demo (8 beats), §6.4 gate, §11 judging criteria
- `TECH_STACK.md` — §8 build order
- `HACKATHON_BUILD_GAPS.md` — G3, G4, G5, G14
- `HACKATHON_JUDGE_QA.md` — §17 row 2, §25 item 9 (source corrections)
- `DEMO_AND_JUDGE_PACK.md` — current pack (7 beats, superseded by G3)
- `ADVERSARIAL_REVIEW_V4.md` — adversarial review
