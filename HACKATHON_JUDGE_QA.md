# HACKATHON_JUDGE_QA — Final Audit Workbook & Answer Pack

**Project:** CADENCE — Closed-Loop OPD Flow Engine
**Event:** HackSpark 2026 · AI & ML Track — "Smart Hospital Queue Management"
**Team:** CATALYST CREW A · Nehru Arts & Science College, Coimbatore
**Tagline:** "Stop measuring the queue. Start closing it."
**Canonical docs:** `PROJECT_SOLUTION_FINAL.md` (v4.0, 858 lines) · `PROJECT_BIBLE.md` · `DEMO_AND_JUDGE_PACK.md` · `ADVERSARIAL_REVIEW_V4.md`
**Code:** `cadence/cadence/taxonomy.py` (381 lines, stdlib only) · `cadence/tests/test_taxonomy.py` (326 lines) · `cadence/tests/test_toolchain.py`
**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE

---

## How to read this file

Three rules govern every section.

**Rule 1 — the row schema.** Every Q&A row uses the same 7 columns:

| Judge question | Why they ask | Correct answer (v4.0 + code) | Doc evidence | Code evidence | What NOT to claim | Risk |

`Risk` is one of **L / M / H / Critical** — the blast radius if we get this answer wrong on stage.

**Rule 2 — the unsupported string.** Any capability that is not in shipped code answers, verbatim:

> **Not currently supported by the implementation.**

No paraphrase, no "almost", no roadmap. That exact sentence is our honesty contract: it defuses the attack and stops a follow-up. A judge who hears it hears "they know exactly what is built and what is not."

**Rule 3 — separation of truth layers.** Every claim is tagged with one evidence class (used in the `Code evidence` column):

- **A** — in shipped code *and* proven by a passing test (25/25 green).
- **A\*** — in shipped code, but a docstring contradicts it (the 32,768 bug) — claimed *with* the note.
- **B** — specified in v4.0 as design; not implemented. Claim as "specified", never as "built".
- **C** — specified as to-build, and explicitly gated/simulated for the demo. Claim as "simulated".
- **D** — externally verifiable public-source fact (source + PMID/level cited).
- **E** — known gap. Claim the gap itself, and the plan, not the capability.

**Source-of-truth block (repeat to yourself before every answer):** the repository is the ground truth. The documents are the *argument*; the code is the *evidence*. Where the demo pack disagrees with the spec, the spec wins; where the spec disagrees with the code, **the code wins and we say so.**

---

## 1 · One-sentence definition

**Q:** Explain the entire project in one sentence a person with no healthcare or AI background understands.

| Column | Answer |
|---|---|
| Judge question | Explain the entire project in one sentence |
| Why they ask | Establishes whether the idea is a sentence or a slide of jargon |
| Correct answer | CADENCE records every minute a patient waits at an OPD — counter, nursing, clinician, diagnostics — labels each minute as one of nine kinds of waste, then runs a "digital twin" that only ever recommends an intervention if it will save more clinician-minutes than it costs, and refuses to recommend otherwise. |
| Doc evidence | `PROJECT_SOLUTION_FINAL.md` §0.1 (thesis), §3.1, §3.2 |
| Code evidence | A — `taxonomy.py:185` `classify()`, `taxonomy.py:38` `Code` |
| What NOT to claim | "AI reduces waiting times" (nothing reduces anything yet — we *measure* and *recommend*) |
| Risk | Critical |

**Backup one-liner (thesis, for the "why should anyone care" follow-up):**

> Nobody owns the loop measure → decide → intervene → verify at the level of a single token. Both instruments India already runs — the LASI survey and the CAG audit — *see* waiting, but neither can act inside a shift. The gap is the missing loop, not missing data.

---

## 2 · What exactly are we building

**Q:** Name your three engines and what they each *do*, in one breath.

| Column | Answer |
|---|---|
| Judge question | What are the three engines and what does each do? |
| Why they ask | Tests whether "the product" is one real thing or three slides |
| Correct answer | (1) **Waste Ledger** — every non-service minute of a visit is labelled W1–W9 (counter idle, counter queue, nursing idle, nursing queue, clinician absent, clinician queue, diagnostics detour, documentation, unclassified) *plus* a provider ledger P1/P2/P3 (absent, busy, unassigned). (2) **Queue Digital Twin** — a stochastic simulation of the OPD's next shift, live-fitted to the ledger, run forward to price the effect of a reconfiguration in clinician-minutes; its recommendation is rejected if net value ≤ 0 ("do not do this"). (3) **RSR (released-slot reallocation)** — at booking level, reallocates a released appointment slot to an adjoining waitlisted patient whose administrative records it can clear, so reallocation is administratively safe. |
| Doc evidence | `PROJECT_SOLUTION_FINAL.md` §3.1 (ledger), §3.2 (twin), §3.3 (RSR), §7.1 (net_value), §9.3 (fallback) |
| Code evidence | A — ledger only: `taxonomy.py:38` (W1–W9), `taxonomy.py:41`–:49 wire codes. Twin + RSR: **Not currently supported by the implementation.** |
| What NOT to claim | "RSR is clinical triage" — §3.3 is explicitly administrative compatibility, never clinical priority (§12.1) |
| Risk | Critical |

**Scope, said out loud before any judge can force us to say it badly:**
- ONE hospital, ONE OPD block. Not a platform. (§0 scope)
- Paper token with a printed number is the primary path; the phone is the secondary/opt-in path. (§2.1)
- Edge SQLite on a mini-PC, LAN-only, offline-first; no hospital device is sent to a public cloud. (§4 EDGE, `:336`)
- No EHR write-back, no ABDM/ABHA write in the MVP. (§14.1)
- No custom hardware — staff run an Android app on 5 existing roles. (§4.1)
- The LLM is optional and **off-path**: it can summarise the reports block, it never gates a recommendation. (§3.2)

**State of build (the honest headline we open with if asked):** today the repo ships the *measuring half*: the nine-code ledger is real, executable, and exhaustively proven correct — 98,304 distinct states enumerated, zero unmapped, all nine codes reachable. The twin and RSR are **specified in v4.0, not yet built**. Our demo is engineered so that every live number is a simulation, clearly labelled, and the one thing that runs genuinely live is the classifier itself.

---

## 3 · What the patient sees

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| What does a patient experience today vs with CADENCE? | Baseline empathy — proves we understand a real OPD queue | Today: a paper token, a wall, and "which counter is mine?" — no one can tell them where they are in the flow. With CADENCE: same paper token (no new habit, no phone required), a counter clerk taps a staff tablet when they take the token, and a wall display + an optional SMS tell them the honest picture: which station they are at, roughly how many ahead, and — after the twin runs — when the flow will clear. | `PROJECT_SOLUTION_FINAL.md` §2.1 (paper token primary), §4.1 (display ~₹6k, SMS via TRAI DLT 2–6 wks), §6.1 (patient view) | A (classification) / B (display, SMS, token link) — display/SMS/token are specified, **Not currently supported by the implementation.** | "Patients get live ETAs in production" — the twin is C, simulated |
| Is the token number PII in the ledger? | Privacy ping | No. The token number is the *key*, never the payload. The ledger stores code + timestamps only. A name is never required to run the system. | §13.1, §13.2 | A (no name field exists in `PatientState` — `taxonomy.py:80`) / B (de-identification policy) | "We encrypt tokens" — see §7 |
| What happens if a patient has no phone? | Reality check | Nothing is lost. The paper token is the primary path; the SMS is an optional added channel, not a precondition. | §2.1 | — | "SMS is required" | L |

**Bottom line:** the demo patient journey is *paper token → counter tap → five icons → done* — and that bullet is 100% design (B). What is real today is the ledger that those seconds feed.

---

