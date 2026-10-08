import random
import sys
from pathlib import Path

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "cadence" / "cadence"))

from taxonomy import PatientState, classify, coverage_report, explain


@api_view(["POST"])
def classify_patient_state(request):
    try:
        state = PatientState(**request.data)
    except TypeError as e:
        return Response(
            {"error": f"Invalid PatientState fields: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    code = classify(state)
    explanation = explain(state)

    return Response(
        {
            "code": code.value if code else None,
            "label": code.name if code else "DATA_GAP",
            "explanation": explanation,
        }
    )


@api_view(["GET"])
def coverage(request):
    report = coverage_report()

    return Response(
        {
            "total_coherent": report.total_coherent,
            "total_raw": report.total_raw,
            "observed": report.observed,
            "data_gaps": report.data_gaps,
            "incoherent_routed": report.incoherent_routed,
            "coverage": report.coverage,
            "residual_share": report.residual_share,
            "counts": {code.value: count for code, count in report.counts.items()},
        }
    )


@api_view(["GET"])
def generate(request):
    seed = request.query_params.get("seed")
    if seed is not None:
        try:
            seed = int(seed)
        except ValueError:
            return Response(
                {"error": "Seed must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        seed = 42

    rng = random.Random(seed)

    states = []
    for _ in range(10):
        state = PatientState(
            in_counter_queue=rng.choice([True, False]),
            in_nursing_queue=rng.choice([True, False]),
            in_consultation_queue=rng.choice([True, False]),
            counters_open_idle=rng.randint(0, 2),
            counters_busy=rng.randint(0, 1),
            nurses_present_idle=rng.randint(0, 1),
            nurses_busy=rng.randint(0, 1),
            room_vacant=rng.choice([True, False]),
            clinician_checked_in=rng.choice([True, False]),
            clinician_with_another_patient=rng.choice([True, False]),
            sent_to_diagnostics=rng.choice([True, False]),
            diagnostics_return_recorded=rng.choice([True, False]),
            diagnostics_returned_within_sla=rng.choice([True, False]),
            clinically_finished=rng.choice([True, False]),
            records_cleared=rng.choice([True, False]),
            transition_missing=rng.choice([True, False]),
        )
        code = classify(state)
        states.append(
            {
                "state": {
                    "in_counter_queue": state.in_counter_queue,
                    "in_nursing_queue": state.in_nursing_queue,
                    "in_consultation_queue": state.in_consultation_queue,
                    "counters_open_idle": state.counters_open_idle,
                    "counters_busy": state.counters_busy,
                    "nurses_present_idle": state.nurses_present_idle,
                    "nurses_busy": state.nurses_busy,
                    "room_vacant": state.room_vacant,
                    "clinician_checked_in": state.clinician_checked_in,
                    "clinician_with_another_patient": state.clinician_with_another_patient,
                    "sent_to_diagnostics": state.sent_to_diagnostics,
                    "diagnostics_return_recorded": state.diagnostics_return_recorded,
                    "diagnostics_returned_within_sla": state.diagnostics_returned_within_sla,
                    "clinically_finished": state.clinically_finished,
                    "records_cleared": state.records_cleared,
                    "transition_missing": state.transition_missing,
                },
                "code": code.value if code else None,
                "explanation": explain(state),
            }
        )

    return Response({"seed": seed, "states": states})
