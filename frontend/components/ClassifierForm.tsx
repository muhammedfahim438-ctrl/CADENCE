"use client";

import { useState } from "react";
import type { PatientStateForm, ClassifyResponse } from "@/lib/types";
import { classifyState } from "@/lib/api";

const INITIAL_STATE: PatientStateForm = {
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

function Toggle({
  label,
  checked,
  onChange,
}: {
  label: string;
  checked: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <label className="flex items-center gap-3 cursor-pointer group">
      <div
        className={`relative inline-flex h-5 w-9 items-center rounded-full transition-colors ${
          checked ? "bg-cadence-600" : "bg-gray-300"
        }`}
        onClick={() => onChange(!checked)}
      >
        <span
          className={`inline-block h-3.5 w-3.5 transform rounded-full bg-white transition-transform ${
            checked ? "translate-x-4.5 ml-0.5" : "translate-x-0.5"
          }`}
        />
      </div>
      <span className="text-sm text-gray-700 group-hover:text-gray-900">
        {label}
      </span>
    </label>
  );
}

function NumberInput({
  label,
  value,
  onChange,
}: {
  label: string;
  value: number;
  onChange: (v: number) => void;
}) {
  return (
    <div>
      <label className="block text-sm text-gray-700 mb-1">{label}</label>
      <input
        type="number"
        min={0}
        max={10}
        value={value}
        onChange={(e) => onChange(parseInt(e.target.value) || 0)}
        className="w-full rounded-md border border-gray-300 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-cadence-500 focus:border-transparent"
      />
    </div>
  );
}

export default function ClassifierForm() {
  const [form, setForm] = useState<PatientStateForm>(INITIAL_STATE);
  const [result, setResult] = useState<ClassifyResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function update<K extends keyof PatientStateForm>(key: K, value: PatientStateForm[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function handleClassify() {
    setLoading(true);
    setError(null);
    try {
      const res = await classifyState(form);
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Classification failed");
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setForm(INITIAL_STATE);
    setResult(null);
    setError(null);
  }

  return (
    <section>
      <h2 className="text-xl font-semibold text-gray-900 mb-4">
        State Classifier
      </h2>
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">
              Station Occupancy
            </h3>
            <Toggle
              label="In counter queue"
              checked={form.in_counter_queue}
              onChange={(v) => update("in_counter_queue", v)}
            />
            <Toggle
              label="In nursing queue"
              checked={form.in_nursing_queue}
              onChange={(v) => update("in_nursing_queue", v)}
            />
            <Toggle
              label="In consultation queue"
              checked={form.in_consultation_queue}
              onChange={(v) => update("in_consultation_queue", v)}
            />
          </div>

          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">
              Counter Resources
            </h3>
            <NumberInput
              label="Counters open & idle"
              value={form.counters_open_idle}
              onChange={(v) => update("counters_open_idle", v)}
            />
            <NumberInput
              label="Counters busy"
              value={form.counters_busy}
              onChange={(v) => update("counters_busy", v)}
            />
          </div>

          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">
              Nursing Resources
            </h3>
            <NumberInput
              label="Nurses present & idle"
              value={form.nurses_present_idle}
              onChange={(v) => update("nurses_present_idle", v)}
            />
            <NumberInput
              label="Nurses busy"
              value={form.nurses_busy}
              onChange={(v) => update("nurses_busy", v)}
            />
          </div>

          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">
              Consultation
            </h3>
            <Toggle
              label="Room vacant"
              checked={form.room_vacant}
              onChange={(v) => update("room_vacant", v)}
            />
            <Toggle
              label="Clinician checked in"
              checked={form.clinician_checked_in}
              onChange={(v) => update("clinician_checked_in", v)}
            />
            <Toggle
              label="Clinician with another patient"
              checked={form.clinician_with_another_patient}
              onChange={(v) => update("clinician_with_another_patient", v)}
            />
          </div>

          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">
              Diagnostics
            </h3>
            <Toggle
              label="Sent to diagnostics"
              checked={form.sent_to_diagnostics}
              onChange={(v) => update("sent_to_diagnostics", v)}
            />
            <Toggle
              label="Return recorded"
              checked={form.diagnostics_return_recorded}
              onChange={(v) => update("diagnostics_return_recorded", v)}
            />
            <Toggle
              label="Returned within SLA"
              checked={form.diagnostics_returned_within_sla}
              onChange={(v) => update("diagnostics_returned_within_sla", v)}
            />
          </div>

          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider">
              Exit & Integrity
            </h3>
            <Toggle
              label="Clinically finished"
              checked={form.clinically_finished}
              onChange={(v) => update("clinically_finished", v)}
            />
            <Toggle
              label="Records cleared"
              checked={form.records_cleared}
              onChange={(v) => update("records_cleared", v)}
            />
            <Toggle
              label="Transition missing"
              checked={form.transition_missing}
              onChange={(v) => update("transition_missing", v)}
            />
          </div>
        </div>

        <div className="mt-6 flex items-center gap-3">
          <button
            onClick={handleClassify}
            disabled={loading}
            className="px-6 py-2.5 bg-cadence-600 text-white font-medium rounded-lg hover:bg-cadence-700 focus:outline-none focus:ring-2 focus:ring-cadence-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? "Classifying..." : "Classify State"}
          </button>
          <button
            onClick={handleReset}
            className="px-6 py-2.5 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition-colors"
          >
            Reset
          </button>
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-6">
            <div
              className={`p-5 rounded-lg border ${
                result.is_data_gap
                  ? "bg-amber-50 border-amber-200"
                  : "bg-green-50 border-green-200"
              }`}
            >
              <div className="flex items-center gap-3 mb-2">
                {result.is_data_gap ? (
                  <span className="text-2xl font-bold text-amber-700">
                    DATA GAP
                  </span>
                ) : (
                  <>
                    <span className="text-2xl font-bold text-green-700">
                      {result.code}
                    </span>
                    <span className="text-sm font-medium text-green-600">
                      {result.label}
                    </span>
                  </>
                )}
              </div>
              <p className="text-sm text-gray-700">{result.explanation}</p>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
