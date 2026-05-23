import {
  ConsolePage,
  PlaceholderTable,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { loadInternal } from "../../lib/runtime-client";

type AuditSummary = {
  events_24h: number | null;
  external_actions_24h: number | null;
  policy_blocks_24h: number | null;
  evidence_attached_pct: number | null;
};

export default async function AuditPage() {
  const payload = await loadInternal<AuditSummary>(
    "/api/v1/internal/founder/audit",
    { events_24h: null, external_actions_24h: null, policy_blocks_24h: null, evidence_attached_pct: null }
  );
  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/audit"
      title="Audit"
      subtitle="Append-only event log: agents · approvals · workers · evals"
      source={payload.source}
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Events (24h)" value={fmt(payload.data.events_24h)} />
        <MetricCard label="External actions (24h)" value={fmt(payload.data.external_actions_24h)} />
        <MetricCard label="Policy blocks (24h)" value={fmt(payload.data.policy_blocks_24h)} />
        <MetricCard label="Evidence attached %" value={payload.data.evidence_attached_pct ?? "—"} />
      </div>

      <SectionHeading title="Recent events" />
      <BrandCard>
        <PlaceholderTable
          columns={["When", "Actor", "Type", "Class", "Policy", "Outcome"]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
