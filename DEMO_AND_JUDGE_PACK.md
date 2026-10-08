# CADENCE — Demo & Judge Pack

### Superseding run book for the live demo, the short pitch, the printed judge card, and cross-examination

**Supersedes:** `CROSS_EXAM_AND_DEMO_CHECKLIST.md` (Queue Intelligence run book). Every beat, figure and answer below is rebuilt against `PROJECT_SOLUTION_FINAL.md` v4.0. Where the old checklist conflicted with v4.0, the old content is dropped, not softened.

**Track:** AI & Machine Learning — Smart Hospital Queue Management
**Team:** CATALYST CREW · **Institution:** NEHRU ARTS AND SCIENCE COLLEGE, COIMBATORE
**Tagline:** *Stop measuring the queue. Start closing it.*
**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE

**What changed versus the old run book, and why it matters on stage:**

| Old checklist | Status now | Reason (v4.0) |
|---|---|---|
| Peak wait 72 min → 47 min (−35%), +12% utilization recovery | **Dropped** | Unanchored simulation figures presented as performance. All demo figures are now Class D `SIMULATED` and every band is *within-model variance*, not accuracy. |
| NHAMCS wait statistics, Synthea cohorts as evidence | **Dropped** | NAMCS is quarantined to a schema/codebook reference and a US-context sanity check. No Indian figure may come from it. |
| Prophet in the model stack | **Dropped** | `facebook/prophet` is in **maintenance mode as of v1.4.0** — bug fixes, dependency bumps, R↔Python parity only, no new features planned. Replaced by `scikit-learn` `HistGradientBoostingRegressor`. |
| "13.4–25.9% of outpatients avoid public hospitals because of queues (NSS)" | **Dropped** | Not attributable to a primary source. Cut from the pitch permanently. |
| "ABHA solved registration — 25 crore registrations — and created the wait" | **Dropped** | Confounds a scale milestone with a causal claim. ABDM is ecosystem context only; **25 crore OPD registrations**, not visits, and not a CADENCE performance claim. |
| Surge mode that "re-prioritizes triage" | **Dropped** | §13.1: no triage, no severity, no clinical inference, anywhere. |
| Patient PWA, WhatsApp/voice/local-language roadmap | **Dropped** | §3.4: no app for patients. QR/USS at the gate, a physical display, and SMS. |
| ABHA/FHIR/HL7 pluggable integration layer | **Dropped** | §9.1: no ABHA/ABDM write path in MVP. Naming it as a dependency is a credibility risk. |
| Per-hospital SaaS licence business model | **Dropped** | v2 is not a commercial model. It is a measurement system a government hospital can run: one building, no hardware, a ₹8k mini-PC. |
| Lead/ML/Design/Backend four-way split | **Replaced** | Three roles. See Part 5. |
| Two-laptop boot, video on two USBs + cloud, "no single point of failure" | **Preserved, tightened** | Still correct. Now joined by a LAN offline duplicate, per §10 fail-safe. |
| Golden Do-Not List | **Preserved and extended** | Carried into Part 4 (one "must not say" per question) and Part 5. |

**What survives unchanged and must stay:** the hard contradiction in beat 1, the refusal in beat 4, the volunteered-gaps slide in beat 7, the printed judge card at beat 7, the 15-second single-retry rule before cutting to video, and the rule that no fabricated metric ever appears on screen.

---

# PART 1 — SPEAKER SCRIPT · 4 min 30 s live demo

**Determinism:** every number and animation is pre-computed at `seed=20261003`, except **one genuinely live computation** — at beat 2 we re-run the `W1`–`W9` attribution live over the day's token log so the room sees code executing on the exact seed. Precomputed Monte-Carlo is acceptable only alongside something live. No live network dependency.

**Pacing budget.** Total 270 s. Spoken content is **525 words** (standalone dashes and the `[4 s silence]` stage marker are not counted). At a calm presentation pace of **132 words per minute** that is **3 min 59 s** of speech, leaving **31 s** of silent operation and pause across the run — 4 s of it held deliberately in beat 4. Do not add words. If a beat overruns, lose a clause, never the pause.

**Stage rule:** one continuous voice (Role A). Role B operates the console and never speaks. Role C times the beats and hands the cards. Silence during beats 3–6 is correct, not dead air — the screen is doing the talking.

---

## BEAT 0 — The honest opener · 0:00–0:12

**Screen:** Title card. The `SIMULATED — within-model variance` banner. Nothing animated.

**Operation:** Slide 0 is already on screen. Touch nothing.

**SAY (24 words):**

> Everything you're about to see is simulated. Every number is within-model variance, not accuracy. Here's the gate that would tell us the second thing.

**TRANSITION:** *(silently to the two-citation slide — no verbal bridge)*

---

## BEAT 1 — The contradiction · 0:12–1:00

**Screen:** Two citations, side by side. Left: LASI patient-experience — waiting is the **worst** of six domains: 9.5% negative, 40.9% neutral or worse. Right: time-flow figure, 85.71% of on-site time spent waiting to see a doctor (De 2024, one Indian tertiary OPD, n=252).

**Operation:** Slide 1 is already on screen. Click once to reveal both citations together.

**SAY (81 words):**

> Different instruments. Same country. A stopwatch in one Indian tertiary OPD — eighty-five point seven one percent of on-site time spent waiting to see a doctor, nearly nine minutes of every ten. India's national patient-experience survey, seventy-two thousand observations — waiting is the worst of six domains: nine point five percent negative, forty point nine percent neutral or worse. Both things are true. Both can see it. Neither can act on it inside a shift. We stopped measuring the queue. We're closing it.

