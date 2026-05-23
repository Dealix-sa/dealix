import {
  ConsolePage,
  PlaceholderTable,
  SafeList,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { loadInternal } from "../../lib/runtime-client";

type DeliverySummary = {
  active_engagements: number | null;
  pending_qa: number | null;
  handoffs_due_7d: number | null;
  blockers_open: number | null;
};

export default async function DeliveryPage() {
  const payload = await loadInternal<DeliverySummary>(
    "/api/v1/internal/founder/delivery",
    { active_engagements: null, pending_qa: null, handoffs_due_7d: null, blockers_open: null }
  );
  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/delivery"
      title="Delivery + QA"
      subtitle="Active engagements, QA queue, handoffs"
      source={payload.source}
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Active engagements" value={fmt(payload.data.active_engagements)} />
        <MetricCard label="Pending QA" value={fmt(payload.data.pending_qa)} />
        <MetricCard label="Handoffs due (7d)" value={fmt(payload.data.handoffs_due_7d)} />
      </div>

      <SectionHeading title="Delivery pipeline" />
      <BrandCard>
        <PlaceholderTable
          columns={["Engagement", "Client", "Stage", "Owner", "Risk"]}
        />
      </BrandCard>

      <SectionHeading title="Delivery non-negotiables" />
      <BrandCard>
        <SafeList
          items={[
            "Every paid engagement has a written scope + sign-off.",
            "QA gate before any external handoff.",
            "Proof published only after client approval.",
            "Retainer ask only after measured outcome.",
          ]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
