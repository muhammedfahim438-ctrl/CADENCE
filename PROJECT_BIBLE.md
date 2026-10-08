# PROJECT BIBLE — CADENCE

**The single orientation document for this repository.** An AI (or human) that reads this file and nothing else should understand what this project is, what problem it solves, what exists today, which rules must never be broken, and where every file lives.

**Project:** CADENCE — Closed-Loop OPD Flow Engine (formerly *"Queue Intelligence"*)
**Tagline:** *Stop measuring the queue. Start closing it.*
**Event:** HackSpark 2026 · AI & ML Track — "Smart Hospital Queue Management"
**Team:** CATALYST CREW A · Nehru Arts and Science College, Coimbatore
**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE
**Source of truth:** `PROJECT_SOLUTION_FINAL.md` **v4.0** (Solution Specification, adversarial-review pass)

---

## 1. How to read this document

| If you need… | Read | Authority |
|---|---|---|
| Orientation, scope, rules, file map | **This file** | Orientation only — never overrides the spec |
| The solution itself — problem, engines, architecture, metrics, ethics, phases | `PROJECT_SOLUTION_FINAL.md` **v4.0** | **Authoritative.** Anything conflicting with it is wrong |
| Why the spec says what it says; what was fixed and why | `ADVERSARIAL_REVIEW_V4.md` | Authoritative history of the v3.1→v4.0 pass |
| Demo choreography, 90-second pitch, judge card, 15 cross-exam answers, rehearsal plan | `DEMO_AND_JUDGE_PACK.md` | **Current run book, synced against v4.0** (§14) |
| The code that exists today | `cadence/` | Executable truth about build status (§5) |

**Internal vs. submission documents.** `ADVERSARIAL_REVIEW_V4.md` §§1–3 are preparation material, explicitly *not* part of any submission. `PROJECT_DRAWBACKS.md` (v2 red-team review) is internal too. The claim ledger's "Removed — do not reinstate" list (§18 here) governs every public artifact.

