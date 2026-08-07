import { loadDeals, summarizeDeals } from "@/lib/finance/deals";

export const metadata = { title: "Revenue — Dealix" };
export const dynamic = "force-static";

export default function RevenuePage() {
  const deals = loadDeals();
  const s = summarizeDeals(deals);
  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Revenue</h1>
      <p className="mt-2 text-sm text-neutral-600">From the deal ledger. Generate the full PDF report with:</p>
      <pre className="mt-3 overflow-x-auto rounded-lg bg-neutral-900 p-4 text-xs text-neutral-100">
{`python3 scripts/generate_revenue_report.py`}
      </pre>

      <section className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card label="Won deals" value={s.won.toString()} />
        <Card label="Won setup" value={`${s.wonSetup.toLocaleString()} SAR`} />
        <Card label="Won MRR" value={`${s.wonMrr.toLocaleString()} SAR`} />
        <Card label="Open deals" value={s.open.toString()} />
      </section>

      <section className="mt-10 grid gap-4 sm:grid-cols-2">
        <Card label="Pipeline setup" value={`${s.pipelineSetup.toLocaleString()} SAR`} />
        <Card label="Pipeline MRR" value={`${s.pipelineMrr.toLocaleString()} SAR`} />
      </section>
    </main>
  );
}

function Card({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-neutral-200 bg-white p-5">
      <p className="text-xs uppercase tracking-wide text-neutral-500">{label}</p>
      <p className="mt-1 text-2xl font-semibold">{value}</p>
    </div>
  );
}
