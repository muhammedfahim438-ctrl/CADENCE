# WORK_DEF — Dev A (Token Machinery & Tooling)

**Role:** Developer A
**Phase:** Build 1 — post-research
**Last updated:** 8 Oct 2026
**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE

---

## Mission

Build the provable core — the taxonomy, the seeded generator, and the honest "show me the code" surfaces — so that the Waste Ledger is reproducible, testable, and never a black box.

---

## In-scope responsibilities

1. **Taxonomy maintenance** — `cadence/cadence/taxonomy.py` is stdlib-only. `classify()` returns exactly one code for every state. Never `None`, never two. W1–W9 exhaustive, exclusive, reachable.
2. **Seeded synthetic generator** (G1) — deterministic `generate()` behind `seed=20261003`, 14 days, 1 OPD block, with a printed provenance sheet and public regeneration command.
3. **Live-classifier runner** (G2) — wires `classify()` / `explain()` / `with_change()` to the demo slide; 15 s watchdog → labelled pre-rendered video; 3-min variant.
4. **Provider fields P1/P2/P3** (G9) — add provider-occupancy dimensions to `PatientState` + `_DIMENSIONS` + coverage counts.
5. **Coverage-report entrypoint** (G7) — `coverage_report()` exists in `taxonomy.py:331`; the `python -m cadence.report` entrypoint / script claim is missing. **Decision needed:** reconcile with ADVERSARIAL §5 "no CLI" before building.
6. **Packaging** (G8) — minimal `pyproject.toml` + test config so `python -m pytest` works from repo root (currently only works from `cadence/`).

---

## Out of scope

- Models, twin, RSR (dev_B owns those).
- Deck, judge cards, demo video (member4 owns those).
- Clinical logic, triage, severity — never.
- Editing the canonical spec.

---

## Definition of Done

| Responsibility | DoD |
|---|---|
| Taxonomy | 25/25 tests pass; stdlib-only; W9 reachable; no dead codes |
| Generator (G1) | `generate(seed=20261003)` produces 14-day token log; provenance sheet printed; regeneration command public |
| Live runner (G2) | Steps `PatientState`s → prints `explain()` overlay; 15 s watchdog → pre-rendered video; 3-min variant |
| Provider fields (G9) | P1/P2/P3 dimensions in `_DIMENSIONS`; coverage counts include provider series |
| Report entrypoint (G7) | `python -m cadence.report` prints coverage; **only after** no-CLI tension resolved |
| Packaging (G8) | `python -m pytest` from repo root → 25 pass |

---

## Handoffs

| Direction | What | To/From |
|---|---|---|
| → | Generator + taxonomy | dev_B (twin/models consume) |
| → | Live runner | member4 (live demo beat) |
| → | Test results | research (claims audit) |
| ← | Gate harness spec | dev_B |
| ← | No-CLI decision | research / team |

---

## Guardrails

- **Stdlib-only taxonomy.** No third-party imports in `taxonomy.py`. Models may use pandas/numpy/sklearn; the ledger may not.
- **No dead codes.** Every code fires on at least one state. If W9 never fires, the residual is decorative and gate 4 is unfalsifiable.
- **W5 ≠ W6.** Clinician absent ≠ clinician busy. Fatal A1 must never regress.
- **Data gaps yield no ledger row.** A gap is not waste; it is a gap.
- **Append-only, timestamped at edge.** Transitions are not back-datable.
- **No clinical function.** No diagnosis, triage, severity, or condition inference.

---

## References

- `PROJECT_SOLUTION_FINAL.md` v4.0 — §3.1 taxonomy, §18 build checklist
- `TECH_STACK.md` — §1 runtime, §3 Engine 1
- `HACKATHON_BUILD_GAPS.md` — G1, G2, G7, G8, G9
- `cadence/cadence/taxonomy.py` — executable core
- `cadence/tests/test_taxonomy.py` — 98,304-state coverage proof
- `ADVERSARIAL_REVIEW_V4.md` §5 — no-CLI/no-CSV tension