**TRANSITION:** *(click to Waste Ledger — no verbal bridge; let the ledger be the bridge)*

---

## BEAT 2 — The cause, not the sentiment · 1:00–1:45

**Screen:** Waste Ledger. One day at the reference OPD block. Every on-site minute attributed to exactly one of nine causes, `W1`…`W9`, with per-provider rows `P1`, `P2`, `P3`. One cause visually dominant.

**Operation:** Land on the ledger. Hover the dominant cause for two seconds so the tooltip reads.

**SAY (79 words):**

> One day at one OPD block. Every on-site minute is attributed to exactly one of nine causes: counter idle, counter queue, nursing idle, nursing queue, clinician absent, clinician queue, diagnostics detour, documentation, or unclassified. Unclassified carries its real value — point three nine nine percent of observed minutes: a residual we pre-defined, not a zero we engineered. The ledger is also per provider: P one, P two, P three. One cause dominates. That's a rostering question, not a sentiment question.

**TRANSITION:** "And the only currency that fixes it is doctor-minutes." *(move to console)*

---

## BEAT 3 — The twin · 1:45–2:35

**Screen:** Counterfactual console. Left panel = proposal. Right panel = baseline vs. proposed, per OPD, three rows: median wait, P90 wait, abandonment. Every banded chart title carries `SIMULATED — within-model variance · UNGATED`.

**Operation:**
1. Call up Proposal 1: *Move one room from Orthopaedics to General Medicine, 11:00–13:00. Convert the Orthopaedics second room to a nurse-run follow-up fast-track.*
2. Click **RUN COUNTERFACTUAL**. Let the render complete — do not narrate over the animation.
3. Point at the P90 row.

**SAY (102 words):**

> Here is a proposal a superintendent would make. Move one room from Orthopaedics to General Medicine, eleven to thirteen. Convert the Orthopaedics second room into a nurse-run fast-track for follow-ups only. CADENCE live-fits a discrete-event twin of this OPD block from the ledger, applies the change, and answers three questions per OPD: median wait, P90 wait, abandonment. I point at P90 because P90 is what a patient feels — the median is the comfortable lie. Two constraints are enforced in the design. The doctor must be credentialed for the receiving department. Nurse capacity is the only thing we may re-route. We never invent doctor-minutes.

**TRANSITION:** "Now the proposal I wish were true." *(switch panel, do not leave the console)*

---

## BEAT 4 — The refusal · 2:35–2:55

**Screen:** Same console, Proposal 2 loaded — a proposal that looks good on paper. The result line renders as: **`net value −14 min/100 cases. Do not do this.`**

**Operation:** Load Proposal 2, click **RUN**. Result line appears. **Then stop moving. Hold 4 seconds of silence.** Do not advance.

**SAY (35 words):**

> Second proposal. CADENCE prices it in clinician-minutes and returns — net value minus fourteen minutes per hundred cases. Do not do this. *\[4 s silence\]* That is the product. A tool that can only say yes is a dashboard.

**TRANSITION:** *(no line. Cut straight to RSR.)*

**Why this beat exists:** it buys credibility for every other number on the screen. If you have eleven seconds left in the whole slot, spend them here.

---

## BEAT 5 — The loop closes · 2:55–3:40

**Screen:** RSR view. A released slot at 14:05. Bipartite matching panel: released capacity (left) against queued demand (right). Match on administrative compatibility; offer only if it pushes no one already queued. SMS confirm animation.

**Operation:**
1. Advance the clock to 14:05 — the slot releases.
2. Click **RE-OFFER**. Matching resolves to one compatible follow-up patient.
3. Let the SMS confirm animation play, then the token re-enter the pipeline as a priority-queued arrival.

**SAY (94 words):**

> Now the part the whole category skips. Every hospital in the world already predicts no-shows. The prediction says this slot will be empty. And then nothing happens to it. The chair is empty either way — that capacity is already paid for. At fourteen-oh-five a slot releases. CADENCE matches it to the longest-waiting administratively-compatible patient — one tap, and only if the offer doesn't push anyone already queued. A compatible follow-up gets one SMS, one tap, and re-enters as a priority arrival. We are not trying to predict better. We're recovering capacity the system already paid for.

**TRANSITION:** "None of that matters if the hospital's auditor can't read it." *(move to export)*

---

## BEAT 6 — The audit · 3:40–4:05

**Screen:** MIS export. The day's figures rendered in CAG audit field names.

**Operation:** Open the export. Scroll once, slowly, down the field mapping.

**SAY (84 words):**

> The day's figures render in CAG audit field names — flow of patients in OPD, waiting time for outpatients, consultation time per patient. We didn't invent a metric; we adopted the auditor's vocabulary. And the export carries the mapping table, showing where our metric is not comparable to theirs. That is the honest part.

**TRANSITION:** "Which brings us to what we don't know." *(advance to the static slide — no animation)*

---

## BEAT 7 — The honesty slide · 4:05–4:30

**Screen:** Static. Seven named `UNKNOWN`s, each with an owner. The seven validation-gate thresholds, printed. `SYNTHETIC DATASET — SIMULATED` banner. The one live computation.

**Operation:** Advance to slide. Role C steps forward with the printed judge cards and places them face-up on each judge's table. Role A does not move.

