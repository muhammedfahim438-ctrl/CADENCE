"use client";

import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const W_CODES = [
  { code: "W1", label: "Counter idle", desc: "Patient waiting at counter, no counter staff available" },
  { code: "W2", label: "Counter queue", desc: "Patient queued at counter with staff busy" },
  { code: "W3", label: "Nursing idle", desc: "Patient waiting at nursing station, no nurse available" },
  { code: "W4", label: "Nursing queue", desc: "Patient queued at nursing station with nurses busy" },
  { code: "W5", label: "Clinician absent", desc: "Patient waiting, clinician not checked in" },
  { code: "W6", label: "Clinician queue", desc: "Patient queued, clinician with another patient" },
  { code: "W7", label: "Diagnostics detour", desc: "Patient sent to diagnostics, return not recorded" },
  { code: "W8", label: "Documentation", desc: "Patient waiting for records to be cleared" },
  { code: "W9", label: "Unclassified", desc: "Residual — observed but cannot attribute" },
];

interface PatientState {
  in_counter_queue: boolean;
  in_nursing_queue: boolean;
  in_consultation_queue: boolean;
  counters_open_idle: number;
  counters_busy: number;
  nurses_present_idle: number;
  nurses_busy: number;
  room_vacant: boolean;
  clinician_checked_in: boolean;
  clinician_with_another_patient: boolean;
  sent_to_diagnostics: boolean;
  diagnostics_return_recorded: boolean;
  diagnostics_returned_within_sla: boolean;
  clinically_finished: boolean;
  records_cleared: boolean;
  transition_missing: boolean;
}

const defaultState: PatientState = {
  in_counter_queue: false,
  in_nursing_queue: false,
  in_consultation_queue: false,
  counters_open_idle: 0,
  counters_busy: 0,
  nurses_present_idle: 0,
  nurses_busy: 0,
  room_vacant: false,
  clinician_checked_in: false,
  clinician_with_another_patient: false,
  sent_to_diagnostics: false,
  diagnostics_return_recorded: false,
  diagnostics_returned_within_sla: false,
  clinically_finished: false,
  records_cleared: false,
  transition_missing: false,
};

export default function Home() {
  const [state, setState] = useState<PatientState>(defaultState);
  const [result, setResult] = useState<string | null>(null);
  const [coverage, setCoverage] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API_URL}/api/coverage/`)
      .then((r) => r.json())
      .then(setCoverage)
      .catch(() => {});
  }, []);

  const handleClassify = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/classify/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(state),
      });
      const data = await res.json();
      setResult(data.code || data.explanation || JSON.stringify(data));
    } catch (e) {
      setResult("Error: " + String(e));
    }
    setLoading(false);
  };

  const updateField = (field: keyof PatientState, value: boolean | number) => {
    setState((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <main className="max-w-7xl mx-auto px-4 py-8">
      <header className="mb-12">
        <h1 className="text-4xl font-bold text-white mb-2">CADENCE</h1>
        <p className="text-gray-400 text-lg">OPD Waste Taxonomy — Classifier & Coverage Dashboard</p>
      </header>

      {/* Taxonomy Grid */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4 text-white">Waste Taxonomy (W1–W9)</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {W_CODES.map((w) => (
            <div key={w.code} className="bg-gray-900 border border-gray-800 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-mono bg-blue-600/20 text-blue-400 px-2 py-0.5 rounded">
                  {w.code}
                </span>
                <span className="font-medium text-white">{w.label}</span>
              </div>
              <p className="text-sm text-gray-400">{w.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Classifier */}
      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4 text-white">State Classifier</h2>
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            {/* Boolean fields */}
            {([
              ["in_counter_queue", "In Counter Queue"],
              ["in_nursing_queue", "In Nursing Queue"],
              ["in_consultation_queue", "In Consultation Queue"],
              ["room_vacant", "Room Vacant"],
              ["clinician_checked_in", "Clinician Checked In"],
              ["clinician_with_another_patient", "Clinician With Another Patient"],
              ["sent_to_diagnostics", "Sent To Diagnostics"],
              ["diagnostics_return_recorded", "Diagnostics Return Recorded"],
              ["diagnostics_returned_within_sla", "Diagnostics Returned Within SLA"],
              ["clinically_finished", "Clinically Finished"],
              ["records_cleared", "Records Cleared"],
              ["transition_missing", "Transition Missing"],
            ] as [keyof PatientState, string][]).map(([field, label]) => (
              <label key={field} className="flex items-center gap-2 text-sm text-gray-300">
                <input
                  type="checkbox"
                  checked={state[field] as boolean}
                  onChange={(e) => updateField(field, e.target.checked)}
                  className="rounded bg-gray-800 border-gray-700"
                />
                {label}
              </label>
            ))}

            {/* Numeric fields */}
            {([
              ["counters_open_idle", "Counters Open Idle"],
              ["counters_busy", "Counters Busy"],
              ["nurses_present_idle", "Nurses Present Idle"],
              ["nurses_busy", "Nurses Busy"],
            ] as [keyof PatientState, string][]).map(([field, label]) => (
              <label key={field} className="flex items-center gap-2 text-sm text-gray-300">
                {label}:
                <input
                  type="number"
                  min={0}
                  value={state[field] as number}
                  onChange={(e) => updateField(field, parseInt(e.target.value) || 0)}
                  className="w-20 bg-gray-800 border border-gray-700 rounded px-2 py-1 text-white"
                />
              </label>
            ))}
          </div>

          <button
            onClick={handleClassify}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white font-medium px-6 py-2 rounded-lg transition-colors"
          >
            {loading ? "Classifying..." : "Classify State"}
          </button>

          {result && (
            <div className="mt-4 bg-gray-800 border border-gray-700 rounded-lg p-4">
              <p className="text-sm text-gray-400 mb-1">Classification Result:</p>
              <p className="text-lg font-mono text-green-400">{result}</p>
            </div>
          )}
        </div>
      </section>

      {/* Coverage */}
      <section>
        <h2 className="text-2xl font-semibold mb-4 text-white">Coverage Report</h2>
        {coverage ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(coverage).map(([key, value]) => (
              <div key={key} className="bg-gray-900 border border-gray-800 rounded-lg p-4">
                <p className="text-xs text-gray-500 uppercase mb-1">{key.replace(/_/g, " ")}</p>
                <p className="text-2xl font-bold text-white">{String(value)}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">Loading coverage data...</p>
        )}
      </section>
    </main>
  );
}
