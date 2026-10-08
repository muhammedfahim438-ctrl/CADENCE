# CADENCE v4.0 — Adversarial Review and Resolution Register

**Target document:** `PROJECT_SOLUTION_FINAL.md` (Solution Specification v3.1 → v4.0)
**Track:** AI & Machine Learning — Smart Hospital Queue Management (HackSpark 2026)
**Team:** CATALYST CREW A · **Institution:** NEHRU ARTS AND SCIENCE COLLEGE, COIMBATORE
**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE

> **This document is internal.** Sections 1–3 are preparation material and are **not** part of any submission. It exists so the flaws below are fixed rather than rediscovered by a judge.
> **Note:** `PROJECT_DRAWBACKS.md` is the **earlier v2 review** of `PROJECT_EXPLANATION.md` and the pitch decks. It is a different document covering a different artifact and is **superseded** by this one for anything concerning the solution specification.

---

## 0. Outcome

| | Count |
|---|---|
| **Fatal** findings | 11 — **all fixed** |
| **Serious** findings | 15 — **all fixed** |
| **Minor** findings | 6 — **all fixed** |
| Sources that could not be re-opened | 2 of 8 — **both downgraded** |

**Two findings would have lost the room on their own.** They were not wording problems; both were design defects that survived the v3.1 "source verification pass" because that pass checked *citations* and never checked *whether the mechanism worked*.

1. **The cause taxonomy did not partition a patient's timeline.** There was no code for queueing behind a clinician who is **busy** — the dominant waiting state, and the one behind our own 85.71% headline — and **no nursing code at all**, while the comparator study we cite decomposes an encounter into registration / **nursing** / clinician. We were citing a three-station structure and shipping two of its three stations.
2. **The north-star metric was not computable from the ledger we specified.** "Idle clinical minutes" is a property of a *provider*; the ledger was keyed to *tokens*, and **not one detection rule described provider-idle-with-no-patient.** The Impact criterion rested on a number the engine produced zero rows of.

**What the review did not overturn:** the 85.71% headline; the LASI distribution and its six-domain rank; the 2.7× encounter contrast (demoted to an existence proof); the AOR direction with its confidence interval; the CAG / ABDM / NSS / Prophet unit discipline; the architecture and scope discipline; the DPDP consent architecture; and the refusal mechanism. **The bones were sound. The arithmetic and the framing were not.**

---

## 1. Fatal findings — design defects

### A1 · The taxonomy never partitioned the timeline
**Was:** `W1` counter-idle · `W2` counter-queue · `W3` clinician-not-present · `W4` diagnostics · `W5` documentation · `W6` patient-side

**Defect:** asked "what is a patient waiting behind a *working* clinician?" there was **no answer**. Asked "what about the nursing station?" there was **no code at all**. The document nonetheless claimed each token's time was "attributed to exactly one of six causes." Ordinary waiting — the majority of it — fell through every rule and would have been silently mis-bucketed.

**Fix:** rebuilt as an **exhaustive state table** in which every state maps to exactly one code:

| Code | Cause | Condition |
|---|---|---|
| `W1` | Counter idle | in counter queue **and** ≥1 counter open and idle |
| `W2` | Counter queue | in counter queue **and** all counters busy |
| `W3` | Nursing idle | in nursing queue **and** nurse present and idle |
| `W4` | Nursing queue | in nursing queue **and** all stage-nurses busy |
| `W5` | Clinician absent | in consultation queue **and** (room vacant **or** clinician not checked in) |
| `W6` | Clinician queue | in consultation queue **and** clinician present **and** with another patient |
| `W7` | Diagnostics detour | sent to imaging/lab **and** not returned within SLA |
| `W8` | Documentation | clinically finished **and** not cleared |
| `W9` | Unclassified | any state no rule above covers |