## 4 · What the staff sees

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| Who uses the app and what do they tap? | Tests whether "zero adoption barrier" is real | Five existing roles, no new hires: registration clerk, counter clerk, nursing assistant, consultant, supervisor. The counter clerk records a patient timeline in **seven taps** (not two): token → counter → nursing → clinician → diagnostics → discharge → save. | `PROJECT_SOLUTION_FINAL.md` §4.2 seven-tap matrix | A (the seven *states* are exactly the 16 observable flags of `PatientState`, `taxonomy.py:80`) / B (the app) | "Two taps per patient" — banned, the honest number is seven and it is fine to say so | M |
| What does a supervisor see? | Governance | A per-cause minute report (W1–W9), the provider ledger P1/P2/P3, a coverage figure ("we have a ledger row for X% of observed minutes"), and — only when the twin is built — a recommendation with a price tag in clinician-minutes and a visible "not worth it" verdict when net value ≤ 0. | §3.1, §3.2, §7.1 | A (coverage numbers are computable by `coverage_report()`, `taxonomy.py:329`) / B (reports block, MIS export) | "Real-time dashboard shipped" — **Not currently supported by the implementation.** | H |
| Is benchmarking between departments/timed? | Fairness + competitive pressure | Visiting benchmarking is **off by default**. Nothing competes; a department opts in. | §8 (opt-in) | — | "Departments compete on scores" | M |
| How long does staff training take? | Deployment realism | Roughly two hours, three-role, covering the seven-tap timeline and what each waste code means. | §4.1 ("staff training ~2 hours") | — | "No training needed" | L |

**Bottom line:** the seven-tap guarantee is honest and the seven taps correspond 1:1 to real observable flags in code. The staff app itself is B, not shipped.

---

## 5 · Architecture

**Q:** Draw the system for us. (Judges love this. Keep it to five boxes.)

```
[Token log]  ──►  [classify()  W1..W9  P1/P2/P3]  ──►  [Waste Ledger]
       │                (real, 98,304 states)                │
       │                                        ┌───────────┴───────────┐
       ▼                                        ▼                       ▼
[Wall display]   [SMS, opt-in]        [Queue Digital Twin]      [RSR reallocation]
   (B)              (B)              (stochastic, live-fitted;   (booking-level,
                                       net_value ≤ 0 ⇒ reject)     admin-compatible)
                                                                  ┌─────────┐
   Everything above the dotted line is DESIGN (B/C).             │ MIS export │
   Below: the OPD runs LAN-only, offline-first, on edge SQLite.  └─────────┘
```

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| Where does the data live? | Security architecture | A mini-PC on the hospital LAN. SQLite database. The OPD can run fully offline; synchronisation (if any) is a design decision, not a live behaviour. | §4 EDGE, `:336` | Not currently supported by the implementation. | "SQLite is implemented" — it is specified; `taxonomy.py` has no I/O at all | H |
| What is the LLM's role? | AI-credibility | Optional, off-path. It can summarise the reports block for a human. It cannot classify a minute, run the twin, or make a recommendation. The classification path is deterministic rules, not a model. | §3.2 (LLM off-path) | A (classification is 100% deterministic: `taxonomy.py:185`) / B (LLM summariser) | "AI diagnoses your queue" – banned | M |
| Is this a cloud platform? | Scope creep | No. One hospital, one OPD block. Anything beyond that is explicitly out of scope for the MVP. | §0 scope | — | "SaaS for all hospitals" | L |
| What is the empty-container rule? | Breadth vs depth | Every admin/clinic/theme is a container; if a container would have fewer than ~50 patients a month it is closed empty. Depth over breadth. | §5.2 | — | "We cover every specialty" | L |

**Empty-container rule, one line for the judge:** "We would rather run one clinic well than fifty clinics shallowly."

**Bottom line:** the architecture sells as *"a closed loop that fits entirely inside the hospital's walls"* — and the only part currently executable is its front door (the classifier). We say exactly that.

---

## 6 · AI / ML — what is actually a model

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| Is your "AI" just rules in a spreadsheet? | The core ML honesty test | The **classification** is rules — deliberately and proudly. Nine causes, 16 observable facts, one code. That is not a weakness: it is exhaustively provable (98,304 states, zero unmapped), and a hospital ledger must be provable, not plausible. The **modelling** — where real ML lives — is the queue digital twin (a stochastic simulation fitted live to the ledger) and the no-show/RSR forecasting. Those are specified, not built. | §6 (AI/ML), §3.2 | A (rules are code + tests) / B (models) | "We trained an ML model that predicts waits" — **Not currently supported by the implementation.** | Critical |
| Why not train on the CAG/LASI/De et al data? | Model provenance | Those are *measurements of the problem*, not training data for our system. We cannot train on another hospital's OPD to predict this hospital's OPD. Our model fits *this* hospital's own ledger on days 1–7 and is held out on days 8–14. | §0.1, §11.1 | B | "Our model was trained on national datasets" | H |
| Where does ML end and the human start? | Agency | Every recommendation is a recommendation. Everything is priced in clinician-minutes; net value ≤ 0 means the twin says "do not do this"; a human decides. The machine never moves a patient, never cancels a slot alone. | §7.1, §3.2 | B (twin) | "The system manages the queue automatically" | H |
| What is the one genuinely-live computation in your demo? | Demo honesty | The **live re-run of the W1–W9 attribution** over seen sample states — we type/step states in front of them and `classify()` labels them instantly, including the data-gap path (a missing transition produces *no ledger row*, never a fake code). Everything else is pre-rendered or simulated and labelled as such. | `PROJECT_SOLUTION_FINAL.md` §10 (beats) | A — `explain()` `taxonomy.py:357`, `with_change()` `taxonomy.py:379`, live in demo | "The whole demo is running live" | Critical |

**The six-→seven-gates trap we flag for the panel:** v4.0 §10 beat 7 still says "six gate thresholds, printed". The gate table (§6.4) and the judge card define **seven**: ① median wait < 20 min (upper CI), ② P90 < 30 min (upper CI), ③ abandonment within ±3 percentage points of prediction, ④ W9 < 2% of on-site minutes *with* a green coverage report, ⑤a stage-order violations < 1%, ⑤b short-idle < 10% of consultation events, ⑤c arrival-to-first-tap P95 < 10 min. **The answer on stage is seven.** This file uses seven.

**Bottom line:** the AI story is "deterministic measure, modelled decision, human veto". The weakest spot a judge will try is *"your classifier is just if-else"* — and the correct answer is *"yes, on purpose, because exhaustion beats elegance in a hospital"*.

---

## 7 · Privacy & security

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| What patient data do you store? | The DPDP reflex | The minimum: the token number (a key, not payload) and the transition timestamps from which waste codes are derived. No name, no diagnosis, no contact number is required to run the ledger. | §13.1, §13.2 | A — `PatientState` fields (`taxonomy.py:80`) are exactly tokens/timestamps/occupancy facts; there is no name or diagnosis field | "We store patient records" | H |
| Are you the data processor or the data fiduciary? | DPDP Act 2023 literacy | Under the DPDP Act 2023, the **hospital is the data fiduciary**; CADENCE is the processor at the hospital's instruction. | §13.1 | — | "We are the data controller" — wrong legal framing | M |
| What encryption/security controls exist? | The reflexive security checklist | Here is the honest answer we must give before any marketing answer: the shipped code has **zero network, zero storage, zero subprocess, zero secrets**. The *design* specifies edge-only storage, LAN-only transport, and role-scoped staff accounts (five roles, RBAC), deployed on the hospital's own device, with JWT auth and HTTPS as the transport design. **No cryptographic claim is made for what is not built.** The demo never touches a real patient, so the demo has nothing to leak. | §4, §13.1 | A (the sweep: no `socket`/`subprocess`/`requests`/`urllib`/`httpx`/pickle/yaml/eval/exec anywhere in `cadence/`) / B (auth, RBAC, JWT, HTTPS) — **Not currently supported by the implementation.** | "AES-256 at rest", "TLS end-to-end", "JWT-protected" as if shipped — all are B, say "specified, not built" | Critical |
| Who can see whose data? | Least-privilege | In design: five roles see only the screens their role needs; a clerk never sees the consultant's clinical summary (there is none anyway); supervisors see aggregates, not patients. | §4.2, §13.1 | B | "Fine-grained RBAC is live" | M |
| What happens in a breach? | Incident maturity | The blast radius is bounded by design: the ledger stores codes and timestamps on a LAN-only device; there is no central database of patients, no PHI transmission, no third-party payment. The incident plan is part of the production checklist, not of today's demo. | §13.1 | E (plan is documented scope, not built) | "We have a live SOC / IR runbook" | M |

