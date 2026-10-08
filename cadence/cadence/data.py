"""Seeded synthetic token generator — stdlib-only, no CLI, no CSV repo."""

from dataclasses import dataclass, field
from random import Random
from typing import Iterator

from cadence.cadence.taxonomy import classify, PatientState


# --- Parameter record for provenance ---
@dataclass(frozen=True)
class GenerationParams:
    """Parameters governing the synthetic token log generation."""
    arrival_rate_per_hour: float        # patients per hour (OPD rate)
    service_time_counter: float         # mean counter service time (minutes)
    service_time_nursing: float         # mean nursing service time (minutes)
    service_time_consult: float         # mean clinician service time (minutes)
    n_counters: int                     # number of counter stations
    nurses_per_counter: int             # nurses assigned per counter


# --- Token log type ---
TokenEvent = dict[str, object]


def generate(seed: int = 20261003, days: int = 14, blocks: int = 1) -> list[TokenEvent]:
    """Generate a deterministic token log for `days` days, `blocks` OPD blocks.

    The log is a list of token-event dicts, each with:
        - 'timestamp': minutes from day start
        - 'state': PatientState at that moment
        - 'code': waste code (W1..W9) from classify(), or CODE_GAP
    Same seed => identical log (deterministic).
    """
    params = _default_params()
    rng = Random(seed)

    total_minutes = days * 24 * 60
    log: list[TokenEvent] = []

    # Simulate one OPD block per day (e.g. 8-hour session = 480 min)
    block_minutes = 240  # 4-hour block; adjust per spec
    for day in range(days):
        for minute in range(0, min(block_minutes, 24 * 60), 15):
            # Arrival: new patient every ~1/arrival_rate hours
            if rng.random() < params.arrival_rate_per_hour / 60.0:
                # Generate a PatientState with some stochastic transitions
                state = _random_state(rng, params)
                code = classify(state)
                log.append({
                    'timestamp': day * block_minutes + minute,
                    'state': state,
                    'code': code,
                })

    return log


def _default_params() -> GenerationParams:
    """Default parameter set based on typical OPD workloads."""
    return GenerationParams(
        arrival_rate_per_hour=3.0,       # ~3 patients/hour
        service_time_counter=12.0,       # mean 12 min per counter visit
        service_time_nursing=8.0,        # mean 8 min per nursing interaction
        service_time_consult=18.0,       # mean 18 min per clinician visit
        n_counters=3,
        nurses_per_counter=1,
    )


def _random_state(rng: Random, params: GenerationParams) -> PatientState:
    """Generate a coherent PatientState using the parameter record.

    Ensures physical invariants so that classify() returns a Code (not None).
    Exactly one of {in_counter_queue, in_nursing_queue, in_consultation_queue}
    may be True (or none, pre-arrival).
    """
    # Default: patient has not arrived yet (all defaults = False/zero)
    in_counter_queue = False
    in_nursing_queue = False
    in_consultation_queue = False

    counters_open_idle = params.n_counters
    counters_busy = 0

    nurses_present_idle = params.nurses_per_counter
    nurses_busy = 0

    room_vacant = bool(rng.getrandbits(1))
    clinician_checked_in = bool(rng.getrandbits(1))
    clinician_with_another_patient = bool(rng.getrandbits(1))

    sent_to_diagnostics = bool(rng.getrandbits(1))
    diagnostics_return_recorded = bool(rng.getrandbits(1)) if sent_to_diagnostics else False
    diagnostics_returned_within_sla = bool(rng.getrandbits(1)) if (sent_to_diagnostics and diagnostics_return_recorded) else False

    clinically_finished = bool(rng.getrandbits(1))
    records_cleared = bool(rng.getrandbits(1)) if clinically_finished else False
    transition_missing = bool(rng.getrandbits(1))

    # Enforce physical invariants so classify() returns a Code:
    # Exactly one station queue may be True (or none, pre-arrival).
    queue_total = in_counter_queue + in_nursing_queue + in_consultation_queue
    if queue_total > 1:
        # Route to residual: patient cannot occupy multiple queues
        in_counter_queue = in_nursing_queue = in_consultation_queue = False

    if in_counter_queue and counters_open_idle + counters_busy == 0:
        # Patient queued at counter with no staff → residual
        in_counter_queue = False

    if in_nursing_queue and nurses_present_idle + nurses_busy == 0:
        # Patient queued at nursing with no nurse → residual
        in_nursing_queue = False

    return PatientState(
        in_counter_queue=in_counter_queue,
        in_nursing_queue=in_nursing_queue,
        in_consultation_queue=in_consultation_queue,
        counters_open_idle=counters_open_idle,
        counters_busy=counters_busy,
        nurses_present_idle=nurses_present_idle,
        nurses_busy=nurses_busy,
        room_vacant=room_vacant,
        clinician_checked_in=clinician_checked_in,
        clinician_with_another_patient=clinician_with_another_patient,
        sent_to_diagnostics=sent_to_diagnostics,
        diagnostics_return_recorded=diagnostics_return_recorded,
        diagnostics_returned_within_sla=diagnostics_returned_within_sla,
        clinically_finished=clinically_finished,
        records_cleared=records_cleared,
        transition_missing=transition_missing,
    )


def provenance_sheet(params: GenerationParams, seed: int, days: int, blocks: int) -> str:
    """Print the provenance sheet overlaid on the demo display.

    Returns a string like:
        seed=20261003 · 14 days · 1 OPD block · SYNTHETIC
    with parameter ranges printed below.
    """
    lines = [
        f"seed={seed} · {days} days · {blocks} OPD block · SYNTHETIC",
        "",
        "Generation parameters:",
        f"  - Arrival rate: {params.arrival_rate_per_hour} patients/hour",
        f"  - Counter service time: {params.service_time_counter} min (mean)",
        f"  - Nursing service time: {params.service_time_nursing} min (mean)",
        f"  - Clinician service time: {params.service_time_consult} min (mean)",
        f"  - Counters: {params.n_counters}, Nurses per counter: {params.nurses_per_counter}",
        "",
        "This is synthetic data — not real hospital data.",
    ]
    return "\n".join(lines)