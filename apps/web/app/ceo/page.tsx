import { FounderShell, KV } from "../../components/founder-shell";
import { getCEOSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function CEOPage() {
  const data = await getCEOSummary();
  return (
    <FounderShell title="CEO Pulse" source={data.source}>
      <section className="card">
        <h2>Top-of-funnel</h2>
        <KV k="Leads in pipeline" v={data.leads_total} />
        <KV k="Approvals waiting on founder" v={data.approvals_open} />
        <KV k="Open incidents" v={data.incidents_open} />
        <KV k="Cash collected (SAR)" v={data.cash_total_sar} />
      </section>
      <section className="card">
        <h2>What this view promises</h2>
        <p>
          This is the founder&apos;s daily pulse. It only renders data the
          private runtime has written. It never claims production
          readiness from fallback data — when the banner above shows,
          treat every number as zero.
        </p>
      </section>
    </FounderShell>
  );
}