**Why `W5`/`W6` is the important addition, not `W3`/`W4`:** they are different problems with different owners. `W5` is a **rostering and punctuality** failure the twin can plan around. `W6` is a **load-versus-service-rate** condition that no reordering fixes. A ledger that collapses both into "waiting for the clinician" cannot tell a hospital whether its problem is staffing or demand — which is the entire reason the ledger exists.

**Effect: better.** We now ship the three-station structure we cite, and nursing is instrumented as a first-class station.

### A2 · The north-star was not computable
**Defect:** the Impact metric is provider-keyed; the ledger was token-keyed. **No rule in v3.1 could ever produce it.**

**Fix:** added a roster-keyed companion ledger — `P1` clinician-minutes consulting, `P2` clinician-minutes **present and idle**, `P3` clinician-minutes rostered but not checked in — with an explicit derivation in §7.2:

```
present_min(c,s) = check_out(c,s) − check_in(c,s)
idle_min(c,s)    = present_min(c,s) − Σ consultation_minutes(c, ·)
north-star       = 100 × Σ idle_min(c,s) / Σ encounters
```

**Effect: better.** The two ledgers **cross-check**: high `W6` with high `P2` is a *demand* signature; high `W6` with high `P3` is a *rostering* signature. The same patient-side number, two root causes, separated by data rather than argument.

### A3 · "Every non-service minute to exactly one of six causes" was false
**Defect:** the additive claim was asserted, not demonstrated; and `W7 — unclassified` was redefined *after* the reconciliation question arose, making it gameable.

**Fix:** every partition claim rewritten to match the A1 state table. `W9`'s definition is **fixed before data collection** and gate 4 tests it against that fixed definition.

### A4 · "The survey is the one the hospital answers to" — contradicted by our own evidence
**Defect:** this was the document's headline, and **row 5 of our own evidence table** — the CAG audit — shows India already audits waiting, flow and consultation time systematically. The claim overstated our case *against* ourselves.

**Fix:** replaced throughout (§0.3, §2.4, §10, §11, §15) with the narrower and stronger claim: **both instruments see the problem, and neither can act on it inside a shift** — one is a recalled household rating, the other a facility-level review over a reporting period. **The gap is the absent loop, not absent data.**

### A5 · Double standard on two-hospital evidence
**Defect:** §2.3 devotes a paragraph proving that a **two-site** Hyderabad comparison cannot identify a causal effect — effective sample of two clusters, CI spanning the null. Meanwhile §0.1 called the **two-hospital** Nigeria contrast *"the cleanest evidence available."* Same structure, opposite treatment. A judge who notices will distrust every other standard in the document.

**Fix:** Nigeria held to the **identical** standard. Downgraded from a causal-sounding claim to an **existence proof against the paperwork thesis**: in these two hospitals, more counter and nursing capacity did not accompany a shorter visit. Nothing more.

### A6 · Gate 5 measured the wrong actor
**Defect:** we claimed the north-star was gameable by a clinician tapping "started" late — then set the gate to **arrival-to-first-tap lag, which measures reception.** The gate pointed at the wrong person.

**Fix:** gate 5 split into three signals:

| Signal | Catches | Threshold |
|---|---|---|
| **Stage-order violation rate** | back-dating (finish before start, clear before finish) | **< 1%** |
| **Short-idle share** (`P2` episodes < 60 s) | idle time chopped up to look busy | **< 10%** |
| Arrival-to-first-tap lag — *demoted, relabelled* | reception **data quality**, not anti-gaming | **P95 < 10 min** |

Plus an **observer spot-audit** twice per quarter — a control no threshold replaces.

### A7 · "Two taps per patient" survived in three sections after v3.1 corrected it in one
**Fix:** corrected everywhere. **The counter→clinician path is seven taps** (2 reception + 2 nursing + 3 clinician). Stated as a real cost with a named risk entry, not minimised.