**Bottom line:** the security posture that wins is *"we designed the system so there is almost nothing to steal, and the demo touches zero real data."* The posture that loses is claiming TLS/JWT/AES as shipped. Say "specified" out loud and we own the room.

---

## 8 · Emergency handling

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| What happens in a medical emergency? | Safety culture | CADENCE never sorts emergencies. There is no triage logic, no clinical severity score, and no "priority" field in the ledger — by design (§6.5, §12). Emergency handling stays exactly where it is today: with the hospital and its staff. The system defers to existing escalation; it never overrides a clinician's call. | §6.5, §12 (no triage / no diagnosis / no severity claims) | A — there is no severity field in `PatientState`, and no code path could set one (`taxonomy.py:80`) | "CADENCE triages patients by priority" — **banned**, it is the single most dangerous claim we could make | Critical |
| What if the system fails mid-shift? | Blast-radius test | The OPD keeps operating on paper exactly as before. CADENCE is an observability layer bolted on to the existing flow; if the mini-PC dies, the token flow does not change — only the measurement pauses. No intervention, once recommended, executes automatically, so a failure cannot act-on-our-behalf. | §4 EDGE (offline-first), §3.2 (human veto) | A (classification is computation only; nothing can "execute") / B (offline mode of the app) | "The system runs the OPD" — it never does | H |
| What is the fail-safe in the live demo? | Judge hears "is this real?" | The live classifier has a 15-second fail-safe: if the live step fails, we cut instantly to the pre-rendered video, which is labelled as such. A 3-minute variant is pre-timed for a tight slot. | `PROJECT_SOLUTION_FINAL.md` §10 | A (the computation is re-runnable; the fail-safe is a demo-runner concern, GAP) | "It never fails" | M |

**Bottom line:** the phrase to rehearse is "CADENCE measures minutes; it does not prioritise patients. Clinicians keep every call they own." Any judge pressing on emergencies is testing that boundary — and the boundary is a design line we hold everywhere.

---

## 9 · EHR / ABDM / ABHA

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| Do you integrate with ABDM/ABHA? | India-stack check | In the MVP: **no write**. CADENCE does not write to any EHR or ABHA health record. Interoperability is a documented design lane (a mapping table between token numbers and ABHA-linked identities) — but the MVP runs on the paper token alone and *does not depend on ABDM being usable*. | §14.1 | B (mapping table is a spec item, not built) | "ABHA solved our registration problem" — banned; ABDM/ABHA adoption problems are precisely why the paper path is primary | H |
| Why paper first then? | Adoption realism | Because ABDM/ABHA onboarding is not universal, and a system that *requires* it fails exactly where queues are worst. Paper token is the zero-dependency floor; ABHA is an optional upgrade path. | §2.1, §0 | — | "Everyone will have ABHA" | M |
| Does the ledger hold clinical data? | Data-minimisation | No. The observable state is administrative: queues, counters, diagnostics send/return/SLA. Nothing clinical — no complaint, no vitals, no examination notes — is captured or classified. | §13.1 | A — every `PatientState` field is an occupancy/timestamp fact (`taxonomy.py:80`) | "The ledger knows the patient's condition" — false | H |

**Bottom line:** the safe sentence is "we integrate with nothing in the MVP; the paper token is the floor and ABHA is a later lane." Judges who love the India stack respect that we did not make the demo hostage to a dependency.

---

## 10 · Digital Twin

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| What exactly is the twin? | Precision test | A stochastic discrete-event simulation of the OPD's next interval, fitted live to the hospital's own ledger (days 1–7), held out on days 8–14. It plays counterfactuals: *what would today's waste ledger look like if counter opened at 09:30 instead of 10:00?* Every counterfactual is priced in clinician-minutes. | §3.2, §6.4, §11.1 | B — **Not currently supported by the implementation.** | "The twin is running in the demo" — the demo twin is C (simulated), say so | Critical |
| Is the twin a physical model of the hospital? | Conflation trap | No, and we never call it one. It is a *queue* twin, not a building or staff twin. Only the OPD flow surface is modelled. | §3.2 | B | "Digital twin of the hospital" — inflates scope | M |
| What does net_value mean and why reject? | The "no" machine | Each intervention changes the ledger: minutes saved minus minutes cost to operate. If net ≤ 0 the twin's verdict is "do not do this." Saying no is a feature — it is how the system earns trust and avoids the classic "automation theatre" of always recommending something. | §7.1 | B | "The system finds the optimal schedule" — optimality is not achievable or claimed; it proposes, human disposes | H |
| Why would a judge trust the twin's numbers? | Falsifiability | Because they are gated: the seven pre-registered thresholds run on held-out days 8–14, *after* the demo. Until a gate passes, every twin number spoken on stage is simulated and labelled simulated. | §6.4 (seven gates, held-out days), §10 | B | "We validated the twin" — nothing is validated yet; the gates are the promised validation | Critical |

**Bottom line:** the twin's credibility is *entirely* in the words "pre-registered" + "held-out" + "not yet". The moment we present twin output as fact, we lose. Present it as a priced hypothesis and we win.

---

## 11 · Waste Ledger

**Q:** What exactly is the ledger, and prove the nine codes are correct.

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| Name the nine causes and their owners. | Taxonomy recall | W1 counter idle, W2 counter queue, W3 nursing idle, W4 nursing queue, W5 clinician absent, W6 clinician queue, W7 diagnostics detour, W8 documentation, W9 unclassified. Owners: W5/W6 are rostering-vs-demand (the v3.1 blind spot — an **absent** clinician is a rostering problem, a **busy** clinician is a demand problem), W1/W3 are capacity-utilisation, W7/W8 are process. | §3.1 | A — `taxonomy.py:41`–:49 (wire codes), `taxonomy.py:222`–:241 (the five rules), tests `test_busy_clinician_and_absent_clinician_are_different_codes` `test_nursing_station_is_instrumented` | "Six causes" — banned; the v3.1 six-cause claim is why A1 was fatal, the count is **nine** and that precision is a design signature | Critical |
| Prove the taxonomy partitions every minute. | The exhaustion test | State space = 16 observable facts (some 2-valued, counters-open-idle is 3-valued) → **98,304** distinct raw states. All 6,976 coherent states classify to exactly one code; **0 unmapped**; 3,488 data-gap states (missing evidence → *no ledger row*, never a fake code); all nine codes reachable including W9 (on 1,392 coherent states). | `PROJECT_SOLUTION_FINAL.md` §3.1 `:242` (98,304, 0 uncovered, 9 reachable) | A — `coverage_report()` `taxonomy.py:329`, `enumerate_states()` `taxonomy.py:272`, tests `test_exhaustive_every_coherent_observed_state_maps_to_exactly_one_code`, `test_every_declared_code_is_reachable`, `test_residual_fires_on_coherent_states` | "98.5% accurate" — stop; coverage is **0.5** of coherent states carrying rows, the rest are honest data gaps; accuracy-of-a-labeller is not accuracy-of-a-prediction | Critical |
| What is W9 and why is it not a data gap? | Falsifiability | W9 = *we watched this patient and cannot attribute the minute* (e.g., wait at an unmodelled pharmacy). A **data gap** = *we did not watch them at all* (a missing transition) and produces **no row**. Reporting the second as waste would manufacture minutes and make the ledger's total unfalsifiable. | §3.1 (A3 lesson) | A — `taxonomy.py:64` (DATA_GAP), `taxonomy.py:205` (integrity first), `test_data_gap_and_residual_are_different_claims`, `test_missing_transition_is_a_data_gap` | "W9 means missing data" — false; see 'Not currently supported' on the definition | H |
| What is the provider ledger P1/P2/P3? | Coverage of the *other* side of the queue | P1 absent, P2 busy, P3 unassigned — the provider-side counterpart of the patient codes, so a wait can be apportioned between patient-side and provider-side truthfully. | §3.1 | B — provider ledger surface is specified; code only carries the patient-side fields (`taxonomy.py:80`) | "P1/P2/P3 are computed in code" — not yet | M |
| What numbers can you quote from the code live? | Show-me-the-code | From `coverage_report()`: 98,304 raw states, 6,976 coherent, 3,488 data-gap states, observed 3,488, **coverage 0.5**, residual share **0.399** (W9 on 1,392 of observed), W1=256 W2=64 W3=192 W4=96 W5=288 W6=48 W7=384 W8=768. These are printed by a script, not a slide. | §3.1 (98,304 agrees) | A — `coverage_report()` `taxonomy.py:329`, re-run via the audit script; 25 tests green | "Every test passes from any folder" — they pass from `cadence/`, they fail from the repo root; say "run from the package directory" and offer the command | H |

