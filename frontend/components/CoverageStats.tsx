import type { CoverageResponse } from "@/lib/types";

function StatCard({
  label,
  value,
  sub,
  color,
}: {
  label: string;
  value: string;
  sub?: string;
  color: string;
}) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
      <p className="text-sm font-medium text-gray-500 mb-1">{label}</p>
      <p className={`text-3xl font-bold ${color}`}>{value}</p>
      {sub && <p className="text-xs text-gray-400 mt-1">{sub}</p>}
    </div>
  );
}

export default function CoverageStats({ data }: { data: CoverageResponse }) {
  const coveragePct = (data.coverage * 100).toFixed(1);
  const residualPct = (data.residual_share * 100).toFixed(1);

  return (
    <section>
      <h2 className="text-xl font-semibold text-gray-900 mb-4">
        Coverage Report
      </h2>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Coherent States"
          value={data.total_coherent.toLocaleString()}
          sub="Observable state space"
          color="text-gray-900"
        />
        <StatCard
          label="Observed"
          value={data.observed.toLocaleString()}
          sub="States with ledger rows"
          color="text-cadence-600"
        />
        <StatCard
          label="Coverage"
          value={`${coveragePct}%`}
          sub="Observed / Coherent"
          color="text-green-600"
        />
        <StatCard
          label="Residual (W9)"
          value={`${residualPct}%`}
          sub="Unclassified share"
          color="text-amber-600"
        />
      </div>

      <div className="mt-4 bg-white rounded-xl border border-gray-200 shadow-sm p-5">
        <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
          State Distribution
        </h3>
        <div className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-9 gap-2">
          {Object.entries(data.counts).map(([code, count]) => (
            <div key={code} className="text-center">
              <div className="text-xs font-medium text-gray-500">{code}</div>
              <div className="text-sm font-bold text-gray-900">
                {count.toLocaleString()}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
