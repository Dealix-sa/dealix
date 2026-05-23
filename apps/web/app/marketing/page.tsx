import {
  ConsolePage,
  PlaceholderTable,
  SafeList,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { StatusBadge } from "../../components/brand/StatusBadge";
import { loadInternal } from "../../lib/runtime-client";

type MarketingSummary = {
  drafts_pending: number | null;
  scheduled_posts: number | null;
  landing_visits_30d: number | null;
  email_subscribers: number | null;
};

export default async function MarketingPage() {
  const payload = await loadInternal<MarketingSummary>(
    "/api/v1/internal/founder/marketing",
    { drafts_pending: null, scheduled_posts: null, landing_visits_30d: null, email_subscribers: null }
  );
  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/marketing"
      title="Marketing OS"
      subtitle="Content drafts, calendar, landing surfaces"
      source={payload.source}
      intro={
        <p style={{ color: "var(--dx-text-secondary)", margin: 0 }}>
          Marketing artifacts are drafted and queued. Nothing is published
          externally without a recorded A2 approval and brand-voice check.
        </p>
      }
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Drafts pending" value={fmt(payload.data.drafts_pending)} />
        <MetricCard label="Scheduled (next 14d)" value={fmt(payload.data.scheduled_posts)} />
        <MetricCard label="Landing visits (30d)" value={fmt(payload.data.landing_visits_30d)} />
      </div>

      <SectionHeading title="Content queue" />
      <BrandCard
        actions={<StatusBadge tone="a2">A2 approval</StatusBadge>}
      >
        <PlaceholderTable
          columns={["Asset", "Channel", "Owner", "Brand check", "Status"]}
        />
      </BrandCard>

      <SectionHeading title="Voice + copywriting rules" />
      <BrandCard>
        <SafeList
          items={[
            "No guaranteed revenue claims.",
            "No fabricated client logos / numbers.",
            "Bilingual copy reviewed for cultural fit.",
            "Every CTA mapped to a rung in the product ladder.",
          ]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