**SAY (66 words):**

> Seven things we don't know — each with an owner. The no-show base rate. Our abandonment rate. Our twin's real-world accuracy. Why the survey compresses waiting. What is addressable. How much is booked. How survey and audit disagree. Seven gates. Miss one, we ship measurement-only and say so. Card in hand: thresholds, unknowns, sources, and the live computation.

**TRANSITION / CLOSE:** *(hold eye contact, do not add a line)*

---

### PART 1 — spoken-word ledger

| Beat | Window | Spoken words | Speech @132 wpm | Silent operation / pause |
|---|---|---|---|---|
| 0 — title card | 0:00–0:12 | 24 | 11 s | 1 s |
| 1 — contradiction | 0:12–1:00 | 81 | 37 s | 11 s (click to reveal both citations) |
| 2 — Waste Ledger | 1:00–1:45 | 79 | 36 s | 9 s (hover W1–W9 / dominant cause) |
| 3 — the twin | 1:45–2:35 | 102 | 46 s | 4 s (counterfactual render) |
| 4 — the refusal | 2:35–2:55 | 35 | 16 s | 4 s held inside the line |
| 5 — RSR | 2:55–3:40 | 94 | 43 s | 2 s (match + SMS confirm) |
| 6 — the audit | 3:40–4:05 | 53 | 24 s | 1 s (scroll the export) |
| 7 — honesty slide | 4:05–4:30 | 57 | 26 s | 0 s (card handout overlaps) |
| **Total** | **4:30 (270 s)** | **525** | **3 min 59 s** | **31 s across the run** |

**Delivery constraints.**
- No filler. No "so", no "basically", no "kind of", no "you know". If you lose a word, restart the clause.
- Numbers are spoken as the audience reads them, not digit-by-digit: "eighty-six point seven", not "eight-six point seven". "P90", "W3", "RSR" are said as written.
- Never narrate over an animation. Silence while the console renders is the correct read of competence.
- Beat 4's silence is 4 full seconds. Count it in rehearsal until it feels long.

---

# PART 2 — 90-SECOND PITCH

*Continuous prose. Read it aloud in a rehearsal and cut anything that makes you run out of breath. ~250 words, ~110 seconds at a calm 138 wpm.*

Indian government outpatient departments do not have a registration problem. They have a load-versus-service-rate mismatch — and the software they already bought cannot see it, and the surveys they already run cannot report it.

In four OPDs at one Indian tertiary hospital, patient flow exceeded the doctor service rate in every department — and in Orthopaedics, eighty-five point seven one percent of on-site time was waiting to see a doctor. At two government hospitals in Hyderabad, the site with a health management information system had forty point two percent of outpatients waiting two hours or more; the site without one had twenty-three point four. And India's national patient-experience survey still ranks waiting the worst of six domains. Both things are true. That is the finding.

CADENCE is the closed loop nobody owns. Every idle minute lands in exactly one of nine causes — unclassified carries its real residual, not a zero. It simulates a proposed reconfiguration before you commit, prices it in clinician-minutes, and tells you when it is not worth it. When a no-show frees a slot, it re-offers it to the longest-waiting administratively-compatible patient — it does not just log the no-show.

We are demoing measurement-only on synthetic data, in one building. Seven unknowns are on the slide, each with an owner. The twin must clear seven pre-registered gates before it recommends anything — miss one, we ship measurement-only and say so.

India already audits for waiting time, flow, and cases per doctor per annum. We did not invent a metric; we are building the loop that moves them.

---

# PART 3 — PRINTED JUDGE CARD

*One page. Print single-sided, 11pt minimum. Hand out at beat 7, face-up, one per judge. Do not narrate the card.*

---

### CADENCE — measurement-only MVP for one government OPD block

**Evidence classes per claim: A verified primary · B published study (setting stated inline) · C structural analogy (e.g. international comparator, setting stated inline) · D simulated · E unknown**

*(Class A\* — CAG of India: §5 appendix p. 8 of the solution spec. Used on the card for audit field-name vocabulary, not as an endorsement of its registered uptake conclusions.)*

---

#### 1. PRE-REGISTERED VALIDATION GATE — the twin must clear all seven

Phase: 14 consecutive operating days, one partner site, token-level logs, n ≥ 1,500 encounters. If the site runs below n, we extend the window rather than lowering the bar.

| # | Metric | Threshold |
|---|---|---|
| 1 | Median wait-time error | MAPE < 20% |
| 2 | P90 wait-time error | MAPE < 30% |
| 3 | Abandonment rate | within ±3 percentage points of observed |
| 4 | W9 `unclassified` residual | < 2% of **observed** on-site minutes (data-gap minutes excluded) |
| 5a | Stage-order violations | < 1% of token transitions |
| 5b | Short idle (provider idle < 60 s) | < 10% of provider-idle episodes |
| 5c | Arrival → first-tap latency | P95 < 10 min |

**If any gate fails:** CADENCE reports the failure, reports by which cause the twin diverges, and **ships in measurement-only mode** (Waste Ledger + RSR, no reconfiguration recommendations). Registered before data collection. Not tuned after.

**Intervention gate (separate, after the twin passes):** one intervention, 10 days, stepped-wedge comparison across matched OPD sessions. Accepted only if measured recovered clinical minutes exceed clinician-minutes cost. Reported either way, including if negative.

---

#### 2. SEVEN DECLARED UNKNOWNS

