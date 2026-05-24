import {
  ConsolePage,
  PlaceholderTable,
  SafeList,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { loadInternal } from "../../lib/runtime-client";

type SecuritySummary = {
  open_findings: number | null;
  critical_open: number | null;
  internal_api_unauth_24h: number | null;
  last_secret_scan: string | null;
};

export default async function SecurityPage() {
  const payload = await loadInternal<SecuritySummary>(
    "/api/v1/internal/founder/security",
    { open_findings: null, critical_open: null, internal_api_unauth_24h: null, last_secret_scan: null }
  );
  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/security"
      title="Security"
      subtitle="Authn / authz · secrets · supply chain · internal API gate"
      source={payload.source}
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Open findings" value={fmt(payload.data.open_findings)} />
        <MetricCard label="Critical open" value={fmt(payload.data.critical_open)} />
        <MetricCard label="Unauth attempts 24h" value={fmt(payload.data.internal_api_unauth_24h)} />
      </div>

      <SectionHeading title="Gates" />
      <BrandCard>
        <SafeList
          items={[
            "Internal API requires X-Internal-Token + audit-log middleware.",
            "Branch protection: required checks include eval gate + policy.",
            "Secrets scanned pre-commit and on PR.",
            "All A3 escalations require evidence + named approver.",
          ]}
        />
      </BrandCard>

      <SectionHeading title="Findings" />
      <BrandCard>
        <PlaceholderTable columns={["Source", "Severity", "Found", "Owner", "Status"]} />
      </BrandCard>
    </ConsolePage>
  );
}
