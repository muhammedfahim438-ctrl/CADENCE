# CADENCE — Closed-Loop OPD Flow Engine

### Solution Specification v4.0 (adversarial review pass)

**Tagline:** *Stop measuring the queue. Start closing it.*

**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE

**What v4.0 is:** v3.1 survived source verification but did not survive an adversarial read. That review found **11 fatal and 15 serious defects.** Two of them would have lost the room on their own:

- **The six-cause taxonomy never actually partitioned a patient's timeline.** There was no code for queueing behind a doctor who *is* busy — the dominant waiting state, and the one behind our own headline number — and no nursing code at all, while the comparator study we cite decomposes visits into registration / **nursing** / doctor. We were citing a three-station structure and shipping two of its three stations.
- **The north-star metric was not computable from the ledger we specified.** "Idle clinical minutes" is a property of a *provider*; our ledger is keyed to *tokens*, and not one detection rule described provider-idle-with-no-patient. The Impact criterion rested on a number our engine produced zero rows of.

Both are now fixed **at the design level, not the wording level** (§3.1, §7.2). All findings and fixes are in §1.5. Several fixes made the product better rather than merely safer.

**Standing rule:** *If a number cannot be traced to a primary source with its exact wording, it does not appear in the pitch. If a claim cannot survive an explicit validation gate, it is a hypothesis until the gate passes.*

---

## 0. Executive summary

Indian government outpatient departments do not have a "registration problem." They have a **load-versus-service-rate mismatch that the standard instruments — dashboards, patient-experience surveys and audits — are failing to capture.**

### 0.1 What patients actually experience

| # | Finding | Source | Class |
|---|---------|--------|-------|
| 1 | In an Indian tertiary hospital, **patient arrival flow exceeded the doctor service rate in every OPD studied** (general medicine, respiratory medicine, general surgery, orthopaedics; n=252 systematic random sample). In orthopaedics, **85.71% of a patient's total on-site time was spent waiting to see a doctor**. 87.30% had visited the institute directly rather than by referral; 63.89% were newly registered. | De, Gupta & Chakraborty (2024), *Dr Sulaiman Al Habib Medical Journal* 6(3):136–141 | B |
| 2 | In a Nigerian public hospital, an ambulatory patient spent **86.7 of 122.6 minutes in non-service ("waste") time; the paper reports the share as 65.3%** — versus 20.9 of 44.9 minutes (41.2%) in a private hospital. Station waits: 17.5 min at registration, 35.4 min for nursing, 51.4 min for the doctor, against 12.6 min of actual consultation. | Kemdirim et al. (2021), *Nigerian Medical Journal* 62(6):325–333. **Nigeria, not India — see §1.2.** | C |

> **Reconciliation note — we volunteer the arithmetic problem rather than wait to be asked.** A judge will divide 86.7 by 122.6 and get **70.7%**, not 65.3%. **We cannot reconcile these to a single figure from the paper's reported numbers, and we say so rather than invent a denominator.** Two candidate explanations, both consistent with the text: (a) 65.3% is a **mean of patient-level percentages**, which is not the same quantity as the ratio of two means; (b) the station figures are **separate means over different denominators**, since not every patient transits every station — which is why they sum to 104.3 min against a total idle mean of 86.7 min. **We state both readings and report the paper's own figure.** We also note the paper's own columns differ from their sum by 0.1 min (86.7 + 35.8 = 122.5, not 122.6), so its table does not close exactly at one decimal — **the discrepancy is in the source, not in our transcription.**

> **And the finding that kills "register patients faster."** The public hospital had **three** registration staff and **three** nurses; the private hospital had **two** and **two**; **both had three doctors.** The better-staffed counter was paired with the **2.7× longer** encounter — 122.6 minutes against 44.9.

> **Now apply our own standard to this, because v3 did not.** We spend §2.3 insisting that a **two-hospital** comparison cannot identify a causal effect — HMIS exposure varies between exactly two clusters. The Nigeria contrast has **exactly the same structure**: two hospitals, staffing varying between them, and every other site-level difference confounded with it. **So we hold it to the identical rule.** It is **not** the "cleanest evidence available" (v3 called it that — an inconsistency a judge would enjoy). It supports exactly one claim: **more counter and nursing capacity did not buy a shorter visit in these two hospitals.** It is an existence proof against the paperwork thesis, **not** a causal estimate of what staffing does, and we will not let it carry more weight than the Hyderabad row does.

### 0.2 What the instruments report

| # | Finding | Source | Class |
|---|---------|--------|-------|
| 3 | On India's LASI patient-experience survey (**Wave 1, fieldwork 2017-18**, published 2024), respondents rated **six** domains on a **five-point Likert scale**; *negative* = **"Bad" or "Very Bad."** Waiting time drew the **highest negative rating of the six — 4.6%** — and **9.5%** among public-facility outpatients. Only **15.0%** rated their wait "Very good," **the lowest of the six**, and **40.9%** were neutral-or-worse, **the highest of the six**. **These are not three independent cuts** — negative is *contained within* neutral-or-worse by definition — **but neither is it one number three times: the 40.9% cell also carries the 59.1% who rated the wait positive, which is the majority, and we report it.** State variation is wide: outpatient waiting negativity reaches **30.7%** in Andaman & Nicobar. | Ambade, Kim & Subramanian (2024), *Public Health in Practice* 8:100541 | B |
| 4 | At two government hospitals in Hyderabad, **40.2% of outpatients reported waits of ≥120 minutes at the hospital *with* an HMIS, versus 23.4% at the hospital *without*** (AOR 2.05, 95% CI 1.04–4.03). High patient load (AOR 1.84) and technological challenges (AOR 1.93) were also significant. **The paper does not report that the no-HMIS site had shorter waits; it reports a proportion, not a mean or median.** We therefore say the HMIS site reported *a higher proportion of long waits* and claim nothing about typical wait. | Comparative cross-sectional study (2026), *BMC Health Services Research* 26:945 | B |
| 5 | India's auditor already collects OPD flow, waiting time, cases per doctor and consultation time — **Chapter III** of the CAG performance audit of the UT of Jammu and Kashmir (Report 2 of 2025, period ended March 2022). **Marked A\*:** the report is official and the chapter is correct, but **the exact field list could not be re-verified in the v4 audit pass** (§5.7), so we do not quote it as confirmed. **No argument depends on it** | CAG of India | **A\*** |

### 0.3 The finding that makes this project worth building

**In India, a stopwatch and a national survey disagree about the same phenomenon. Both instruments are already embedded in the accountability system — and neither can run the loop.**

Objective time-flow measurement of four OPDs at an Indian tertiary hospital found that patient flow exceeded the doctor service rate in **every** one, and that in orthopaedics **85.71% of a patient's entire on-site time was spent waiting to see a doctor** (row 1).

India's national patient-experience survey asks people how they *rated* that wait. Waiting ranks **worst of all six domains** — and the rating is still single-digit: **9.5%** of public-facility outpatients call it bad or very bad, **15.0%** call it very good (the lowest of the six), and **40.9%** sit in the neutral bucket or worse (the highest of the six) (row 3).

**These are not the same quantity, and we do not claim they are.** One is stopwatch time inside four hospital departments; the other is a recalled five-point rating from a national household sample of adults aged 45 and above, fieldwork six years earlier, about a vaguer thing. Populations, instruments and years differ.

**What we do claim is narrower, and it survives.** On *every* way the survey is cut — highest negative, lowest very-positive, highest neutral-or-worse — waiting is the **worst** of six domains, **and 59.1% rated it positively.** The instrument designed to detect the problem agrees it is the worst problem, and then reports it in single digits, while the stopwatch says patients spend most of the visit not being served. **What is compressing the number is unknown — that is unknown #4, now with a named owner, a date and a resolution path (§5.5).**

**Correcting v3 overreach here.** v3's headline was *"the survey is the one the hospital answers to."* That was wrong on our own evidence: **row 5** shows India already runs a **CAG performance audit** that collects flow, waiting time, cases per doctor and consultation time. The audit is the harder accountability instrument. The accurate statement is narrower and stronger: **the survey and the audit both see the problem, and neither of them can act on it inside a shift** — one is a recalled rating from a household sample, the other a facility-level review over a reporting period. **Nobody owns measure → decide → intervene → verify at the token level. That is the gap, and it is a gap between instruments we already have, not an absence of data.**

### 0.4 What CADENCE does

1. **Waste Ledger** — two additive ledgers over an **exhaustive, test-proved** token-state taxonomy: a **patient-time** ledger (`W1`–`W9`, with `W9` the published unclassified residual) and a **roster-keyed provider** ledger (`P1` consulting / `P2` present-idle / `P3` absent-despite-roster). `P2` is what makes the north-star computable; the two cross-check each other to separate a **demand** problem from a **rostering** problem (§3.1, §7.2). **The partition property is proved by `tests/test_taxonomy.py`, not asserted here — 98,304 states enumerated, 0 unmapped, no dead codes.**
2. **Queue Digital Twin** — a live-fitted discrete-event simulation of *that specific OPD*, used to evaluate a proposed reconfiguration **before** the hospital makes it, with interventions costed in clinician-minutes.
3. **Released-Slot Reallocation (RSR)** — when a predicted no-show frees a slot at T-90min, the freed slot is **matched to a queued patient** rather than left to expire. Scoped to the **booked** subset only, because that is the only subset a slot exists for (§3.3).

Every intervention is priced in clinician-minutes and compared against its predicted gain. **CADENCE returns "do not do this" for any change whose net value is negative.**

**Every demo number is labelled SIMULATED. CADENCE reports zero real-world outcome claims until a pre-registered validation gate (§6.4) is passed.**

---

## 1. Corrections in this revision

### 1.1 Factual errors found and fixed

| # | v2 said | Truth | Effect on the argument |
|---|---|---|---|
| E1 | 86.7 min idle time presented as evidence from **Indian** public hospitals | It is **Nigeria** (Rivers State, Port Harcourt), 2021, n=299 | **Weakened.** Demoted to Class C international comparator (§0.1 row 2). The Indian evidence base is now rows 1, 3, 4, 5 only. |
| E2 | LASI 5% negative reporting framed as India's **best**-performing domain | It is India's **worst** of six domains, at **4.6%**; 9.5% among public-facility outpatients | **Strengthened.** "Worst of six, and still single-digit" is a far stronger version of the measurement-gap argument than "best." |
| E3 | CAG report attributed to the **Government of India, Chapter IV** | It is a **performance audit of the UT of Jammu and Kashmir**, Report 2 of 2025, and the OPD indicators are in **Chapter III** (Chapter IV covers drugs, medicines, equipment and consumables) | **Weakened.** Corrected throughout. The interoperability argument survives; the citation no longer overreaches. |
| E4 | NSS "79.3% of outpatient care in the private sector" attributed to MoSPI/NSS 75th | 79.3% comes from a **NITI Aayog** analysis of **21 larger states pooled across three rounds**. The all-India 75th-round components are ≈62% rural / 71% urban | **Weakened.** The 79.3% figure is now removed from the evidence base entirely and replaced with the SAR 586 components if needed. |
| E5 | LASI reference title included a subtitle "all-India and sub-national estimates from LASI" | No such subtitle exists. The phrase survives only in the paper's **Highlights** ("We provide all-India and sub national estimates on six domains…"), which is not the title | Corrected to the real title, journal, volume and DOI. |
| E6 | MoSPI report URL unencoded | 404s | Percent-encoded URL substituted. |

**E1 was the most serious.** v2 opened with "four independent lines of published evidence from Indian public hospitals" and one of them was not Indian. A judge who opened the link would have found it, and would then have doubted all four.

### 1.2 The Nigeria study: what it is and why it stays

Kemdirim CJ, Uduak A, Opurum N, Hart D, Ogaji DS. *Time-Flow Study for Receipt of Outpatient Services in Public and Private Hospitals: Implications for Lean Approach in Health Facilities in Rivers State, Nigeria.* Niger Med J 2021;62(6):325–333. doi:10.60787/NMJ-62-6-63. PMID 38736516.

**Verified definition of the quantity** (this was disputed and is load-bearing):
> "Waiting (Idle) time at each station — from the point of arrival at a particular service station to the time of initiation of the intended service at that station."
> "Total idle time — cumulative duration of time spent waiting for attention to be provided by the health providers at all service stations."

It is **patient-side waiting**, self-recorded by patients timing their own visit with wristwatches or handsets. It is *not* clinician idle time. The paper attributes long waits partly to *"health attendants being unprepared or unavailable to begin their clinical duties to early visitors who arrive before the clinic officially opens"* — in a setting with **no appointment system**.

