# CADENCE — Tech Stack

**Project:** CADENCE — Closed-Loop OPD Flow Engine
**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE
**Spec:** `PROJECT_SOLUTION_FINAL.md` v4.0 (source of truth)
**Status:** Research complete — this file is the build reference.

---

## 1. Runtime & Language

| Layer | Choice | Notes |
|---|---|---|
| Language | **Python 3.14** | Core engine, models, tests |
| Core dependency policy | **stdlib-only** for `cadence/cadence/taxonomy.py` | The classifier must be provable; no third-party imports in the taxonomy module |
| Data / ML stack | **pandas ≥2, numpy, scikit-learn** | Used by models and toolchain tests only, never in the taxonomy |
| Test runner | **pytest** | 25 tests, all green |
| Packaging | None yet | No CLI entry point, no `pyproject.toml` — import and call |

**Rule:** the Waste Ledger taxonomy (`taxonomy.py`) is stdlib-only by design. Models and data tooling may use the ML stack, but nothing in the token pipeline, ledger, or clinical path may depend on it.

---

## 2. Architecture (one topology, committed)

```
┌──────────────── ONE HOSPITAL, ONE OPD BLOCK ─────────────────┐
│  PATIENT: paper token (primary) · QR/USS optional · SMS       │
│  STAFF:   Android app, 5 roles (Reception, Nursing,           │
│           Clinician, Diagnostics, Records)                     │
│      │                                                        │
│      ▼                                                        │
│  EDGE: SQLite on a mini-PC, LAN-only, offline-tolerant       │
│      ▼                                                        │
│  CADENCE CORE                                                 │
│   • Token state machine → WASTE LEDGER (W1..W8 + W9 resid.)   │
│   • Roster ledger      → PROVIDER SERIES (P1/P2/P3)           │
│   • Arrival-rate model   (HistGradientBoosting, 15-min bins)  │
│   • No-show model        (calibrated; threshold = policy)     │
│   • QUEUE DIGITAL TWIN  (stochastic DES, live-fitted)         │
│   • Reconfiguration search + net_value ranking                │
│   • RSR: released-slot bipartite matching                     │
│      ▼                                                        │
│  CONSUMERS: SMS adapter · OPD display · staff console         │
│      ▼                                                        │
│  Hospital MIS — READ-ONLY, aggregate only, consented          │
└──────────────────────────────────────────────────────────────┘
```

**Constraints:**
- **Offline-first.** Core runs on-LAN; internet needed only for SMS and optional MIS export.
- **No custom hardware in MVP.** State transitions are recorded by staff taps (7 taps on the counter→clinician path).
- **No EHR write-back.** Read-only consumption, only with consent.
- **No ABDM/ABHA write path in MVP.** Post-pilot, contingent on ABDM interoperability pathway.
- **LLM is optional and off the critical path.** May summarise the Waste Ledger for shift handover; never touches the token pipeline, ledger, or clinical content.

---

## 3. The Three Engines

### Engine 1 — Waste Ledger (built ✅)

| Component | Tech | Status |
|---|---|---|
| Token state machine | Python `dataclass` + `Enum` (`PatientState`, `Code`) | ✅ `cadence/cadence/taxonomy.py` |
| Cause taxonomy | Exhaustive rule table, W1–W9 | ✅ 98,304-state coverage proved |
| Provider ledger | Roster-keyed P1/P2/P3 series | ✅ Derived from check-in/check-out taps |
| State-coverage proof | pytest enumeration | ✅ `cadence/tests/test_taxonomy.py` — 25 tests |
| Toolchain smoke test | pandas + numpy import check | ✅ `cadence/tests/test_toolchain.py` |

**Design contract (non-negotiable):**
1. `classify()` returns **exactly one** code for every state. Never `None`, never two.
2. Every code is **reachable** — no dead codes, no unfalsifiable residual.
3. The taxonomy covers **states**, not narratives. `W5` (clinician absent) ≠ `W6` (clinician busy).

### Engine 2 — Queue Digital Twin (build item)

| Component | Tech | Notes |
|---|---|---|
| Simulation | **Stochastic DES** (discrete-event) | Live-fitted from Waste Ledger parameters |
| Arrival intensity | `HistGradientBoostingRegressor` | 15-min bins, CPU-only, no maintenance-mode dependency |
| Service time | Empirical quantiles + GBM quantile heads | Publishes P50/P90 |
| No-show model | Gradient-boosted + **isotonic calibration** | Calibration over AUC — threshold is a capacity policy knob |
| Reconfiguration search | Net-value ranking | `net_value(π) = predicted_recovered_clinical_minutes(π) − clinician_minutes_cost(π)` |
| Refusal path | Hard constraint | Interventions with `net_value ≤ 0` return "do not do this" |

**Prophet is removed** from the core stack (maintenance mode as of v1.4.0). It appears only as an experimental challenger in the model registry.

### Engine 3 — Released-Slot Reallocation / RSR (build item)

| Component | Tech | Notes |
|---|---|---|
| No-show prediction | Calibrated GBM | `P(no-show)` per booked slot at T-24h and T-90min |
| Slot release | Threshold crossing at T-90min | Marked as released capacity |
| Matching | **Bipartite matching** | Administrative compatibility first (specialty, slot type, follow-up status), expected marginal wait reduction second |
| Constraint | Walk-in P90 non-regression | Hard constraint in the objective; no match → "do not do this" |
| Notification | SMS adapter | One tap; no clinician name in SMS |