| Unknown | Why it matters | How we resolve it |
|---|---|---|
| Indian government OPD **no-show base rate** | Sets the ceiling on RSR entirely | Phase 0: 14 consecutive days of token-level logs at one partner site |
| Indian government OPD **abandonment** ("left without being seen") rate | Primary harm metric | Same Phase 0 measurement. Never estimated from foreign data |
| **Real-world accuracy of our twin** | All benefit numbers depend on it | The gate above. Until it passes, every benefit figure is Class D `SIMULATED` |
| **Why the survey compresses waiting** | Both a survey and a time-flow audit can be true | Phase 0: paired comparison of survey response and token-log waiting for the same sessions |
| **What is addressable** | Caps every recovery claim | Phase 0 attribution: the sub-2-hour idle stock we can actually release without service-rate change |
| **How much is booked** | Only booked sessions are schedulable in RSR | Phase 0: booked share of all encounters by department |
| **How survey and audit disagree** | Is the spread of views real, or an instrument artefact? | Phase 0: run survey instruments alongside the audit vocabulary and diff the two readings |

Also constrained: the Hyderabad HMIS finding is stated as **association only**. Our thesis is written to survive that restriction.

---

#### 3. SOURCES — six, Class A and B (one Class C comparator quarantined below)

| Class | Source | Figure used |
|---|---|---|
| **A** | **CAG of India, Report 2 of 2025** — *Public Health Infrastructure and Management of Health Services*, period ended March 2022, Chapter III | Audits: flow of patients in OPD; registration of outpatients; waiting time for outpatients; OPD cases per doctor per annum; consultation time per patient in OPD; patient satisfaction survey for outdoor patients |
| **A** | **NSS 75th Round, Household Social Consumption: Health** (Jul 2017 – Jun 2018), MoSPI Summary Analysis Report 586 | Treated ailment spells at government/public institutions: 33% rural / 26% urban. Avg medical expenditure per hospitalisation case (excl. childbirth): ₹16,676 rural / ₹26,475 urban |
| **A** | **ABDM press releases**, abdm.gov.in/press-releases | 25 crore OPD **registrations** under Scan & Register — registrations, not visits, not consultations |
| **B** | **De A, Gupta S, Chakraborty A.** Dr Sulaiman Al Habib Medical Journal 2024;6(3):136–141. DOI 10.4103/dshmj.dshmj_63_24 — time-and-motion, 4 OPDs, Indian tertiary hospital, n=252 | Patient flow exceeded doctor service rate in **all** OPDs; **87.30% visited the institute directly**; 63.89% newly registered; Orthopaedics: **85.71%** of total patient time spent waiting to see a doctor |
| **B** | **BMC Health Services Research** 2026. DOI 10.1186/s12913-026-14997-y — two government facilities, Hyderabad, n=214 | Long wait (≥120 min): **40.2% HMIS site vs. 23.4% non-HMIS site**. Adjusted ORs — HMIS presence **2.05** (1.04–4.03); high patient load **1.84** (1.03–3.46); technological challenges **1.93** (1.04–3.61). **Association, not causation** |
| **B** | **Ambade M et al.** 2024, LASI all-India + sub-national patient experience, 72,270 observations | Waiting time is the **worst** of six service domains: **9.5% negative**, **40.9% neutral or worse**. Overall satisfaction reads high — the wait itself is saturated negative |

**Quarantine — what is deliberately NOT cited here.**
- **Kemdirim CJ et al.** 2021, *Niger Medical Journal* 62(6):325–333 (DOI 10.60787/NMJ-62-6-63, PMID 38736516, PMC11087679) — **Class C**, Nigeria, public vs. private outpatient time-flow. Mechanism generalises to Indian OPDs; magnitude does **not** (86.7 min vs 20.9 min idle per encounter; 65.3% share — never "70.7%").
- **CDC NAMCS 2023 Health Center Component** — schema/codebook reference and US-context sanity check only. `US health centers, 2023 (NAMCS HC) — not generalisable to Indian OPD.` No Indian rate is derived from it. (`VISWT` weight variable corrected 31 August 2025; pre-correction analyses must be re-run.)
- **Brazilian no-show dataset** — pipeline unit-test fixture only. No figure from it appears in any slide or in this card.
- **Removed, not reinstated without a primary source:** the "13.4–25.9% avoided a hospital visit due to waiting time" attribution. Not traceable.
- `facebook/prophet` is in **maintenance mode as of v1.4.0**, not deprecated: bug fixes, dependency bumps, R↔Python parity only, no new features planned.

---

#### 4. THE ONE LIVE COMPUTATION

Everything on stage is pre-computed at `seed=20261003` — except one step that must run live in the demo: beat 2 re-runs the **W1–W9 attribution** (`taxonomy.classify()`) over the day's token log, and the Waste Ledger renders from that run.

Synthetic 14-day, single-OPD-block dataset with a printed provenance sheet and explicit parameter ranges. **This is not real hospital data and is not presented as any.** Deterministic at the seed above.

---

#### 5. REPO

`https://github.com/muhammedfahim438-ctrl/CADENCE`

---

#### 6. WHAT THE BAND ON EVERY CHART MEANS

> **SIMULATED — within-model variance.** Stochastic inputs of our fitted model — arrival jitter, service-time draws — are re-drawn 10,000 times and the spread reported. It answers: given our model of this OPD, how sensitive is the outcome to randomness inside that model? It does **not** answer: how accurate is our model of the real OPD. That is the gate above, and we claim no answer before it runs.

