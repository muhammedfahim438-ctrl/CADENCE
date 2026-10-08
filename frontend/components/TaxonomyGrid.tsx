import type { TaxonomyCode } from "@/lib/types";

const CODE_COLORS: Record<string, string> = {
  W1: "bg-blue-50 border-blue-200 text-blue-800",
  W2: "bg-blue-50 border-blue-200 text-blue-800",
  W3: "bg-purple-50 border-purple-200 text-purple-800",
  W4: "bg-purple-50 border-purple-200 text-purple-800",
  W5: "bg-red-50 border-red-200 text-red-800",
  W6: "bg-orange-50 border-orange-200 text-orange-800",
  W7: "bg-yellow-50 border-yellow-200 text-yellow-800",
  W8: "bg-green-50 border-green-200 text-green-800",
  W9: "bg-gray-50 border-gray-200 text-gray-800",
};

const DESCRIPTIONS: Record<string, string> = {
  W1: "Patient in counter queue while a counter is open and idle",
  W2: "Patient in counter queue while all counters are busy",
  W3: "Patient in nursing queue while a nurse is present and idle",
  W4: "Patient in nursing queue while all nurses are busy",
  W5: "Patient in consultation queue, room vacant or clinician not checked in",
  W6: "Patient in consultation queue, clinician present with another patient",
  W7: "Patient sent to diagnostics, return recorded outside SLA",
  W8: "Patient clinically finished, records not yet cleared",
  W9: "Observed state not covered by any rule (residual)",
};

export default function TaxonomyGrid({ codes }: { codes: TaxonomyCode[] }) {
  return (
    <section>
      <h2 className="text-xl font-semibold text-gray-900 mb-4">
        Waste Taxonomy
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {codes.map((code) => (
          <div
            key={code.code}
            className={`rounded-lg border p-4 ${CODE_COLORS[code.code] || "bg-gray-50 border-gray-200"}`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-lg font-bold">{code.code}</span>
              {!code.covered && (
                <span className="text-xs font-medium px-2 py-0.5 rounded bg-gray-200 text-gray-600">
                  Residual
                </span>
              )}
            </div>
            <p className="text-sm font-medium mb-1">{code.label}</p>
            <p className="text-xs opacity-75">{DESCRIPTIONS[code.code]}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
