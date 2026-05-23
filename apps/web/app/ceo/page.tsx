import { FounderShell } from "../../components/founder-shell";
import { getCeoSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function CeoPage() {
  const summary = await getCeoSummary();
  return (
    <FounderShell>
      <main className="p-8">
        <h1 className="text-4xl font-bold">CEO</h1>
        <p className="mt-2 max-w-3xl">
          One top action, the operating status, and the headline counters
          Sami needs to start the day.
        </p>
        <section className="mt-8 rounded-2xl border p-6">
          <h2 className="text-lg font-semibold">Top action</h2>
          <p className="mt-2 text-xl">{summary.top_action}</p>
          <p className="mt-2 text-sm">Status: {summary.status}</p>
        </section>
        <section className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
          <Metric label="Risk flags" value={summary.risk_flags} />
          <Metric label="Cash collected (SAR)" value={summary.cash_collected_sar} />
          <Metric label="Approved outreach" value={summary.approved_outreach} />
          <Metric label="Positive replies" value={summary.positive_replies} />
          <Metric label="Proposals due" value={summary.proposals_due} />
          <Metric label="Payment follow-ups due" value={summary.payment_followups_due} />
        </section>
        <p className="mt-6 text-xs">
          Source: {summary.source ?? "internal"} · Last updated:{" "}
          {summary.last_updated || "—"}
        </p>
      </main>
    </FounderShell>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-xl border p-4">
      <p className="text-sm">{label}</p>
      <p className="mt-2 text-2xl font-bold">{value}</p>
    </div>
  );
}