**North-star:** idle clinical minutes per 100 encounters — lower is better. **Guardrail:** abandonment rate must never rise.

---
---

# PART 4 — ANTICIPATED CROSS-EXAMINATION · 15 QUESTIONS

Answer rules for all fifteen: **three sentences maximum.** Sentence 1 = the honest answer. Sentence 2 = the evidence or the mechanism. Sentence 3 = the limit or the gate. Never volunteer a fifth thing. If the answer needs a fourth sentence, the answer is "no" plus a reason.

Evidence class per §5.1: **A** verified primary · **B** published study · **C** structural analogy · **D** simulated · **E** unknown.

---

### Q1 — "Every number on that screen came out of your own simulation. How do I know your model isn't just agreeing with itself?"

**Answer:** We don't — yet, and that's why the demo is measurement-only. The pre-registered gate tests it: 14 operating days, n ≥ 1,500 encounters, seven gates — median wait MAPE under 20%, P90 under 30%, abandonment within ±3 points, the W9 `unclassified` residual under 2% of observed on-site minutes, and three fidelity gates on the token pipeline (stage-order violations under 1% of transitions, short-idle under 10% of provider-idle episodes, arrival-to-first-tap P95 under 10 minutes). The bands you saw are within-model variance across 10,000 re-draws; they say how sensitive our model is to its own randomness, not how close it is to the real OPD. Until the gate runs, every benefit figure in CADENCE is Class D, simulated, and labelled on the same visual.
**Class:** D (demo figures) + A (pre-registered gate) · **Spec:** §6.2, §6.3
**Do NOT say:** anything of the form "our model is about X% accurate." That number does not exist yet. Do not call the band a confidence interval on real-world wait.

---

### Q2 — "This is just another queue-display app with a nice screen. Why wouldn't a hospital just buy that?"

**Answer:** Because a display is exactly what the reference site already tried, and it was *associated* with longer waits — 40.2% of outpatients waiting two hours or more at the Hyderabad HMIS site versus 23.4% at the non-HMIS site, adjusted OR 2.05. The reasonable reading isn't that HMIS causes queues; it's that a system which displays a queue without owning an intervention leaves every driver of the queue untouched. CADENCE holds the model, chooses the intervention, prices it in clinician-minutes, executes it through staff, verifies it, and reverts it if it didn't work.
**Class:** B (setting stated: two government facilities, Hyderabad, n=214) · **Spec:** §2 Step 3, §5.2 item 3
**Do NOT say:** that HMIS *causes* longer waits. It is a cross-sectional association with a CI that touches 1.04. Also do not say "the category has no closed loop" as an absolute — say it is unowned in the public OPD.

---

### Q3 — "You're building a database of how patients move through a hospital. What happens the day it leaks?"

**Answer:** We store token, timestamps, department, role, service type, and a pseudonymous patient reference — no clinical content, and no write-back to any hospital's clinical record. There is no individual patient score: the no-show model produces a probability used once, to decide whether to re-offer a slot, and it is never persisted as a patient attribute, displayed, or exported. Patient-side waste is aggregated at OPD level only. QR scan carries a plain-language consent notice, SMS opt-out is honoured permanently and immediately, and the MIS feed is read-only and aggregate.
**Class:** A (design constraints, testable in code) · **Spec:** §4, §13
**Do NOT say:** "the data is anonymised" as a blanket reassurance. It is pseudonymised at the token level and aggregated on export — say that instead, precisely.

---

### Q4 — "Your whole ledger depends on a doctor tapping a button twice per patient. Doctors won't do that. What then?"

**Answer:** That's a High-severity risk and we've planned for it rather than around it: the clinic taps two of seven token transitions, keyed to the user's role, and the ledger is computable only if the clinic taps — so the mitigation is that the ledger itself is the incentive, because departments compete on their own number. We pilot with the department that volunteers. And the honest floor: if taps don't happen, the system degrades to counter and display, and the doctor-not-present cause goes dark.
**Class:** A (design) + E (adoption is unmeasured) · **Spec:** §12
**Do NOT say:** that there is a fallback sensor or IoT counter. Hospital IoT was deleted from scope, not deferred. Do not claim any adoption rate — we have none.

---

### Q5 — "Eighty-seven point three percent of that traffic is walk-ins. Released-slot reallocation only works for booked appointments. Isn't RSR solving a problem that barely exists?"

**Answer:** You're right that it applies to the booked subset only, and we've listed it as a High-severity risk: Phase 0 quantifies the appointment share first, and if that share is small, RSR is deprioritised and we say so. What RSR does not depend on is a rate we haven't measured — its ceiling is exactly the no-show base rate, which we have declared UNKNOWN and refused to estimate from foreign data.
**Class:** B (direct-visit share 87.30%, Indian tertiary hospital, n=252) + E (appointment share and no-show rate, both unmeasured) · **Spec:** §12, §5.3
**Do NOT say:** any Indian no-show percentage, from NAMCS, from the Brazilian dataset, or from your imagination. The honest sentence is "we don't know the base rate yet — that is Phase 0."

---

### Q6 — "There's no Indian data in this demo. It's all synthetic. Why should I believe anything you showed me?"

