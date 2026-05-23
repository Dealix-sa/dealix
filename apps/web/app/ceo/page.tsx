import { getCEOSummary } from "../../lib/dealix-api";

export default async function CEOCommandCenterPage() {
  const summary = await getCEOSummary();
  return (
    <main className="min-h-screen p-8">
      <section>
        <p className="text-sm uppercase tracking-wide opacity-70">Dealix Internal</p>
        <h1 className="text-4xl font-bold">CEO Command Center</h1>
        <p className="mt-2 max-w-3xl">
          Control Dealix revenue, approvals, workers, trust, finance, and delivery from one screen.
        </p>
      </section>
      <section className="mt-8 rounded-2xl border p-6">
        <p className="text-sm opacity-70">Top CEO Action</p>
        <h2 className="mt-2 text-2xl font-semibold">{summary.top_action}</h2>
        <p className="mt-2 text-sm opacity-70">Status: {summary.status}</p>
      </section>
      <section className="mt-6 grid gap-4 md:grid-cols-3">
        <Metric label="Risk Flags" value={summary.risk_flags} />
        <Metric label="Cash SAR" value={summary.cash_collected_sar} />
        <Metric label="Approved Outreach" value={summary.approved_outreach} />
        <Metric label="Positive Replies" value={summary.positive_replies} />
        <Metric label="Proposals Due" value={summary.proposals_due} />
        <Metric label="Payment Follow-ups" value={summary.payment_followups_due} />
      </section>
      <p className="mt-6 text-xs opacity-60">Last updated: {summary.last_updated}</p>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded-2xl border p-5">
      <p className="text-sm opacity-70">{label}</p>
      <p className="mt-2 text-3xl font-bold">{value}</p>
    </div>
  );
}
