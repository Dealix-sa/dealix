import { dealixActions } from "../../lib/dealix-actions";
import { DataTable, FounderShell } from "../../components/founder-shell";

export const dynamic = "force-dynamic";

export default async function CEOPage() {
  const env = await dealixActions.ceoDailyBrief();
  return (
    <FounderShell
      titleEn="CEO — Daily Brief"
      titleAr="ملخّص الرئيس اليومي"
      source={env.source}
      freshness={env.freshness}
      isEstimate={env.is_estimate}
    >
      <p style={{ opacity: 0.7, fontSize: 14 }}>
        Read-only view over <code>$PRIVATE_OPS/founder/decision_log.csv</code>.
        Numbers shown when <code>is_estimate=false</code> only.
      </p>
      <DataTable rows={env.data} />
    </FounderShell>
  );
}