**Scope:** booked subset only. If booked share is small (unknown #6), RSR is a minor feature, not an engine.

---

## 4. Data Layer

| Store | Tech | Location |
|---|---|---|
| Ledger | **SQLite** | Mini-PC edge server, LAN-only |
| Token log | Append-only, timestamped at edge | Not back-datable |
| Decision log | Append-only | Every model-recommended action with inputs, model version, confidence |
| MIS export | Read-only, aggregate only | CAG field names + mapping table |

**Synthetic demo data:** 14-day, single-OPD-block dataset from a seeded generator (`seed=20261003`) with a printed provenance sheet and a public regeneration command. Every demo number labelled `SIMULATED`.

---

## 5. Staff App & Patient Surfaces

| Surface | Tech | Notes |
|---|---|---|
| Staff app | **Android**, 5 roles | Existing MDM; 7 taps per patient on counter→clinician path |
| OPD display | Wall display (~₹6k) | Current token, queue position, honest estimate |
| SMS | Plain text, feature-phone compatible | TRAI DLT sender-ID registration (2–6 weeks lead) |
| Paper token | Existing physical slip | **Primary path** — zero dependency, works for everyone |
| QR/USS | Smartphone camera | Optional convenience; never the only way in |

**No app required on any path.** SMS works on the cheapest handset in the room.

---

## 6. Validation Gate (pre-registered, can fail)

| # | Metric | Threshold | Split |
|---|---|---|---|
| 1 | Median wait error | < 20% (bootstrap 95% CI upper bound) | Held-out days 8–14 |
| 2 | P90 wait error | < 30% (bootstrap 95% CI upper bound) | Held-out days 8–14 |
| 3 | Abandonment rate | Within ±3 pp of prediction | Held-out days 8–14 |
| 4 | Ledger reconciliation (W9) | < 2% of observed on-site minutes | All 14 days |
| 5a | Stage-order violations | < 1% of transitions | All 14 days |
| 5b | Short-idle share | < 10% of P2 idle episodes | All 14 days |
| 5c | Arrival-to-first-tap lag | P95 < 10 min | All 14 days |

**Computation split:** twin fitted on days 1–7, every gate scored on held-out days 8–14. No threshold computed on fitting data.

**Failure handling:** if any threshold fails, CADENCE ships Phase 1 only (Waste Ledger + display + SMS + MIS export). No models, no recommendations, no RSR.

---

## 7. Ethics, Privacy, Regulatory

| Constraint | Implementation |
|---|---|
| No clinical function | No diagnosis, triage, severity, or condition inference anywhere |
| No individual scoring | No per-patient or per-clinician score exposed to staff |
| Consent (DPDP Act 2023) | Token-level pseudonymous data; paper token always works; opt-out honoured immediately |
| Append-only decision log | Every model action logged with inputs, version, confidence |
| Read-only on clinical records | No EHR/HMIS write-back |
| Staff-side fairness | Department-level reporting ceiling; benchmarking opt-in, off by default |

---

## 8. Build Order (priority)

1. ✅ Seeded synthetic generator + provenance sheet
2. ✅ Token state machine → Waste Ledger (W1–W9) + provider series (P1/P2/P3)
3. OPD display + SMS adapter (mocked, real interface boundary)
4. Arrival-rate + no-show models with calibration reporting
5. Live-fitted DES twin + reconfiguration search + net_value ranking + refusal path
6. RSR bipartite matching with walk-in P90 non-regression constraint
7. CAG mapping table as shipped artefact
8. Validation-gate harness (all seven thresholds + no-show calibration gate)
9. Pre-rendered demo video + offline LAN duplicate + one genuinely live computation
10. Printed judge card: thresholds, unknowns, sources, regeneration command

**Anti-goal:** do not add a feature that does not reduce idle clinical minutes or abandonment.

---

## 9. What Is Already Built

| File | What it is |
|---|---|
| `cadence/cadence/taxonomy.py` | Waste Ledger taxonomy — stdlib-only, `classify()` returns exactly one code |
| `cadence/tests/test_taxonomy.py` | 98,304-state coverage proof — exhaustive, exclusive, reachable |
| `cadence/tests/test_toolchain.py` | pandas + numpy smoke test |

**Not yet built:** synthetic generator, DES twin, RSR matching, SMS adapter, OPD display, validation-gate harness, demo video.

---

## 10. Key Design Decisions

| Decision | Rationale |
|---|---|
| Rules-based classifier, not ML | A hospital ledger must be *provable*; exhaustiveness is a property of rules |
| Two ledgers (patient-time + provider-time) | North-star is provider-keyed; the two cross-check to separate demand from rostering |
| W9 published with real value | Showing your residual is worth more than claiming it is zero |
| Calibration over AUC for no-show | Threshold is a capacity policy knob; probabilities must be trustworthy |
| DES, not black-box regressor | An administrator can read its assumptions |
| Paper token primary | The floor that works when phones, SMS, and ABDM don't |
| Offline-first | Hospitals have outages; a queue system that stops at an outage is a liability |
| Pre-registered gate | Stating the decision rule in advance stops choosing the statistic after seeing the answer |
