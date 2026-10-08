"""
The state-coverage proof.

This file exists because fatal finding A1 was invisible to reading. The v3.1
taxonomy was internally consistent, correctly sourced, and completely
non-functional — no code existed for queueing behind a busy clinician, and none
for the nursing station, while the document claimed every minute mapped to
exactly one cause.

Repository: https://github.com/muhammedfahim438-ctrl/CADENCE

A review pass that only checks that words match tables cannot find that. An
exhaustive enumeration can. These tests enumerate all 98,304 discrete states and
assert the taxonomy behaves.

The two properties that matter, stated precisely:

  EXHAUSTIVE  every coherent state classifies to exactly one code
  EXCLUSIVE   no state is claimed by two rules

And the property that catches over-correction in the other direction:

  REACHABLE   every code fires on at least one state, including W9

The last one matters. If W9 never fires, the residual is decorative and gate 4
is unfalsifiable — the same over-claim that A3 flagged, rebuilt. A residual you
cannot demonstrate is reachable is a residual you have quietly assumed away.
"""

from __future__ import annotations

from collections import Counter

import pytest

from cadence.taxonomy import (
    COVERED,
    Code,
    PatientState,
    classify,
    coverage_report,
    enumerate_states,
    explain,
)


# ----------------------------------------------------------------------
# The partition proof
# ----------------------------------------------------------------------


def test_exhaustive_every_coherent_observed_state_maps_to_exactly_one_code():
    """EXHAUSTIVE. The claim that was false in v3.1, now executable."""
    report = coverage_report()

    assert report.uncovered_coherent == (), (
        "these coherent states produced no classification, so the taxonomy does "
        f"not partition the timeline: {report.uncovered_coherent[:5]}"
    )
    assert sum(report.counts.values()) + report.data_gaps == report.total_coherent
    assert report.observed > 0


def test_residual_denominator_excludes_data_gaps():
    """W9 is measured against patients we watched, not patients we did not.

    Including gaps in the denominator would let missing instrumentation look like
    an honest residual, which is precisely the over-claim A3 flagged.
    """
    r = coverage_report()
    expected = r.counts[Code.W9] / r.observed
    assert abs(r.residual_share - expected) < 1e-12
    assert 0.0 < r.residual_share < 1.0
    assert r.coverage < 1.0, (
        "every in-scope state produced a row — if coverage is 100% the residual "
        "and the data-gap path are both decorative and the gates are theatre"
    )


def test_coherent_state_space_is_not_trivially_small():
    """Guard against the coverage test silently enumerating almost nothing."""
    report = coverage_report()
    assert report.total_coherent > 1_000, (
        f"only {report.total_coherent} coherent states enumerated — the coverage "
        "test is not exercising the space and proves nothing"
    )


def test_residual_fires_on_coherent_states():
    """W9 must be reachable from *coherent* states.

    A residual that only ever catches corrupt data is a data-quality metric, not
    a measured unknown. Genuine coverage gaps exist (a patient waiting on a
    transport or a pharmacy that no rule covers is physically coherent), and W9
    is where they land.
    """
    report = coverage_report()
    assert report.counts[Code.W9] > 0, (
        "W9 never fires on a coherent state — gate 4 (<2% of on-site minutes) "
        "would be unfalsifiable, which is fatal finding A3 rebuilt"
    )


@pytest.mark.parametrize("code", COVERED)
def test_every_declared_code_is_reachable(code: Code):
    """No dead codes. A code no state can produce is documentation, not design."""
    report = coverage_report()
    assert report.counts[code] > 0, (
        f"{code} is declared in the taxonomy but no enumerated state produces it"
    )


def test_pair_exclusivity():
    """EXCLUSIVE. Within each station the two codes cannot both apply.

    This is the property that makes 'W1 idle or W2 queue' a real dichotomy rather
    than a rhetorical one.
    """
    idle = PatientState(in_counter_queue=True, counters_open_idle=1, counters_busy=1)
    busy = PatientState(in_counter_queue=True, counters_open_idle=0, counters_busy=1)
    assert classify(idle) == Code.W1
    assert classify(busy) == Code.W2

    n_idle = PatientState(in_nursing_queue=True, nurses_present_idle=1, nurses_busy=1)
    n_busy = PatientState(in_nursing_queue=True, nurses_present_idle=0, nurses_busy=1)
    assert classify(n_idle) == Code.W3
    assert classify(n_busy) == Code.W4


# ----------------------------------------------------------------------
# The distinction v3.1 could not express — regression test for A1
# ----------------------------------------------------------------------


def test_busy_clinician_and_absent_clinician_are_different_codes():
    """The heart of A1.

    v3.1 had no way to express 'queueing behind a clinician who is busy' — the
    single most common waiting state and the one behind our own 85.71% headline.
    A taxonomy that cannot distinguish an absent clinician from a busy one cannot
    tell a hospital whether its problem is rostering or demand, which is the
    entire reason the ledger exists.
    """
    absent_no_room = PatientState(
        in_consultation_queue=True, room_vacant=True, clinician_checked_in=False
    )
    absent_not_checked_in = PatientState(
        in_consultation_queue=True, room_vacant=False, clinician_checked_in=False
    )
    busy = PatientState(
        in_consultation_queue=True,
        room_vacant=False,
        clinician_checked_in=True,
        clinician_with_another_patient=True,
    )

    assert classify(absent_no_room) == Code.W5
    assert classify(absent_not_checked_in) == Code.W5
    assert classify(busy) == Code.W6
    assert classify(absent_no_room) != classify(busy)


