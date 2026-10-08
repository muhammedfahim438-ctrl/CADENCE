import type { TaxonomyCode, ClassifyResponse, CoverageResponse, PatientStateForm } from "./types";

const API_BASE = "http://localhost:8000";

export async function fetchTaxonomy(): Promise<TaxonomyCode[]> {
  const res = await fetch(`${API_BASE}/api/taxonomy`);
  if (!res.ok) throw new Error("Failed to fetch taxonomy");
  const data = await res.json();
  return data.codes;
}

export async function classifyState(state: PatientStateForm): Promise<ClassifyResponse> {
  const res = await fetch(`${API_BASE}/api/classify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(state),
  });
  if (!res.ok) throw new Error("Classification failed");
  return res.json();
}

export async function fetchCoverage(): Promise<CoverageResponse> {
  const res = await fetch(`${API_BASE}/api/coverage`);
  if (!res.ok) throw new Error("Failed to fetch coverage");
  return res.json();
}
