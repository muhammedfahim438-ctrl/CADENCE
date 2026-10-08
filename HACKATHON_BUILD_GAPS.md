# HACKATHON_BUILD_GAPS — Pre-Demo Build Backlog (priority-ordered)

**Companion to:** `HACKATHON_JUDGE_QA.md` (the audit workbook) and `PROJECT_SOLUTION_FINAL.md` v4.0 (canonical spec).
**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE
**Rule of the file:** every line names a gap, the spec it belongs to, the evidence that proves it open, the cost to close, and what the demo loses if it stays open. Nothing here is code that has been written — this is the honest to-do between today and stage.

Read top-down: **P0 = blocks the demo's core honesty move**, **P1 = materially improves a judge's verdict**, **P2 = deliberate non-builds, named so nobody wastes time across them.**

---

## P0 · Blocks the demo's core honesty move

| # | Gap | Spec anchor | Evidence it is open | What closes it | Demo impact if left open |
|---|---|---|---|---|---|
| G1 | **Synthetic-token generator** | §4.4, §10 | Seeds + parameter sets exist only inside the temp audit script; no module produces a seeded token log | A deterministic `generate()` behind a seed + parameter record (arrival rates, service times, counter profile), printing the seed overlay the demo displays | The demo's "live numbers" have no honest provenance; the "reproducible synthetic" claim collapses |
| G2 | **Live-classifier runner** | §10 (one genuinely live computation; 15s fail-safe to pre-rendered video) | No runner wires `classify()`/`explain()`/`with_change()` to the slide; no fail-safe exists | A thin runner: step/type sample `PatientState`s → print `explain()` overlay; 15s watchdog → labelled pre-rendered video; 3-min variant | The single "live" beat we promise (beat 2) would be a recording, silently — the honesty story breaks at its best moment |
| G3 | **8-beat demo retime** | §10 windows (beat 0 0:00–0:12 … beat 7 4:05–4:30) | `DEMO_AND_JUDGE_PACK.md` has 7 beats, no beat 0, and mismatched timings | Rebuild the deck to the 8 specified beats with the per-beat windows and SIMULATED labels | Judges comparing demo to spec find the structure itself is out of date |
| G4 | **Corrected gate card** | §6.4 (seven gates) vs `§10` beat 7 ("six") | Spec internally disagrees; demo/judge card say "four thresholds" | Print the seven-gate card (median<20, P90<30, ±3pp, W9<2%+coverage, stage-order<1%, short-idle<10%, first-tap P95<10min) everywhere; flag the §10 "six" line in the sync log | The most-quoted numbers on stage would be wrong two ways |
| G5 | **Corrected source card** | §0.1, §5.3 B1, ADVERSARIAL source table | Demo pack: CAG "Chapter IV" (→III), LASI "best domain" (→worst, 4.6%), Kemdirim "2022" (→2021), "87.30% walk-ins" (→ visited directly) | Rewrite the judge-card sources block verbatim per the QA file §17 row 2 + §25 item 9 | A precise judge catches a citation error; the entire "we read the sources" credibility is a one-line error away |
| G6 | **Docstring truth fix** | — | `taxonomy.py:275`, `test_taxonomy.py:11`: "32,768" vs computed 98,304 | Doc-only edit, both files (`_DIMENSIONS` at `taxonomy.py:252` is the authority) | The find-your-own-bug move is currently a trap only we know about — announce it first (§22 F, row 3) |

## P1 · Materially improves a judge's verdict

