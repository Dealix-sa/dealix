import { FounderShell } from "../../components/founder-shell";
import { getSalesFunnel } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SalesCockpitPage() {
  const funnel = await getSalesFunnel();
  const rows: Array<[string, number]> = [
    ["Lead intelligence", funnel.lead_intelligence],
    ["A-grade leads", funnel.a_leads],
    ["Pending approval", funnel.pending_approval],
    ["Approved outreach", funnel.approved_outreach],
    ["Sent", funnel.sent],
    ["Replies", funnel.replies],
    ["Positive replies", funnel.positive_replies],
    ["Samples", funnel.samples],
    ["Proposals", funnel.proposals],
    ["Payment capture", funnel.payment_capture],
  ];
  return (
    <FounderShell>
      <main className="p-8">
        <h1 className="text-4xl font-bold">Sales Cockpit</h1>
        <p className="mt-2 max-w-3xl">
          Funnel-stage counters straight from the revenue runtime.
        </p>
        <section className="mt-8 grid grid-cols-2 gap-4 md:grid-cols-5">
          {rows.map(([label, value]) => (
            <div key={label} className="rounded-xl border p-4">
              <p className="text-sm">{label}</p>
              <p className="mt-2 text-2xl font-bold">{value}</p>
            </div>
          ))}
        </section>
        <p className="mt-6 text-xs">
          Source: {funnel.source ?? "internal"} · Updated:{" "}
          {funnel.last_updated || "—"}
        </p>
      </main>
    </FounderShell>
  );
}
