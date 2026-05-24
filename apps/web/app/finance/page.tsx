import {
  ConsolePage,
  PlaceholderTable,
  SafeList,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { loadInternal } from "../../lib/runtime-client";

type Finance = {
  cash_collected: number | null;
  mrr: number | null;
  pipeline_weighted: number | null;
  ai_cost_per_lead: number | null;
  ai_cost_per_proposal: number | null;
  ai_cost_per_paid_client: number | null;
  runway_months: number | null;
};

export default async function FinancePage() {
  const payload = await loadInternal<Finance>(
    "/api/v1/internal/founder/finance",
    {
      cash_collected: null,
      mrr: null,
      pipeline_weighted: null,
      ai_cost_per_lead: null,
      ai_cost_per_proposal: null,
      ai_cost_per_paid_client: null,
      runway_months: null,
    }
  );
  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/finance"
      title="Finance + Unit Economics"
      subtitle="Cash · pipeline · AI unit cost · runway"
      source={payload.source}
    >
      <SectionHeading title="Top line" />
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Cash collected" value={fmt(payload.data.cash_collected)} helper="SAR · 30d" />
        <MetricCard label="MRR" value={fmt(payload.data.mrr)} helper="SAR" />
        <MetricCard label="Weighted pipeline" value={fmt(payload.data.pipeline_weighted)} helper="SAR" />
      </div>

      <SectionHeading title="AI unit economics" />
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="AI cost / lead" value={fmt(payload.data.ai_cost_per_lead)} helper="SAR" />
        <MetricCard label="AI cost / proposal" value={fmt(payload.data.ai_cost_per_proposal)} helper="SAR" />
        <MetricCard label="AI cost / paid client" value={fmt(payload.data.ai_cost_per_paid_client)} helper="SAR" />
      </div>

      <SectionHeading title="Runway + spend rules" />
      <BrandCard>
        <p style={{ marginTop: 0, color: "var(--dx-text-secondary)" }}>
          Runway (months): <strong style={{ color: "var(--dx-text-primary)" }}>{fmt(payload.data.runway_months)}</strong>
        </p>
        <SafeList
          items={[
            "No AI spend without a pre-attached unit-economics tag.",
            "Tool cost reviewed weekly; anything > 1.5x trailing month flagged A2.",
            "Founder hours saved logged per workflow.",
            "Bad-revenue filter applies before any deal closes.",
          ]}
        />
      </BrandCard>

      <SectionHeading title="Recent finance events" />
      <BrandCard>
        <PlaceholderTable columns={["Event", "Type", "Amount", "Account", "When"]} />
      </BrandCard>
    </ConsolePage>
  );
}