**Answer:** We didn't dress it up as real, and we won't. It's a seeded synthetic 14-day, single-OPD-block dataset with a printed provenance sheet, deterministic at seed 20261003. The ledger computation is **live in this demo** — beat 2 re-runs the W1–W9 attribution over the day's token log — and the `pytest` suite (25 tests) is green on the demo machine. The Indian evidence we *do* stand on is published and cited: 86.7 minutes mean idle time per public outpatient encounter in a Nigerian teaching hospital (structural analogy — mechanism, not magnitude), 40.2% versus 23.4% at two Hyderabad government facilities, and arrival flow exceeding doctor service rate in all four OPDs studied.
**Class:** D (demo dataset) + B (published Indian studies) · **Spec:** §5.4, §16
**Do NOT say:** "synthetic-but-realistic" as a substitute for stating it is synthetic. And do not quote the removed NSS "13.4–25.9% avoided a visit" figure — it is not attributable to a primary source.

---

### Q7 — "You've built this for one OPD block. Government hospitals run fifty. How does this scale?"

**Answer:** By argument, not by assertion — and we're specific about which argument. The twin is per-site *by design*: a flow model that transfers across sites without re-fitting is a flow model that is wrong. What transfers is the metric vocabulary, which is already national because we adopted the CAG's audit field names, and RSR, which scales free inside a fixed roster. Second OPD block in the same hospital is Phase 4, and multi-hospital only becomes a roadmap item on the strength of published Phase 1–3 results.
**Class:** A (CAG Report 2 of 2025 field names) + E (cross-site performance, unmeasured) · **Spec:** §9.2, §11
**Do NOT say:** any district-network or state-wide number. We have no cross-site evidence, and "one engine, pluggable adapters worldwide" is exactly the claim we cut.

---

### Q8 — "What does the CAG actually require? Don't you just use their name to sound legitimate?"

**Answer:** Our data is about to be audited and audited things need to be measurable and defined. India's CAG audits flow of patients in OPD, registration of outpatients, waiting time for outpatients, OPD cases per doctor per annum, consultation time per patient in OPD, patient satisfaction survey for outdoor patients, and prescription audit — in Report 2 of 2025, period ended March 2022, Chapter III. We map to those field names directly: idle clinical minutes per hundred encounters is OPD cases per doctor per annum inverted; flow efficiency is flow of patients in OPD; service-time distribution is consultation time per patient in OPD.
**Class:** A (primary, official) · **Spec:** §5.2 item 5, §7
**Do NOT say:** that CAG has endorsed, approved, or is piloting CADENCE. We use their vocabulary. That is interoperability, not endorsement.

---

### Q9 — "What does this cost a district hospital to run?"

**Answer:** A ₹8k mini-PC running SQLite on the hospital LAN, plus whatever tablets already exist, plus one SMS gateway. Zero custom hardware in the MVP — no sensors, no turnstiles, no door counters, no wearables; the clinic taps two of seven token transitions, keyed to the user's role. Internet is needed only for SMS delivery and optional MIS export, so the pipeline keeps running through an outage.
**Class:** A (design constraint) · **Spec:** §4, §11
**Do NOT say:** a per-hospital licence price or a B2G SaaS model. v2 is not a commercial model and we have no pricing study. Do not quote a total cost of ownership figure we have not computed.

---

### Q10 — "Is there an LLM in this? Because if there is, I don't trust a single number you showed me."

**Answer:** There is an optional LLM surface, and it is off the critical path. It may render the Waste Ledger into a plain-language shift-handover summary in the staff console. It never touches the token pipeline, the ledger, the twin, or any clinical content — and if it is unavailable, nothing breaks. There is no clinical reasoning, no triage, no diagnosis anywhere in the system. The models that matter are small and conventional: gradient-boosted arrival intensity, quantile service-time heads, and a calibrated no-show model.
**Class:** A (architecture) · **Spec:** §1.3, §4, §9.1
**Do NOT say:** "AI/LLM" as a blanket label for the whole product. If asked to define your AI, say: small supervised models and a discrete-event simulation, with the LLM optional and off the path. Also do not let the word "triage" near a reallocation feature — we do not triage.

---

### Q11 — "What happens if your twin fails the gate? Then you've demoed nothing."

**Answer:** Then we ship measurement-only, and we said so before we ran it — the fallback is written into the spec, not decided afterwards. Measurement-only is the Waste Ledger plus RSR with no reconfiguration recommendations, and it's genuinely useful: a per-cause, additive, audited ledger, in the auditor's own vocabulary — the `unclassified` residual W9 carries its true share, not a zero. CADENCE would report the failure and report by which cause the twin diverges.
**Class:** A (pre-registered failure handling) · **Spec:** §6.3, §12
**Do NOT say:** that the twin will probably pass, or that a near-miss is a pass. Also do not defend the gate by lowering it — if the site runs below n ≥ 1,500 we extend the window, we don't lower the bar.

---

### Q12 — "What's your no-show model's accuracy?"

**Answer:** Calibration, not AUC. The threshold is a capacity-policy knob, so the probabilities have to be trustworthy at the operating point, not just rank-order well — so we calibrate with isotonic regression and publish a reliability curve in the repo. Accuracy is currently **UNKNOWN**, because we have not collected Indian token-level logs yet; Phase 0 is fourteen consecutive days at one partner site. Until then we don't quote a performance figure for it.
**Class:** E (unknown) + A (modelling choice) · **Spec:** §6.1, §5.3, §9.2
**Do NOT say:** an AUC from the Brazilian dataset, or any no-show percentage from the US NAMCS file. If pressed for a US comparison, the only permitted sentence is a magnitude sanity check tagged `US health centers, 2023 (NAMCS HC) — not generalisable to Indian OPD`.