**Bottom line:** the ledger is the entire credibility of the project and the entire *current* build. Every demo minute discussing the ledger must pivot on the words "98,304 states, zero unmapped, nine causes, held to a test file." That sentence is worth more than any graph we could print.

---

## 12 · RSR / No-show

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| What is RSR and why does compatibility beat priority? | The ethical heart of slot reallocation | RSR reallocates a *released* appointment slot to an adjoining waitlisted patient **whose administrative records it can clear** — documentation, eligibility, pre-requisites. That is administrative safety: the next patient in line who is actually *ready to be seen*. It is explicitly **not** clinical triage and never assigns clinical priority. | §3.3 ("administrative compatibility"), §12.1 (no triage/severity claims) | B — **Not currently supported by the implementation.** | "RSR prioritises by clinical need" — inverts the design and triggers the severest risk | Critical |
| How do you model no-shows? | Forecast realism | A no-show model is specified (forecast of who won't arrive, feeding slot-release), fitted on the hospital's own history, **not** on national averages. | §3.3 | B | "We predict individual no-shows with X% accuracy" — nothing is calibrated yet | M |
| Is a no-show stored as a patient attribute? | Staleness trap — the demo pack's Q3 is out of date | Corrected answer: a no-show is **computed and logged once** into an append-only decision record (the historical feed the model learns from), then **never displayed, never exported, never joined to a clinician's name, never used for a single slot-release**. The old "never persisted as a patient attribute" phrasing is retired — a patient's actual arrival is a ground-truth fact, not a judgment to hide. | §13.2 (corrected wording in the demo sync) | B (decision record is a spec surface) | "The system blacklists no-show patients" — never, not in any version | M |
| Why are twin and RSR both "not yet"? | Build honesty | Because both act *after* measurement, and the release order is deliberate: ledger → model → gate → RSR. Shipping a rescheduler before a validated ledger would put action in front of evidence. The demo therefore shows them as specified + simulated, with the build order printed. | §3.1→§3.2→§3.3 ordering, §11.1 | E (acknowledged gap with a printed build order) | "Everything in the demo is production" | H |

**Bottom line:** RSR is the moment judges test our ethics vocabulary. The three phrases to nail: *administrative compatibility*, *never clinical priority*, *append-only decision record*. Lose any one and the follow-up is about fairness.

---

## 13 · Offline operation

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| Does the system work without internet? | The Indian-district reality test | Yes, by design and it is one of the three non-negotiables. The OPD runs on the LAN; the classifier and ledger are pure computation with no network at all; SQLite on the mini-PC is the specified store. If the internet disappears, measurement continues. | §4 EDGE `:336` | A (classification runs with zero I/O) / B (SQLite, LAN app) — storage/app are **Not currently supported by the implementation.** | "Offline mode is battle-tested in a live hospital" — not yet, say 'specified' | H |
| What breaks if power drops mid-shift? | Failure maturity | Measurement pauses, the flow continues on paper exactly as it does today without us. Nothing in the system can move a patient or cancel a slot, so there is no automated action to go wrong. | §4, §3.2 (human veto) | A (no executable action exists) | "Seamless failover" — E, we don't have a live cluster | M |
| What is the EDGE constraint, precisely? | Design literacy | SQLite on a mini-PC, LAN-only transport, offline-tolerant: **the EDGE rule is a design constraint, not yet a codebase.** | §4 `:336` | B | "Our edge stack is implemented" | H |

**Bottom line:** offline-first is the answer to *"will this work in a real district hospital?"* — say "designed as a LAN appliance, not a SaaS feature" and the room hears we read the actual problem. Keep the "specified, not built" qualifier audible.

---

## 14 · Validation

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| How do you *prove* your system does anything? | The whole point of the hack | Pre-registered validation: fit on days 1–7 of the hospital's own ledger, **held out on days 8–14**, against **seven** gates: ① median wait < 20 min (upper CI < 20), ② P90 < 30 min (upper CI < 30), ③ abandonment within ±3 percentage points of prediction, ④ W9 < 2% of on-site minutes *and* green coverage report, ⑤a stage-order violations < 1%, ⑤b short-idle < 10% of consultation events, ⑤c arrival-to-first-tap P95 < 10 min. Nothing is "validated" before these run. | §6.4 (seven gates), §11.1 (holdout), §10 (demo registers them) | B (the gate harness is a build item, P1) | "Our model achieved X" — no gate has been run, ever | Critical |
| What are you actually measuring in this demo? | Honesty of the demo | The demo measures the *classifier* (98,304 states, coverage report) — which is real and proven by tests — and *simulates* everything downstream, labelled simulated. The demo is **not** a claim that patient waits will drop. | §10 | A (classifier) / C (simulated twin/live numbers) | "This demo shows reduced waiting" — false, the demo shows a measured ledger and a priced suggestion | Critical |
| Is 98,304 a real number or a slide number? | Reproducibility | A real number the code prints. Run `python -m pytest tests -q` from `cadence/` (25 tests), or run the coverage script; it enumerates the full product space of 16 dimensions (one 3-valued: `counters_open_idle`) = 3 × 2¹⁵ = 98,304. | §3.1 `:59`, `:242` (98,304 both places) | A — `_DIMENSIONS` `taxonomy.py:248`, `coverage_report()` `taxonomy.py:329` | "98,304 *coherent* states" — no: 98,304 raw; 6,976 coherent; say both | H |
| Where is the 32,768 bug and how do we handle the judge who finds it? | The adversarial catch, owned | `taxonomy.py:275` and `test_taxonomy.py:11` both say "32,768" — the count before `counters_open_idle` was widened from 2 to 3 states. The code itself is correct (98,304); only the docstrings are stale. **We find it before they do.** Flagged in §23; fixed doc-only in the same pass as this file. | — | A\* — `taxonomy.py:275`, `test_taxonomy.py:11` (doc-comments only; `_DIMENSIONS` at `taxonomy.py:252` is the authoritative 3-valued truth) | "There is no bug" — we named it, we fixed it, we win the exchange | M |
| What does a "green coverage report" mean? | Gate ④ literacy | `coverage_report()` returns zero unmapped coherent states, data gaps counted separately (3,488), and every gap is either a missing transition or a physical contradiction (0 contradictions silently absorbed). | §3.1 | A — `test_exhaustive_every_coherent_observed_state_maps_to_exactly_one_code`, `test_incoherent_states_produce_no_row_and_nothing_else` | "Coverage 100%" — that would make W9 decorative; coverage < 100% is the honest, tested state | M |

**Bottom line:** validation is where this project is strongest to a discerning judge and weakest to a credulous one. The sentence that threads it: "Every number in the demo is either a proven test result or a labelled simulation, and every future claim about the hospital runs through seven pre-registered gates that have not been run yet."

---

## 15 · Synthetic-data honesty

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| Where do the demo numbers come from? | The #1 trap | The demo's live numbers are explicitly **synthetic** — token streams generated for the demo, fed through the *real* classifier. Every screen says SIMULATED. The only things not synthetic are the national/audit citations (real, sourced) and the state-space coverage figures (real, computed). | §10, §14.4 (no fabricated outcomes) | A (coverage figures) / C (generated token streams — the generator itself is a P0 build item) | "We used real hospital data" — false and dangerous; also never quote a fabricated result as ours | Critical |
| If the data is synthetic, why should we believe the numbers? | Provenance | Because provenance is the product: every simulated number carries its generator seed and parameter set (arrival rates, service times, counters) printed on the overlay, so a judge could reproduce the stream. And the *only* claim attached to them is "this is what our pipeline would measure," never "this is what your hospital will see." | §4.4, §10 | C | "We tuned parameters until the graph looked good" — a confession, never say it | H |
| What is the generator-seed convention? | Reproducibility | Deterministic seeds per run, parameters logged with the output. Same seed → same token log → same ledger → reproducible demo. | §4.4 | E (generator is a P0 build gap, currently the seeds are hard-coded in the audit script only) | "Fully reproducible instrumentation in production" — the generator ships as a build item first | M |

**Bottom line:** the winning move is to say what the data *is* before a judge asks: "Every number on this screen is synthetic and labelled; the coverage numbers are real and computed; the citations are real and sourced; nothing here claims to be a hospital's data."

---

## 16 · Ethical boundaries

| Judge question | Why they ask | Correct answer | Doc evidence | Code evidence | What NOT to claim | Risk |
|---|---|---|---|---|---|---|
| Who does this system serve first? | Power-and-economics | The hospital and its clinicians are the primary customer; patients benefit through shorter, explainable waits — but the system never reorders, deprioritises, or ranks a patient clinically. | §0 (institution as customer), §12 (no severity) | A (no priority machinery exists) | "CADENCE is patient-first software that overrides hospitals" — neither true nor wise | H |
| No-triage boundary, one sentence. | The moral line | CADENCE counts minutes; it does not triage, diagnose, or assign clinical priority. Every prioritisation call stays with the clinician, and the design says so in five places. | §6.5, §12.1, §13.1, §3.3, §2.1 | A (no severity field in `PatientState`, `taxonomy.py:80`) | "Smart triage", "AI-prioritised queue" — banned outright | Critical |
| What if a hospital uses your ledger to blame staff? | The P1/P2/P3 blast radius | The provider ledger is a shared, named fact, and we design against blame: reports are aggregates for supervisors, recommendations are priced and optional, and the twin's "do not do this" is explicit. The demo shows the provider view without shaming any individual. | §3.1 (provider ledger), §7.1 | B (aggregation redaction is a spec surface) | "The system identifies the lazy clinician" — never; it attributes minutes, not blame | Critical |
| Fairness in slot reallocation? | Admission of the hardest case | RSR's fairness guarantee is *administrative*: it takes the next waitlisted patient whose records are clear. It makes no clinical or demographic ranking, and the twin cannot search for "better" patients to leapfrog. | §3.3, §12.1 | B | "RSR optimises waiting-list fairness" — it optimises *readiness*, nothing more | H |

**Bottom line:** ethics is where this project has done the most pre-emptive work — the killer line is "we built the 'no' into the machine." Quote it at the first ethics question and the follow-ups get softer.

---

## 17 · Top 20 difficult judge questions

Full 7-column treatment for the twenty hardest attacks, ordered roughly by likelihood × severity.

| # | Judge question | Why they ask | Correct answer | Doc evidence | Code evidence (or "Not currently supported by the implementation.") | What NOT to claim | Risk |
|---|---|---|---|---|---|---|---|
| 1 | "Is this just a queue counter with extra steps?" | Deflation | The counter labels wait; the ledger *owns* it — nine causes, owned by rostering-vs-demand, plus a provider ledger, priced recommendations, and an explicit veto. That is a control loop, not a counter. | §3.1, §3.2, §7.1 | A (nine-code partition proven) | "We invented the queue counter" | H |
| 2 | "Show me a real hospital's numbers." | Provenance | We have none of our own and will not fake one. Real citations: De, Gupta & Chakraborty (2024), n=252 across four OPDs, orthopaedics **85.71% of total on-site time** waiting to see a doctor, 87.30% visited the institute directly, 63.89% newly registered (Dr Sulaiman Al Habib Medical Journal 6(3):136–141, DOI 10.4103/dshmj.dshmj_63_24); CAG audit of the hospital (Chapter III, Class A observations); LASI survey shows access-to-health is India's **worst-performing** domain, 4.6% negative reporting; Kemdirim et al. (2021), Nigerian public general outpatient encounter **86.7 of 122.6 minutes in non-service time — the paper reports the share as 65.3%, not the surface ratio (§0.1 note)** (Niger Med J 62(6):325–333, PMID 38736516). Our own numbers are synthetic, labelled, and upcoming. | §0.1 (`:26`–`:29`), §5.3 B1, adversarial source table | B (published citations) / D (synthetic ours) | "Distance=k, real numbers later" — cite *their* numbers or label ours synthetic | Critical |
| 3 | "Why nine codes and not six?" | Recall of the lesson | Six was the v3.1 claim that was wrong in the only way that mattered — no code for a busy clinician, none for nursing. Nine is the fixed partition, each code reachable and tested. | §3.1, ADVERSARIAL A1 | A — `taxonomy.py:41`–:49; regression tests `test_busy_clinician_and_absent_clinician_are_different_codes`, `test_nursing_station_is_instrumented` | "Six causes" ever again | Critical |
| 4 | "Your classifier is just if-else. That's not AI." | ML snobbery | Correct — and deliberately. A hospital ledger must be *provable* (98,304 states, 0 unmapped), and exhaustiveness is a property of rules, not of a fitted model. The modelling — the twin, the no-show forecast — is where statistical learning belongs, and it is specified. | §6 | A (rules) / B (models) | "Our classifier is a neural network" | H |
| 5 | "What gate has actually passed?" | The credibility question | The coverage gate (④'s coverage half): 0 unmapped states, verified by 25 green tests. The seven *threshold* gates (holds out days 8–14) have not been run — no demo can claim a pass. | §6.4, §11.1 | A (coverage) / E (threshold run pending) | "All gates passed" | Critical |
| 6 | "What does the hospital actually deploy on day one?" | Procurement realism | A mini-PC, a SQLite ledger on the LAN, five-role staff app, wall display, opt-in SMS. All specified (B); on day one of the build, the classifier is the only code that ships first. We print the build order. | §4, §4.1 | B | "Day-one full stack" | M |
| 7 | "Why paper token when phones exist?" | Feature-flip | Because the floor must work when phones/SMS/ABDM do not. Paper is the zero-dependency primary; phone is the opt-in secondary. | §2.1, §0 | — | "No paper handled at all" | M |
| 8 | "How do you know the counter clerk will tap on time?" | Implementation realism | We do not assume compliance; the ledger detects it — a missing transition is a data gap, counted and surfaced, and coverage is itself the metric of adoption. The demo shows a gap being surfaced, not hidden. | §3.1 (transition_missing), §15 | A — `transition_missing` is a real field (`taxonomy.py:125`), `test_missing_transition_is_a_data_gap` | "Gericht naturally 100% of the time" | H |
| 9 | "What is the SMS channel and the cost?" | India specifics | Opt-in, transactional (TRAI DLT registration, 2–6 weeks lead), phone number stored only on the patient's opt-in row; the per-message economics sit in the build's budget (~₹ table, per §4.1). | §4.1 (SMS credits + DLT 2–6 wks), §13.1 | B | "Free SMS to everyone" | M |
| 10 | "Who owns the recommendation if a patient is harmed?" | Governance | The hospital, medically and legally — and we design so CADENCE cannot be the proximate cause: it never reorders a patient clinically, no recommendation executes automatically, every intervention is priced and human-approved. | §3.2, §12.1 | B (human-veto surface) | "CADENCE takes responsibility" | Critical |
| 11 | "What is your data footprint?" | DPDP | Ledger = token key + timestamps + occupancy facts. No name/diagnosis/contact required. Data minimisation is a design value, and there is no field for clinical data in the code. | §13.1 | A (`PatientState` has no name/diagnosis fields, `taxonomy.py:80`) | "We hold complete patient records" | H |
| 12 | "What is the EDGE rule, exactly?" | Architecture recall | SQLite on a mini-PC, LAN-only, offline-tolerant — a design constraint, not yet a codebase. | §4 `:336` | B | "Implemented edge stack" | H |
| 13 | "Why should a hospital trust your holdout split?" | Method literacy | Fit days 1–7, evaluate days 8–14, thresholds pre-registered in v4.0 *before* results exist, gates printed. Pre-registration is the anti-p-hack. | §6.4, §11.1 | B (harness) + A (the same honesty applies to the coverage test suite) | "We validated against the SAME data we trained on" | H |
| 14 | "What if the gate fails your demo?" | Risk ownership | Then the hospital gets an honest ledger with a lower stuck claim and a corrected intervention — failing a gate is a *finding*, not a shame. The demo explicitly rehearses "gate not passed → nothing claimed, lesson logged." | §10, §11.1 | E | "Gates always pass" | M |
| 15 | "What is 32,768 vs 98,304?" | The code-eye test | 98,304 is raw states = 3×2¹⁵ (8 counter-open-idle is 3-valued). 32,768 is a stale docstring at two lines, caught by our own audit, being fixed doc-only; the code and tests compute 98,304. | §3.1 `:59`, `:242` (98,304 correct) | A\* — `taxonomy.py:275`, `test_taxonomy.py:11` | "98,304 coherent states" — raw vs coherent confusion | M |
| 16 | "What happens when two clinics run one mini-PC?" | Scale honesty | The empty-container rule answers it: beneath ~50 deliveries a month a container is closed. Scale-up to a cluster is out of MVP scope and we say so. | §5.2 | — | "Horizontally scaled multi-site SaaS" | L |
| 17 | "Whose data trained your model?" | Provenance | Nobody's — there is no trained model. The twin will fit to *this hospital's own* ledger; fitting another hospital's data to predict this one would be methodologically wrong. | §11.1 | B | "Trained on national data" | H |
| 18 | "Is a no-show a patient attribute?" | Staleness of the demo Q&A | No-show is computed and logged once into an append-only decision record; it is never displayed, exported, joined to a clinician's name, or used for a single slot release. (Corrected wording — the old "never persisted as a patient attribute" is retired.) | §13.2 | B | "We flag no-show patients" | M |
| 19 | "What happens in a power cut?" | Failure maturity | Measurement pauses; the paper flow it observed proceeds unchanged; no automated action exists to misfire. We resume logging; coverage counts the gap honestly. | §4, §3.1 | A (no action machinery) | "Seamless clustering failover" | M |
| 20 | "Why is Q3 of your own demo pack wrong?" | Reading-docs test | Because the pack predates the v4.0 wording on no-shows and thresholds; the banker sync fixes it, and this file is the corrected authority. | DEMO_AND_JUDGE_PACK Q3 (stale) vs §13.2 (correct) | — | "Our docs have never changed" | M |

### 17A · Show-me-the-code matrix (template §18 requirement — 18+ rows, keyed to `PROJECT_BIBLE.md` §5.1)

| # | Claimed capability | Evidence in repo | Verdict + how to say it |
|---|---|---|---|
| 1 | Nine-code waste taxonomy (W1–W9) | `taxonomy.py:38`–:49 enum; rules at :185–:241 | **Implemented** — "here is the enum, here are the five rules, here are the tests" |
| 2 | Exhaustive state-space enumeration | `enumerate_states()` `taxonomy.py:272`; `_DIMENSIONS` :248; product = 98,304 | **Implemented** — "3×2¹⁵, proven by the audit script" |
| 3 | Coverage proof (0 unmapped, 9 reachable) | `test_exhaustive_every_coherent_observed_state_maps_to_exactly_one_code`, `test_every_declared_code_is_reachable` | **Implemented** — 25 tests green |
| 4 | Data-gap vs residual separation | `DATA_GAP` :64; integrity-first rule :205; `test_data_gap_and_residual_are_different_claims` | **Implemented** |
| 5 | Incoherent states never become codes | `violations()` :136; `test_incoherent_states_produce_no_row_and_nothing_else` | **Implemented** |
| 6 | classify never raises, never returns two | `test_classification_never_raises`; contract docstring :20 | **Implemented** |
| 7 | Human-readable per-state explanation | `explain()` :357; `test_explain_is_human_readable` | **Implemented** — demo overlay lives on this |
| 8 | Timeline scrubber helper | `with_change()` :379 | **Implemented** — demo interacts through this |
| 9 | Provider ledger P1/P2/P3 | — | **Not currently supported by the implementation.** (spec B) |
| 10 | Queue Digital Twin (DES, live-fitted) | — | **Not currently supported by the implementation.** (spec B, simulated in demo) |
| 11 | net_value ≤ 0 rejection | — | **Not currently supported by the implementation.** (spec B) |
| 12 | RSR slot reallocation (admin-compatible) | — | **Not currently supported by the implementation.** (spec B) |
| 13 | No-show forecast / model | — | **Not currently supported by the implementation.** (spec B) |
| 14 | Edge SQLite store, LAN-only, offline | — | **Not currently supported by the implementation.** (design B, `:336`) |
| 15 | Five-role staff app / seven-tap timeline | — | **Not currently supported by the implementation.** (design B; the seven *states* map 1:1 to `PatientState`, A) |
| 16 | Wall display + opt-in SMS + MIS export | — | **Not currently supported by the implementation.** (spec B, `§4.1`) |
| 17 | Auth, RBAC, JWT, HTTPS | — | **Not currently supported by the implementation.** (spec B) |
| 18 | Seven-gate validation harness (days 8–14) | — | **Not currently supported by the implementation.** (P1 build item; coverage half proven today) |
| 19 | Synthetic-token demo generator | — | **Not currently supported by the implementation.** (P0 build item; seeds live in the audit script) |
| 20 | Test suite runs from repo root | 25/25 green from `cadence/` only | **Partial** — "run from the package directory; that is a packaging gap we have named" (P1) |

**18 · Twenty-second answers** (the ones that survive a cut-off)

| Question | 20-second answer |
|---|---|
| What is it? | A closed-loop OPD flow engine: measure every waiting minute into nine causes, price any fix in clinician-minutes, and refuse fixes that don't pay for themselves. |
| Why does it exist? | India already measures queues (LASI, CAG), but nothing closes the loop inside a shift. CADENCE owns measure → decide → intervene → verify, at token level. |
| Is the AI real? | The classifier is provable rules — 98,304 states, zero unmapped, all nine codes reachable, held by 25 tests. The models (twin, no-show) are specified for days 1–7 fit, days 8–14 holdout. |
| Any real data? | We have no hospital's data and we won't fake one — every demo number is synthetic and labelled; the citations are real and sourced; the only live computation is the classifier. |
| What is your single boldest claim? | That we'd rather print "do not do this" than a recommendation. The system's veto is its trust feature. |
| Seven gates? | Median <20, P90 <30, abandonment ±3pp, W9 <2% with green coverage, stage-order <1%, short-idle <10%, first-tap P95 <10 min — pre-registered, run on held-out days 8–14, never yet run. |
| Paper token? | Primary. It's the floor that works when phones, SMS, and ABDM don't. |
| What's built today? | The measuring half: the nine-code ledger, executable and proven. Twin and RSR are specified, labelled simulated in the demo. |

**19 · Sixty-second answers** (the full arc — rehearsal script)

> "CADENCE is a control loop for an OPD wait. It records what actually happens to a patient's minute — nine codes: counter idle, counter queue, nursing idle, nursing queue, clinician absent, clinician busy, diagnostics detour, documentation, unclassified — plus a provider ledger. That taxonomy is real code: all 98,304 observable states, zero unmapped, every code reachable; 25 tests prove it, and a missing transition is surfaced as a data gap so we never manufacture minutes.

> "The second stage is the Queue Digital Twin — a stochastic simulation fitted to the hospital's own first seven days, held out on days 8–14, gated by seven pre-registered thresholds including W9 under two percent and a green coverage report. Every intervention is priced in clinician-minutes; if it doesn't pay for itself the twin says 'do not do this' — that veto is the feature. The third stage, RSR, reallocates a released slot to the next waitlisted patient whose administrative records are clear — administrative compatibility, never clinical triage.

> "The demo is honest by construction: numbers are synthetic and labelled, citations are real, and the one thing running live is the classifier itself. We are not claiming we cut anyone's wait; we are claiming we can measure it provably and refuse to advise what won't work."

---

## 20 · Questions we cannot answer honestly (overfill guards)

These get the unsupported string or a documented boundary — never a conjured answer.

| Unanswerable question | What we actually have | Audible reply |
|---|---|---|
| "What is your measured improvement in real patient waits?" | No hospital data yet; gates unrun | "We have no measured improvement to report. The demo shows a provable measure and a priced proposal — the gates on held-out days 8–14 are the improvement claim, and they have not run." |
| "What is the accuracy of your no-show model?" | No model exists | "Not currently supported by the implementation. The no-show forecast is specified, unfitted, uncalibrated." |
| "Which departments will best benefit?" | No per-department data, benchmarking off by default | "We can't say. Benchmarking is opt-in and nothing has run." |
| "What does your twin predict for a real hospital's queue?" | Specified, not built | "Not currently supported by the implementation. The twin is specified and its demo output is always labelled simulated." |
| "Is your system compliant with any hospital's security policy?" | Design controls only | "The security controls are specified, not deployed. The demo touches no real data, so nothing in the demo is subject to a hospital policy." |
| "How long before a hospital sees ROI?" | Cost header is synthetic | "We publish the build-order and costing table, but an ROI figure would be a guess, so we won't give one." |

## 21 · Features that MUST be implemented before the demo

| # | Feature | Why now | Evidence today |
|---|---|---|---|
| 1 | **Synthetic-token generator** (deterministic seeds, parameter overlay) | The demo's live numbers come from it; seeds currently only live in the temp audit script | C/P0 — GAP |
| 2 | **The 8-beat demo, retimed**, incl. beat 0 label (0:00–0:12) | Current pack has 7 beats, no beat 0, and stale content (six causes, four thresholds, three unknowns) | GAP — sync in the demo task |
| 3 | **Live-classifier runner** wiring `classify()`/`explain()`/`with_change()` to the slide, with the 15-second fail-safe to pre-rendered video | It is the one genuinely live computation, and the fail-safe is specified in §10 | E — GAP |
| 4 | **Seven-gate summary card, corrected** (in the demo overlay and judge card) | Spec and demo must not disagree on stage | GAP — sync |
| 5 | **Docstring fix 32,768 → 98,304** at `taxonomy.py:275` and `test_taxonomy.py:11` | A judge reading the code will find it; we announce the find | A\* — fix in pass |

## 22 · Features that may remain simulated

| Feature | How it stays honest in the demo |
|---|---|
| Queue Digital Twin (DES, net_value) | Every twin output carries a "SIMULATED" label and parameter overlay; the twin is never presented as measured |
| RSR slot reallocation | Demo shows the *rule*, labelled simulated; the rule is administrative-compatibility only |
| No-show forecast | Shown as a pipeline step, not a forecast |
| Wall display / SMS / MIS export | Shown as screens; labelled B/design |
| Wait-time graphs | Synthetic token streams through the *real* classifier |
| LLM summariser | Optional off-path; present only if the demo's LLM is genuinely off-path |

## 23 · Security fixes required before demo

| # | Fix | Severity | Note |
|---|---|---|---|
| 1 | Doc-only correction of both 32,768 docstrings | Low | Done in the doc pass; a *finding we named first* |
| 2 | Test-suite-from-root packaging (pyproject/`-m pytest` UX) | Medium | Named: "tests pass from `cadence/`, not the repo root — a packaging gap, not a coverage gap" |
| 3 | Lock the demo to zero real data (no env leak, no network calls) | High | Demo touches nothing real; verify with a network sweep before stage |
| 4 | No secrets in any demo artefact (keys, tokens, URLs) | High | Repo already clean; re-sweep before stage |
| 5 | Version banner on every slide reads v4.0 (currently "v2" in the demo pack footer) | Medium | Sync item |

## 24 · Production-only requirements (NOT demo items)

| # | Requirement | Yes/no today |
|---|---|---|
| 1 | Hospital data-processing agreement + DPDP fiduciary/processor roles | No — demo uses no real data |
| 2 | TRAI DLT registration for SMS (2–6 weeks) | No |
| 3 | RBAC, JWT, HTTPS, LAN control validation | No — specified (B) |
| 4 | Seven-gate validation run (days 8–14 holdout) | No — future |
| 5 | Incident runbook for breach/power | No — documented scope |
| 6 | Per-hospital privacy notice / consent flow | No |
| 7 | Edge deployment on the hospital's mini-PC | No |

## 25 · Final "Do Not Claim" list

Read this list aloud before any judge interaction; anything here is banned on stage.

1. "We validated the twin" / "all gates passed"
2. "Six causes" / "zero remainder / zero unassigned minutes"
3. "Two taps per patient"
4. "Clinical triage, priority, severity, or diagnosis by CADENCE"
5. "Real hospital data" (we have none; the demo is synthetic + labelled)
6. "98,304 *coherent* states" (98,304 raw; 6,976 coherent)
7. "AES-256 / TLS / JWT / RBAC shipped" (specified, not built)
8. "The demo is measurement-only waste-ledger" — it is measure + propose, twin/RSR simulated; the §9.3 fallback *excludes* RSR — be precise about which claim
9. "CAG Chapter IV" (must be Chapter III), "LASI best domain" (worst of six, 4.6%), "Kemdirim 2022" (2021), "87.30% walk-ins" (87.30% *visited directly* — not a walk-in rate)
10. "ABHA solved registration" / "ABDM runs the MVP"

---

## Final output (§22 of the audit template · sections A–I)

### A · Executive summary (read this on entry)

> CADENCE is a closed-loop OPD flow engine. It measures every waiting minute into nine provable causes, prices any intervention in clinician-minutes, and owns the verdict "do not do this." The measuring half is real code today: 98,304 states enumerated, zero unmapped, all nine codes reachable, 25 tests green, a missing transition surfaced as a data gate instead of manufactured waste. The deciding half — the Queue Digital Twin and RSR — is specified in v4.0 and shown simulated, honestly labelled. The demo makes exactly one live computation: the classifier itself. Success criteria are seven pre-registered gates on held-out days 8–14 that have not yet been run — the demo therefore claims provable measurement and honest refusal, never a wait-time miracle.

### B · The 10 biggest risks on stage

| # | Risk | Pre-empt in the demo |
|---|---|---|
| 1 | Presenting twin/simulated output as real | Every simulated screen carries the SIMULATED label + parameter overlay; say it aloud at beat 2 |
| 2 | Saying "six causes" or "zero unassigned minutes" | Banned list §25; rehearse "nine codes, held by a test file" |
| 3 | Not citing sources precisely (CAG chapter/Class, LASI direction, Kemdirim year, walk-in phrasing) | Read the corrected source card before every Q&A session |
| 4 | Claiming gates passed | The only pass claim today is coverage (0 unmapped states); thresholds are unrun by design |
| 5 | The 32,768 docstring found by a judge | We announce it first (§23 row 1), turning the attack into a credibility win |
| 6 | Reproducing the demo's numbers live and failing in 15s | Pre-rendered fallback video, labelled, pre-rehearsed cue |
| 7 | No-show / privacy wording drift from §13.2 | Use "computed, logged once, never displayed/exported/joined/used" |
| 8 | "2 taps", "10 taps" — any tap count but seven | Seven taps, printed on the swipe, matching the 16 observable flags 1:1 |
| 9 | Financing/costing guessed on stage | Tablet ₹9–15k × role-count, mini-PC ~₹8k, display ~₹6k, SMS credits + TRAI DLT 2–6 wks; say "estimate" |
| 10 | "The demo is measurement-only" | It is measure + propose; the §9.3 fallback *excludes* RSR — be exact about which claim |

### C · Exact answers to memorise (word-for-word)

1. **Definition:** "A closed-loop OPD flow engine: measure every waiting minute into nine causes, price any fix in clinician-minutes, and refuse fixes that don't pay for themselves."
2. **The thesis:** "Nobody owns measure → decide → intervene → verify at token level. LASI and CAG see waiting; neither can act inside a shift. The gap is the missing loop, not missing data."
3. **The unsupported string (for anything not built):** "Not currently supported by the implementation."
4. **The security posture:** "We designed the system so there is almost nothing to steal, and the demo touches zero real data. Auth, TLS, and role controls are specified, not shipped."
5. **The ethics line:** "CADENCE counts minutes; it does not triage, diagnose, or assign clinical priority. Every prioritisation call stays with the clinician, and we built the 'no' into the machine."
6. **The seven gates:** "Median wait under 20 minutes with upper CI under 20; P90 under 30 with upper CI under 30; abandonment within three percentage points of prediction; W9 under 2% of on-site minutes with a green coverage report; stage-order violations under 1%; short-idle under 10% of consultation events; arrival-to-first-tap P95 under 10 minutes. Pre-registered, run on held-out days 8–14, never yet run."
7. **The data-gap sentence:** "A missing transition produces no ledger row at all. We watch what we can prove, and we count the watch as coverage."

### D · Implementation gaps (admit all five)

1. Classifier is implemented; **everything downstream** (twin, RSR, no-show, display, SMS, MIS export, mapping table, gate harness) is specified, not built.
2. Synthetic-token generator exists only as the temp audit script — a P0 build item before the demo.
3. Tests pass from `cadence/`, not from the repo root — a named packaging gap.
4. The 32,768 docstring at `taxonomy.py:275` and `test_taxonomy.py:11` — fixed in the doc pass, announced first.
5. Demo pack is a pre-v4.0 artefact (7 beats, stale gates/sources/) — retimed and corrected in the demo sync task.

### E · Security gaps

| Gap | Status |
|---|---|
| No auth/RBAC/TLS/JWT in code | Specified (B) — never claim shipped |
| No network/DB/storage in code | Verified zero-surface sweep — the strong quiet point |
| Demo must stay zero-real-data | Verify no env/network/secrets before stage (§23 rows 3–4) |
| Knee-jerk crypto claims | All "AES-256/TLS" references retrained to "specified" in this file |

### F · Emergency workflow (drill this)

1. Live classifier fails → at t+15s cut to pre-rendered video (labelled), continue beat flow. No dead air.
2. Judge asks a triage/clinical-safety question → "We never reorder a patient clinically; that stays with the clinician" + point to §12 boundary.
3. Judge reads the 32,768 docstring on screen → "That is the stale count we found and fixed in this pass; the code computes 98,304 — `_DIMENSIONS` at `taxonomy.py:252`."
4. Judge pressures for a real-world number on waits → "None of our numbers are a hospital's numbers. Here is the source card and here is what is synthetic."
5. Judge catches a demo-pack/spec contradiction → "You're right, and the correction is registered in the QA file, section 17A/sync log."

### G · Demo screen map (8 beats, per spec §10)

| Beat | Window | Screen | Source |
|---|---|---|---|
| 0 | 0:00–0:12 | **The label:** "Stop measuring the queue. Start closing it." | §10 |
| 1 | 1:00 | **The problem:** LASI/CAG saw waiting; the loop is absent. Sources on card (CAG Ch. III Class A; LASI worst of six, 4.6%; De et al. 85.71% >1h) | §5.3 B1 |
| 2 | 1:45 | **The measure:** nine codes live — walk sample states through the real `classify()`; every number is synthetic + labelled | §3.1, §10 |
| 3 | 2:35 | **The twin:** counterfactual priced in clinician-minutes; "SIMULATED"; net_value ≤ 0 shows the veto | §3.2, §7.1 |
| 4 | 2:55 | **The veto printed:** "do not do this" — a feature | §7.1 |
| 5 | 3:40 | **RSR:** released slot → next *administratively compatible* waitlisted patient; never clinical priority | §3.3 |
| 6 | 4:05 | **The integrity story:** data-gap vs W9; coverage 0.5; 3,488 gaps counted, never hidden | §3.1 |
| 7 | 4:30 | **The gate:** seven thresholds, held-out days 8–14; "SIMULATED" everywhere; close | §6.4, §10 |

### H · Readiness scores (0–100, nine dimensions)

| Dimension | Score | Basis |
|---|---|---|
| Problem clarity | 95/100 | Thesis is crisp; gap (absent loop) is auditable in LASI/CAG |
| Product definition | 90/100 | Three engines, one hospital, paper-primary, EDGE constraint — exact |
| Code quality | 88/100 | stdlib-only, contract-tested, 25 green, zero attack surface |
| Build completeness | 35/100 | Only the classifier ships; twin/RSR specified — the honest aching point |
| Data / provenance | 85/100 | Real citations, synthetic demo labelled, coverage computable |
| Privacy / security | 80/100 | Zero-surface code; controls specified, not shipped |
| Demo fit | 65/100 | Pre-2026 doc pack (7 beats) — retime + relabel to 8 beats with fallback |
| Ethics / fairness | 95/100 | No-triage boundary, veto, admin-compatible RSR, opt-in benchmarking |
| Validation honesty | 80/100 | Pre-registered gates, held-out days, not-yet-run — exactly the right posture |

### I · Verdict & the asked-for RAG

Given the demo pack has NOT yet been synced to v4.0 (7 beats; stale gates/sources; missing beat 0), **the pack is not yet demo-ready.**

- After the demo-sync pass completes (8-beat retime, SIMULATED labels, corrected source card), verdict: **READY — with the build gaps printed in the opening Q&A (twin/RSR = specified + simulated).**
- If the live-classifier runner and its 15-second fail-safe are not wired: **PARTIALLY READY** — the demo must then rely on the pre-rendered video alone and the honesty story weakens.
- Verdict today, honestly logged: **PARTIALLY READY** — the strong assets (provable ledger, ethics, provenance, 25 green tests) are real; the demo layer and the twin/RSR story are the two things standing between us and full READY.