**Why it stays in the deck:** it is one of very few studies anywhere that decomposes an outpatient encounter into station-level waits (registration / nursing / consultation) against total encounter time. That decomposition *is* the Waste Ledger's structure, measured externally. **How it must be labelled:** `Nigeria, 2021 — international comparator; mechanism generalises, magnitude does not.`

### 1.3 Structural contradictions found and fixed

| # | Problem | Fix |
|---|---|---|
| S1 | v2 claimed "the version we demo" was measurement-only, then specified a demo showing the twin (Phase 2) and RSR (Phase 3) | Demo scope corrected and stated precisely (§10). The honesty claim is kept but made accurate. |
| S2 | v2's stated fallback contained RSR in one section and "no models" in another | One fallback, defined once (§9.3). |
| S3 | Phase 0 promised to measure the Indian no-show rate from 1,500 encounters at a site assumed to be 87.30% walk-in — arithmetically yields ~195 booked slots, far too few. **v4 correction: "87.30% visited the institute directly" means *not by referral*. It is not a walk-in figure** — a directly-presenting patient may hold an appointment. **The booked share is therefore unknown #6, not something we can assume** | Phase 0 redesigned to a **multi-site appointment-register log**, which measures booked share directly rather than inferring it (§9.2) |
| S4 | v2 cited **zero prior art**; a knowledgeable judge would supply it against us | Prior-art section added with a narrowed novelty claim (§16). **v4 withdraws the RSR novelty claim entirely as self-defeating (§16.3).** |
| S5 | v2 claimed "two taps per patient"; v3.1 corrected the count in §4.2 but left the false claim standing in §11, §12 and §16 | Corrected everywhere. **The counter→clinician path is seven taps** and there are **five** instrumented roles (§4.2) |
| S6 | v2 called the 86.7 minutes "recoverable capacity" — an assumption in the grammar of a finding | Split into measured vs. addressable; addressable share declared **unknown #5** (§7.3) |
| S7 | North-star metric was gameable by when a clinician taps "started" — but the gate built to prevent it measured **reception's** tap lag, not the clinician's | Gate 5 split into **clinician-side** stage-order violations and short-idle share, with arrival-to-first-tap demoted to a data-quality signal (§6.4, §7.2) |
| S8 | DPDP Act 2023 never mentioned in a system processing patient movement data | Consent architecture and DPDP scoping added (§13.4). |
| S9 | "Digital twin" used without justification | Terminology defended or dropped (§3.2).

### 1.4 Verification pass in v3.1 — four fixes, two of them improvements

> **Historical record.** This table records what v3.1 fixed. **Four of its conclusions were themselves wrong and are reversed by v4.0** — marked **[revised in §1.5]**. It is kept, not deleted: a revision log that hides its own errors is not a revision log.

Every Class B figure below was re-checked against the **full text of the primary source**, not a search snippet or an abstract.

| # | Problem found in v3 | What the primary source actually says | Effect on the argument |
|---|---|---|---|
| **V1** | §0.3, §2.4, §11 and §16.3 called the objective and self-report numbers "**the same quantity measured two ways**" | They are **not** the same quantity. LASI is a recalled **five-point rating** among Indian adults 45+, fieldwork 2017-18. Kemdirim is **measured time-share** among Nigerian ambulatory adults, 2021. De et al. is measured time-share inside four Indian OPDs, 2024. Different constructs, countries, populations and years | **Weakened — and fixed.** Narrowed to what survives. **[revised in §1.5 A4]** — v3.1 then over-corrected into "the survey is the instrument the hospital acts on," which our own CAG row contradicts |
| **V2** | The Nigeria figures invited an arithmetic ambush: 86.7 ÷ 122.6 = **70.7%**, not 65.3%; and the station waits sum to 104.3 min against a total idle mean of 86.7 min | v3.1 concluded: "both are correct as reported" | **[revised in §1.5 B3]** — **we cannot reconcile 65.3% to 70.7% from the reported numbers.** v3.1 asserted a denominator explanation it had not verified. v4 states two candidate readings and discloses the source's own 0.1-min discrepancy |
| **V3** | LASI was cited as a single cherry-picked cell — "4.6% negative" — and its **fieldwork year was never stated** | The paper's full distribution is reported in full, and fieldwork is LASI Wave 1, **2017-18**; *negative* = **"Bad" or "Very Bad"** on a five-point scale | **De-cherry-picked.** **[revised in §1.5 B1]** — v3.1 then called these "**three independent cuts**", which is algebraically false: negative is *contained within* neutral-or-worse. v4 also reports the omitted **59.1% positive** share |
| **V4** | §0.4, §3.1, §4.2 and gate 4 disagreed about whether the ledger reconciles to zero; and the role count did not match the matrix | v3.1 claimed the rules **partition** the timeline "zero unassigned by construction", with **four instrumented** roles and a `W7` residual | **This row is wrong on both halves and is the origin of fatal finding A1.** **[revised in §1.5 A1, A2, A8]** — the v3.1 rules did **not** partition (no code for queueing behind a busy clinician, no nursing code), and there are **five** instrumented roles. The residual is now `W9`, with its definition fixed before data collection |

**Also added, because it is verified and it kills the obvious objection:** the Nigerian public hospital had **more** registration staff and nurses than the private one and still took 2.7× longer (§0.1).

**One claim we could not verify, and therefore cut rather than hedged:** the "Australia 21% / UK 30%" waiting-time comparators attributed to the LASI paper. They do not appear in the retrieved text. The paper's own interpretation reads India's *absolute* level favourably; we now use only the **rank** and the **distribution**, and say so (§5.3).

### 1.5 Adversarial review pass — v4.0

An adversarial read of v3.1 returned **11 fatal and 15 serious findings.** Full detail, including the two findings that were genuine design defects rather than wording errors, is in `ADVERSARIAL_REVIEW_V4.md`. This table records what changed and whether it made the product better or merely safer.

**Fatal findings, all fixed:**

| # | Finding | Fix | Effect |
|---|---|---|---|
| **A1** | The `W1`–`W6` taxonomy **never partitioned a token's timeline.** No code existed for queueing behind a *busy* clinician — the dominant waiting state, and the one behind our own 85.71% figure — and no nursing code existed at all, while our comparator study decomposes visits into registration / **nursing** / clinician | Rebuilt as an **exhaustive state table**: `W1` counter-idle, `W2` counter-queue, `W3` nursing-idle, `W4` nursing-queue, `W5` clinician-absent, `W6` clinician-queue, `W7` diagnostics, `W8` documentation, `W9` unclassified. **Nursing is now instrumented as a first-class station** | **Better.** We now ship the three-station structure we cite, and `W5` vs `W6` separates a rostering failure from a demand failure — a distinction the v3 ledger could not express |
| **A2** | **The north-star was not computable from the specified ledger.** "Idle clinical minutes" is provider-keyed; the ledger was token-keyed, so no rule produced the Impact metric | Added the roster-keyed companion ledger `P1`/`P2`/`P3` and an explicit derivation for `P2` (§7.2) | **Better.** The two ledgers cross-check, and the cross-check is the diagnostic |
| **A3** | "Attributes every non-service minute to exactly one of six causes" was false, and `W7 — unclassified` was redefined after the fact | Every partition claim rewritten; `W9`'s definition is now **fixed before data collection** and cannot be re-tuned to pass gate 4 | Safer |
| **A4** | "The survey is the one the hospital answers to" was **contradicted by our own row 5** (CAG audits waiting systematically) | Replaced with: **both instruments see it, neither can act on it inside a shift.** §0.3, §2.4, §10, §11, §15 all corrected | **Better.** The gap is now the absence of a *loop*, not the absence of data — which is a more defensible product thesis |
| **A5** | **Double standard.** v3 called the Nigeria two-hospital contrast "the cleanest evidence available" while spending §2.3 proving a two-site Hyderabad comparison cannot identify causation | Nigeria held to the **identical** two-hospital standard; downgraded from a causal-sounding claim to an existence proof against the paperwork thesis | Safer, and visibly consistent |
| **A6** | Gate 5 measured **arrival-to-first-tap** — a *reception* signal — while claiming to defend against a *clinician* gaming vector | Gate 5 split into **5a stage-order violations** and **5b short-idle share**, both clinician-side, plus 5c arrival-to-first-tap **demoted and relabelled** as data quality. Added an **observer spot-audit** no threshold replaces | **Better.** We now measure the actor we actually worried about |
| **A7** | "Two taps per patient" survived in §11 and §12 after v3.1 corrected it in §4.2 | Corrected everywhere. **The counter→clinician path is seven taps** (§4.2) | Safer |
| **A8** | "Four instrumented roles" contradicted a five-row matrix | **Five** instrumented roles (Reception, Nursing, Clinician, Diagnostics, Records) + one human observation, everywhere | Safer |
| **A9** | "**No clinical function**" was false against our own product: RSR matched on "clinical compatibility" and SMS'd a clinician's name | Matching is now **administrative compatibility** (specialty, slot type, follow-up status); **no clinician is named in any SMS** | Safer, and the ethics claim is now true |
| **A10** | "The no-show probability is **not persisted** as a patient attribute" — contradicted by `T-24h`/`T-90min` scoring *and* by reporting priority-queued arrivals as a tracked cohort | Corrected: the score **is** logged in the append-only decision record, and what is actually true is stated — **never displayed, never exported, never joined to a clinician's name, used once** | Safer |
| **A11** | §16.3's novelty claim was **self-defeating**: capacity-recovery for a "**walk-in-dominant OPD that has no scheduling system to fill**" — no slots means nothing to reallocate | Claim **withdrawn** and replaced with an honest dependency on unknown #6 (booked share). Novelty now rests on the **dual-ledger taxonomy**, not on RSR | Safer, and materially weaker — which is the point |

**The serious findings that changed published numbers:**

| # | Finding | Fix |
|---|---|---|
| **B1** | "**Three independent cuts**" of the LASI distribution is algebraically false — negative is *contained within* neutral-or-worse | Corrected. We now say so explicitly **and report the 59.1% who rated the wait positively**, which v3 omitted while leading with the 40.9% |
| **B2** | The 30.7% state figure (Andaman & Nicobar) was cited and never used | Now used: **waiting negativity varies enormously by state**, which is an argument for local measurement, not national averages |
| **B3** | v3 asserted it had "**verified**" the Nigeria denominators it had not | Rewritten: **we cannot reconcile 65.3% to 70.7% from the reported numbers**, we state two candidate explanations, and we note the source's own columns miss by 0.1 min. **The discrepancy is in the source** |
| **B4** | Hyderabad framed as "waits were **longer**" — the paper reports a **proportion** of ≥120-min waits, not a mean | Restated as "a higher *share* reported long waits." We do not claim the other site had shorter waits |
| **B5** | The **primary path was QR/USS — which requires a smartphone — while the persona owns a feature phone** | The **existing paper token is now the primary path**; QR/USS is optional; nothing about care changes if a patient declines (§3.4) |
| **B6** | Consent is captured **through the digital path**, so the ledger is a self-selected sample — undisclosed | Now disclosed, with a required **coverage metric**: the hospital supplies an aggregate paper-token count so we report *what fraction of visits the digital ledger covers* |
| **B7** | Gate 3's "±3 pp" had no justification; gates 1–2 had no unit, split or decision rule | Every gate now states **quantity, unit, computation split and decision rule**, with a stated **fit/holdout split (days 1–7 fit, 8–14 scored)** and bootstrap CI bounds instead of point estimates |
| **B8** | The 3-minute demo variant summed to **150s, not 180s**; the 15s failure rule pushed the total to **4:45** | Re-timed to 180s; the 15s is drawn from beat 0's allocation, so the worst case is 4:30 |
| **B9** | Unknown #4 had **no owner, no date, and its favourable branch was assumed** | All seven unknowns now have **owner + date + resolution path**. Unknowns **6** (booked share) and **7** (does the audit compress too?) are **new** — both were previously assumed |
| **B10** | Relevance criterion cell was **self-refuting**: it sold "we find your survey wrong" while conceding we don't know why it compresses | Now states the honest version — **the instrument we would replace is not broken and we don't know why it compresses waiting** |
| **B11** | Two sources (CAG, NAMCS) could not be re-opened in the v4 audit, yet were listed as "verified primary" | Downgraded to **A\*** with the failed re-check documented in a new **§5.7 source re-verification log**. Their detail is removed from asserted claims, and **nothing in the argument depends on either** |

