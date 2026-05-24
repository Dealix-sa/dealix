import { dealixActions } from "../../lib/dealix-actions";
import { DataTable, FounderShell } from "../../components/founder-shell";

export const dynamic = "force-dynamic";

export default async function TrustPage() {
  const env = await dealixActions.trustFlags();
  return (
    <FounderShell
      titleEn="Trust — Flags"
      titleAr="إشارات الثقة"
      source={env.source}
      freshness={env.freshness}
      isEstimate={env.is_estimate}
    >
      <p style={{ opacity: 0.7, fontSize: 14 }}>
        Backed by <code>$PRIVATE_OPS/trust/trust_flags.csv</code>. High-risk
        flags route to the approval center; no auto-action.
      </p>
      <DataTable rows={env.data} />
    </FounderShell>
  );
}
