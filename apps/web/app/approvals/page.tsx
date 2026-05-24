import {
  ConsolePage,
  PlaceholderTable,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { StatusBadge } from "../../components/brand/StatusBadge";
import { loadInternal } from "../../lib/runtime-client";

type ApprovalsSummary = {
  total: number | null;
  by_class: { A1: number | null; A2: number | null; A3: number | null };
  avg_age_hours: number | null;
};

export default async function ApprovalsPage() {
  const payload = await loadInternal<ApprovalsSummary>(
    "/api/v1/internal/founder/approvals",
    {
      total: null,
      by_class: { A1: null, A2: null, A3: null },
      avg_age_hours: null,
    }
  );
  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/approvals"
      title="Approval Queue"
      subtitle="Founder gating for external-impact actions"
      source={payload.source}
      intro={
        <p style={{ color: "var(--dx-text-secondary)", margin: 0 }}>
          A1 may pass policy autoroute. A2 requires explicit founder approval.
          A3 is never executed without a recorded escalation and matching
          evidence.
        </p>
      }
    >
      <div className="dx-grid dx-grid--cols-3" style={{ marginTop: 16 }}>
        <MetricCard label="A1 auto-safe" value={fmt(payload.data.by_class.A1)} />
        <MetricCard label="A2 founder" value={fmt(payload.data.by_class.A2)} />
        <MetricCard label="A3 escalation" value={fmt(payload.data.by_class.A3)} />
      </div>

      <SectionHeading title="Queue" />
      <BrandCard>
        <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          <StatusBadge tone="a1">A1</StatusBadge>
          <StatusBadge tone="a2">A2</StatusBadge>
          <StatusBadge tone="a3">A3</StatusBadge>
        </div>
        <PlaceholderTable
          columns={["Item", "Class", "Owner", "Risk", "Submitted", "Status"]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