### A8 · "Four instrumented roles" contradicted a five-row matrix
**Fix:** **five** instrumented roles (Reception, Nursing, Clinician, Diagnostics, Records) + one human observation. Corrected in §4.2, §4 diagram, §11, §12.

### A9 · "No clinical function" was false against our own product
**Defect:** the ethics section claimed **no clinical function anywhere**, while RSR matched patients on **"clinical compatibility"** and the SMS read *"a slot has opened with **Dr. ___**."* Both are clinical-adjacent. The claim was falsified by our own demo script.

**Fix:** matching is now **administrative compatibility** — specialty, slot type, follow-up status, all attributes already on the booking. **No clinician is named in any patient-facing SMS.**

### A10 · "No-show probability is not persisted as a patient attribute"
**Defect:** contradicted twice in the same document — we score slots at `T-24h` and `T-90min`, and we report priority-queued arrivals as a **tracked cohort**. Both require persistence.

**Fix:** replaced with what is actually true and actually matters: the per-slot score **is** written to the append-only decision record, because an unauditable decision is worse than a logged one — but it is **never displayed to staff, never exported, never joined to a clinician's name, and used exactly once.** Patient-side non-arrival holds no minutes and is reported as OPD-level counts only.

### A11 · The RSR novelty claim was self-defeating
**Was:** *"we apply capacity-recovery to a walk-in-dominant Indian public OPD that has no scheduling system to fill."*

**Defect:** if there is no scheduling system there are **no slots to reallocate**, and RSR has nothing to act on. The sentence dismissed its own engine in the same clause. v3 asserted Engine 3 as a headline while its primary evidence described a setting that would minimise Engine 3.

**Fix:** claim **withdrawn**. Replaced with an honest dependency on **unknown #6 (booked share of the day)**, measured directly by Phase 0(b). Novelty now rests on the **dual-ledger taxonomy**, not on RSR. *This makes the deck weaker, which is the point.*

---

## 2. Serious findings — published numbers and framing

| # | Finding | Fix |
|---|---|---|
| **B1** | **"Three independent cuts" of the LASI distribution is algebraically false** — negative is *contained within* neutral-or-worse by definition | Corrected, and we now **report the omitted 59.1% who rated the wait positively**. Leading with 40.9% while omitting its complement was the cherry-pick v3.1 claimed to have removed |
| **B2** | The 30.7% Andaman & Nicobar figure was cited and **never used** | Now used: waiting negativity varies enormously by state, which argues for local measurement over national averages |
| **B3** | v3.1 asserted it had **verified** Nigeria denominators it had not | Rewritten. **We cannot reconcile 65.3% to 70.7% from the reported numbers.** Two candidate readings are stated; we also disclose that **the source's own columns miss by 0.1 min** (86.7 + 35.8 = 122.5, not 122.6; 20.9 + 23.9 = 44.8, not 44.9). **The discrepancy is in the source, not our transcription** |
| **B4** | Hyderabad framed as *"waits were **longer**"* — the paper reports a **proportion** of ≥120-min waits, **not a mean or median** | Restated as "a higher *share* reported long waits." We explicitly do **not** claim the non-HMIS site had shorter waits |
| **B5** | **The primary patient path was QR/USS — which needs a smartphone — while our own persona owns a feature phone** | The **existing paper token is now the primary path.** QR/USS is optional convenience. Nothing about a patient's care changes if they decline the digital path |
| **B6** | Consent is captured **through the digital path**, so the ledger is a **self-selected sample** — undisclosed | Disclosed, with a required **coverage metric**: the hospital supplies an aggregate paper-token count so we report *what fraction of the day's visits the digital ledger covers*. **A consent-based system that cannot report its own coverage is not measuring the OPD** |
| **B7** | Gates 1–3 were **not independently evaluable** — no unit, no split, no decision rule; "±3 pp" had no justification | Every gate now states **quantity, unit, computation split, threshold and decision rule.** Fit on **days 1–7**, scored on **held-out days 8–14**. P90 gated on the **bootstrap CI upper bound**, not a point estimate — stricter, and it cannot be chosen after seeing the answer |
| **B8** | Demo arithmetic: the **3-minute variant summed to 150 s**, and the 15 s failure rule pushed the worst case to **4:45** | Re-timed to exactly **180 s**; the 15 s is drawn from beat 0's allocation, so the worst case is **4:30** |
| **B9** | **Unknown #4 had no owner, no date, and its favourable branch was silently assumed** | All **seven** unknowns now carry **owner + date + resolution path**. Unknowns **#6 (booked share)** and **#7 (does the audit compress too?)** are **new** — both were previously assumed rather than unknown |
| **B10** | The **Relevance** cell was self-refuting: it sold "we find your survey wrong" while conceding we don't know why it compresses | Restated honestly: **the instrument we would replace is not broken, and we do not know why it compresses waiting.** That is a weaker claim than v3 made and a survivable one |
| **B11** | **Two of eight sources could not be re-opened** (CAG unreachable; NAMCS HTTP 403) yet were listed as "verified primary" | Downgraded to **A\*** with a new **§5.7 source re-verification log**. Unsupported detail removed from asserted claims. **Nothing in the argument depends on either source** — the load-bearing claim now rests on LASI, which was read in full |

