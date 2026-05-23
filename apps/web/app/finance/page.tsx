import { FounderShell } from "../../components/founder-shell";
import { getFinanceSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function FinancePage() {
  const finance = await getFinanceSummary();
  const rows: Array<[string, number]> = [
    ["Cash collected (SAR)", finance.cash_collected_sar],
    ["MRR (SAR)", finance.mrr_sar],
    ["Pipeline (SAR)", finance.pipeline_sar],
    ["Weighted pipeline (SAR)", finance.weighted_pipeline_sar],
    ["Payment follow-ups due", finance.payment_followups_due],
  ];
  return (
    <FounderShell>
      <main className="p-8">
        <h1 className="text-4xl font-bold">Finance</h1>
        <p className="mt-2 max-w-3xl">
          Cash, MRR, pipeline, and payment follow-ups — all from the
          finance runtime, none hard-coded.
        </p>
        <section className="mt-8 grid grid-cols-2 gap-4 md:grid-cols-3">
          {rows.map(([label, value]) => (
            <div key={label} className="rounded-xl border p-4">
              <p className="text-sm">{label}</p>
              <p className="mt-2 text-2xl font-bold">{value}</p>
            </div>
          ))}
        </section>
        <p className="mt-6 text-xs">
          Source: {finance.source ?? "finance_runtime"} · Updated:{" "}
          {finance.last_updated || "—"}
        </p>
      </main>
    </FounderShell>
  );
}