**MINOR findings fixed:** "measurably" as an unsupported intensifier (removed); patient-side time described as "attributed to a cause" when a non-arrival has no timeline to attribute (moved to OPD-level counts); the Nigeria comparison's 4× ratio restated against its denominator; "both are correct as reported" softened to "both readings are consistent with the text"; the De et al. "all OPDs" time-window caveat stated in §5.3; NSS updated to the **80th round (35% rural public share)**; the Hyderabad reference's author list flagged as not captured.

**What the red team did *not* overturn, and we are keeping:** the 85.71% headline, the LASI distribution and its six-domain rank, the 2.7× encounter contrast (as an existence proof only), the AOR direction with its CI, the CAG/ABDM/NSS/Prophet/ABDM unit discipline, the entire architecture and scope discipline, the DPDP consent architecture, and the refusal mechanism. **The bones were sound; the arithmetic and the framing were not.** |

---

## 2. Thesis

### 2.1 The queue is a capacity condition, not a friction condition

At an Indian tertiary hospital, arrival flow exceeded doctor service rate in **every** OPD studied. In orthopaedics, 85.71% of a patient's on-site time was spent waiting to see a doctor. Only 12.6 minutes of a 122.6-minute encounter in the comparator study was actual consultation.

Registering patients faster does not create doctor-minutes. Whatever the queue is, it is not primarily a paperwork problem.

### 2.2 The waste is large and asymmetric

In the Nigerian comparator the paper reports **65.3% of the public-hospital encounter as non-service ("waste") time** against 41.2% privately (§0.1 reconciliation note applies). The largest single component was *waiting for the doctor* — **51.4 minutes against the 12.6 minutes of consultation it precedes, roughly four times as long.**

**And more counter staff did not fix it.** The public hospital had three registration staff and three nurses; the private hospital had two and two; both had three doctors. The better-staffed counter was paired with the **2.7× longer** encounter. **By the same two-hospital standard we apply to Hyderabad (§2.3), this cannot establish that staffing causes the difference** — it establishes only that in these two hospitals, more counter capacity did not accompany a shorter visit. That is an existence proof against the paperwork thesis, not an estimate of a staffing effect.

Critically, that idle is **not evenly addressable.** Waiting at registration and for nursing is partly a staffing decision; waiting for the doctor in a clinic where the doctor arrives late is a scheduling and rostering decision. Section 7.3 separates what CADENCE can act on from what it can only surface, and declares the addressable share **unknown**.

### 2.3 Software alone does not close it — and the evidence for that is weaker than it looks

At two Hyderabad government hospitals, waits ≥120 min were reported by 40.2% of outpatients at the HMIS site versus 23.4% at the non-HMIS site (AOR 2.05, 95% CI 1.04–4.03).

**Read this honestly.** It is a cross-sectional comparison of **two** sites. HMIS exposure is constant within each site and varies only between them, so the effective sample for that coefficient is two clusters — the estimate is confounded with all site-level differences, and a 95% CI of 1.04–4.03 spanning the null reflects that fragility. The same study found *high patient load* significant (AOR 1.84), which is exactly the variable most likely to differ between two specific hospitals. **We therefore do not claim an HMIS causes longer waits.**

What the study *does* license is much narrower and sufficient: **the presence of an information system is not, on its own, evidence of a shorter queue.** v2 overreached by assigning the site a capability profile ("displays a queue without owning an intervention") that no instrument in that study could observe. That profile is now labelled **our hypothesis about mechanism, untested** (§16.2).

**Our argument does not depend on row 4.** §2.1, §2.2 and §2.4 stand without it.

### 2.4 Both instruments see it; neither can act on it

Waiting is the **worst** of six patient-experience domains in India on every cut of the distribution — and the instrument still returns single digits: **4.6%** negative nationally among adults 45+, **9.5%** among public-facility outpatients, **only 15.0%** rating the wait "very good," and **40.9%** neutral-or-worse.

Objective measurement of waiting returns **85.71% of on-site time** in one Indian OPD — and **65.3% of the encounter** as non-service time in the international comparator.

We do not claim these are the same quantity; §1.4 V1 sets out exactly how they differ. We claim the survey is measuring a **different construct** from the one that causes harm, and that its neutral bucket absorbs a structural time problem. **Which mechanism compresses it — normalisation, item wording, reference-point effects or social desirability — is unknown #4, now owned and dated (§5.5).** The disagreement is measured regardless of which mechanism is responsible.

**The second instrument matters more, and v3 underplayed it.** India already runs a **CAG performance audit** collecting flow of patients in OPD, waiting time for outpatients, OPD cases per doctor per annum and consultation time per patient (row 5). So this is **not** a country flying blind. It is a country with two instruments that can both *see* waiting and neither of which can **act on it inside a shift** — the survey is a recalled household rating, the audit is a facility-level review over a reporting period. **The missing thing is not measurement. It is the loop.**

> **Nobody owns measure → decide → intervene → verify.** That is the product.

---

## 3. The solution

### 3.1 Engine 1 — The Waste Ledger

**The v3 design failed here, and it failed fatally.** v3 said "each token's non-service time is attributed to exactly one of six causes." It was not true. Its rules had **no code for queueing behind a doctor who is busy** — the single most common waiting state in any outpatient department, and the one that sits behind our own headline 85.71% figure. They also had **no nursing code at all**, while the comparator study we cite (§0.1 row 2) decomposes an encounter into registration / **nursing** / doctor. We were citing a three-station structure and shipping two of its three stations. A judge who asked "what about the patient waiting behind a working doctor?" would have got no answer, and the whole additive claim would have collapsed.

**The v4 taxonomy is built so that it cannot fail that way.** The governing rule is: *every state a token can be in is mapped to exactly one cause, and the mapping is exhaustive by construction.* Here is the complete state space.

| Code | Cause | Exhaustive detection rule | Owner of the fix |
|---|---|---|---|
| `W1` | Counter idle | In counter queue **and** ≥1 counter is open and idle **and** this token is next | Reception |
| `W2` | Counter queue | In counter queue **and** all counters busy | Counter staffing — *surfaced, not controlled* |
| `W3` | Nursing idle | In nursing queue **and** the nurse for this stage is present and idle | Nursing supervision |
| `W4` | Nursing queue | In nursing queue **and** all nurses for this stage busy | Nursing staffing |
| `W5` | Clinician absent | In consultation queue **and** (assigned room vacant **or** assigned clinician not checked in) | Clinic / administration |
| `W6` | Clinician queue | In consultation queue **and** assigned clinician present **and** currently with another patient | Demand vs clinician capacity |
| `W7` | Diagnostics detour | Sent to imaging/lab **and** not returned within SLA | Diagnostics |
| `W8` | Documentation | Clinically finished **and** not cleared | Records |
| `W9` | **Unclassified** | **Observed** and in a state no rule above covers — most often a patient at a station we have not modelled | Data quality / scope |

**Why `W6` is the code that was missing, and it is not a minor addition.** `W5` and `W6` are different problems with different owners and different fixes. `W5` — clinician not checked in — is a rostering and punctuality failure, and it is addressable by scheduling. `W6` — clinician present and working — is a **load-versus-service-rate condition**, and no amount of reordering fixes it. A ledger that collapses both into "waiting for the doctor" cannot tell a hospital whether its problem is staffing or demand. That distinction is the entire reason the Waste Ledger exists.

**`W9` means "we watched, and cannot attribute." It is not where lost data goes.** These are two different claims and conflating them would overstate how much we understand:

| | Meaning | Ledger row? | Reported as |
|---|---|---|---|
| **`W9`** | We observed this patient and no rule covers the state | **Yes** | Residual, gated at < 2% of observed on-site minutes |
| **Data gap** | We have no evidence — missing tap, or a self-contradictory log | **No row at all** | Coverage metric, alongside consent coverage |

Filing a missing transition under *waste* would **manufacture minutes for patients we never observed**, and would make the ledger's own total unfalsifiable — the same over-claim as fatal finding A3, rebuilt one level down. A data gap therefore produces **no row**, and is reported as a coverage percentage instead (§18.2).

**Four properties, and the first one is now executable rather than asserted:**

- **Additive, and the partition is proved by a test rather than by a sentence.** For every observed token: `arrival → exit` decomposes into **service time** plus exactly one of `W1`–`W9`. **This is not a claim in a document — it is `tests/test_taxonomy.py`, which enumerates the full 98,304-state observable space and fails if any in-scope state is unmapped or any declared code is unreachable.** The current run: **0 uncovered states, all nine codes reachable, `sum(W1…W9) + data gaps == in-scope states`.**
- **`W9` is non-zero by construction and published on the same chart as the causes**, gated at **< 2% of observed on-site minutes** (§6.4). We no longer claim zero remainder anywhere; **there is no phrase "zero remainder" left in this document.**
- **Provider-time is a second, separate ledger — because the north-star is provider-keyed.** v3's fatal flaw #2: the north-star is *idle clinical minutes*, a property of a clinician, while the ledger was keyed to tokens, so **no v3 rule could ever produce the Impact metric.** v4 adds a roster-keyed companion series: `P1` clinician-minutes consulting, `P2` clinician-minutes **present and idle**, `P3` clinician-minutes rostered but not checked in. **`P2` is the north-star numerator, computed from check-in/check-out pairs minus consultation minutes (§7.2).** The two ledgers then cross-check each other: high `W6` alongside high `P2` is the signature of a **demand** problem; high `W6` alongside high `P3` is the signature of a **rostering** problem. The same patient-side number, two different root causes, distinguished by data rather than by argument.
- **Comparable to existing audit fields — with an explicit mapping table.** `W2` maps to *flow of patients in OPD*; the service-time distribution maps to *consultation time per patient in OPD*. **These are not the same measurement protocol** — the CAG collects by exit survey and record review at facility level over a reporting period; we instrument at token level per shift. We ship a **documented mapping table** stating exactly which numbers are and are not comparable. That table is a deliverable, not a footnote.
- **Rule-derived, not inferred.** Causes are detected from the state machine, so the ledger is a measurement. Models act on top of it; they cannot corrupt it.

**What the enumeration exposed, stated plainly because it is a real limitation.** The state-coverage test proves the taxonomy is *complete over the states we model*. It does **not** prove we model every place a patient can stand. Enumerating the space shows `W9` is the landing zone for a large share of observed states, dominated by **patients at locations with no modelling dimension at all** — pharmacy, billing/payment, waiting for an escort or wheelchair, and corridor transit between stations. None of these appear in the Nigerian comparator's station decomposition either, so we are not contradicting it — but we are **not measuring them.**

This does **not** mean gate 4 will fail, and the distinction matters: **`W9`'s gate is on minutes, and share-of-states is not share-of-minutes.** A station where patients stand for four minutes contributes four minutes. The honest position is that we do not yet know whether unmodelled stations carry a material share of patient-minutes, and **that is precisely what the < 2% gate is for.**

**So the expected response to a gate-4 failure is to add a station, not to widen `W9`'s definition.** Widening `W9` after seeing the data is exactly the move that made this finding invisible in v3.1. We commit in advance: if gate 4 fails, the taxonomy is extended with a named code (`W10` pharmacy, `W11` billing, …) and the state table, the coverage test and this section are revised together. The residual stays defined before data collection, or the gate means nothing.

**Patient-side time (`W6` in v3, now reclassified) is not part of this arithmetic at all.** Did-not-arrive and left-early produce **no token timeline** — there is no arrival, so there are no minutes to attribute. v3 listed it as a sixth cause and then had to exclude it from the reconciliation, which is what created the appearance of a broken sum. In v4 it is reported where it belongs: as **OPD-level counts and rates**, human-observed, never as minutes, never as a token cause (§13.2).

### 3.2 Engine 2 — The Queue Digital Twin

**Not** "AI that predicts wait time" — a commodity claim, trivially mocked, unverifiable at hackathon scale.

The Twin is a **live-fitted discrete-event simulation** of one OPD block: counters → consultation rooms → diagnostics → exit, with rosters, service-time distributions estimated from the Waste Ledger, and arrival intensity per 15-minute bin.

It answers counterfactuals, not predictions:

> *"Move one room from Orthopaedics to General Medicine for 11:00–13:00, and run the other as a nurse-led follow-up fast-track. What happens to median wait, P90 wait, and abandonment in each OPD?"*

**On the term "digital twin":** the healthcare literature generally reserves "twin" for a live data-connected simulation of a physical asset. What we have is a stochastic DES whose parameters are refit from live data. **We use the term because it is the common name for the category, and we define it precisely here so no judge can accuse us of inflating it.** If challenged on terminology, DES is the accurate word and we will use it.

**Role separation, stated once:** the **doctor is scarce and non-delegable** — available doctor-minutes *are* the service rate, and no intervention may invent them. The **nurse is elastic** — nurse capacity is the only thing CADENCE *creates*. Rooms and counters are *reassigned within existing rosters*; that is not the same as inventing capacity.