def test_nursing_station_is_instrumented():
    """The second half of A1: there was no nursing code at all."""
    assert (
        classify(
            PatientState(in_nursing_queue=True, nurses_present_idle=1, nurses_busy=1)
        )
        == Code.W3
    )
    assert (
        classify(
            PatientState(in_nursing_queue=True, nurses_present_idle=0, nurses_busy=2)
        )
        == Code.W4
    )


def test_patient_in_two_queues_is_a_data_gap_not_a_real_cause():
    """Corrupt data must not be silently bucketed as a genuine finding.

    This is stronger than routing corruption to W9. Filing "the log is
    self-contradictory" under *waste* would manufacture minutes we never observed
    and make the ledger's own total unfalsifiable. No ledger row is produced.
    """
    impossible = PatientState(in_counter_queue=True, in_consultation_queue=True)
    assert impossible.violations()
    assert classify(impossible) is None


def test_missing_transition_is_a_data_gap():
    """Integrity is checked before cause. We do not classify what we did not see."""
    lost = PatientState(in_consultation_queue=True, transition_missing=True)
    assert classify(lost) is None


def test_data_gap_and_residual_are_different_claims():
    """W9 and a data gap must never be conflated.

    W9 says: we watched this patient and cannot attribute the time.
    A gap says: we have no evidence about this patient at all.

    Reporting the second as the first would overstate how much we understand, and
    would quietly inflate the residual gate — which is the failure mode A3 named.
    """
    observed_but_unattributable = PatientState()
    assert classify(observed_but_unattributable) == Code.W9
    assert classify(PatientState(transition_missing=True)) is None


# ----------------------------------------------------------------------
# Data-quality routing
# ----------------------------------------------------------------------


def test_incoherent_states_produce_no_row_and_nothing_else():
    """Every impossible state yields a data gap. Nothing corrupt becomes a code."""
    leaked = Counter()
    for state in enumerate_states(only_coherent=False):
        if state.violations():
            leaked[classify(state)] += 1
    assert set(leaked) == {None}, (
        f"incoherent states were classified as real causes: "
        f"{ {str(c): n for c, n in leaked.items() if c is not None} }"
    )
    assert sum(leaked.values()) > 0, "no incoherent states were exercised at all"


def test_classification_never_raises():
    """The ledger must not be able to crash on unexpected input.

    A classifier that raises in production takes the transition log with it, and
    an unclassifiable minute is exactly the minute we most need to see.
    """
    for state in enumerate_states(only_coherent=False):
        classify(state)


# ----------------------------------------------------------------------
# Regression guards on the documented behaviours
# ----------------------------------------------------------------------


def test_documentation_and_diagnostics():
    assert classify(PatientState(clinically_finished=True, records_cleared=False)) == Code.W8
    # Return recorded but outside the SLA -> a real detour.
    assert (
        classify(
            PatientState(
                sent_to_diagnostics=True,
                diagnostics_return_recorded=True,
                diagnostics_returned_within_sla=False,
            )
        )
        == Code.W7
    )
    # Sent away and still not back: observed, but not attributable to a modelled
    # cause. That is W9, not a data gap — we *know* this patient is out at
    # imaging, we just cannot say how long. The data gap is losing the send
    # event entirely, which returns None.
    assert (
        classify(
            PatientState(
                sent_to_diagnostics=True,
                diagnostics_return_recorded=False,
                diagnostics_returned_within_sla=False,
            )
        )
        == Code.W9
    )
    # A return marked inside the SLA with no return event recorded is a genuine
    # contradiction and must never be accepted.
    contradictory = PatientState(
        sent_to_diagnostics=True,
        diagnostics_return_recorded=False,
        diagnostics_returned_within_sla=True,
    )
    assert contradictory.violations()
    assert classify(contradictory) is None
    # Returned in time and clinically fine -> no waste code applies.
    assert (
        classify(
            PatientState(
                sent_to_diagnostics=True,
                diagnostics_return_recorded=True,
                diagnostics_returned_within_sla=True,
                clinically_finished=True,
                records_cleared=True,
            )
        )
        == Code.W9
    )


def test_documentation_takes_precedence_over_station_queue():
    """A finished patient must not be re-counted as waiting in a queue.

    Ordering here is load-bearing: if station rules ran first, a patient cleared
    by records while a stale queue flag lingered would be double-counted as waste.

    The state is physically contradictory — queued at the counter and clinically
    finished — so it yields no ledger row at all. The property under test is that
    it is never reported as W1.
    """
    state = PatientState(
        in_counter_queue=True,
        counters_open_idle=1,
        counters_busy=1,
        clinically_finished=True,
        records_cleared=False,
    )
    assert state.violations()
    assert classify(state) != Code.W1
    assert classify(state) is None


def test_clean_documentation_state_is_w8_not_a_gap():
    """The ordering case that is actually reachable: finished, in no queue."""
    state = PatientState(clinically_finished=True, records_cleared=False, counters_busy=2)
    assert not state.violations()
    assert classify(state) == Code.W8


def test_explain_is_human_readable():
    s = PatientState(in_consultation_queue=True, clinician_checked_in=True,
                     clinician_with_another_patient=True)
    text = explain(s)
    assert "W6" in text and "another patient" in text