import {
  ConsolePage,
  PlaceholderTable,
  SafeList,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { loadInternal } from "../../lib/runtime-client";

type RetentionSummary = {
  active_clients: number | null;
  retainer_asks_open: number | null;
  referral_asks_open: number | null;
  nps_30d: number | null;
};

export default async function RetentionPage() {
  const payload = await loadInternal<RetentionSummary>(
    "/api/v1/internal/founder/retention",
    { active_clients: null, retainer_asks_open: null, referral_asks_open: null, nps_30d: null }
  );
  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/retention"
      title="Retention + Referral"
      subtitle="Existing client expansion and warm intro flow"
      source={payload.source}
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Active clients" value={fmt(payload.data.active_clients)} />
        <MetricCard label="Retainer asks open" value={fmt(payload.data.retainer_asks_open)} />
        <MetricCard label="Referral asks open" value={fmt(payload.data.referral_asks_open)} />
      </div>

      <SectionHeading title="Pipeline of expansions" />
      <BrandCard>
        <PlaceholderTable
          columns={["Account", "Type", "Owner", "Value", "Status"]}
        />
      </BrandCard>

      <SectionHeading title="Retention rules" />
      <BrandCard>
        <SafeList
          items={[
            "Retainer ask gated on outcome evidence.",
            "Referral ask only after explicit client satisfaction.",
            "No referral incentive published as guarantee.",
            "Every expansion logged with source, owner, and policy class.",
          ]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