| Intervention | Constraint enforced | Mechanism |
|---|---|---|
| Reassign a room between OPDs | Clinician must be credentialed for the receiving OPD | Addresses `W5` (clinician absent) and relieves `W6` |
| Nurse-led fast-track for follow-ups | **Requires state scope-of-practice approval and a clinical protocol. Phase 3 only.** | Converts clinician load to nursing load — attacks `W4`/`W6` at the source |
| Open/close a counter by hour | Staffing is a hospital variable we surface, not control | Addresses `W2` |
| RSR (Engine 3) | Within the existing clinician roster; booked slots only | Recovers already-freed capacity |

**Governance honesty:** the highest-leverage intervention (nurse-led fast-track) is a scope-of-practice question governed by the state nursing and medical councils, not a design choice. It enters the candidate set only when a protocol exists. **In Phase 2 the twin ranks room reassignment and counter-hour scheduling first, because those need only the medical superintendent's sign-off.** A twin that cannot run its own top recommendation says so — that is a refusal, and we ship refusals.

Ranking function:

```
net_value(π) = predicted_recovered_clinical_minutes(π) − clinician_minutes_cost(π)
```

Interventions with `net_value ≤ 0` are returned with **"do not do this."**

### 3.3 Engine 3 — Released-Slot Reallocation (RSR)

> A no-show prediction tells you a slot will be empty. The capacity is freed either way. The only question is whether anyone takes it.

1. No-show model produces `P(no-show | features)` per booked slot at `T-24h` and again at `T-90min`.
2. Slots crossing the release threshold at T-90min are marked **released capacity**.
3. **Bipartite matching** between released capacity and queued demand, on **administrative compatibility** first and expected marginal wait reduction second. *"Administrative compatibility"* means facts already on the booking — **specialty, slot type, and whether the visit is a follow-up to one this clinician already saw.** It is a scheduling attribute, not a clinical judgement, and CADENCE makes no clinical determination at any point (§13.1).
4. Matched patients get an SMS: *"a slot has opened today at 14:20 in the Orthopaedics clinic. Confirm?"* One tap. **No clinician's name is sent** — naming an individual in an SMS about a specific slot discloses more than the queue function requires, and the specialty is what the patient needs. Confirmed patients re-enter as priority-queued arrivals.

**Honest framing.** RSR's realised ceiling is not the no-show rate. It is:

```
no_show_rate × booked_slot_share × match_rate × T-90min_reach × compatibility_rate
```

We do not state this product, because **we have not measured the first factor in an Indian setting** (§9.2). RSR is presented as a mechanism plus a measurement protocol — not as a claimed percentage.

**RSR's scope is the booked subset only, and v3 contradicted itself here.** §16.3 claimed novelty in the *booked* segment while our own headline evidence describes a **walk-in-dominant** OPD — in which **there is no slot to reallocate.** Both cannot be the primary story. The resolution is honest and weaker than v3 wanted: **RSR applies to whatever share of the day is booked**, we do not yet know that share, and **if it is small, RSR is a minor feature, not an engine.** Phase 0(b) measures it. We would rather state that dependency than sell a mechanism the setting may not support.

**Walk-in fairness is a hard constraint in the objective, not a KPI shown beside it.** The matching maximises recovered capacity **subject to** non-regression of already-queued patients' P90 wait. When no match satisfies the constraint, RSR returns "do not do this."

### 3.4 What the patient gets

**v3 listed "QR / USS scan" as the primary path while its own persona owns a feature phone. A QR code requires a smartphone camera, so the primary path excluded the exact user we designed for.** v4 has three paths, and the primary one is the one that already works in every Indian OPD today:

| Path | Requires | Who |
|---|---|---|
| **1 — Existing paper token** *(primary)* | **Nothing.** Today's slip, today's number | **Everyone, including feature-phone users.** Preserved deliberately |
| **2 — QR / USS scan → token → SMS** | A smartphone camera | Optional convenience; **never the only way in** |
| **3 — SMS on a feature phone** | Any handset with SMS | Position, estimate, and RSR confirmation |

- **No app required, on any path.** SMS is plain text and works on the cheapest handset in the room.
- **One physical display** showing the current token — patients already understand this, and displays already exist in many OPDs.
- **If a patient declines the digital path, nothing about their care changes.** They take a paper slip and appear in the same queue. Consent is not a condition of service (§13.4).
- **No clinical content, ever.** No diagnosis, severity, triage or condition inference. Queue position and time only. "Administrative compatibility" in RSR (§3.3) is a scheduling attribute, not a clinical judgement.
- **No patient-side accountability surface.** No individual score, no leaderboard, no per-patient flag exposed to staff.

---

## 4. Architecture

**One topology, committed.** A jury reads two alternatives as indecision.

```
┌──────────────── ONE HOSPITAL, ONE OPD BLOCK ─────────────────┐
│  PATIENT: paper token (primary) · QR/USS optional · SMS       │
│  STAFF:   Android app, 5 roles (§4.2)                        │
│      │                                                        │
│      ▼                                                        │
│  EDGE: SQLite on a mini-PC, LAN-only, offline-tolerant       │
│      ▼                                                        │
│  CADENCE CORE                                                │
│   • Token state machine → WASTE LEDGER (W1..W8 + W9 resid.)  │
│   • Roster ledger      → PROVIDER SERIES (P1/P2/P3)          │
│   • Arrival-rate model   (HistGradientBoosting, 15-min bins) │
│   • No-show model        (calibrated; threshold = policy)    │
│   • QUEUE DIGITAL TWIN  (stochastic DES, live-fitted)        │
│   • Reconfiguration search + net_value ranking               │
│   • RSR: released-slot bipartite matching                    │
│      ▼                                                        │
│  CONSUMERS: SMS adapter · OPD display · staff console        │
│             (ledger + counterfactuals + refusals)            │
│      ▼                                                        │
│  Hospital MIS — READ-ONLY, aggregate only, consented         │
└──────────────────────────────────────────────────────────────┘
```

### 4.1 Constraints, and what the hospital actually buys

We do **not** claim "procurement surface at zero." That was an overstatement. The honest BOM:

| Item | Cost | Note |
|---|---|---|
| Tablet per staff role | ₹9–15k × roles | Android, existing MDM |
| Mini-PC (edge server) | ~₹8k | Runs the entire pipeline on-LAN |
| SMS credits + **TRAI DLT sender-ID registration** | credits + **2–6 weeks lead time** | Entity-level approval; a named pilot dependency |
| Display, if absent | ~₹6k | Many OPDs already have one |
| Staff training | ~2 hours per shift | The real cost. See §12 |

- **Offline-first.** The core runs on-LAN; internet is needed only for SMS and optional MIS export. Hospitals have outages; a queue system that stops at an outage is a liability.
- **No custom hardware in MVP.** No IoT counters, turnstiles or sensors. State transitions are recorded by staff taps.
- **No EHR write-back.** Read-only consumption, and only with consent.
- **No ABDM/ABHA write path in MVP.** The ABHA linkage is post-pilot, contingent on the ABDM interoperability pathway. Where ABDM is referenced, the unit is **registrations** — the 25-crore Scan & Register figure is OPD *registrations*, not visits or consultations.
- **The LLM is optional and off the critical path.** It may summarise the Waste Ledger for shift handover. If unavailable, nothing breaks. It never touches the token pipeline, the ledger, or any clinical content.

### 4.2 Honest role × transition matrix (replaces "two taps per patient")

**v3's "two taps per patient" was false, and v3.1 corrected it in one place while leaving the false claim standing in §11, §12 and §16.** Here is the only place it is stated, and here is the corrected count.

| Role | Transitions tapped | For | Taps per patient on the counter→exit path |
|---|---|---|---|
| Reception | Issue token; forward to nursing | `W1`, `W2` | 2 |
| Nursing | Start nursing stage; forward to clinician | `W3`, `W4` | 2 |
| Clinician | Call next; start consult; finish consult | `W5`, `W6`, `P1` | 3 |
| Diagnostics | Send; return | `W7` | 2 *(only for patients sent to diagnostics)* |
| Records | Clear | `W8` | 1 |
| Any (human-observed) | Mark did-not-arrive / left-early | patient-side counts (§13.2) | 0 |

**The counter→clinic path is `2 + 2 + 3 = 7 taps`, not two.** A full counter→exit visit with diagnostics is 10. Two further taps — clinician **check-in** and **check-out** — are per **session**, not per patient, and they are what make the north-star computable (§7.2). **Seven taps is the honest number and it is a real cost**, which is why §12 carries "staff don't tap" as a High risk with a named mitigation rather than a reassurance.

**Four instrumented roles** — Reception, Nursing, Clinician, Diagnostics — **plus Records**, plus one human observation any role can make. **v3 said "four roles" and meant four; the matrix had five rows and the fifth was not a role, which is how the count went wrong.** There are **five instrumented roles** (Reception, Nursing, Clinician, Diagnostics, Records) and **one human observation**. Every place that says "four roles" has been corrected.

**`W7` and `W8` require two roles beyond the counter→clinician path.** Negotiating Diagnostics and Records participation is **Phase 0's first task, not a build task.** If it fails, `W7`/`W8` are reported as **unavailable** rather than estimated, and the state-coverage test in §18.2 records which states are therefore unmapped.

**Patient-side non-arrival holds no minutes and is excluded from the reconciliation.** A patient who never arrived has no token timeline, so there is no time to attribute. It is reported as **counts and rates at OPD level** (§13.2), and the reconciliation in §6.4 runs over `W1`–`W8` + `W9` + service time only.

**`W9 — unclassified` is defined precisely and cannot be redefined later:** the share of on-site minutes spent in a state that no attribution rule covers — a missing, duplicated or out-of-order transition. It is displayed with its **real, non-zero** value, and gate 4 caps it at **< 2%** (§6.4). Showing your residual is worth more than claiming it is zero.

---

## 5. Data and provenance discipline

### 5.1 Claim evidence classes

| Class | Meaning | How it may be pitched |
|---|---|---|
| **A** | Verified primary source | Assert plainly |
| **B** | Published study, setting stated inline | Assert with setting stated, every time |
| **C** | Structural / international analogy | Assert only as analogy, never as a local rate |
| **D** | Simulated by us | Always labelled `SIMULATED` on the same visual |
| **E** | Not measured | **Stated as unknown.** A feature, not a gap. |

*Class describes the **source** and, separately, the **use**. A primary source (Class A) may be quarantined to Class C for a specific inference — NAMCS is Class A as a document and Class C as evidence about Indian no-shows.*

### 5.2 Class A — verified primary

**Provenance honesty first.** An audit re-check in this pass **could not open the CAG report** (§5.7) and could not open the NAMCS data-documentation pages. v3.1 listed both as "verified primary" on the strength of a search result. **Being unable to re-open a source is not the same as being wrong about it, and it is certainly not the same as being verified.** They are marked **A\*** below: the documents are official and their titles are correct, but the specific field lists were not re-confirmed against the retrieved text in this pass. **If a claim cannot be re-opened, it does not get asserted plainly.**

| # | Source | Status | What we assert, and what we do not |
|---|---|---|---|
| A1 | **CAG of India**, *Report 2 of 2025: performance audit of the Government of UT of Jammu and Kashmir — Public Health Infrastructure and Management of Health Services* (period ended March 2022), **Chapter III** | **A\*** — official document, title confirmed, **field list not re-verified in this pass** | We assert that a national audit framework exists that collects OPD flow, waiting time, cases per doctor and consultation time. **We do not assert the exact chapter field list as verified.** The strongest form of our §2.4 argument survives without it |
| A2 | **NSS 75th Round, Social Consumption: Health** (Jul 2017 – Jun 2018), MoSPI Summary Analysis Report 586 | **A**, and **superseded** | 75th round: government/public share of treated ailment spells **33% rural / 26% urban**; average medical expenditure per hospitalisation case (excl. childbirth) **₹16,676 rural / ₹26,475 urban**. **The 80th round (2025) reports the rural public share at 35%** — we cite the later figure as current and the 75th as the round behind the expenditure numbers |
| A3 | **ABDM / PIB**: **25 crore OPD registrations** via Scan & Register | **A** | Assert plainly. **Registrations — never visits or consultations** |
| A4 | **CDC NAMCS 2023 Health Center Component** | **A\*** — dataset documentation not re-opened this pass (HTTP 403) | We assert only what is low-risk: NAMCS exists, is US, and is **not** transferable to Indian OPDs. **The response-rate, visit-count and weight-correction specifics are not re-verified and are not load-bearing for any argument** — NAMCS appears in exactly two permitted uses (§5.4), neither of which depends on those numbers |
| A5 | **`facebook/prophet`** | **A** | **Maintenance mode as of v1.4.0** — bug fixes, dependency bumps, R↔Python parity only; no new features planned |

