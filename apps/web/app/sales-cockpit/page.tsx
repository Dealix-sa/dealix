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

type Funnel = {
  leads_researched: number | null;
  a_leads: number | null;
  approved_outreach: number | null;
  sent_actions: number | null;
  replies: number | null;
  positive_replies: number | null;
  samples_sent: number | null;
  proposals_sent: number | null;
};

export default async function SalesCockpitPage() {
  const payload = await loadInternal<Funnel>(
    "/api/v1/internal/founder/sales",
    {
      leads_researched: null,
      a_leads: null,
      approved_outreach: null,
      sent_actions: null,
      replies: null,
      positive_replies: null,
      samples_sent: null,
      proposals_sent: null,
    }
  );

  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/sales-cockpit"
      title="Sales Cockpit"
      subtitle="Founder-led sales motion"
      source={payload.source}
    >
      <SectionHeading title="Funnel" />
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Leads researched" value={fmt(payload.data.leads_researched)} />
        <MetricCard label="A leads" value={fmt(payload.data.a_leads)} />
        <MetricCard label="Approved outreach" value={fmt(payload.data.approved_outreach)} />
        <MetricCard label="Sent / manual actions" value={fmt(payload.data.sent_actions)} />
        <MetricCard label="Replies" value={fmt(payload.data.replies)} />
        <MetricCard label="Positive replies" value={fmt(payload.data.positive_replies)} />
        <MetricCard label="Samples sent" value={fmt(payload.data.samples_sent)} />
        <MetricCard label="Proposals sent" value={fmt(payload.data.proposals_sent)} />
      </div>

      <SectionHeading title="Today's draft queue" meta="A2 approval required" />
      <BrandCard
        actions={<StatusBadge tone="a2">Founder approval</StatusBadge>}
      >
        <PlaceholderTable
          columns={["Account", "Channel", "Draft owner", "Score", "Status"]}
        />
      </BrandCard>

      <SectionHeading title="Playbook reminders" />
      <BrandCard>
        <SafeList
          items={[
            "Score every lead before any outreach draft.",
            "No A3 actions automated — escalate before sending.",
            "Every proposal links back to a Source Passport.",
            "All payment terms require explicit founder approval.",
          ]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