---

### Q13 — "You re-offer a freed slot. What if that patient doesn't show either? Now you've double-booked and made it worse."

**Answer:** Matched patients get one SMS and one tap — the slot is only re-offered as a *confirmed* re-entry, so a non-response leaves the slot released, exactly as it would have been. That's why RSR recovers waste already paid for rather than creating new risk: it requires no new staff, no new budget line, and no new doctor-minutes. It also targets the booked subset only, so it never touches the walk-in pipeline.
**Class:** A (mechanism design) + E (net recovery rate unmeasured) · **Spec:** §3.3, §12
**Do NOT say:** a recovery percentage. The recovery rate — released slots refilled ÷ slots released — has no existing auditing counterpart and we have not measured ours. Do not claim it "cannot make waits worse"; say the release is confirmed, not assumed.

---

### Q14 — "You quoted a study where the hospital with better software had *longer* waits. That's a convenient finding. You're cherry-picking to justify your existence."

**Answer:** It's inconvenient, which is why we lead with it. And we hold it as an association only — it's a cross-sectional comparison of two government facilities, n=214, adjusted OR 2.05 with a 95% CI of 1.04 to 4.03. Our thesis is written to survive that restriction: the capacity gap, the 86.7 minutes of idle time in the Nigerian comparator (structural analogy — mechanism, not magnitude), and the satisfaction-saturation finding each stand on their own published study without it.
**Class:** B (with setting inline) + E (causality not resolvable by us) · **Spec:** §2 Step 3, §5.3, §14
**Do NOT say:** "HMIS makes queues worse," "digitisation failed," or any causal verb on this study. The permitted sentence is "installing an information system was *associated with* longer waits."

---

### Q15 — "You tell a superintendent to move a room out of Orthopaedics. If Orthopaedics collapses next week, whose problem is it?"

**Answer:** It's the manager's decision, not ours — the twin produces counterfactuals and a `net_value` ranking, and the console shows the median, P90 and abandonment effect for *both* departments side by side, so the cost lands where it lands and is visible before anyone commits. Two hard constraints are enforced in the design: the doctor must be credentialed for the receiving OPD, and no intervention may invent doctor-minutes. And the one intervention we gate after the twin passes runs 10 days with a stepped-wedge comparison across matched OPD sessions, reported either way, including if it's negative.
**Class:** A (architecture and pre-registered intervention gate) + D (any counterfactual number shown) · **Spec:** §3.2, §6.3
**Do NOT say:** that CADENCE auto-executes reallocations, or that we can guarantee a department won't be harmed. It is a decision-support console with a refusal path — the human owns the decision.

---

## Golden do-not list — quick reference for all three speakers