**Why a downgrade can strengthen a pitch.** v3.1 led §2.4 with the CAG field list as its proof that India already audits waiting. That claim was doing real work and was the least verifiable claim in the document. The argument does not need it: **the LASI survey (B) already establishes that India measures patient experience systematically.** So the load-bearing claim is now a Class B source we have read in full, and the CAG is a supporting mention.

### 5.3 Class B — published studies

1. **De A, Gupta S, Chakraborty A (2024).** *Navigating Patient Flow: Assessing the Bottlenecks in Out-Patient Services in a Tertiary Care Hospital in India.* Dr Sulaiman Al Habib Medical Journal 6(3):136–141. doi:10.4103/dshmj.dshmj_63_24. n=252, four OPDs. Patient flow exceeded doctor service rate in all OPDs; orthopaedic OPD spent 85.71% of on-site time waiting to see a doctor; surgical OPD lowest waiting share (25.62%) and highest consultation share (65.88%); **87.30% visited the institute directly rather than by referral** (this is *not* a walk-in rate — see §9.2); 63.89% newly registered. **Time-window caveat:** "all OPDs" describes the observation window, not a constant all-day condition.
2. **Ambade M, Kim R, Subramanian SV (2024).** *Experience of health care utilization for inpatient and outpatient services among older adults in India.* Public Health in Practice 8:100541. doi:10.1016/j.puhip.2024.100541. **Data: LASI Wave 1, fieldwork 2017-18; published 2024.** Six domains — waiting time, respectful treatment, clarity of explanation, privacy during consultation, treated by provider of choice, cleanliness of facility — rated on a **five-point Likert scale**; **negative = "Bad" or "Very Bad."** Sample: 72,270 LASI observations → 4,781 hospitalised / 37,494 outpatient → **analytic sample after excluding under-45s and missing records: 4,330 inpatient / 33,724 outpatient.** Outpatients: waiting negative **4.6%** (bad 4.0 + very bad 0.6), the **highest of the six**; the lowest is respectful treatment at 2.2%. **Public facilities: waiting 9.5%** (8.2 + 1.3), the highest negative in public facilities; **private facilities: 3.5%**, the highest there too. **The distribution is the stronger cut:** among public-facility outpatients, waiting draws the **lowest "very good" share of the six (15.0%)** and the **highest neutral-or-worse share (40.9%)**. Across states, outpatient waiting negativity reaches **30.7% (Andaman & Nicobar)**; in most states under 5% report negative on all six domains. *The paper's own interpretation reads India's absolute level favourably; we use only the rank and the distribution, and we disclose the fieldwork year.*
3. **Comparative waiting-time study, two government facilities, Hyderabad (2026).** BMC Health Services Research 26:945. doi:10.1186/s12913-026-14997-y. PMID 42365278. n=214, 107 per hospital. Long wait defined as ≥120 min: **40.2% HMIS site vs 23.4% non-HMIS site.** AOR 2.05 (1.04–4.03) HMIS presence; 1.84 (1.03–3.46) high patient load; 1.93 (1.04–3.61) technological challenges. **Two-site cross-sectional design; HMIS exposure is between-site and confounded — reported as association only (§2.3).**

### 5.4 Class C — the quarantine

- **Kemdirim et al. (2021), Nigeria** — station-level decomposition of outpatient waiting time. Always tagged `Nigeria, 2021 — international comparator; mechanism generalises, magnitude does not.`
- **NAMCS 2023** — permitted uses are exactly two: (a) a schema and ICD-10-CM codebook reference; (b) a US-context sanity check on no-show magnitude. Prohibited: any statement of the form "Indian OPD no-shows are approximately X%." Any figure carries the tag `US health centers, 2023 (NAMCS HC) — not generalisable to Indian OPD.` Note also that 2023 is not a trend series.
- **Brazilian no-show dataset** — demoted to a **unit-test fixture** proving the training pipeline runs on a file with a `No-show` column. It is Brazilian, single-facility, appointment-based (not walk-in), and derivative. **No figure from it appears in any slide.**

### 5.5 Class E — declared UNKNOWN

| # | Unknown | Why it matters | Owner | By when | Resolution path |
|---|---|---|---|---|---|
| 1 | Indian government OPD **no-show base rate** | Sets the ceiling on Engine 3 | Pilot lead | Phase 0, week 2 | §9.2(b) multi-site appointment-register log |
| 2 | **Abandonment** ("left without being seen") rate | Primary harm metric, and the north-star guardrail | Pilot lead | Phase 0, week 2 | §9.2(a) token-level logging |
| 3 | **Real-world accuracy** of the twin | Every benefit number depends on it | Twin owner | Phase 2 | §6.4 gate, pre-registered |
| 4 | **Why** the survey compresses waiting — normalisation vs. item wording vs. reference point vs. social desirability | Determines whether our contribution is a **measurement** discovery or a **survey-design** critique. **These have different audiences and different remedies, so guessing wrong is not harmless** | Research lead | Phase 1, written up with the first ledger | **Instrument-critique work: re-field a single waiting item with an explicit anchored scale alongside the existing one, n ≥ 300, same OPD.** Cheap, and it produces a publishable result either way |
| 5 | **Addressable share** of total idle time | §2.2 vs §3.2's scope limits | Twin owner | Phase 2 | §9.2 ledger + twin fit |
| 6 | **Booked share** of a typical OPD day | If small, **RSR is a minor feature, not an engine** (§3.3) | Pilot lead | Phase 0(b) | §9.2(b), same register log — one query, and it decides whether Engine 3 is worth building |
| 7 | Which **mechanism** compresses the survey number: does it also compress the **audit** number? | Determines whether the loop is missing, or the accountability layer too | Research lead | Phase 1 | Follows from unknown #4 |

**Unknowns 4 and 6 are new in v4, and both were previously assumed rather than unknown.** v3 asserted RSR as an engine while the booked share was unmeasured; v3 named a mechanism it had not tested. **Both are now unknowns with owners and dates, which is the only honest place for them to live.**

### 5.6 Reference implementation vs. pilot

The demo runs on a **synthetic 14-day, single-OPD-block dataset** from a seeded generator (`seed=20261003`) with a printed provenance sheet and a public regeneration command. It is not presented as real hospital data.

**Circularity, stated openly:** the twin is fitted to data our own generator produced, so **no demo output is evidence of real-world accuracy.** The §6.4 gate is the only such evidence, and it requires partner-site logs. The demo says this on screen.

### 5.7 Source re-verification log

A second audit pass attempted to re-open every cited source. **Two could not be opened, and are downgraded accordingly rather than left as "verified."**

| Source | Attempt | Result | Consequence |
|---|---|---|---|
| Nigerian time-flow paper (PMC11087679) | Full text | **Opened.** All six figures confirmed verbatim, including the "percentage waste time" definition | Stays Class C; the 0.1-min arithmetic discrepancy is in the source and is disclosed (§0.1) |
| LASI (PMC11413678) | Full text | **Opened.** Distribution, scale definition, fieldwork years and analytic sample confirmed | Stays Class B, and the "independent cuts" claim is corrected — negative is *contained in* neutral-or-worse (§0.2 row 3) |
| De et al. (LWW) | Full text | **Opened** after a redirect. All six claims confirmed | Stays Class B. "All OPDs" is time-windowed, not all-day |
| **CAG Report 2 of 2025** | `cag.gov.in` | **Could not open** (site unreachable from this environment) | **Downgraded A → A\*.** Field list no longer asserted as verified (§5.2 A1) |
| **NAMCS 2023 documentation** | `cdc.gov/nchs` | **Could not open** (HTTP 403) | **Downgraded A → A\*.** Response rate, visit counts and the `VISWT` correction removed from asserted figures (§5.2 A4) |
| NSS 75th / 80th | MoSPI, PIB | 75th confirmed; **80th round found and now cited as current** | Rural public share updated to **35% (80th round, 2025)** |
| ABDM 25 crore | PIB | Confirmed | Registrations — unit enforced everywhere |
| `prophet` | GitHub README | Confirmed | Maintenance mode, correctly stated |

**The lesson we are keeping:** a source that cannot be opened on the day you cite it is a source you cannot claim to have verified. Two of eight could not be. That is a 25% failure rate on a document whose entire credibility rests on citation discipline — and it is now visible in the deck rather than latent in a footnote.

---

## 6. Modelling and the honesty protocol

### 6.1 Models are small, deliberately

| Model | Task | Method | Why |
|---|---|---|---|
| Arrival intensity | Patients per 15-min bin | `HistGradientBoostingRegressor` | Robust, CPU-only, no maintenance-mode dependency |
| Service time | Per-OPD consultation duration | Empirical quantiles + GBM quantile heads | Publishes P50/P90 — P90 is what the patient feels |
| No-show | `P(no-show)` per booked slot | Gradient-boosted + isotonic calibration | **Calibration over AUC** — the threshold is a capacity policy knob, so probabilities must be trustworthy |
| Twin | Counterfactual flow | Stochastic DES, live-fitted | Mechanism, not a black box — an administrator can read its assumptions |

Prophet is removed from the core stack (maintenance mode) and appears only as an experimental challenger in the model registry.

### 6.2 What the variance bands mean

Verbatim, for the pitch:

> "This band is **within-model variance under simulation**. We re-draw the stochastic inputs our fitted model uses — arrival jitter, service-time draws — 10,000 times and report the spread. It answers: *given our model of this OPD, how sensitive is the outcome to the randomness inside that model?* It does **not** answer: *how accurate is our model of the real OPD?* The second question is what the validation gate tests, and we will not claim an answer before it runs."

### 6.3 No "prediction vs reality" panels

Because we have no reality to place beside them, v2's comparison charts are deleted. Every chart carrying a band is titled `SIMULATED — within-model variance`.

### 6.4 The validation gate — pre-registered, and it can fail

Registered before data collection, published with a commit hash and timestamp. **v3 wrote thresholds that no third party could evaluate.** v4 states, for each one: the quantity, its units, the computation split, and the decision rule.

**Phase:** token-level logs at one partner site, `n ≥ 1,500` encounters (extended, not relaxed, if the site runs below).

**Computation split, stated so the metric cannot be gamed by the split:** the twin is fitted on **days 1–7** and every gate below is scored on the **held-out days 8–14**. No threshold is ever computed on the data used to fit.

**The twin must clear all seven gates — gates 1–4 plus the three integrity gates 5a–5c:**

| # | Metric | Definition and units | Split | Threshold | Decision rule |
|---|---|---|---|---|---|
| 1 | **Median wait error** | `100 × \|median(sim) − median(obs)\| / median(obs)`, pooled over all held-out encounters, **percentage** | held-out days 8–14 | **< 20%**, bootstrap 95% CI upper bound | Fail if the **CI upper bound** ≥ 20% |
| 2 | **P90 wait error** | same construction on the 90th percentile, **percentage** | held-out days 8–14 | **< 30%**, bootstrap 95% CI upper bound | Fail if the **CI upper bound** ≥ 30% |
| 3 | **Abandonment rate** | `100 × (left-before-seen ÷ tokens issued)` in the held-out period, in **percentage points** against observed | held-out days 8–14 | **within ±3 pp** | Fail outside ±3 pp |
| 4 | **Ledger reconciliation** | `W9 — unclassified` as a **percentage of _observed_ on-site minutes** (minutes in data gaps are excluded from the denominator, not counted as waste), all days, published on the chart. **Reported alongside: log coverage % and consent coverage %** — a low residual achieved by dropping cases is not a pass | all 14 days | **< 2%** | Fail at ≥ 2%. **`W9` is defined in §3.1 and cannot be redefined after seeing the data — a failure means we add a station (`W10`, `W11`, …), not that we widen `W9`** |
| 5a | **Stage-order violations** | `100 × (out-of-order transitions ÷ all transitions)`, **percentage** | all 14 days | **< 1%** | Fail at ≥ 1% |
| 5b | **Short-idle share** | `100 × (P2 idle episodes < 60 s ÷ all P2 idle episodes)`, **percentage** | all 14 days | **< 10%** | Fail at ≥ 10% |
| 5c | **Arrival-to-first-tap lag** | minutes from token issuance to first transition, **P95 in minutes** — a *reception* data-quality signal | all 14 days | **P95 < 10 min** | Fail at ≥ 10 min |

