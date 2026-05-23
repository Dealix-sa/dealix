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

type ProofSummary = {
  candidates: number | null;
  awaiting_client: number | null;
  approved_published: number | null;
  rejected: number | null;
};

export default async function ProofPage() {
  const payload = await loadInternal<ProofSummary>(
    "/api/v1/internal/founder/proof",
    { candidates: null, awaiting_client: null, approved_published: null, rejected: null }
  );
  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/proof"
      title="Proof Approval"
      subtitle="Case-study and testimonial intake → approval → publish"
      source={payload.source}
      intro={
        <p style={{ color: "var(--dx-text-secondary)", margin: 0 }}>
          No outcome, quote, logo, or screenshot reaches a public surface until
          client written approval and an internal A2 approval are both
          recorded.
        </p>
      }
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Candidates" value={fmt(payload.data.candidates)} />
        <MetricCard label="Awaiting client" value={fmt(payload.data.awaiting_client)} />
        <MetricCard label="Approved + published" value={fmt(payload.data.approved_published)} />
      </div>

      <SectionHeading title="Approval pipeline" />
      <BrandCard
        actions={<StatusBadge tone="a2">A2 approval</StatusBadge>}
      >
        <PlaceholderTable
          columns={["Asset", "Client", "Status", "Approver", "Updated"]}
        />
      </BrandCard>

      <SectionHeading title="Proof rules" />
      <BrandCard>
        <SafeList
          items={[
            "No published claim without client written approval.",
            "No before/after numbers without source evidence.",
            "No logos without trademark check + approval.",
            "No revenue claims without bookkeeping confirmation.",
          ]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