| # | Gap | Spec anchor | Evidence it is open | What closes it | Demo impact if left open |
|---|---|---|---|---|---|
| G7 | **Coverage-report CLI/script checked into the repo** | §3.1 | The numbers (98,304 / 6,976 / 3,488 / W1=256 … W9=1392 / coverage 0.5) are produced by a temp script, not a repo command | A `coverage_report()` print entrypoint (e.g., `python -m cadence.report`) | "Show me the code" has no one-command answer |
| G8 | **Pyproject / package packaging** (tests from repo root) | — | `pytest` from `D:\HACKKKKKK\cadence` = 25 pass; from repo root = ModuleNotFoundError | Minimal packaging + test config so `python -m pytest` works repo-wide | The bluntest possible "does it even run" probe scores a maybe |
| G9 | **P1/P2/P3 provider fields in code** | §3.1 (provider ledger) | Code carries only the patient-side flags | Add the provider-occupancy dimensions to `PatientState` + `_DIMENSIONS` + coverage counts | "Where is the provider ledger?" has no cell in the show-me-the-code matrix |
| G10 | **Gate harness (seven thresholds, held-out days)** | §6.4, §11.1 | No harness; the §10 demo prints gates from a static card | A harness that reads a held-out ledger and prints pass/fail vs the seven thresholds — even offline with synthetic held-out data | "What gate has actually passed?" stays a coverage-only story (fine, but a harness makes the answer concrete) |
| G11 | **MIS export schema** | §4.1 | No export surface at all | A documented CSV/JSON export of the ledger (codes, providers, coverage) — export can stay simulated | Downstream "what does the hospital export" is vague |
| G12 | **No-show decision-record lane** | §13.2 | Wording only in spec | A small notion of "computed once, append-only, never displayed/exported/joined" made concrete (even as a labelled demo fixture) | The corrected Q3 answer has no artefact behind it |
| G13 | **Twin + RSR net_value fixture** | §3.2, §3.3, §7.1 | Not built | A deterministic priced-counterfactual fixture (ledger → net_value → veto) powering demo beats 3–5, labelled SIMULATED | Beats 3–5 must otherwise be pure narration |
| G14 | **Version banner sweep** | — | Demo pack header/footer say "v2"; spec is v4.0 | Sweep every deck/QA/card to v4.0 | A judge flips the footer and sees the wrong version |
| G15 | **Test-from-root note in README/gaps** | — | The 25/25 result is folder-dependent | Document `cd cadence && python -m pytest tests -q` with the note that root-folder packaging is G8 | The "25 tests" claim needs its one-line repro on stage |

## P2 · Deliberate non-builds (read twice before adding anything here)

| # | Non-build | Spec anchor | Why it stays a non-build |
|---|---|---|---|
| G16 | No clinical triage / severity / diagnosis layer | §12.1, §6.5 | The no-triage boundary is the project's ethics spine; building even a "demo severity" invites the one question that kills us ("does it prioritise patients?") |
| G17 | No cloud / SaaS control plane | §0 scope, §4 EDGE | One hospital, one OPD, LAN appliance. A demo of scaling is a demo of scope-creep |
| G18 | No EHR / ABDM / ABHA write-back | §14.1 | MVP runs on paper token; write-back is a later lane precisely because ABDM onboarding is not universal |
| G19 | No benchmarking by default | §8 | Opt-in only; "departments compete" draws competitive-pressure criticism we do not need |
| G20 | No cross-hospital "AI" training | §11.1 | We do not train a model on another hospital's OPD to predict this one — methodologically wrong, and states it loudly |

## Flagged-but-not-touched (out of scope for build; noted for the team)

- `.slides/` — stale stack logos and any deck tooling there predate v4.0; flagged, not edited (deck rebuild is G3's job).
- `opencode.json` — the PowerPoint MCP binding is an editor-affordance file, not project code; no action.
- `PROJECT_SOLUTION_FINAL.md` — canonical. It is the *authority*, not a build artefact; the §10 "six gates" line is logged in the demo sync, not edited here.

## Standing rule for the whole backlog

Every P0/P1 item will be presented on stage as either **implemented** (with a file:line), **specified** (B), or the exact sentence **"Not currently supported by the implementation."** The unconditional thing: no item above ever crosses from "to build" to "built" inside a demo without a test run beside it.