**Why the P90 gate is a CI bound and not a point estimate.** A P90 estimated from a single site's held-out week is a noisy statistic; a point estimate of 29% against a threshold of 30% is not evidence of passing. **We gate on the bootstrap upper bound**, which is the stricter and more honest test, and we accept that it may fail a model that a point estimate would have passed. Stating the decision rule in advance is what stops us from choosing the statistic after seeing the answer.

**Gate 4 cannot be gamed by relabelling.** `W9` is fixed by §3.1's state table before data collection. If a team wanted to make `W9` small, the only honest route is to capture more transitions correctly — which is the behaviour the gate is meant to produce.

**The no-show model gets its own gate**, or RSR is ungated and therefore worthless: **expected calibration error < 0.05** on site-held-out booked slots, plus a **non-regression constraint** on already-queued patients' P90 (§3.3).

**Failure handling, stated in advance:** if any threshold fails, CADENCE reports the failure, reports by which cause the twin diverges, and ships **measurement-only** (§9.3). **Partial passes do not license partial claims** — gate 1 failing voids the median-wait claim even if 2, 3 and 4 pass.

**Gate 2 — feasibility, not efficacy.** One intervention runs 10 days with a stepped-wedge across matched sessions. **This is explicitly not powered to detect a wait-time effect** — ten days at one site cannot separate that signal from noise, and we will not pretend otherwise. It tests only: does the intervention execute without harm, at acceptable clinician cost? Efficacy is claimed only after a multi-site stepped-wedge with pre-registered power analysis. The result is reported either way, including if negative.

---

## 7. Metrics

### 7.1 Aligned to the auditor's vocabulary — with an honest caveat

| Our metric | Auditing counterpart | Comparable? |
|---|---|---|
| Median / P90 total wait | *Waiting time for outpatients* | Directionally; different protocol |
| P50 / P90 service time | *Consultation time per patient in OPD* | Directionally |
| Idle clinical minutes / 100 cases | *OPD cases per doctor per annum* | **No.** Not an inverse. Annual record-derived facility ratio vs. shift-level instrument quantity. See the shipped mapping table. |
| Flow efficiency (service ÷ total on-site) | *Flow of patients in OPD* | Directionally |
| Abandonment rate | *Patient satisfaction survey for outdoor patients* | Leading indicator, not equivalent |
| Counter idle minutes / 100 cases | *Registration of outpatients* | Directionally |
| RSR recovery rate | *(no counterpart — new)* | — |

v2 claimed the idle-minutes metric was the *inverse* of cases-per-doctor-per-annum. **It is not**, and that mapping is deleted. A documented mapping table ships as a deliverable so an auditor can see exactly what is and is not comparable.

### 7.2 North-star, and exactly how it is computed

> **North-star: idle clinical minutes per 100 encounters** (lower is better).
> **Numerator: `P2` — clinician-minutes present, checked in, and with no patient.**
> **Guardrail: abandonment must never rise.**

**v3 asserted this metric without ever defining its computation, which is a fatal gap: not one of its rules produced a provider-keyed quantity.** The fix is the `P1`/`P2`/`P3` roster ledger in §3.1 and an explicit derivation:

```
for each clinician c, for each rostered session s:
  present_min(c,s) = check_out(c,s) − check_in(c,s)              # two taps per session
  idle_min(c,s)    = present_min(c,s) − Σ consultation_minutes(c, patients in s)

idle clinical minutes per 100 encounters
  = 100 × Σ idle_min(c,s) / Σ encounters(OPD block)

P1 = Σ consultation minutes      (service)
P2 = Σ idle_min                  (present-idle)   ← the north-star numerator
P3 = Σ rostered_min − present_min (absent-despite-roster)
```

**This is now computable from the ledger, and it is falsifiable.** It needs two taps per clinician **session** (check-in, check-out), not per patient — the burden is real and we name it. It is also self-checking: `P2` cannot be large without `P1` being recorded, so a department cannot improve the metric by simply declining to log consultations without also destroying the denominator.

**The gaming vector, named precisely — and it is not the one v3 claimed.** v3 said the metric was gameable because a clinician taps "started" late, and then set its tamper gate to **arrival-to-first-tap lag, which measures reception, not the clinician.** That was a gate pointed at the wrong actor. The real vector is clinician-side: marking *start* late or *finish* early to inflate `P1` and shrink `P2`.

**Mitigation, designed rather than asserted:** transitions are append-only, timestamped at the edge, and not back-datable. Gate 5 (§6.4) therefore tests **three clinician-side integrity signals**, not one:

| Signal | What it catches | Threshold |
|---|---|---|
| **Stage-order violation rate** | A finish before a start, a clear before a finish — the signature of back-dating | **< 1%** of transitions |
| **Short-idle share** | `P2` split into episodes **< 60 s**, the signature of idle time being chopped up to look busy | **< 10%** of idle episodes |
| **Arrival-to-first-tap lag** *(demoted, not deleted)* | A **reception** data-quality signal, correctly labelled as such rather than as anti-gaming | **P95 < 10 min** |

Plus one thing no threshold can replace: **observer spot-audit.** Twice per quarter, an observed shift records real arrival and start times on paper and the two are compared. **We publish the divergence even if it is unflattering, because a self-reported integrity metric with no external check is a claim, not a control.**

### 7.3 Measured vs. addressable — and why "recoverable" was the wrong word

v2 called the 86.7 minutes "recoverable capacity." The source measured idle time; it did not measure recoverability, and by our own §3.2 two of the largest buckets are things we *surface but do not control*.

Correct statement, restated against the v4 taxonomy:

