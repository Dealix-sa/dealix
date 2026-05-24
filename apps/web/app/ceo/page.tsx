import {
  ConsolePage,
  PlaceholderTable,
  SafeList,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { loadInternal } from "../../lib/runtime-client";

type CeoSummary = {
  pipeline_weighted: number | null;
  cash_collected: number | null;
  approvals_pending: number | null;
  trust_flags_open: number | null;
  workers_fresh: number | null;
};

export default async function CeoPage() {
  const payload = await loadInternal<CeoSummary>("/api/v1/internal/founder/ceo", {
    pipeline_weighted: null,
    cash_collected: null,
    approvals_pending: null,
    trust_flags_open: null,
    workers_fresh: null,
  });

  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/ceo"
      title="CEO Command"
      subtitle="Daily operating picture"
      source={payload.source}
    >
      <SectionHeading
        title="Top of the funnel"
        meta={`updated ${new Date(payload.fetchedAt).toLocaleTimeString()}`}
      />
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard
          label="Weighted pipeline"
          value={fmt(payload.data.pipeline_weighted)}
          helper="SAR"
        />
        <MetricCard
          label="Cash collected"
          value={fmt(payload.data.cash_collected)}
          helper="SAR · last 30 days"
        />
        <MetricCard
          label="Approvals pending"
          value={fmt(payload.data.approvals_pending)}
          helper="A2 in queue"
        />
      </div>

      <SectionHeading title="Operating health" />
      <div className="dx-grid dx-grid--cols-2">
        <MetricCard
          label="Trust flags open"
          value={fmt(payload.data.trust_flags_open)}
        />
        <MetricCard
          label="Workers fresh"
          value={fmt(payload.data.workers_fresh)}
        />
      </div>

      <SectionHeading title="Decisions this week" />
      <BrandCard>
        <PlaceholderTable
          columns={["Decision", "Owner", "Status", "Due"]}
          emptyLabel="No decisions on file — run the bootstrap script to seed."
        />
      </BrandCard>

      <SectionHeading title="Daily focus" />
      <BrandCard>
        <SafeList
          items={[
            "Clear A2 approvals before 11:00",
            "Review trust flags before any A3 escalation",
            "Confirm worker freshness across CEO / sales / finance / trust",
            "Decide tomorrow's outbound queue size",
          ]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
