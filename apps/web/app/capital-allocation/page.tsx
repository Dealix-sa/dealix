import { dealixActions } from "../../lib/dealix-actions";
import { DataTable, FounderShell } from "../../components/founder-shell";

export const dynamic = "force-dynamic";

export default async function CapitalAllocationPage() {
  const env = await dealixActions.capitalAllocation();
  return (
    <FounderShell
      titleEn="Capital Allocation"
      titleAr="توزيع رأس المال"
      source={env.source}
      freshness={env.freshness}
      isEstimate={env.is_estimate}
    >
      <p style={{ opacity: 0.7, fontSize: 14 }}>
        Backed by <code>$PRIVATE_OPS/finance/capital_allocation.csv</code>.
        Every number requires a source OR <code>is_estimate=true</code>
        per the claim policy.
      </p>
      <DataTable rows={env.data} />
    </FounderShell>
  );
}
