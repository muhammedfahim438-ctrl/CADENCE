# TODOS — Member 4 (Delivery & Demo)

**Role:** Member 4
**Phase:** Build 1 — post-research
**Last updated:** 8 Oct 2026
**Repository:** https://github.com/muhammedfahim438-ctrl/CADENCE

---

## Status legend

- ☑ Done
- ◐ In progress
- ☐ Todo
- ⛔ Blocked / needs a decision

---

## Next up

| # | Task | GAP id | Why now |
|---|---|---|---|
| 1 | 8-beat deck rebuild | G3 | Judges comparing demo to spec find the structure itself is out of date |
| 2 | Seven-gate judge card | G4 | The most-quoted numbers on stage would be wrong two ways |
| 3 | Source card rewrite | G5 | A precise judge catches a citation error; credibility is one line away |
| 4 | v4.0 version banner sweep | G14 | A judge flips the footer and sees the wrong version |
| 5 | Pre-rendered video + offline LAN dup | — | Fail-safe for the live beat |
| 6 | Live-computation wire-up | G2 | Needs dev_A's runner; without it the "live" beat is a recording |
| 7 | Printed judge card + 3-min variant timing | — | Thresholds, unknowns, sources, regeneration command |

---

## Backlog

| # | Task | Spec anchor | GAP id | Status |
|---|---|---|---|---|
| 1 | 8-beat deck rebuild | §10 | G3 | ☐ |
| 2 | Seven-gate judge card | §6.4 | G4 | ☐ |
| 3 | Source card rewrite | §0.1, §5.3 | G5 | ☐ |
| 4 | v4.0 version banner sweep | — | G14 | ☐ |
| 5 | Pre-rendered video + offline dup | §10 | — | ☐ |
| 6 | Live-computation wire-up | §10 | G2 | ☐ |
| 7 | Printed judge card + 3-min variant | §10 | — | ☐ |

---

## Done

| Item | Evidence |
|---|---|
| Demo pack drafted | `DEMO_AND_JUDGE_PACK.md` — 7 beats, superseded by G3 rebuild |

---

## Blocked / needs a decision

| Item | Blocker | Needed from |
|---|---|---|
| Live-computation wire-up (G2) | Needs dev_A's live-classifier runner | dev_A |
| Pre-rendered video | Needs final deck (G3) | Self (after G3) |

---

## Standing rule

Every item will be presented on stage as either **implemented** (with a file:line), **specified** (B), or the exact sentence **"Not currently supported by the implementation."** No item crosses from "to build" to "built" inside a demo without a test run beside it.
