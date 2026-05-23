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

type TrustSummary = {
  flags_open: number | null;
  flags_resolved_30d: number | null;
  high_risk_open: number | null;
  policies_evaluated_24h: number | null;
};

export default async function TrustPage() {
  const payload = await loadInternal<TrustSummary>(
    "/api/v1/internal/founder/trust",
    { flags_open: null, flags_resolved_30d: null, high_risk_open: null, policies_evaluated_24h: null }
  );
  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/trust"
      title="Trust"
      subtitle="Policy-as-code posture · open flags · evidence gaps"
      source={payload.source}
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Flags open" value={fmt(payload.data.flags_open)} />
        <MetricCard label="High-risk open" value={fmt(payload.data.high_risk_open)} />
        <MetricCard label="Resolved (30d)" value={fmt(payload.data.flags_resolved_30d)} />
      </div>

      <SectionHeading title="Active flags" />
      <BrandCard>
        <PlaceholderTable
          columns={["Source", "Rule", "Severity", "Opened", "Owner"]}
        />
      </BrandCard>

      <SectionHeading title="Non-negotiables" />
      <BrandCard>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 12 }}>
          <StatusBadge tone="success">No external sending</StatusBadge>
          <StatusBadge tone="success">No unsafe claims</StatusBadge>
          <StatusBadge tone="warning">A3 requires escalation</StatusBadge>
        </div>
        <SafeList
          items={[
            "no_a3_auto",
            "no_suppressed_outreach",
            "high_risk_requires_evidence",
            "no_guaranteed_revenue_claims",
            "approved_a2_can_request_execution",
            "public_proof_requires_approval",
            "pricing_commit_requires_approval",
            "data_export_requires_escalation",
            "payment_terms_require_escalation",
            "contract_change_requires_escalation",
            "destructive_operation_requires_escalation",
          ]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
