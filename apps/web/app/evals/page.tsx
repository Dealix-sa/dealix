import {
  ConsolePage,
  PlaceholderTable,
  SafeList,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { loadInternal } from "../../lib/runtime-client";

type EvalSummary = {
  suites_total: number | null;
  passing: number | null;
  failing: number | null;
  last_run: string | null;
};

const suites = [
  "no_guaranteed_claims",
  "approval_bypass",
  "prompt_injection",
  "sensitive_data_leakage",
  "suppression_compliance",
  "evidence_required",
  "arabic_business_quality",
  "proposal_safety",
  "tool_misuse",
  "A3_escalation",
  "proof_safety",
  "pricing_safety",
  "data_export_safety",
  "contract_safety",
  "payment_terms_safety",
];

export default async function EvalsPage() {
  const payload = await loadInternal<EvalSummary>(
    "/api/v1/internal/founder/evals",
    { suites_total: suites.length, passing: null, failing: null, last_run: null }
  );
  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/evals"
      title="Eval + Red-Team Gate"
      subtitle="Required for any prompt / agent / tool change"
      source={payload.source}
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Suites" value={fmt(payload.data.suites_total)} />
        <MetricCard label="Passing" value={fmt(payload.data.passing)} />
        <MetricCard label="Failing" value={fmt(payload.data.failing)} />
      </div>

      <SectionHeading title="Suites" />
      <BrandCard>
        <SafeList items={suites} />
      </BrandCard>

      <SectionHeading title="Latest runs" />
      <BrandCard>
        <PlaceholderTable
          columns={["Suite", "Pass rate", "Last run", "Owner"]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