**Reading order for a new contributor:** §2 (what this is) → §3–4 (problem + solution) → §5 (what's built) → §7 + §10 (the two mechanics everything hangs on: the ledger and the gate) → §18 (the rules). Then read `PROJECT_SOLUTION_FINAL.md` in full.

---

## 2. Identity and document history

### 2.1 Identity

- **Name:** CADENCE (v1/v2 documents used the name *Queue Intelligence*).
- **One-line thesis:** *Nobody owns measure → decide → intervene → verify at the token level. Both instruments India already runs — the national patient-experience survey and the CAG performance audit — can see the waiting problem; neither can act on it inside a shift. The gap is the absent loop, not absent data.*
- **Anti-goal (§18 of the spec):** do not add a feature that does not reduce idle clinical minutes or abandonment.

### 2.2 Document lineage v1 → v4

| Stage | Documents | What it contained | Status |
|---|---|---|---|
| **v1/v2** — "Queue Intelligence" | `PROJECT_EXPLANATION.md`, `Hackathon_Pitch_Slides.md`, `queue-explained.deck.md`, `CROSS_EXAM_AND_DEMO_CHECKLIST.md` | 4-module command center; cloud/multi-tenant SaaS; Django REST + React + Postgres + Redis + SimPy + Synthea; Prophet; headline claims 72→47 min peak wait (−35%), +12% utilisation; "two taps per patient"; NHAMCS as evidence | **Deleted 8 Oct 2026** (§17) |
| **v2 red-team review** | `PROJECT_DRAWBACKS.md` | 26 findings (8 fatal F1–F8, 11 serious S1–S11, 7 minor M1–M7); §5 triage verdict; §6 paste-ready limitations statement; §4 contradiction table | **Superseded for the solution spec by `ADVERSARIAL_REVIEW_V4.md`**; salvageable content harvested into §16 here |
| **v3 / v3.1** | `PROJECT_SOLUTION_FINAL.md` (rewritten) | Full spec rewrite with claim classes, gates, phases; v3.1 was a source-verification pass (rows V1–V4) that re-checked citations | **Superseded by v4.0 within the same file** — revision log deliberately kept (a log that hides its own errors is not a log) |
| **v4.0 — current** | `PROJECT_SOLUTION_FINAL.md` + `ADVERSARIAL_REVIEW_V4.md` | Adversarial review found **11 fatal / 15 serious / 6 minor**, all fixed; 2 of 8 sources could not be re-opened and were downgraded to A\* | **Source of truth** |
| **Demo/pitch** | `DEMO_AND_JUDGE_PACK.md` | 4:30 speaker script (8 beats), 90-second pitch, printed judge card, 15 cross-exam answers, rehearsal plan | **Current run book, synced against v4.0** — footer and supersede note say so (§14) |
| **Orientation** | `PROJECT_BIBLE.md` (this file) | Everything | Current |

### 2.3 What v4.0 changed at the design level (not wording)

1. **A1** — the six-cause taxonomy never partitioned a patient's timeline (no code for queueing behind a *busy* clinician, no nursing code at all). Rebuilt as an exhaustive nine-code state table `W1–W9`, proved by test.
2. **A2** — the north-star was not computable: "idle clinical minutes" is provider-keyed, the ledger was token-keyed. Fixed by adding the roster-keyed `P1/P2/P3` companion ledger.
3. Plus A3–A11 (partition claims rewritten; "the survey is the one the hospital answers to" replaced by "both instruments see it, neither can act inside a shift"; Nigeria held to the same two-hospital standard as Hyderabad; gate 5 split into clinician-side signals; "two taps" → **seven taps**; "four roles" → **five roles**; "clinical compatibility" → **administrative compatibility**; no-show score persistence claim corrected; RSR novelty claim **withdrawn**).
4. Serious B1–B11 changed published numbers (LASI "independent cuts" corrected + 59.1% positive reported; Nigeria 65.3% vs 70.7% unreconcilable, disclosed; Hyderabad restated as a *proportion* not a mean; paper token made the primary patient path; coverage metric added for the consent self-selection; gates given units/splits/decision rules; demo re-timed to exactly 180 s; all seven unknowns given owners + dates; CAG and NAMCS downgraded to A\*).

---

## 3. The problem (with evidence discipline)

### 3.1 The five-row evidence table

| # | Finding | Source | Class |
|---|---|---|---|
| 1 | Patient arrival flow exceeded doctor service rate in **every** OPD studied (4 departments, n=252). In orthopaedics, **85.71% of total on-site time was waiting to see a doctor**; 87.30% visited directly rather than by referral (*not* a walk-in rate); 63.89% newly registered | De, Gupta & Chakraborty (2024), *Dr Sulaiman Al Habib Med J* 6(3):136–141 | **B** |
| 2 | Nigerian public hospital: 86.7 of 122.6 min non-service time (paper reports 65.3%; 86.7÷122.6 = 70.7% — **cannot be reconciled, disclosed**); station waits 17.5/35.4/51.4 min vs 12.6 min consultation; better-staffed counter paired with **2.7× longer** encounter | Kemdirim et al. (2021), *Nigerian Med J* 62(6):325–333 | **C** (two-hospital contrast, existence proof only) |
| 3 | LASI patient-experience survey (Wave 1, fieldwork 2017-18, pub. 2024): waiting drew the **highest negative rating of the six domains** — 4.6% nationally, **9.5%** among public-facility outpatients — and the **lowest "very good" (15.0%)** and **highest neutral-or-worse (40.9%)** (so **59.1% rated it positively; we report that**); state spread to 30.7% (A&N). Not three independent cuts: negative is contained in neutral-or-worse | Ambade, Kim & Subramanian (2024), *Public Health in Practice* 8:100541 | **B** |
| 4 | Two government hospitals, Hyderabad: **40.2% reported ≥120-min waits at the HMIS site vs 23.4%** at the non-HMIS site (AOR 2.05, 95% CI 1.04–4.03). A **proportion**, not a mean. Two-site design — association only; we do not claim causation, and the argument does not depend on this row | *BMC Health Services Research* 26:945 (2026), n=214 | **B** |
| 5 | India's auditor already collects OPD flow, waiting time, cases per doctor, consultation time — **Chapter III**, CAG Report 2 of 2025 (UT of J&K, period ended March 2022). Site unreachable on re-check | CAG of India | **A\*** |

### 3.2 The thesis (§2 of the spec)

- The queue is a **capacity condition**, not a friction condition: registering faster does not create doctor-minutes (rows 1–2).
- The waste is large and asymmetric, and **not evenly addressable** — addressable share is **unknown #5**.
- Software alone does not close it: an HMIS is not, on its own, evidence of a shorter queue (row 4, read narrowly).
- **Both instruments see it; neither can act on it inside a shift.** The missing thing is not measurement. It is the loop.

### 3.3 Claim evidence classes (§5.1 of the spec)

| Class | Meaning | How it may be pitched |
|---|---|---|
| **A** | Verified primary source | Assert plainly |
| **A\*** | Official document; specific detail **not re-verified** in the v4 audit pass (CAG, NAMCS) | Assert only what is low-risk; nothing load-bearing may depend on the unverified detail |
| **B** | Published study | Assert **with setting stated inline, every time** |
| **C** | Structural / international analogy | Assert only as analogy, never as a local rate |
| **D** | Simulated by us | Always labelled `SIMULATED` on the same visual |
| **E** | Not measured | **Stated as unknown** — a feature, not a gap |

---

## 4. The solution

**Three engines** (spec §3), every intervention priced in clinician-minutes, negative-net-value changes return **"do not do this"**:

1. **Waste Ledger** — two additive ledgers over an exhaustive, test-proved token-state taxonomy: patient-time `W1–W9` and roster-keyed provider `P1/P2/P3`. Rule-derived, not modelled; models act on top and cannot corrupt it. Full spec in §7 below.
2. **Queue Digital Twin** — a live-fitted discrete-event simulation (DES) of *that specific OPD*, evaluating proposed reconfigurations **before** the hospital makes them. Answers counterfactuals, not predictions. "Digital twin" is the category name; if challenged, the accurate word is DES.
3. **Released-Slot Reallocation (RSR)** — at T-90min a predicted no-show's freed slot is matched to a queued patient on **administrative compatibility** (specialty, slot type, follow-up status — never clinical judgement), SMS offer with **no clinician's name**, one tap, and a hard **walk-in P90 non-regression constraint**. Scoped to the **booked** subset only; the booked share is **unknown #6** and if small, RSR is a minor feature, not an engine.

**What the patient gets** (§3.4) — three paths, primary first:

| Path | Requires | Who |
|---|---|---|
| **1 — Existing paper token** *(primary)* | Nothing | Everyone; preserved deliberately |
| **2 — QR/USS scan → token → SMS** | Smartphone camera | Optional convenience; never the only way in |
| **3 — SMS on a feature phone** | Any handset | Position, estimate, RSR confirmation |

No app required, ever. One physical display. Declining the digital path changes nothing about care. No clinical content, ever. No patient-side score.

**Staff instrumentation** (§4.2) — **five instrumented roles** (Reception, Nursing, Clinician, Diagnostics, Records) + one human observation. The counter→clinic path is **2 + 2 + 3 = seven taps**, not two; full counter→exit with diagnostics is 10; clinician check-in/check-out are per **session** (and are what make the north-star computable). "Staff don't tap" is a High risk with a named mitigation — never a reassurance.

---

## 5. What we're building, and what is built today

### 5.1 Build checklist (spec §18), with live status

| # | Item | Status |
|---|---|---|
| 1 | Seeded synthetic generator (14 days, 1 OPD block, `seed=20261003`) + provenance sheet | **Not built** — everything depends on it |
| 2 | Token state machine → `W1–W9` Waste Ledger + `P1/P2/P3` provider series | **✅ Built and proved** — `cadence/cadence/taxonomy.py` + `cadence/tests/test_taxonomy.py` |
| 3 | OPD display + SMS adapter (mocked, real interface boundary) | Not built |
| 4 | Arrival-rate + no-show models with calibration reporting | Not built |
| 5 | Live-fitted DES twin + reconfiguration search + `net_value` ranking + refusal path | Not built |
| 6 | RSR bipartite matching with walk-in P90 non-regression constraint | Not built |
| 7 | CAG mapping table as a shipped artefact | Not built |
| 8 | Validation-gate harness (7 thresholds + no-show calibration gate) — **build before demoing the twin** | Not built |
| 9 | Pre-rendered demo video + offline LAN duplicate + one genuinely live computation | Not built |
| 10 | Printed judge card | **Drafted and synced** (DEMO pack Part 3 + pack §5.3 print checks) |

### 5.2 The built code — exact facts

- `cadence/cadence/taxonomy.py` (~15 KB) — `classify()` returns exactly one code, never None, never two. Stdlib only.
- `cadence/tests/test_taxonomy.py` — enumerates the full **98,304-state** observable space; asserts **0 uncovered states, all nine codes reachable, no dead codes, `sum(W1…W9) + data gaps == in-scope states`**, `W5`/`W6` remain distinct (fatal A1), and **a data gap yields no ledger row rather than being filed as waste**.
- `cadence/tests/test_toolchain.py` — pins pandas ≥ 2.x / numpy basics.
- **Test status: 25 passed.** Run **from `D:\HACKKKKKK\cadence`** with `python -m pytest tests -q`. From the repo root it fails with `ModuleNotFoundError: No module named 'cadence.taxonomy'`.

---

## 6. Architecture (spec §4)

```
┌──────────────── ONE HOSPITAL, ONE OPD BLOCK ─────────────────┐
│  PATIENT: paper token (primary) · QR/USS optional · SMS       │
│  STAFF:   Android app, 5 roles                                │
│      ▼                                                        │
│  EDGE: SQLite on a mini-PC, LAN-only, offline-tolerant       │
│      ▼                                                        │
│  CADENCE CORE                                                │
│   • Token state machine → WASTE LEDGER (W1..W8 + W9 residual)│
│   • Roster ledger      → PROVIDER SERIES (P1/P2/P3)          │
│   • Arrival-rate model   (HistGradientBoosting, 15-min bins) │
│   • No-show model        (calibrated; threshold = policy)    │
│   • QUEUE DIGITAL TWIN  (stochastic DES, live-fitted)        │
│   • Reconfiguration search + net_value ranking               │
│   • RSR: released-slot bipartite matching                    │
│      ▼                                                        │
│  CONSUMERS: SMS adapter · OPD display · staff console        │
│      ▼                                                        │
│  Hospital MIS — READ-ONLY, aggregate only, consented         │
└──────────────────────────────────────────────────────────────┘
```

**Committed constraints (one topology, no alternatives):**

- **Offline-first**, LAN-only core; internet needed only for SMS and optional MIS export.
- **No custom hardware in MVP** — no IoT, turnstiles or sensors; state transitions come from staff taps. (Honest BOM: tablets ₹9–15k/role, mini-PC ~₹8k, display ~₹6k if absent, SMS credits + **TRAI DLT sender-ID registration with 2–6 weeks lead time**, ~2 h/shift training — the real cost.)
- **No EHR write-back.** Read-only, consented, aggregate only.
- **No ABDM/ABHA write path in MVP** — post-pilot, contingent on the interoperability pathway. Where ABDM is referenced the unit is **registrations** (25 crore Scan & Register figure).
- **The LLM is optional and off the critical path** — may summarise the ledger for shift handover; never touches the token pipeline, ledger, or clinical content.

---

## 7. The Waste Ledger — full mechanics (spec §3.1, §7.2)

### 7.1 The state table (exhaustive; the partition is *proved by test*, not asserted)

| Code | Cause | Detection rule (summary) | Owner of the fix |
|---|---|---|---|
| `W1` | Counter idle | In counter queue, a counter open+idle, this token next | Reception |
| `W2` | Counter queue | In counter queue, all counters busy | Counter staffing — *surfaced, not controlled* |
| `W3` | Nursing idle | In nursing queue, stage-nurse present and idle | Nursing supervision |
| `W4` | Nursing queue | In nursing queue, all stage-nurses busy | Nursing staffing |
| `W5` | Clinician absent | In consultation queue, room vacant or clinician not checked in | Clinic / administration (**rostering** failure) |
| `W6` | Clinician queue | In consultation queue, clinician present and with another patient | Demand vs clinician capacity (**load-vs-service-rate**) |
| `W7` | Diagnostics detour | Sent to imaging/lab, not returned within SLA | Diagnostics |
| `W8` | Documentation | Clinically finished, not cleared | Records |
| `W9` | **Unclassified** | Observed in a state no rule covers — definition **fixed before data collection**, cannot be re-tuned | Data quality / scope |

- **`W5` vs `W6` is the distinction the ledger exists for:** rostering failure vs demand condition — different problems, different owners. Collapsing them makes the ledger useless.
- **`W9` ≠ data gap.** `W9` = we watched and cannot attribute → **is** a ledger row, gated at **< 2% of observed on-site minutes** (gate 4). Data gap = no evidence at all → **no row**, reported as coverage % alongside consent coverage. Filing gaps as waste would manufacture minutes and make the total unfalsifiable.
- **Expected gate-4 failure response is to add a station (`W10` pharmacy, `W11` billing…), never to widen `W9`.** The enumeration already shows `W9` lands mostly on unmodelled locations (pharmacy, billing, escort waits, corridor transit) — share-of-states is not share-of-minutes, and the < 2% gate is what decides whether that matters.
- **Did-not-arrive / left-early hold no minutes** (no timeline exists) — reported as OPD-level counts and rates (§13.2 of the spec), excluded from reconciliation.
- **Provider ledger:** `P1` consulting, `P2` present-and-idle, `P3` rostered-but-absent. North-star derivation:
  ```
  present_min(c,s) = check_out − check_in        # two taps per session
  idle_min(c,s)    = present_min − Σ consultation_minutes
  north-star       = 100 × Σ idle_min / Σ encounters
  ```
- **Cross-check (the diagnostic):** high `W6` + high `P2` → **demand** problem; high `W6` + high `P3` → **rostering** problem.
- **Addressability honesty (§7.3):** `W5` addressable; `W1`/`W3` only where a roster permits; `W2`/`W4` report-only; `W6` the twin can **redistribute, not remove**; `W7`/`W8` owned elsewhere. Addressable share = **unknown #5**. The honest ceiling is bounded by demand and we say so.
- **Audit comparability:** a documented CAG mapping table ships as a deliverable — including the mapping that is **not** valid (idle-minutes is *not* the inverse of cases-per-doctor-per-annum).

---

## 8. Models (spec §6)

| Model | Task | Method | Why |
|---|---|---|---|
| Arrival intensity | Patients per 15-min bin | `HistGradientBoostingRegressor` | Robust, CPU-only, no maintenance-mode dependency |
| Service time | Per-OPD consultation duration | Empirical quantiles + GBM quantile heads | Publishes P50/**P90** — P90 is what the patient feels |
| No-show | `P(no-show)` per booked slot | Gradient-boosted + isotonic calibration | **Calibration over AUC** — the threshold is a capacity-policy knob, so probabilities must be trustworthy |
| Twin | Counterfactual flow | Stochastic DES, live-fitted | Mechanism an administrator can read, not a black box |

- **Prophet** is out of the core stack (**maintenance mode as of v1.4.0** — not deprecated) and appears only as an experimental challenger in the model registry.
- **Variance bands** = within-model variance under simulation (10,000 re-draws of stochastic inputs). They do **not** answer "how accurate is our model of the real OPD" — only the gate does. Every banded chart is titled `SIMULATED — within-model variance`.
- **No "prediction vs reality" panels exist** — there is no reality to put beside them.
- The demo twin is fitted to data our own generator produced — **circularity stated on screen**; no demo output is evidence of real-world accuracy.

---

## 9. Current stack vs. dropped v2 stack

| Aspect | v2 "Queue Intelligence" (dropped) | v4 CADENCE (current) |
|---|---|---|
| Backend / front end | Django REST, React/PWA, Postgres, Redis | Python core, edge **SQLite**, staff Android app, SMS, one physical display |
| Simulation | SimPy; Synthea/NHAMCS parameterisation | Stochastic DES live-fitted from the site's own token log |
| Forecasting | Prophet (and LightGBM mention) | `HistGradientBoostingRegressor`; Prophet → challenger only |
| Deployment | Multi-tenant cloud SaaS, Azure/GCP/AWS | **On-prem/LAN, one building, offline-first** — multi-tenancy was a mutual exclusion, not a feature |
| Headline numbers | 72→47 min peak (−35%), +12% utilisation | **Removed.** Zero real-world outcome claims until the gate passes; demo is Class D `SIMULATED` |
| Patient entry | QR/USS primary | **Paper token primary** (feature-phone persona) |
| Staff burden | "Two taps per patient" | **Seven taps** counter→clinic; five roles |
| Evidence use | NHAMCS as evidence, NSS 13.4–25.9%, "ABHA 25 crore visits", LASI "best-performing domain" | All cut/quarantined — see §18 do-not-say list |
| Built code | None (docs only) | `cadence/` — taxonomy module + 25 passing tests |

---

## 10. Validation gates (spec §6.4) — the claims licence

**Phase:** token-level logs, one partner site, **n ≥ 1,500** encounters (extend the window, never relax the bar).
**Split, stated so the metric cannot be gamed by the split:** fit on **days 1–7**, score every gate on **held-out days 8–14**. No threshold is computed on fitting data.

The twin must clear **all seven**:

| # | Metric | Threshold | Decision rule |
|---|---|---|---|
| 1 | Median wait error (%) | < 20% | Fail if **bootstrap 95% CI upper bound** ≥ 20% |
| 2 | P90 wait error (%) | < 30% | Fail if CI upper bound ≥ 30% (a point estimate cannot claim a pass) |
| 3 | Abandonment rate | within ±3 pp of observed | Fail outside ±3 pp |
| 4 | `W9` as % of **observed** on-site minutes | < 2% | Fail at ≥ 2%; `W9` definition is pre-fixed — failure means add a station, not widen `W9`; reported alongside log-coverage % and consent-coverage % |
| 5a | Stage-order violations | < 1% of transitions | Anti-back-dating (clinician-side) |
| 5b | Short-idle share (`P2` episodes < 60 s) | < 10% of idle episodes | Anti-chopping (clinician-side) |
| 5c | Arrival-to-first-tap lag | P95 < 10 min | **Reception data-quality signal, demoted and relabelled — not anti-gaming** |

Plus **observer spot-audit** twice per quarter (a control no threshold replaces), and a separate **no-show gate: ECE < 0.05** on site-held-out booked slots + the non-regression constraint on queued patients' P90.

**Failure handling, pre-registered:** report the failure and by which cause the twin diverges; ship **measurement-only** (Phase 1). **Partial passes do not license partial claims.** Gate-2 (10-day stepped-wedge) is explicitly *feasibility, not efficacy*.

---

## 11. Data and provenance

- **Sources:** Class A — NSS 75th (SAR 586; 80th round 2025 gives rural public share 35% as current), ABDM 25 crore **registrations**, `facebook/prophet` README; A\* — CAG Report 2 of 2025 Ch. III, NAMCS 2023 (both failed re-open in §5.7). Class B — De, Gupta & Chakraborty 2024 (DOI 10.4103/DSHMJ.DSHMJ_63_24), Ambade, Kim & Subramanian 2024 (DOI 10.1016/j.puhip.2024.100541), Gowda, Sachin J, Sudha Bala & Tondare 2026 (DOI 10.1186/s12913-026-14997-y). Class C (quarantine) — Kemdirim Nigeria (tag: *international comparator; mechanism generalises, magnitude does not*), NAMCS magnitudes (US-only tag), Brazilian no-show dataset (**unit-test fixture only; no figure in any slide**).
- **Source re-verification log (§5.7):** 8 sources attempted, **2 could not be opened → downgraded, not left as "verified."** A source you cannot open on the day you cite it is a source you cannot claim to have verified.
- **External verification pass (7 Oct 2026, websearch):** all five load-bearing citations re-confirmed with DOIs — De (10.4103/DSHMJ.DSHMJ_63_24), Ambade (10.1016/j.puhip.2024.100541), Gowda (10.1186/s12913-026-14997-y), ABDM 25-crore figure via PIB/News on AIR (unit = **registrations**), Prophet README (maintenance mode; newest tag **v1.5.0** is bug-fix-only, status unchanged).
- **Seven declared unknowns (Class E), each with owner + date + resolution path:** 1 no-show base rate · 2 abandonment rate · 3 twin's real-world accuracy · 4 **why** the survey compresses waiting · 5 addressable share of idle · 6 **booked share of the day** (decides whether RSR is an engine) · 7 whether the audit number is compressed by the same mechanism. Unknowns 6 and 7 are new in v4 — both were previously *assumed*.
- **Demo data:** synthetic 14-day, single-OPD-block, **`seed=20261003`**, provenance sheet + public regeneration command:
  `python -m cadence.data.generate --seed 20261003 --days 14 --blocks 1 --out data/synthetic/opd_block_14d.csv`
  *(generator itself not yet built — §5.1 item 1.)*

---

## 12. Ethics, privacy, regulatory — 8 product constraints (spec §13)

1. **No clinical function** — no diagnosis, triage, severity or condition inference, anywhere. CADENCE answers "how long," never "what's wrong."
2. **No individual patient or clinician score exposed to staff.** The no-show score is computed, **logged once** in the append-only decision record (an unauditable decision is worse than a logged one), and is **never displayed, never exported, never joined to a clinician's name, used only for one slot-release decision.** Non-arrival → OPD-level counts only.
3. **No financial or clinical ranking of patients**; matching on administrative compatibility; **no clinician's name in any patient-facing SMS**.
4. **Consent / DPDP Act 2023:** token-level pseudonymous, purpose-limited; consent at QR scan **with the paper token as the non-digital alternative**; no token ever denied for refusing consent; institution is the data fiduciary; obligations scoped as named pilot work. **Self-selection disclosed:** the ledger is a consenting subset; the hospital supplies an aggregate paper-token count so we report **ledger coverage %** — *a consent-based system that cannot report its own coverage is not measuring the OPD.*
5. **Append-only decision log** — every model-recommended action with inputs, model version, confidence at decision time; priority-queued arrivals logged as a distinct cohort; no priority queue without clinical sign-off on the policy.
6. **Read-only on clinical records** — no EHR/HMIS write-back.
7. **Staff-side fairness** — no individual clinician metric displayed or exported; department-level ceiling; benchmarking opt-in, off by default (v2's department league table is withdrawn).
8. **The refusal is a feature** — CADENCE must be able to say an intervention failed or wasn't worth doing.

---

## 13. Scope and phases (spec §9)

**Non-goals — deleted, not deferred:** multi-hospital roll-out · hospital IoT · bed/inpatient/pharmacy · chat-bot · ABHA/ABDM write in MVP · per-patient or per-clinician scoring · LLM in the queue or clinical path.

**Phase 0 — Measure (redesigned):** (a) 14-day walk-in token-level logging at one site → first real ledger, abandonment, addressable share; (b) multi-site **appointment-register log** (a paper book — no OPD integration) → no-show base rate **and booked share**, deciding whether RSR is worth building. *v2 built Phase 0 on a misread: "87.30% visited directly" is not a walk-in rate.*
**Phase 1 — Measurement-only CADENCE:** ledger + SMS + display + MIS export in CAG vocabulary + mapping table. No models.
**Phase 2 — Twin + counterfactual console:** runs the §10 gate; ships recommendations only if it passes.
**Phase 3 — RSR:** requires Phase 0(b) and scope-of-practice approval for nurse-led fast-track.
**Phase 4 — Extension:** second block, then multi-site, only on published Phase 1–3 results.

**The single fallback, defined once:** *if the gate fails, ship Phase 1 only — ledger, display, SMS, MIS export, mapping table. No models, no recommendations, no RSR.* (v2 contradicted this in three places.)

---

## 14. Demo run book — pointer (synced to v4.0)

`DEMO_AND_JUDGE_PACK.md` is the run book: **Part 1** speaker script, **8 beats**, 4:30 (beat 0 = the SIMULATED label; beat 1 = the instrument gap; beat 2 = the waste ledger; beat 3 = the twin; beat 4 = the refusal with a 4-second hold; beat 5 = RSR loop; beat 6 = the audit; beat 7 = the gaps) · **3-minute variant** = beats 0,1,2,4,7 re-timed to exactly 180 s · **failure rule**: not working in 15 s → cut to pre-rendered video, drawn from beat 0's budget, no apology · **Part 2** 90-second pitch · **Part 3** printed judge card · **Part 4** 15 cross-exam answers, each **three sentences max** (honest answer → evidence/mechanism → limit/gate) · **Part 5** three-person roles, T−24h→T−0 rehearsal plan, T−15 checklist.

> ✅ **SYNCED TO v4.0 (8 Oct 2026) — the pack's footer and supersede note now say "built against `PROJECT_SOLUTION_FINAL.md` v4.0."** The table below is the **correction record**: every contradiction the pack's v2 content carried against v4.0. Verify against the pack at T−24h before the demo; do not reintroduce any row of it. No v2 row below survives in the synced pack.
>
> | Pack says (v2) | v4.0 truth |
> |---|---|
> | "exactly one of **six** causes… reconciles to **zero remainder**" | **nine** causes `W1–W9`; residual **non-zero, gated < 2%**; "zero remainder" is banned |
> | Judge card: "**four** thresholds", ledger "**zero unassigned minutes**" | **Seven** gates (1–4 + 5a/5b/5c) + no-show ECE gate; W9 < 2% |
> | "three declared unknowns" | **Seven** unknowns, each with owner + date |
> | CAG "**Chapter IV**" | **Chapter III** (E3 correction) |
> | LASI "India's **best-performing** domain, ~5% negative" | India's **worst** of six domains, 4.6% (9.5% public) |
> | Kemdirim classed **B**, "2022" | Class **C**, 2021 |
> | "87.30% direct walk-ins" | 87.30% visited **directly, not by referral** — not a walk-in rate |
> | "India… ranks the country among the world's best on waiting" (90-s pitch) | Cut — untraceable comparator |
> | Fallback = "Waste Ledger + RSR, no reconfiguration recommendations" | Fallback = **no RSR** either (gated on unknown #6) |
> | "measurement-only MVP" framing | Demo shows **all three engines**, labelled SIMULATED, twin UNGATED |
>
> The **golden do-not list** (pack Part 4) and the rehearsal/checklist machinery remain sound and are cited in §18 below.

---

## 15. Judging-criteria map and prior art (spec §11, §16)

**Ten criteria** (Sustainability added in v4 — v2 omitted it): Innovation (closed loop + refusal + dual ledger; narrowed per §16.3) · Relevance (Indian headline numbers; volunteers that the instrument we'd replace *isn't* broken and we don't know why it compresses — unknown #4) · Technical depth (calibration over AUC, live-fitted DES, bipartite matching, exhaustive taxonomy with published residual, computable north-star, three integrity signals, offline-first) · Feasibility (one building, no custom hardware, five roles, real BOM with DLT lead time) · Impact (north-star `P2` derivation published; guardrail = abandonment; does **not** call idle "recoverable") · Scalability (argued from Phase 4 evidence; twin is per-site by design — *a flow model that transfers without re-fitting is wrong*) · UX (seven taps stated honestly; paper token primary; SMS; no patient score) · Presentation (beat 1 gap, beat 4 refusal, beat 7 volunteered gaps, written failure rule, printed source card) · Sustainability (per-facility licence; **Indian public procurement runs 9–18 months**).

**Defensible novelty statement (§16.3) — exactly three claims:**
1. **Two ledgers on one taxonomy** — patient-time and provider-time — enabling a *demand* vs *rostering* diagnosis from the same observed waiting number.
2. Every recommendation attached to a **measured** local base rate; no-show, abandonment and addressable share treated as **unknown until measured**.
3. Every recommendation gated on a **live-fitted twin and a pre-registered threshold**, including the option to recommend *against* an intervention and to ship measurement-only.

**Withdrawn:** RSR's novelty claim (self-defeating: no scheduling system → no slots to reallocate). Waitlist auto-fill and no-show ML are commodity EHR features — conceded in advance. The **instrument disagreement motivates the work but is not novelty** (measuring the same thing two ways is standard practice).

---

## 16. Risks, open gaps, and salvaged wisdom

### 16.1 Live risks (spec §12)

| Risk | Severity | Mitigation |
|---|---|---|
| Twin fails the gate | High (plausible) | Documented fallback: Phase 1 only |
| Walk-in traffic defeats RSR | High | Booked subset only; Phase 0(b) quantifies first; deprioritise and say so if small |
| **Staff don't tap** | High | Seven taps is a real cost, stated not minimised; opt-in not league table; pilot with a volunteering department; **"we have not yet secured clinical sponsorship — our single largest project risk, a relationship risk, not a technical one"** |
| `W7`/`W8` roles won't participate | High | Phase 0's first negotiation; if it fails, codes reported **unavailable**, coverage test records unmapped states |
| Data privacy | High | §12 architecture; DPDP scoping; paper token preserved |
| SMS / DLT dependency (2–6 wks) | Medium | LAN-local core; display works with zero external services |
| "Just another queue app" | Medium | Beats 1 and 4 exist to defeat this read |
| Procurement timeline | Medium | Stated openly in the Sustainability cell, not discovered in Q&A |
| Overclaiming under cross-exam | Medium | Claim classes A–E; unknowns slide mandatory; three-sentence answers |

### 16.2 Open gaps (carried forward; not blockers, but unresolved)

1. ✅ **Closed 8 Oct 2026 — `DEMO_AND_JUDGE_PACK.md` synced to v4.0.** Every row in the §14 correction record was applied; footer and supersede note now read "built against `PROJECT_SOLUTION_FINAL.md` v4.0."
2. **Accessibility / UX is asserted, not tested** (PROJECT_DRAWBACKS S8/M6): we *target* WCAG 2.2 AA (semantic markup, keyboard paths, non-colour-only encoding) but no formal audit has run — say "designed for, not yet audited," never "conformant."
3. **Business model has no numbers** (S6): §15's Sustainability cell names per-facility licence + infra cost + 9–18 month procurement, but no figures exist. Either quantify or state plainly that pricing is post-pilot.
4. **Clinical sponsorship not secured** (named in §12 as the largest project risk).
5. ✅ **Closed — Hyderabad reference authors identified (7 Oct 2026 pass):** Bindiya C. Gowda, Sachin J, Sudha Bala, Devidas P. Tondare, *BMC Health Services Research* 26:945 (DOI 10.1186/s12913-026-14997-y); recorded in §11's verification log.
6. **Repo URL placeholder** on the judge card is still `<your-org>`.

### 16.3 Salvaged from `PROJECT_DRAWBACKS.md` (v2 review — content kept, file deleted)

- **§5 strategic read (still valid):** the strongest numbers in a pitch are the least defensible when they come from a simulator that has never met a hospital. The winning move is to **pre-empt the limitation yourself, early, in plain language** — "modelled numbers under stated assumptions, here is how wrong we could be, here is how the pilot replaces our assumptions with theirs." *A team that names its own biggest limitation first is nearly impossible to score down on judgement. A team that gets caught naming it is finished.*
- **§6 paste-ready limitations statement** — the *structure* is the template for the submission's Known Limitations section: simulation-validated not field-validated; bands = within-model variance not predictive accuracy; training data not from the target setting; geographic transfer assumed not validated; deployment topology narrow; automation is advisory with human sign-off; accessibility designed not audited; a "not yet built" list volunteered. **Its v2 numbers (NHAMCS/Synthea parameterisation, −35%, WhatsApp roadmap) are all cut — rewrite against v4 before use.**
- **§4 contradiction table** — all ten clashes (nurses-vs-doctors, 24h-vs-48h, `[Name]` placeholders, SaaS-vs-LAN, visits-vs-registrations, bad no-show URL, two-vs-four architecture taxonomies, boarding-risk, privacy absolutes, module count) were **resolved by v4.0**; kept here as a checklist for any new artifact.

---

## 17. Repository file map

```
D:\HACKKKKKK\
├── PROJECT_BIBLE.md            ← THIS FILE (orientation)
├── PROJECT_SOLUTION_FINAL.md   ← SOURCE OF TRUTH, v4.0 (858 lines)
├── ADVERSARIAL_REVIEW_V4.md    ← v3.1→v4.0 defect register (internal)
├── DEMO_AND_JUDGE_PACK.md      ← demo/pitch/judge run book — SYNCED to v4.0 (§14)
├── opencode.json               ← opencode config (MCP servers, etc.)
├── cadence/                    ← THE CODE
│   ├── cadence/                ← package source (taxonomy.py — W1–W9 classify(); stdlib only; ~15 KB)
│   └── tests/                  ← test_taxonomy.py (98,304-state partition proof) + test_toolchain.py
├── .opencode/                  ← commands/ + skills/ (build-deck, narrative, revise, slop-check, presentation-craft)
└── .slides/                    ← Marp deck build pipeline
```

**Kept by decision:** `PROJECT_BIBLE.md`, `PROJECT_SOLUTION_FINAL.md`, `ADVERSARIAL_REVIEW_V4.md`, `DEMO_AND_JUDGE_PACK.md`, `cadence/`, `.opencode/`, `.slides/`, `opencode.json`.

**Deleted 8 Oct 2026** (approved list; salvage complete — harvested content lives in §16.2/§16.3):
- v2 artifacts (superseded): `PROJECT_EXPLANATION.md`, `PROJECT_DRAWBACKS.md`, `CROSS_EXAM_AND_DEMO_CHECKLIST.md`, `Hackathon_Pitch_Slides.md`, `queue-explained.deck.md`.
- Junk: `.playwright-mcp/`, `docs/` (empty), root `.pytest_cache/`, `cadence/**/__pycache__`, `cadence/.pytest_cache`, `.slides/build/__pycache__` (the cache dirs regenerate on their own).

---

## 18. Glossary, standing rules, and the do-not-say list

### 18.1 Glossary

| Term | Meaning |
|---|---|
| **Waste Ledger** | The additive patient-time ledger over codes `W1–W9` |
| **Provider series / `P1/P2/P3`** | Roster-keyed clinician-minutes: consulting / present-idle / absent-despite-roster. `P2` is the north-star numerator |
| **North-star** | *Idle clinical minutes per 100 encounters* (lower better); guardrail: abandonment never rises |
| **Twin / DES** | Live-fitted discrete-event simulation of one OPD block; "digital twin" is the category name, DES the accurate term |
| **RSR** | Released-Slot Reallocation — fills a predicted-freed booked slot with a queued patient, P90 non-regression constraint |
| **The refusal** | `net_value ≤ 0` → "do not do this." A feature, demoed in beat 4 |
| **Gate** | The pre-registered validation thresholds (§10) that license real-world claims; **it can fail, and we ship measurement-only if it does** |
| **Claim class A/B/C/D/E** | Evidence discipline (§3.3); A\* = official but not re-verified |
| **Unknown #1–#7** | Declared unknowns with owner + date (§11) |
| **`SIMULATED`** | Label required on every Class-D visual; bands are within-model variance |
| **Seven taps** | The honest counter→clinic staff-burden count |
| **DLT** | TRAI Distributed Ledger Technology sender-ID registration — 2–6 week SMS lead time |

**Acronyms (spelled out once here; used freely above):** OPD = outpatient department · HMIS = hospital management information system · MIS = management information system · ABDM = Ayushman Bharat Digital Mission · ABHA = Ayushman Bharat Health Account · DPDP Act 2023 = Digital Personal Data Protection Act, 2023 · TRAI = Telecom Regulatory Authority of India · NSS = National Sample Survey · SMS = short message service · WCAG = Web Content Accessibility Guidelines · AOR = adjusted odds ratio · ECE = expected calibration error

### 18.2 Standing rules

1. *"If a number cannot be traced to a primary source with its exact wording, it does not appear in the pitch. If a claim cannot survive an explicit validation gate, it is a hypothesis until the gate passes."* (spec, header)
2. **A partition claim must be provable by a test, not by a sentence.** (ADVERSARIAL §4)
3. **A metric must name its numerator, its denominator, and the record that produces it.** (ADVERSARIAL §4)
4. A source that cannot be opened on the day you cite it is a source you cannot claim to have verified (§5.7).
5. One topology, committed — a jury reads two alternatives as indecision.
6. Pre-empt your own biggest limitation early, in plain language (§16.3).
7. Partial passes do not license partial claims.
8. Anti-goal: no feature that does not reduce idle clinical minutes or abandonment.

### 18.3 DO-NOT-SAY list (from the spec §14 "Removed — do not reinstate" + the pack's golden list + dropped v2 claims)

**Never say — wrong, cut, or untraceable:**
- "13.4–25.9% avoided a visit due to waiting time" (untraceable) · "79.3% outpatient care in the private sector" as all-India NSS (it's NITI Aayog, 21 states, pooled rounds) · "NSS 79.3%" generally · LASI's "Australia 21% / UK 30%" comparators (not in the text).
- "Prophet is archived/deprecated" → **maintenance mode as of v1.4.0**.
- "25 crore OPD **visits**" → **registrations**. Never "consultations."
- "Government of India, CAG Report **Chapter IV**" → **UT of Jammu and Kashmir, Chapter III**.
- "**Two taps** per patient" → **seven** on counter→clinic. "**Four** instrumented roles" → **five**.
- "The survey is the one the hospital answers to" → both instruments see it, neither can act inside a shift.
- "The Nigeria contrast is the cleanest evidence available" → two-hospital existence proof, same standard as Hyderabad.
- "No-show probability is not persisted" → it **is** logged, never displayed.
- "Three independent cuts" of LASI → negative is contained in neutral-or-worse; report the 59.1% positive too.
- Hyderabad "waits were **longer** with an HMIS" → a higher **proportion** of ≥120-min waits; association only; never causal language.
- "Zero remainder" / "reconciles to zero unassigned minutes" → `W9` is non-zero by construction, gated < 2%.
- "India's best-performing domain" (LASI) → **worst** of six.
- "87.30% walk-in" → 87.30% visited **directly rather than by referral**.
- Any Indian no-show rate, Indian abandonment rate, or Indian wait-accuracy figure — **none exist** (unknowns 1–3).
- Any figure from the Brazilian dataset (unit-test fixture) · any NAMCS figure without its US-only tag.
- "72→47 minutes" / "−35%" / "+12% utilisation" (v2 simulator outputs) · "deployed," "live in," "pilot partner," "CAG-approved."
- Any band described as accuracy, a confidence interval on real-world wait, or forecast error.
- Any "prediction vs reality" panel · any individual clinician ranking or patient score · any clinician's name in an SMS · any clinical inference of any kind.

---

*CADENCE · CATALYST CREW A · NEHRU ARTS AND SCIENCE COLLEGE, COIMBATORE · HackSpark 2026 · AI & ML Track — Smart Hospital Queue Management*
*If a line in any artifact is not traceable to `PROJECT_SOLUTION_FINAL.md` v4.0 or to a source in its claim ledger, it does not go on stage.*