> Of measured idle, **`W5`** (clinician absent) is CADENCE-addressable — it is a rostering and punctuality failure the twin can re-plan around. **`W1` and `W3`** (counter and nursing idle) are addressable only where a roster permits reallocation; we surface them with evidence. **`W2` and `W4`** (counter and nursing saturated) are pure capacity findings: we report them and cannot act on them. **`W6`** (clinician busy) is a demand-versus-service-rate condition — **the twin can redistribute it, not remove it**, and claiming otherwise would be the single easiest thing for a judge to demolish. **`W7`/`W8`** are owned by Diagnostics and Records. **The addressable share is a Phase-0 measurement and is currently UNKNOWN (unknown #5).**

We will not present a total as addressable when a material fraction is out of scope by design. **The largest bucket in our own headline evidence is `W6`-shaped, which means the honest ceiling on this product is bounded by demand — and saying that up front is worth more than a larger number we cannot defend.**

---

## 8. Personas

| Persona | Need | What CADENCE gives | What it never gives |
|---|---|---|---|
| **OPD patient** (walk-in, feature phone) | To know how long, and not lose their place | SMS position + estimate; QR/USS token with no app; the display they already understand | Any clinical inference, score or penalty |
| **Receptionist** | Not to be blamed for a queue she cannot control | `W2` surfaced so counter-staffing asks are evidence-backed | A target requiring her to work faster |
| **Doctor** | Protect consultation time | Fast-track filtered to follow-ups; own queue state | Their own idle-minutes number displayed or ranked |
| **OPD manager / superintendent** | Justify staffing and reallocation with evidence; answer an auditor | Waste Ledger by cause; counterfactuals with `net_value`; MIS export in audit vocabulary | A black box; a dashboard with no recommendation |
| **Patient advocate / state programme** | Know whether reform is working | Aggregate, de-identified trend in Class-A metric names | Any patient-level record |

**On staff metrics:** individual clinician identifiers are **not** surfaced in any displayed or exported metric. Department-level reporting is the ceiling, and departmental benchmarking is **opt-in per department, off by default**. v2 proposed publishing each department's number to make them compete; that is a public-performance mechanism in a public hospital, and it is withdrawn.

---

## 9. Scope

### 9.1 Non-goals — deleted, not deferred

| Cut | Reason |
|---|---|
| Multi-hospital / state roll-out | Fantasy in 24h; dilutes the demo |
| Hospital IoT (sensors, turnstiles) | Hardware kills an MVP; taps replace it for our metrics |
| Bed / inpatient / pharmacy management | Different queue, different owner, different metric |
| Chat-bot interface | Patients want a number, not a conversation |
| ABHA/ABDM write integration in MVP | Contingent on an external pathway |
| **Per-patient or per-clinician scoring** | Ethically unacceptable (§13) |
| LLM in the queue or clinical path | Latency, determinism, safety |

### 9.2 Phase 0 — Measure, redesigned

v2 promised to measure the Indian no-show rate from 1,500 encounters at a site it described as **"87.30% walk-in."** That phrase was wrong, and the error mattered: **"87.30% visited the institute directly rather than by referral" is not a walk-in rate.** A directly-presenting patient may hold a booked appointment. **v2 built an entire Phase-0 design on a number it had misread** — that the booked share was small — and that inference does not follow from the source.

**So the booked share is unknown #6, and we now measure it rather than assume it.** Phase 0(b) reads appointment registers directly, which yields the booked share as a by-product of the no-show base rate. **If the booked share turns out to be small, RSR is a minor feature rather than an engine (§3.3, §16.3) — and we will report that and deprioritise it.**

**Phase 0 now runs two instruments:**

**(a) Walk-in encounter logging** — 14 days, one partner site, token-level. Delivers the first real Waste Ledger, measured abandonment rate, and the **addressable share** (unknown #5).

**(b) Multi-site appointment-register log** — 14 days across 6–10 facilities' appointment desks. This needs **no OPD integration whatsoever**: an appointment register is a paper book. It yields thousands of booked slots in 14 days and delivers **two** unknowns at once — unknown #1 (no-show base rate, **with its confidence interval stated in advance**) **and unknown #6 (booked share of the day), which is a by-product of the same query and decides whether Engine 3 is worth building at all.**

Deliberately split because walk-in and booked traffic are different problems with different measurements.

### 9.3 Phases

**Phase 0 — Measure.** As above. Publishes the unknowns it resolves.

**Phase 1 — Measurement-only CADENCE.** Waste Ledger + SMS + display + MIS export in CAG vocabulary + mapping table. No models, no recommendations. Deployable with a tablet and a mini-PC.

**Phase 2 — Twin + counterfactual console.** Runs the §6.4 gate. **Ships recommendations only if it passes.**

**Phase 3 — RSR.** Requires Phase 0(b). Requires scope-of-practice approval for nurse-led fast-track.

**Phase 4 — Extension.** Second OPD block, then multi-site, only on published Phase 1–3 results.

**The single fallback, defined once:** *if the §6.4 gate fails, CADENCE ships Phase 1 only — Waste Ledger, display, SMS, MIS export, mapping table. No models, no recommendations, no RSR. RSR is deferred to Phase 3 because it is gated on a measured base rate we will not have.* v2 contradicted this in three places; there is now one definition.

---

## 10. Demo — 4 min 30 s

**Scope, stated accurately:** the demo shows **all three engines on synthetic data**, with every number labelled `SIMULATED` and the twin marked **UNGATED**. It is not "measurement-only," and we do not claim it is. What we claim is that the pipeline is correct end-to-end and that the gate which would license real-world claims is specified, published, and not yet passed.

| Beat | Time | Screen | Spoken point |
|---|---|---|---|
| **0 — The label** | 0:00–0:12 | On-screen banner | *"Everything you're about to see is simulated. Our twin is fitted to data our own generator produced. This shows the pipeline is correct — not that the OPD is. Here's the gate that would tell us the second thing."* |
| **1 — The gap** | 0:12–1:00 | Two numbers side by side | Stopwatch, an Indian OPD: **85.71%** of on-site time spent waiting to see a doctor. Survey, India: waiting is the **worst of six** domains, **9.5%** negative, **40.9%** neutral-or-worse. *"Different instruments, same country. Both can see it. Neither can act on it inside a shift."* |
| **2 — The ledger** | 1:00–1:45 | Waste Ledger `SIMULATED` | One day, on-site minutes split across `W1…W8`, one cause dominant, **`W9` shown with its real value**. Then the **provider bar**: `P1` / `P2` / `P3`. *"That's a rostering question, not a sentiment question."* |
| **3 — The twin** | 1:45–2:35 | Counterfactual console `SIMULATED` `UNGATED` | Move a room between OPDs; run the other as a nurse-led fast-track. Median wait, P90, abandonment for both. |
| **4 — The refusal** | 2:35–2:55 | Same console | A proposal that looks good returns **"net value −14 min/100 cases. Do not do this."** *Pause.* This beat buys credibility for every other number. |
| **5 — The loop** | 2:55–3:40 | RSR `SIMULATED` | Slot frees at 14:05 → matched to the longest-waiting administratively-compatible patient → SMS confirm. **Voiceover:** *"one tap — and only if the offer doesn't push anyone already queued."* |
| **6 — The audit** | 3:40–4:05 | MIS export | Numbers in CAG field names, **plus the mapping table** showing what is not comparable. |
| **7 — The gaps** | 4:05–4:30 | Static | **Seven** unknowns, named, each with an owner. Six gate thresholds, printed. |

**Three-minute variant** (when the slot is short — it will be): beats **0, 1, 2, 4, 7**, re-timed to **12 + 60 + 55 + 25 + 28 = 180s.** *v3 wrote "three-minute variant" without re-timing the beats, and they summed to 150s. A variant that runs 30 seconds short is worse than no variant.*

**Failure rule, written down:** if not working within **15 seconds**, cut to the pre-rendered video. **The 15 seconds are drawn from beat 0's allocation, not added to it, so the worst case is still 4:30.** No apology. Keep talking.

**Fail-safe:** pre-rendered 4:30 MP4 in a second tab, plus an offline LAN duplicate. Plus **one piece of genuinely live computation** — re-running the `W1`–`W9` attribution live over the day's token log (fast, deterministic, non-Monte-Carlo) so the room sees code executing. Precomputed Monte-Carlo is acceptable *only* alongside something live, because a pre-rendered frame is indistinguishable from a mock-up.

**Printed judge card:** the seven thresholds, seven unknowns with owners, sources with URLs, and the regeneration command.

---

## 11. Judging-criteria map

| Criterion | What we put in front of them |
|---|---|
| **Innovation** | A closed loop that prices interventions in clinician-minutes and **returns "do not do this"**; **RSR**, reframing no-show prediction from reporting into capacity recovery; **two ledgers on one taxonomy** — patient-time and provider-time — which is what lets us tell a *demand* problem from a *rostering* problem using data rather than argument; and the tap-integrity discipline of publishing our own instrument's error, including the one signal that points at us. Narrowed per §16.3. |
| **Relevance** | Every headline number is Indian and traceable to a named source — published 2024–2026, with LASI's **2017-18 fieldwork stated** — except one, which we label a Nigerian comparator rather than dress up. **And the Relevance cell is self-refuting in v3, so we say so here:** the honest finding we lead with is that *the instrument we would replace is not broken, and we do not know why it compresses waiting* (unknown #4). We chose the uncomfortable findings: waiting is India's **worst** domain and its ratings still compress it, and the one Indian HMIS datapoint does not support the digitise-it thesis. |
| **Technical depth** | Calibration over AUC (threshold is policy); live-fitted DES rather than an opaque regressor; bipartite matching as the mechanism; **an exhaustive token-state taxonomy with a published, non-zero residual and a pre-fixed definition of that residual**; a roster-keyed provider ledger that makes the north-star computable and cross-checkable against the patient ledger; tamper-evident taps with three integrity signals; offline-first. Model choices justified against a real maintenance-mode risk. |
| **Feasibility** | One building. No custom hardware. **Five staff roles** (§4.2). A real BOM with a DLT lead time. Phase 1 needs no model and no ML ops. |
| **Impact** | North-star is **idle clinical minutes per 100 encounters**, computed as `P2` — clinician-minutes present and with no patient — from **check-in/check-out taps minus consultation minutes**, a derivation we publish (§7.2). Guardrail is abandonment. We deliberately do *not* call idle time "recoverable": the addressable share is **unknown #5**, and the largest bucket is a demand condition the twin can redistribute but not remove (§7.3). |
| **Scalability** | RSR scales free within a roster. Scalability is argued from Phase 4 evidence, not asserted in Phase 1. **The twin is per-site by design: a flow model that transfers across sites without re-fitting is a flow model that is wrong.** |
| **UX** | **Seven taps** on the counter→clinician path, stated honestly (§4.2); **five instrumented roles** plus one human observation. **The paper token stays primary**, so a feature-phone patient is never excluded (§3.4). SMS for feature phones. Offline-first. No patient-facing score, ever. |
| **Presentation** | The gap in beat 1, the refusal in beat 4, the volunteered gaps in beat 7, a 3-minute variant, a written failure rule, and a printed source card. No slide claims anything the ledger cannot reproduce. |
| **Sustainability** *(added — v2 omitted this)* | Per-facility annual licence, infra cost at pilot scale, and the honest acknowledgement that **Indian public procurement runs 9–18 months**, so the Phase 0→3 roadmap is roughly one fiscal year. Government health deployments are typically funded as an institutional capability, not a per-seat SaaS; we model accordingly. |

---

## 12. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Twin fails the gate | High (plausible) | Documented fallback: Phase 1 only (§9.3) |
| Walk-in traffic defeats RSR | High | RSR targets the booked subset only; Phase 0(b) quantifies the booked share first. If small, RSR is deprioritised and we say so |
| Staff don't tap | High | **Seven taps per patient** on the counter→clinician path (§4.2). This is a real cost and we state it rather than minimise it. Mitigation: departmental benchmarking opt-in not a league table; pilot with a volunteering department; **and we state plainly that we have not yet secured clinical sponsorship — this is our single largest project risk, and it is a relationship risk, not a technical one** |
| `W7`/`W8` roles won't participate | High | Named as Phase 0's first negotiation. If it fails, those codes are reported **unavailable** rather than estimated, and the state-coverage test records which states are unmapped |
| Data privacy | High | §13 architecture; DPDP scoping; paper token preserved |
| SMS / DLT dependency | Medium | LAN-local core; OPD display works with zero external services; 2–6 week lead time flagged |
| "It's just another queue app" | Medium | Beats 1 and 4 exist to defeat this read |
| Procurement timeline | Medium | Stated openly in §11 rather than discovered in Q&A |
| Overclaiming under cross-examination | Medium | §5 classes; every claim tagged A–E; the unknowns slide is mandatory |

---

## 13. Ethics, privacy, regulatory

Stated as product constraints, so they are testable.

1. **No clinical function.** No diagnosis, triage, severity or condition inference, anywhere, for anyone. CADENCE answers "how long," never "what's wrong." **v3 asserted this while also matching patients on "clinical compatibility" and texting them a clinician's name — both are clinical-adjacent, so v3's own claim was false on its own product. v4 fixes both:** matching is on **administrative** compatibility (§3.3), and no clinician is named in any SMS.
2. **No individual patient or clinician score exposed to staff.** The no-show model produces a probability used **once**, to decide whether to re-offer a slot. **v3 claimed it is "not persisted as a patient attribute" — that was false and self-contradictory**, since v3 also scored slots at `T-24h` and `T-90min` and reported priority-queued arrivals as a tracked cohort. v4 states what actually happens: the per-slot score is computed and **logged in the append-only decision record** (§13.5), because an unauditable decision is worse than a logged one. What is true is narrower and is what matters: **it is never displayed to staff, never exported, never joined to a clinician's name, and never used for anything except one slot-release decision.** Patient-side non-arrival is reported as **OPD-level counts and rates only** — no individual no-show score exists anywhere, because a non-arrival has no token timeline to score.
3. **No financial or clinical ranking of patients.** Slot matching is on **administrative compatibility** first (specialty, slot type, follow-up status — scheduling attributes, not clinical judgements) and expected marginal wait reduction second. Cashless and eligibility checks remain the hospital's function and are never inferred. **No clinician's name appears in any patient-facing SMS** (§3.3).
4. **Consent architecture — DPDP Act 2023.** Token-level pseudonymous data, purpose-limited to queue operations. Consent is captured at QR scan **with an explicit non-digital alternative: the existing paper token continues to function, and CADENCE never denies a token for refusing consent.** Opt-out is honoured immediately and permanently. The institution is the data fiduciary. DPDP 2023 obligations — notice, purpose limitation, consent records, data-principal rights — are scoped as explicit pilot work with named owners.

   **The self-selection consequence, stated because v3 missed it:** consent is captured *through the digital path*, so patients who take the paper token or decline consent are **systematically absent from the ledger**. The ledger is therefore a **consenting subset**, and if refusing correlates with language, literacy or trust, the published distribution is **not** the distribution of all patients. Mitigation: the hospital supplies an **aggregate paper-token count** for OPD-level reconciliation, so we can report *what fraction of the day's visits the digital ledger covers*. **A consent-based system that cannot report its own coverage is not measuring the OPD.**
5. **Append-only decision log.** Every model-recommended action — reallocation, priority-queue insertion, schedule change — is written with its inputs, model version, and confidence at time of decision. **Priority-queued arrivals are logged and reported as a distinct cohort** (this is the cohort whose composition §13.2 describes; v3's two statements about persistence contradicted each other, and v4 keeps only the one that is true), and no patient is priority-queued without clinical sign-off on the reallocation policy.
6. **Read-only on clinical records.** No write-back to any EHR/HMIS.
7. **Staff-side fairness.** No individual clinician metric is displayed or exported. Department-level reporting is the ceiling; benchmarking is opt-in and off by default.
8. **The refusal is a feature.** CADENCE must be able to report that an intervention failed or was not worth doing.

---

## 14. Claim ledger

### Class A — assert plainly
- **ABDM:** **25 crore OPD registrations** under Scan & Register — **registrations, never visits.**
- **NSS:** 75th round (Jul 2017 – Jun 2018) government/public share of treated ailment spells 33% rural / 26% urban; average medical expenditure per hospitalisation case (excl. childbirth) ₹16,676 rural / ₹26,475 urban. **The 80th round (2025) puts the rural public share at 35% — cite that as current.**
- `facebook/prophet`: **maintenance mode as of v1.4.0**; no new features planned.

### Class A\* — official document, specific detail not re-verified this pass
- **CAG of India**, *Report 2 of 2025, performance audit of the UT of Jammu and Kashmir* (period ended March 2022), **Chapter III**: we assert that a national audit framework exists covering OPD flow, waiting time, cases per doctor and consultation time. **We do not assert the exact field list as verified** — the site was unreachable on re-check (§5.7). **Nothing in the argument depends on the field list.**
- **NAMCS 2023 HC:** the dataset exists, is US-based, and is **not** transferable to Indian OPDs. The response-rate, visit-count and `VISWT`-correction specifics were **removed from asserted figures** — CDC pages returned 403 on re-check, and no argument depended on them.

### Class B — assert with setting stated inline, every time
- De et al. (2024), Indian tertiary hospital, n=252: flow exceeded doctor service rate in **all** OPDs; orthopaedic OPD **85.71%** of on-site time spent waiting to see a doctor; 87.30% visited directly; 63.89% newly registered.
- Ambade, Kim & Subramanian (2024), **LASI Wave 1, fieldwork 2017-18**, analytic sample **33,724 outpatient** records (from 72,270 observations; 4,781 hospitalised / 37,494 outpatient pre-exclusion). Negative = **"Bad"/"Very Bad"** on a five-point Likert scale. Waiting time: **4.6% negative — highest of six domains** (4.0 bad + 0.6 very bad); **9.5%** among public-facility outpatients, the highest negative in public facilities; **3.5%** in private facilities. Among public outpatients, waiting draws the **lowest "very good" share of the six (15.0%)** and the **highest neutral-or-worse share (40.9%)** — which means **59.1% rated the wait positively, and we report that alongside the rest.** State spread is wide: **30.7%** negative in Andaman & Nicobar. *Rank and distribution only; fieldwork year disclosed; the paper's own favourable reading of India's absolute level is acknowledged; **the three cuts are not independent — negative is contained within neutral-or-worse.***
- Hyderabad (2026), two government facilities, n=214: **40.2% of outpatients at the HMIS site reported waits ≥120 min, vs 23.4% at the non-HMIS site**; AOR 2.05 (1.04–4.03). **Association only; two-site design; a proportion compared to a proportion, not a mean wait (§2.3). We do not claim the non-HMIS site had shorter waits** — the paper reports no mean or median.

### Class C — assert only as analogy
- Kemdirim et al. (2021), **Nigeria**: 86.7 of 122.6 min non-service (paper reports 65.3%) public vs 20.9 of 44.9 (41.2%) private; waiting-for-clinician 51.4 min vs 12.6 min consultation; 3/3/3 vs 2/2/3 staff, both 3 clinicians. Tag: `Nigeria, 2021 — international comparator; mechanism generalises, magnitude does not; two-hospital contrast, association only.` **Arithmetic discrepancy disclosed in source — 86.7 ÷ 122.6 = 70.7%, and the source's own columns miss by 0.1 min (§0.1).**
- NAMCS 2023 magnitudes → US health centers only, tagged in-line, never converted to an Indian rate.
- Brazilian dataset → unit-test fixture only. No figure in any slide.

### Class D — always labelled on the same visual
- Every demo figure, every twin counterfactual, every `SIM` band: **"SIMULATED — within-model variance."**

### Class E — stated as unknown
1. Indian government OPD no-show base rate · 2. abandonment rate · 3. twin's real-world accuracy · 4. **why** the survey compresses waiting · 5. addressable share of idle time · 6. **booked share of a typical day** · 7. whether the survey and the audit are compressed by the same mechanism. **All seven have a named owner and a date (§5.5).**

### Removed — do not reinstate
- "13.4–25.9% avoided a visit due to waiting time (NSS 75th)." Untraceable to a primary source. Cut in v2, still cut.
- "79.3% of outpatient care in the private sector" as an all-India NSS 75th figure. It is a **NITI Aayog** figure for **21 larger states pooled across three rounds**. Removed from the evidence base.
- "Prophet is archived/deprecated." **Wrong** — maintenance mode.
- "25 crore OPD visits." **Wrong unit** — registrations.
- "Government of India, CAG Report Chapter IV." **Wrong** — UT of Jammu and Kashmir, Chapter III.
- **"Two taps per patient."** **Wrong** — it is seven on the counter→clinician path (§4.2).
- **"Four instrumented roles."** **Wrong** — five (§4.2).
- **"The survey is the one the hospital answers to."** **Wrong** — the CAG audit is the harder instrument; both see it, neither acts on it (§0.3, §2.4).
- **"The Nigeria contrast is the cleanest evidence available."** **Inconsistent** — it is a two-hospital contrast and is held to the same standard as Hyderabad (§0.1).
- **"No-show probability is not persisted."** **Wrong** — it is logged, never displayed (§13.2).
- **"Three independent cuts" of the LASI distribution.** **Wrong** — negative is contained within neutral-or-worse; the 59.1% positive share is now reported too (§0.2).
- **Hyderabad "waits were longer where an HMIS was present."** **Overreach** — a higher *proportion* of ≥120-min waits, not a longer mean wait (§0.2 row 4).

---

## 15. What we would say in 90 seconds

> Indian government OPDs don't have a registration problem. They have a load-versus-service-rate mismatch, and the instruments the system already runs — the survey and the audit — can both *see* it and neither can *act* on it inside a shift.
>
> In four OPDs at an Indian tertiary hospital, patient flow exceeded doctor service rate in **every single one**. In one of them, 85.71% of a patient's entire on-site time was spent waiting to see a doctor.
>
> Now the national survey asks how people *rated* that wait. Waiting comes **worst of six domains** — and only **9.5%** of public-facility outpatients call it bad, **15%** call it very good, and **41%** say it's neutral or worse — which means **59% rated it positively.** A stopwatch and a survey, same country, and they do not agree. **We don't know why. That's one of seven named unknowns, not a rhetorical flourish.**
>
> Here's the trap: the obvious fix is to buy software. At two government hospitals in Hyderabad, **a higher share** of outpatients reported two-hour waits where an HMIS was present — two sites, so it's an association, not a cause, and we won't claim more. But it does mean an information system isn't evidence of a shorter queue. Nobody owns the loop.
>
> **CADENCE is that loop.** It gives every idle minute exactly one of eight causes — and it runs a **second ledger keyed to the clinician**, so it can tell a **demand** problem from a **rostering** problem instead of guessing. It simulates a reconfiguration of *your* OPD *before* you make it, prices that change in clinician-minutes, and tells you when the change **isn't worth it**. And when a no-show frees a slot, it doesn't log the no-show — it **fills the slot**, unless that would push someone already queued.
>
> We're showing you all of it on synthetic data, and the twin is **ungated** — we show you the gate. Seven thresholds, seven unknowns, one regeneration command.
>
> India already audits for waiting time and flow. We're not inventing a metric. We're building the loop that moves them.

---

## 16. Prior art — what we build on

*Volunteering prior art is the highest-return move available on the Innovation criterion. A judge who knows the field will otherwise supply it against us.*

### 16.1 The honest landscape

| Our component | Closest prior art | What survives |
|---|---|---|
| **Waste Ledger** | Time-and-motion / time-flow study methodology (incl. Kemdirim's station-level decomposition); Lean healthcare waste taxonomy (Graban & Toussaint; Costa et al. 2016 review); process mining with conformance checking, which generates conformance gaps from event logs automatically; **value-stream mapping** (Lean) | The *method* is standard. What is ours: **exhaustive, rule-derived cause attribution in an Indian auditor's own vocabulary, with a published residual whose definition is fixed before data collection, plus a companion provider-keyed ledger.** That is an implementation and interoperability contribution, not a discovery |
| **Queue Digital Twin** | Hospital discrete-event simulation — a twenty-year Health Care Management Science literature; commercial tools (AnyLogic, SimPy, PROMEDICA, MED-Mod, COSTSIM); healthcare "digital twin" as a live data-connected simulation | A DES with online parameter refitting is established. Our contribution is **fitting it per-site from that site's own token log and using it to rank reconfigurations by clinician-minute net value.** Standard tooling, applied somewhere it is not |
| **Released-Slot Reallocation** | **EHR waitlist auto-fill ("Fill-In" scheduling) is a shipped commercial feature.** No-show prediction with ML is a large literature. SMS reminders reducing no-shows is well established. Appointment overbooking is a twenty-year literature | **This is the weakest novelty claim in the deck and is presented as such.** Reframing it as "nobody does this" is false and would be caught. **Its applicability to our setting is also unmeasured** — see the withdrawn claim in §16.3 |

### 16.2 The mechanism hypothesis, labelled

v2 asserted that the Hyderabad HMIS "displays a queue without owning an intervention." **No instrument in that study observed functional scope.** That is **our hypothesis about why display-only systems underperform — untested.** It is a plausible design rationale, not evidence.

### 16.3 The defensible novelty statement

> Waitlist auto-fill and no-show prediction are commodity EHR features, and hospital DES and time-and-motion study are established methods. We claim three narrower things: **(1)** we build **two ledgers on one taxonomy** — patient-time and provider-time — which is what makes it possible to distinguish a *demand* condition from a *rostering* condition from the same observed waiting number, instead of reporting one undifferentiated "wait"; **(2)** we attach every recommendation to a **measured** local base rate rather than an assumed one, and we treat the no-show rate, the abandonment rate and the addressable share as **unknown until we go and measure them** — three of which v3 would have asserted; **(3)** we gate every recommendation on a **live-fitted twin and a pre-registered validation threshold**, including the option to recommend against an intervention and the option to ship measurement-only.
>
> **The instrument disagreement** — a stopwatch returning 85.71% of on-site time spent waiting to see a clinician, while India's national patient-experience survey ranks waiting the worst of six domains and still returns single digits — is what **motivates** the work. It is **not** novelty, and we do not claim it as such: measuring the same thing two ways is standard practice, and LASI and De et al. were not built to be compared.

**The novelty claim that v3 made and v4 withdraws.** v3 claimed RSR's novelty was applying capacity-recovery to a "**walk-in-dominant Indian public OPD that has no scheduling system to fill**." That sentence is self-defeating: **if there is no scheduling system, there are no slots to reallocate, and RSR has nothing to act on.** v3 asserted Engine 3 as a headline while its own primary evidence describes a setting that would minimise Engine 3. The honest position is a dependency: **RSR applies to the booked share of the day, that share is unmeasured (unknown #6), and if it is small, RSR is a minor feature rather than an engine.** We would rather say that than defend a claim that dissolves on contact.

---

## 17. References

**Primary / official** — *see §5.7: two of these could not be re-opened in the v4 audit pass and are marked A\**
1. CAG of India — *Report 2 of 2025: performance audit of the Government of UT of Jammu and Kashmir, Public Health Infrastructure and Management of Health Services* (period ended March 2022), **Chapter III**. *(A\* — site unreachable on re-check; field list not asserted as verified.)*
2. MoSPI — *NSS 75th Round, Household Social Consumption: Health*, Summary Analysis Report 586. `mospi.gov.in/sites/default/files/announcements/Summary%20Analysis%20Report_586_Health.pdf`
3. PIB — *Household social consumption in India: Health, NSS 75th round* (23 Nov 2019). **Superseded for the public-share figure by the NSS 80th round (2025): rural public share 35%.**
4. PIB — ABDM Scan & Register milestone, **25 crore OPD registrations** (registrations, not visits).
5. CDC/NCHS — *2023 NAMCS Questionnaires, Datasets, and Documentation*. doi chain: PMC / NHSR No. 216 (as of v3.1). *(A\* — CDC pages returned HTTP 403 on re-check; detailed response-rate and `VISWT` figures removed from asserted claims as unverified.)*
6. `facebook/prophet` README — maintenance-mode notice (v1.4.0).

**Peer-reviewed**
7. De A, Gupta S, Chakraborty A. *Navigating Patient Flow: Assessing the Bottlenecks in Out-Patient Services in a Tertiary Care Hospital in India.* Dr Sulaiman Al Habib Medical Journal 2024;6(3):136–141. doi:10.4103/dshmj.dshmj_63_24
8. Ambade M, Kim R, Subramanian SV. *Experience of health care utilization for inpatient and outpatient services among older adults in India.* Public Health in Practice 2024;8:100541. doi:10.1016/j.puhip.2024.100541
9. *Comparison of the factors influencing the patients' waiting time between two healthcare facilities with and without health management information system in Hyderabad.* BMC Health Services Research 2026;26:945. doi:10.1186/s12913-026-14997-y. **Author list not captured in the v4 retrieval — add before submission.** *26:945 is the article number, not a page range.*

**International comparator — mechanism, not magnitude**
10. Kemdirim CJ, Uduak A, Opurum N, Hart D, Ogaji DS. *Time-Flow Study for Receipt of Outpatient Services in Public and Private Hospitals: Implications for Lean Approach in Health Facilities in Rivers State, Nigeria.* Nigerian Medical Journal 2021;62(6):325–333. doi:10.60787/NMJ-62-6-63

**Prior art we build on**
11. Costa LB, Godinho Filho M. *Lean healthcare: review, classification, and analysis of literature.* Production Planning & Control 2016;27:823–36.
12. Graban M, Toussaint J. *Lean Hospitals.* Productivity Press, 2018.
13. Tlapa D, Zepeda-Lugo CA, Tortorella GL, et al. *Effects of lean healthcare on patient flow: a systematic review.* Value in Health 2020;23:260–73.
14. Process mining with conformance checking — event-log-derived deviation analysis.
15. Hospital discrete-event simulation literature (Health Care Management Science; SimPy/AnyLogic tooling).

**Notes on removed sources**
- "13.4–25.9% avoided a visit due to waiting time (NSS 75th)" — **untraceable; cut.**
- "79.3% outpatient care in the private sector" as an all-India NSS 75th figure — **NITI Aayog, 21 larger states, three pooled rounds; removed from the evidence base.**
- Brazilian `No-show Appointments` dataset — **unit-test fixture only; no figure in any slide.**

---

## 18. Build checklist, in priority order

1. Seeded synthetic generator (14 days, 1 OPD block, `seed=20261003`) + provenance sheet. Everything depends on it.
2. Token state machine → additive Waste Ledger with an **exhaustive** `W1…W9` cause set and the roster-keyed `P1/P2/P3` provider series. **✅ Already built and proved — `cadence/cadence/taxonomy.py` + `cadence/tests/test_taxonomy.py`: 25 tests, all 98,304 observable states enumerated, 0 uncovered, all nine codes reachable, `sum(W1…W9) + data gaps == in-scope states`.** The suite also pins three properties no amount of reading this document would have caught: `W5`/`W6` remain distinct (fatal A1), **no declared code is dead**, and **a data gap yields no ledger row rather than being filed as waste.**
3. OPD display + SMS adapter (mocked, with a real interface boundary).
4. Arrival-rate + no-show models **with calibration reporting** (reliability curve in the repo).
5. Live-fitted DES twin + reconfiguration search + `net_value` ranking + **the refusal path**.
6. RSR bipartite matching **with the walk-in P90 non-regression constraint**.
7. **CAG mapping table** as a shipped artefact.
8. **Validation-gate harness** running all seven thresholds + the no-show calibration gate, printing pass/fail. *Build before demoing the twin — it is what makes the twin claimable.*
9. Pre-rendered demo video + offline LAN duplicate + **one genuinely live computation**.
10. Printed judge card: thresholds, unknowns, sources, regeneration command.

**Anti-goal:** do not add a feature that does not reduce idle clinical minutes or abandonment. That rule alone eliminates roughly half of what a team would otherwise attempt in 24 hours — and, per §16.1, roughly half of what would be reinvented prior art.