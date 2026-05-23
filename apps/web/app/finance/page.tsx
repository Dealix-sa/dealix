import { FounderShell, MetricGrid } from "../../components/founder/founder-shell";
import { getFinanceSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function FinancePage() {
  const data = await getFinanceSummary();
  return (
    <FounderShell title="Finance" source={data.source}>
      <MetricGrid
        items={[
          { label: "Cash collected (SAR)", value: data.cash_collected_sar },
          { label: "Pipeline (SAR)", value: data.pipeline_sar },
          { label: "Weighted pipeline (SAR)", value: data.weighted_pipeline_sar },
          { label: "Payment follow-ups", value: data.payment_follow_ups },
          { label: "MRR (SAR)", value: data.mrr_sar }
        ]}
      />
    </FounderShell>
  );
}
