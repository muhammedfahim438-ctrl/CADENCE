# CADENCE

CADENCE is a hospital patient-flow triage taxonomy. It reads a day's token log
and assigns every patient exactly one wait-time code (W1-W9), with no CLI, no
API, and no data download required. Import and call - that is the whole surface.

## What ships

- `cadence/cadence/taxonomy.py` - the runnable module (stdlib-only). `classify()`
  returns exactly one code, never `None`, never two.
- `cadence/tests/test_taxonomy.py` - 98,304-state coverage; all nine codes
  reachable, no dead codes.
- `cadence/tests/test_toolchain.py` - toolchain guard.

## Run the tests

```bash
cd cadence
python -m pytest tests/ -v
```

Expected: all tests pass.

## Where everything lives

| Path | What it is |
|------|------------|
| `PROJECT_SOLUTION_FINAL.md` | v4.0 spec - the source of truth |
| `PROJECT_BIBLE.md` | project bible - rules that must never be broken |
| `TECH_STACK.md` | tech stack and constraints |
| `ADVERSARIAL_REVIEW_V4.md` | adversarial review of the v4.0 spec |
| `HACKATHON_JUDGE_QA.md` | judge Q&A |
| `HACKATHON_BUILD_GAPS.md` | known build gaps |
| `DEMO_AND_JUDGE_PACK.md` | demo + judge pack |
| `research/`, `dev_A/`, `dev_B/`, `member4/` | role work-defs and todos |

## Datasets

Raw CSV datasets are **not** in this repo. They are shared separately via the
**[v4.0-datasets release](https://github.com/muhammedfahim438-ctrl/CADENCE/releases/tag/v4.0-datasets)**.

Direct downloads:

- [healthcare_analytics_patient_flow_data.csv](https://github.com/muhammedfahim438-ctrl/CADENCE/releases/download/v4.0-datasets/healthcare_analytics_patient_flow_data.csv)
- [healthcare_noshows_appointments.csv](https://github.com/muhammedfahim438-ctrl/CADENCE/releases/download/v4.0-datasets/healthcare_noshows_appointments.csv)
- [hospital_sim_6_scenarios.csv](https://github.com/muhammedfahim438-ctrl/CADENCE/releases/download/v4.0-datasets/hospital_sim_6_scenarios.csv)
- [KaggleV2-May-2016.csv](https://github.com/muhammedfahim438-ctrl/CADENCE/releases/download/v4.0-datasets/KaggleV2-May-2016.csv)

The engine reads a day's token log in memory; nothing here requires a data
download.