---

## 3. Minor findings — all fixed

| # | Finding | Fix |
|---|---|---|
| **m1** | "**measurably** failing to capture" — an unsupported intensifier doing rhetorical work | Removed |
| **m2** | Patient-side time described as "attributed to a cause" when a **non-arrival has no timeline to attribute minutes to** | Moved to OPD-level counts and rates; excluded from the additive reconciliation |
| **m3** | The Nigeria "4× longer" ratio was stated without its denominator | Restated as 51.4 min against 12.6 min of consultation — **4.08×** |
| **m4** | "Both are correct as reported" asserted more than the evidence supported | Softened to "both readings are consistent with the text" |
| **m5** | De et al. "all OPDs" could be read as all-day | Time-window caveat stated in §5.3 |
| **m6** | NSS 75th figures presented as current | **80th round (2025)** added: rural public share **35%** |

---

## 4. The generalisable lesson

**v3.1's verification pass checked citations. This review checked mechanisms.** Every one of the two fatal findings was invisible to citation-checking: the taxonomy was internally consistent, correctly sourced, and completely non-functional. The taxonomy claim survived three revisions because each revision checked that the words matched the table — never that the table covered the states a real patient passes through.

**Two standing rules adopted:**
1. **A partition claim must be provable by a test, not by a sentence.** §18.2 now requires a state-coverage test proving no state is unmapped. That test would have caught A1 immediately.
2. **A metric must name its numerator, its denominator, and the record that produces it.** "Idle clinical minutes" named none of the three. §7.2 now specifies all three.

**The honest summary for the team:** the deck's *evidence* was in good shape and its *engineering claims* were not. Anyone can check a citation in thirty seconds; almost nobody will build a state-coverage test in twenty-four hours. **We built the pitch and not the engine, then wrote as if we had both.** v4.0 closes the gap by making the document say only what the engine can support — and by shipping the test that proves it.

## 5. What actually ships (no CLI, no CSV repo)

The deliverable is **one runnable module, one import, and tests**: `cadence/cadence/taxonomy.py` (stdlib-only, `classify()` returns exactly one code, never None, never two), proven by `cadence/tests/test_taxonomy.py` (98,304-state coverage, all nine codes reachable, no dead codes) and `cadence/tests/test_toolchain.py`. There is **no CLI entry point** in the repo and **no CSV dataset** (no `.csv` files anywhere in `cadence/`); the day's token log feeds `classify()` directly in memory, and the demo's one live computation is BEAT 2 re-running the W1–W9 classification over that log. Nothing in the demo or the tests requires a command-line tool, an API, or a data download. Import and call — that is the whole surface.