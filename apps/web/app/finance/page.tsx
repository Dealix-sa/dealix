import { FounderShell, KV } from "../../components/founder-shell";
import { getFinanceSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function FinancePage() {
  const data = await getFinanceSummary();
  return (
    <FounderShell title="Finance" source={data.source}>
      <section className="card">
        <h2>Cash + capture</h2>
        <KV k="Cash collected (SAR)" v={data.cash_total_sar} />
        <KV k="Open capture rows" v={data.capture_open} />
        <KV k="AI unit-economics rows" v={data.ai_unit_economics_rows} />
      </section>
      <section className="card">
        <p className="muted">
          Finance never auto-changes payment terms or refunds. Those are
          A3 actions in the policy file and require explicit founder
          intervention recorded in the audit log.
        </p>
      </section>
    </FounderShell>
  );
}