1. No causal language on the Hyderabad HMIS finding. Ever.
2. No Indian no-show rate. No Indian abandonment rate. No Indian wait-accuracy figure.
3. No figure from the Brazilian dataset. It is a unit-test fixture.
4. No NAMCS figure without the tag `US health centers, 2023 (NAMCS HC) — not generalisable to Indian OPD`.
5. No "25 crore OPD visits." It is **25 crore OPD registrations**.
6. No "Prophet is deprecated." It is in **maintenance mode as of v1.4.0**.
7. No "13.4–25.9% avoided a hospital visit." Untraceable; cut.
8. No "prediction vs. reality" panel. We have no reality to put beside it.
9. No "deployed," "live in," "pilot partner," or "CAG-approved."
10. No band described as accuracy, confidence interval on real-world wait, or forecast error.
11. No "zero remainder." The ledger is per-cause and additive; `unclassified` carries a real residual (W9), it is not zeroed.
12. No "clinical compatibility." Released-slot matching is on **administrative compatibility**, and only if it pushes no one already queued.
13. No inverted "cases per doctor per annum" stated as the same figure. It lives in the export's mapping table, with the places our metric is *not* comparable made explicit.
14. No "six causes." The Waste Ledger is **W1–W9**, nine causes.
15. No "four thresholds" / "six gate thresholds" / "three unknowns." It is **seven gates** and **seven unknowns**, each with an owner.
16. No "87.30% walk-ins." Say "87.30% visited the institute directly."
17. No regeneration command on the card or the slide, and do not say "byte-identically." There is **the one live computation** (beat 2 re-runs W1–W9 attribution over the day's token log); everything else is pre-computed at `seed=20261003`.
18. No "measurement-only" as a put-down. Say it is Phase 1, documented honestly, and the pre-registered fallback if a gate fails.
19. No "two taps." Say "two of seven token transitions, keyed to the user's role."
20. No "three-minute" or "four-minute" beat gross overstatement. The ledger says four minutes thirty, and the pitch and beats stay inside it.

---

# PART 5 — REHEARSAL PLAN & PRE-DEMO CHECKLIST

## 5.1 Roles — three people, fixed, rehearsed

| Role | Who | Owns | Speaks? |
|---|---|---|---|
| **A — Voice + thesis** | Most fluent speaker, lowest nerves under interruption | All eight beats, continuous voice. Script on the lectern, never behind the laptop | Yes, all beats |
| **B — Console operator + fail-safe** | Fastest hands, calmest under pressure | Executes every operation in Part 1 on cue; owns the offline-duplicate laptop; owns the single-keystroke video switch | **No.** Silence during beats 3–6 is correct |
| **C — Timekeeper + evidence lead** | Best recall on provenance and thresholds | Calls the 60 s and 15 s warnings; hands out the judge cards at beat 7; leads cross-ex afterwards | No during the demo |

**Swap rule:** if A loses voice mid-demo, B reads the next beat's paragraph from the card verbatim. Rehearse that one handover three times. Nobody improvises numbers.

---

## 5.2 Time-boxed rehearsal plan

| When | Duration | Session | Exit condition |
|---|---|---|---|
| **T−24 h** | 35 min | Run 1 — full 4:30, timed, script on the lectern, no stopping, no notes from the floor | Finish inside 4:30. Then 10 min: mark every place A looked at the screen instead of the room |
| **T−24 h** | 20 min | Fix pass — cut only. Delete clauses to hit the per-beat word budget; do not add | Per-beat word counts in Part 1's ledger are still true |
| **T−18 h** | 30 min | Beats 4 and 5 only, five repetitions each | Beat 4's held silence is a full 4 s and A does not fidget; beat 5's SMS animation lands every time |
| **T−12 h** | 25 min | Full run, standing, B operating, C timing aloud | C calls both warnings without A needing to look at the clock |
| **T−6 h** | 30 min | Cross-exam drill — all 15 questions, split: C answers 8, A answers 4, B answers 3 (the data/privacy/ops ones) | Every answer is three sentences or fewer and ends with the limit or the gate. Nobody uses a banned phrase |
| **T−2 h** | 15 min | Adversarial drill — C plays the hostile judge and pushes past the answer on Q1, Q2, Q11, Q14 | The team repeats the "must not say" line rather than defending a number |
| **T−1 h** | 15 min | One full run. Then stop. | Nothing new is introduced after this point |
| **T−0** | 20 min | Print, stage, run the checklist in 5.3 | Every box ticked |

**Rehearsal prohibitions.**
- Never rehearse the demo on the real stage machine on the night. Rehearse on the backup, on purpose.
- Never let anyone rehearse a number that is not on the printed card. If it's not on the card, it doesn't get said.
- B rehearses the *operations* separately from the words, so B never has to listen to A to know what to click.

---

## 5.3 Pre-demo technical checklist — run at T−15 min, tick before you start

**Redundancy — no single point of failure**
- [ ] Primary demo laptop: booted, on AC, screen brightness and display scaling confirmed on the projector, notifications and sleep disabled.
- [ ] Offline duplicate on the second laptop, on the same LAN, running the same build and the same `seed=20261003` — booted and sitting on beat 1, not on a login screen.
- [ ] Pre-rendered 4:30 MP4 on the primary machine, second tab, one keystroke away. Confirm the keystroke works from a cold start, not just from a warm one.
- [ ] Same MP4 on the backup laptop, on two USB drives, and cached offline.
- [ ] If the live demo fails twice in a row with a single retry under 15 s: **cut to the video immediately.** One line only — "Rapid-fire demo, here's the recording." No apology tour, no debugging on stage.

**Data integrity**
- [ ] Checkout is at the demo tag; `pytest` green (25 tests) on the demo machine; the live beat-2 computation re-runs `W1`–`W9` attribution via `taxonomy.classify()` over the day's token log.
- [ ] Provenance sheet present in the repo and referenced in the console footer.
- [ ] **Every** banded chart title carries `SIMULATED — within-model variance`. Zoom in on each one.
- [ ] No `SIM` / `OBSERVED` confusion anywhere; there is no prediction-vs-reality panel in the deck.
- [ ] Seed and window printed on screen somewhere a judge can photograph: `seed=20261003 · 14 days · 1 OPD block · SYNTHETIC`.

**The "net value ≤ 0" beat — verify it, do not assume it**
- [ ] Proposal 2 loads, runs, and returns exactly: **`net value −14 min/100 cases. Do not do this.`**
- [ ] The refusal renders in the same place the proposal did, at the same zoom, so no one misses it.
- [ ] Ran it live three times in rehearsal — it is deterministic, and if it failed once it will fail on stage.
- [ ] The 4-second hold is in the script at beat 4 and is not being talked through.
- [ ] B knows the fallback: if the refusal line fails to render, say "it refused" and move on. Never debug the negative result on stage.

**Print and stage**
- [ ] Judge cards printed, single-sided, one per judge plus two spares. Check: seven gate thresholds, seven unknowns each with an owner, six Class A/B sources plus one Class C comparator in Quarantine, the NAMCS tag line, the one live computation, the repo URL, and the band explanation are all present and legible at 11pt.
- [ ] Repo URL on the card confirmed as the real URL.
- [ ] Lectern script printed at 14pt with the beat times in the margin and the per-beat word counts.
- [ ] C has the cards in hand and knows they go out at beat 7, face-up, one per judge, silently.
- [ ] Timer: C's watch is on, silent mode on. Warnings at 60 s remaining and 15 s remaining, whispered to A only.
- [ ] Water, cables taped, no laptop fan noise near the mic, no notification sounds on either machine.
- [ ] Hard stop confirmed with the stage manager: the demo ends at 4:30 whether or not every beat has fired. If you are behind at beat 5, drop nothing — compress beat 6 to two sentences and protect beat 7 entirely.

---

*CADENCE — CATALYST CREW · AI & ML Track · Smart Hospital Queue Management · built against `PROJECT_SOLUTION_FINAL.md` v4.0. If a line here is not traceable to that document, it does not go on stage.*
