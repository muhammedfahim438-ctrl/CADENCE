"""
CADENCE API — FastAPI backend for the OPD Waste Taxonomy dashboard.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cadence"))

from cadence.taxonomy import (
    PatientState,
    classify,
    explain,
    coverage_report,
    Code,
    LABELS,
    COVERED,
)

app = FastAPI(title="CADENCE API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ClassifyRequest(BaseModel):
    in_counter_queue: bool = False
    in_nursing_queue: bool = False
    in_consultation_queue: bool = False
    counters_open_idle: int = 0
    counters_busy: int = 0
    nurses_present_idle: int = 0
    nurses_busy: int = 0
    room_vacant: bool = False
    clinician_checked_in: bool = False
    clinician_with_another_patient: bool = False
    sent_to_diagnostics: bool = False
    diagnostics_return_recorded: bool = False
    diagnostics_returned_within_sla: bool = False
    clinically_finished: bool = False
    records_cleared: bool = False
    transition_missing: bool = False


class ClassifyResponse(BaseModel):
    code: Optional[str]
    label: Optional[str]
    explanation: str
    is_data_gap: bool


@app.get("/api/taxonomy")
def get_taxonomy():
    codes = []
    for code in Code:
        codes.append({
            "code": code.name,
            "value": code.value,
            "label": LABELS[code],
            "covered": code in COVERED,
        })
    return {"codes": codes}


@app.post("/api/classify", response_model=ClassifyResponse)
def post_classify(request: ClassifyRequest):
    state = PatientState(
        in_counter_queue=request.in_counter_queue,
        in_nursing_queue=request.in_nursing_queue,
        in_consultation_queue=request.in_consultation_queue,
        counters_open_idle=request.counters_open_idle,
        counters_busy=request.counters_busy,
        nurses_present_idle=request.nurses_present_idle,
        nurses_busy=request.nurses_busy,
        room_vacant=request.room_vacant,
        clinician_checked_in=request.clinician_checked_in,
        clinician_with_another_patient=request.clinician_with_another_patient,
        sent_to_diagnostics=request.sent_to_diagnostics,
        diagnostics_return_recorded=request.diagnostics_return_recorded,
        diagnostics_returned_within_sla=request.diagnostics_returned_within_sla,
        clinically_finished=request.clinically_finished,
        records_cleared=request.records_cleared,
        transition_missing=request.transition_missing,
    )

    result = classify(state)
    explanation = explain(state)

    if result is None:
        return ClassifyResponse(
            code=None,
            label=None,
            explanation=explanation,
            is_data_gap=True,
        )

    return ClassifyResponse(
        code=result.name,
        label=LABELS[result],
        explanation=explanation,
        is_data_gap=False,
    )


@app.get("/api/coverage")
def get_coverage():
    report = coverage_report()
    return {
        "total_coherent": report.total_coherent,
        "total_raw": report.total_raw,
        "observed": report.observed,
        "data_gaps": report.data_gaps,
        "coverage": report.coverage,
        "residual_share": report.residual_share,
        "counts": {k.name: v for k, v in report.counts.items()},
    }


@app.get("/health")
def health():
    return {"status": "ok"}
