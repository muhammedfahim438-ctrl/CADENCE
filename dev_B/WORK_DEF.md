# WORK_DEF — Dev B (Models, Twin, RSR & MIS)

**Role:** Developer B
**Phase:** Build 1 — post-research
**Last updated:** 8 Oct 2026
**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE

---

## Mission

Build the engines that run only when the gate runs — arrival/no-show models, the queue digital twin, RSR bipartite matching, and the CAG/MIS export — so that every recommendation is priced, every refusal is honest, and no claim survives without a gate pass.

---

## In-scope responsibilities

1. **Arrival-rate model** — `HistGradientBoostingRegressor`, 15-min bins, CPU-only. Patients per bin.
2. **No-show model** — gradient-boosted + isotonic calibration. `P(no-show)` per booked slot at T-24h and T-90min. Calibration over AUC — threshold is a capacity policy knob.
3. **Queue digital twin** (G13) — stochastic DES, live-fitted from Waste Ledger parameters. Counterfactual flow; reconfiguration search; `net_value` ranking; refusal path.
4. **RSR bipartite matching** — released-slot matching on administrative compatibility first (specialty, slot type, follow-up status), expected marginal wait reduction second. Walk-in P90 non-regression is a hard constraint.
5. **Validation-gate harness** (G10) — reads a held-out ledger, prints pass/fail vs the seven §6.4 thresholds + no-show calibration gate. Build before demoing the twin.
6. **MIS export schema** (G11) — documented CSV/JSON export of the ledger (codes, providers, coverage). CAG field names + mapping table. Export can stay simulated.
7. **No-show decision-record lane** (G12) — computed once, append-only, never displayed/exported/joined. Labelled demo fixture.
8. **CAG mapping table** — shipped artefact showing what is and is not comparable to auditor metrics.

---

## Out of scope

- Taxonomy, generator, packaging (dev_A owns those).
- Deck, judge cards, demo video (member4 owns those).
- Clinical logic, triage, severity — never.
- Cross-hospital "AI" training — methodologically wrong (G20).
- Cloud / SaaS control plane — one hospital, one OPD, LAN appliance (G17).

---

## Definition of Done

| Responsibility | DoD |
|---|---|
| Arrival model | Publishes patients per 15-min bin; fitted on days 1–7 |
| No-show model | Calibration curve in repo; ECE < 0.05 on held-out slots; threshold = policy |
| Twin (G13) | Live-fitted DES; `net_value(π) = predicted_recovered_clinical_minutes(π) − clinician_minutes_cost(π)`; refusal path returns "do not do this" when net_value ≤ 0 |
| RSR | Bipartite matching; walk-in P90 never worsens; no clinician name in SMS |
| Gate harness (G10) | Prints pass/fail vs seven thresholds + no-show calibration gate; can print FAIL |
| MIS export (G11) | Documented schema; CAG field names; mapping table shipped |
| Decision-record lane (G12) | Append-only; never displayed/exported/joined; labelled fixture |
| CAG mapping table | Shipped artefact; every metric mapped or declared not comparable |

---

## Handoffs

| Direction | What | To/From |
|---|---|---|
| → | Gate harness + twin results | research (claims audit) |
| → | Twin + RSR fixtures | member4 (demo beats 3–5) |
| → | MIS export schema | research (CAG vocabulary) |
| ← | Generator + taxonomy | dev_A |
| ← | No-CLI/CSV decision | research / team |

---

## Guardrails

- **Calibration over AUC.** The threshold is a capacity policy knob; probabilities must be trustworthy.
- **Gate can fail.** If any §6.4 threshold fails, CADENCE ships Phase 1 only. No models, no recommendations, no RSR.
- **Per-site fitting.** A flow model that transfers across sites without re-fitting is a flow model that is wrong.
- **Walk-in P90 non-regression.** Hard constraint in RSR objective; no match → "do not do this."
- **No per-clinician scoring.** Department-level reporting is the ceiling.
- **No clinician name in SMS.** Administrative compatibility only.
- **Append-only decision log.** Every model action logged with inputs, model version, confidence.
- **SIMULATED labelling.** Every demo number labelled `SIMULATED`; twin marked `UNGATED`.

---

## References

- `PROJECT_SOLUTION_FINAL.md` v4.0 — §3.2 twin, §3.3 RSR, §6.1 models, §6.4 gate, §7 metrics
- `TECH_STACK.md` — §3 Engines 2–3, §6 validation gate
- `HACKATHON_BUILD_GAPS.md` — G10, G11, G12, G13
- `cadence/cadence/taxonomy.py` — Waste Ledger input
- `ADVERSARIAL_REVIEW_V4.md` §5 — no-CLI/no-CSV tension
