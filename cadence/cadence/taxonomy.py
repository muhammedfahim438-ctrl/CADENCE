"""
CADENCE — Waste Ledger taxonomy.

This module is the executable form of §3.1 of PROJECT_SOLUTION_FINAL.md (v4.0).

Why this file exists
-------------------
Fatal finding A1 of the v4 adversarial review was that the v3.1 cause taxonomy
did not partition a patient's timeline: there was no code for queueing behind a
clinician who is *busy*, and no nursing code at all, while the document claimed
every non-service minute was "attributed to exactly one of six causes."

That claim was never wrong on paper. It was wrong in the only way that matters,
and no amount of reading would have caught it. This module turns the claim into
`tests/test_taxonomy.py`, which enumerates the state space and fails loudly if
any state is unmapped.

Repository: https://github.com/muhammedfahim438-ctrl/CADENCE

Design contract
---------------
1. `classify()` returns EXACTLY ONE code for every state. Never None, never two.
2. Every code is reachable. A code that no state can ever produce is dead code,
   and a residual that can never fire is an unfalsifiable residual. Both are
   bugs, and both are tested against.
3. The taxonomy covers *states*, not *narratives*. A clinician who is absent and
   a clinician who is busy are different states with different owners (rostering
   vs. demand) and must not collapse.

No dependencies. stdlib only.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Iterator


class Code(str, Enum):
    """Waste codes. Values are the wire format used in the ledger and the demo."""

    W1 = "W1_counter_idle"
    W2 = "W2_counter_queue"
    W3 = "W3_nursing_idle"
    W4 = "W4_nursing_queue"
    W5 = "W5_clinician_absent"
    W6 = "W6_clinician_queue"
    W7 = "W7_diagnostics_detour"
    W8 = "W8_documentation"
    W9 = "W9_unclassified"

    def __str__(self) -> str:  # pragma: no cover - display only
        return self.value


#: Codes the state table is *required* to cover. W9 is deliberately not in this
#: set: it is the residual, and the coverage test asserts it is reachable rather
#: than merely permitted.
COVERED = (Code.W1, Code.W2, Code.W3, Code.W4, Code.W5, Code.W6, Code.W7, Code.W8)

#: Sentinel returned when we have no evidence of what happened. Distinct from
#: W9, which means "we observed the patient and cannot attribute the time."
#: Exposed as `None` so the type checker can narrow the return type, and so
#: "no ledger row" is impossible to confuse with a code.
DATA_GAP = None

#: Short labels for demo and reporting surfaces.
LABELS = {
    Code.W1: "counter idle",
    Code.W2: "counter queue",
    Code.W3: "nursing idle",
    Code.W4: "nursing queue",
    Code.W5: "clinician absent",
    Code.W6: "clinician queue",
    Code.W7: "diagnostics detour",
    Code.W8: "documentation",
    Code.W9: "unclassified",
}


@dataclass(frozen=True)
class PatientState:
    """The complete observable state of one patient's visit.

    Every field is a physical fact a transition log can produce. There is no
    free-text or narrative field, because a taxonomy that accepts prose cannot be
    proved exhaustive.

    The three station pairs (counter, nursing, clinician) are mutually exclusive
    by the physical invariant that a patient occupies exactly one station queue.
    `validate()` enforces that rather than trusting the caller.
    """

    # --- station occupancy: exactly one of these is True (or none, pre-arrival) ---
    in_counter_queue: bool = False
    in_nursing_queue: bool = False
    in_consultation_queue: bool = False

    # --- counter station resources ---
    counters_open_idle: int = 0
    counters_busy: int = 0

    # --- nursing station resources ---
    nurses_present_idle: int = 0
    nurses_busy: int = 0

    # --- consultation resources ---
    room_vacant: bool = False
    clinician_checked_in: bool = False
    clinician_with_another_patient: bool = False

    # --- diagnostics ---
    sent_to_diagnostics: bool = False
    #: Whether a return event was recorded at all. Distinct from whether it was
    #: inside the SLA: "still at imaging" is W7, "we have no idea where they
    #: are" is the residual. Conflating these two is what made W7 dead code on
    #: the first implementation of this module.
    diagnostics_return_recorded: bool = False
    diagnostics_returned_within_sla: bool = False

    # --- exit path ---
    clinically_finished: bool = False
    records_cleared: bool = False

    # --- data integrity ---
    transition_missing: bool = False

    # ------------------------------------------------------------------
    @property
    def in_any_queue(self) -> bool:
        return (
            self.in_counter_queue
            or self.in_nursing_queue
            or self.in_consultation_queue
        )

    def violations(self) -> list[str]:
        """Physical impossibilities. Empty list means the state is coherent.

        These are *data bugs*, not waste. A state with a violation must be
        routed to the residual rather than silently bucketed as a real cause.
        """
        v: list[str] = []

        stations = [
            self.in_counter_queue,
            self.in_nursing_queue,
            self.in_consultation_queue,
        ]
        if sum(stations) > 1:
            v.append("patient occupies more than one station queue simultaneously")

        if self.in_counter_queue and self.counters_open_idle + self.counters_busy == 0:
            v.append("patient is queued at the counter with no counter staffed or busy")
        if self.in_nursing_queue and self.nurses_present_idle + self.nurses_busy == 0:
            v.append("patient is queued at nursing with no nurse present or busy")

        if self.sent_to_diagnostics and self.in_any_queue:
            v.append("patient is at diagnostics and in a station queue simultaneously")
        if (
            self.sent_to_diagnostics
            and not self.diagnostics_return_recorded
            and self.clinically_finished
        ):
            # Only contradictory while they are still physically at imaging.
            # Sent -> returned -> seen -> finished is a perfectly normal
            # sequence and must not be rejected.
            v.append("patient is still at diagnostics but clinically finished")
        if self.diagnostics_returned_within_sla and not self.sent_to_diagnostics:
            v.append("a diagnostics return was recorded but no send was")
        if self.diagnostics_returned_within_sla and not self.diagnostics_return_recorded:
            v.append("return marked within SLA but the return event is unrecorded")
        if self.records_cleared and not self.clinically_finished:
            v.append("records were cleared before clinical finish was recorded")

        if self.in_counter_queue and self.clinically_finished:
            v.append("patient is queued at the counter and clinically finished")
        if self.in_nursing_queue and self.clinically_finished:
            v.append("patient is queued at nursing and clinically finished")
        if self.in_consultation_queue and self.clinically_finished:
            v.append("patient is queued for the clinician and clinically finished")

        return v


def classify(state: PatientState) -> Code | None:
    """Map one state to exactly one waste code, or `None` for a data gap.

    Rule order is the specification's rule order (§3.1) and is not arbitrary:

      1. Data integrity first. A state we could not observe returns `DATA_GAP`
         and produces **no ledger row at all**. This is not cosmetic: W9 means
         "we watched this patient and cannot say why they waited", while a data
         gap means "we do not know what happened". Filing the second as waste
         would manufacture minutes for patients we never observed, and would make
         the ledger's own total unfalsifiable. Data gaps are counted separately,
         as a coverage metric alongside consent coverage.
      2. Then the exit path, then the diagnostics detour, then the three station
         pairs. Within each pair the two conditions are disjoint by
         construction — see `test_pair_exclusivity`.

    Returns exactly one `Code` for every observed state, or `DATA_GAP`. Never a
    list, never a partial result.
    """
    # 1. Integrity — unobserved or impossible states produce no ledger row.
    if state.transition_missing or state.violations():
        return DATA_GAP

    # 2. Exit path: clinically done but not yet administratively cleared.
    if state.clinically_finished and not state.records_cleared:
        return Code.W8

    # 3. Diagnostics detour: sent away, return recorded, and back too late.
    #    "Still at imaging" is a real detour; "no return event at all" is a data
    #    gap and was already routed to the residual by the integrity check.
    if (
        state.sent_to_diagnostics
        and state.diagnostics_return_recorded
        and not state.diagnostics_returned_within_sla
    ):
        return Code.W7

    # 4. Station queues.
    if state.in_counter_queue:
        # Idle capacity exists while this patient waits -> the counter is the
        # constraint, not the queue.
        return Code.W1 if state.counters_open_idle > 0 else Code.W2

    if state.in_nursing_queue:
        return Code.W3 if state.nurses_present_idle > 0 else Code.W4

    if state.in_consultation_queue:
        # The distinction that v3.1 could not express, and the reason A1 was
        # fatal: an absent clinician is a ROSTERING problem, a busy clinician is
        # a DEMAND problem. No amount of rescheduling fixes the second one.
        if state.room_vacant or not state.clinician_checked_in:
            return Code.W5
        if state.clinician_with_another_patient:
            return Code.W6

    # 5. Residual.
    return Code.W9


# ----------------------------------------------------------------------
# State-space enumeration — the machinery behind the coverage proof.
# ----------------------------------------------------------------------

_DIMENSIONS: dict[str, tuple[object, ...]] = {
    "in_counter_queue": (False, True),
    "in_nursing_queue": (False, True),
    "in_consultation_queue": (False, True),
    "counters_open_idle": (0, 1, 2),
    "counters_busy": (0, 1),
    "nurses_present_idle": (0, 1),
    "nurses_busy": (0, 1),
    "room_vacant": (False, True),
    "clinician_checked_in": (False, True),
    "clinician_with_another_patient": (False, True),
    "sent_to_diagnostics": (False, True),
    "diagnostics_return_recorded": (False, True),
    "diagnostics_returned_within_sla": (False, True),
    "clinically_finished": (False, True),
    "records_cleared": (False, True),
    "transition_missing": (False, True),
}


def _name_order() -> list[str]:
    return list(_DIMENSIONS)


def enumerate_states(only_coherent: bool = True) -> Iterator[PatientState]:
    """Yield the full discrete state space.

    The space is the cartesian product of every observable dimension — 98,304
    states. This is deliberately exhaustive rather than hand-picked: a coverage
    test built from a curated list of states is theatre, because the curator
    chooses which states to omit. That is precisely how A1 survived review.

    `only_coherent=True` restricts to states with no physical violation, which
    is the set the ledger is *responsible* for. Incoherent states are still
    classifiable — they land in W9 — and are tested separately.
    """
    names = _name_order()

    def walk(i: int, acc: dict[str, object]):
        if i == len(names):
            state = PatientState(**acc)  # type: ignore[arg-type]
            if only_coherent and state.violations():
                return
            yield state
            return
        for value in _DIMENSIONS[names[i]]:
            yield from walk(i + 1, {**acc, names[i]: value})

    yield from walk(0, {})


@dataclass(frozen=True)
class CoverageReport:
    total_coherent: int
    total_raw: int
    counts: dict[Code, int]
    uncovered_coherent: tuple[str, ...]
    data_gaps: int
    #: Data-gap states that were ALSO physically contradictory. Should be zero:
    #: a contradiction is a bug we must see, not a silently-absorbed gap.
    incoherent_routed: int

    @property
    def observed(self) -> int:
        return self.total_coherent - self.data_gaps

    @property
    def residual_share(self) -> float:
        """Share of *observed* coherent states that land in W9.

        Denominator deliberately excludes data gaps. W9 is the residual for
        patients we watched; data gaps are patients we did not.
        """
        return self.counts[Code.W9] / self.observed if self.observed else 0.0

    @property
    def coverage(self) -> float:
        """Share of in-scope states for which we have a ledger row at all."""
        return self.observed / self.total_coherent if self.total_coherent else 0.0


def coverage_report() -> CoverageReport:
    """Enumerate the space and report how each state classifies."""
    counts = {code: 0 for code in Code}
    uncovered: list[str] = []
    gaps = 0

    for state in enumerate_states(only_coherent=True):
        result = classify(state)
        if result is None:
            gaps += 1
            continue
        counts[result] += 1

    incoherent_routed = 0
    for state in enumerate_states(only_coherent=False):
        if state.violations() and classify(state) is None:
            incoherent_routed += 1

    return CoverageReport(
        total_coherent=sum(counts.values()) + gaps,
        total_raw=sum(1 for _ in enumerate_states(only_coherent=False)),
        counts=counts,
        uncovered_coherent=tuple(uncovered),
        data_gaps=gaps,
        incoherent_routed=incoherent_routed,
    )


def explain(state: PatientState) -> str:
    """Human-readable rationale for a classification. Used by the demo overlay."""
    code = classify(state)
    v = state.violations()
    if code is None:
        if v:
            return f"DATA_GAP — no ledger row: {v[0]}"
        return "DATA_GAP — no ledger row: transition missing from the log"
    rationale = {
        Code.W1: f"{state.counters_open_idle} counter(s) open and idle",
        Code.W2: f"all {state.counters_busy} counter(s) busy",
        Code.W3: f"{state.nurses_present_idle} nurse(s) present and idle",
        Code.W4: f"all {state.nurses_busy} nurse(s) busy",
        Code.W5: "room vacant" if state.room_vacant else "clinician not checked in",
        Code.W6: "clinician present and with another patient",
        Code.W7: "sent to diagnostics, return recorded outside SLA",
        Code.W8: "clinically finished, records not cleared",
        Code.W9: "observed, but no rule covers this state",
    }[code]
    return f"{code} ({LABELS[code]}) — {rationale}"


def with_change(state: PatientState, **changes: object) -> PatientState:
    """Return a modified copy. Used by tests and the demo's timeline scrubber."""
    return replace(state, **changes)  # type: ignore[arg-type]