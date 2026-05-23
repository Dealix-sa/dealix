import {
  ConsolePage,
  PlaceholderTable,
  SafeList,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { loadInternal } from "../../lib/runtime-client";

type ControlSummary = {
  policies_loaded: number | null;
  agents_registered: number | null;
  open_risks: number | null;
  scorecard_score: number | null;
};

export default async function ControlPlanePage() {
  const payload = await loadInternal<ControlSummary>(
    "/api/v1/internal/control/summary",
    { policies_loaded: null, agents_registered: null, open_risks: null, scorecard_score: null }
  );
  const fmt = (n: number | null) => (n === null ? "—" : n.toLocaleString());

  return (
    <ConsolePage
      active="/control-plane"
      title="Control Plane"
      subtitle="Policies · agents · risks · scorecard"
      source={payload.source}
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Policies loaded" value={fmt(payload.data.policies_loaded)} />
        <MetricCard label="Agents registered" value={fmt(payload.data.agents_registered)} />
        <MetricCard label="Open risks" value={fmt(payload.data.open_risks)} />
        <MetricCard label="Scorecard" value={fmt(payload.data.scorecard_score)} helper="0-100" />
      </div>

      <SectionHeading title="Read-only API surface" />
      <BrandCard>
        <SafeList
          items={[
            "GET /api/v1/internal/control/summary",
            "GET /api/v1/internal/control/policies",
            "GET /api/v1/internal/control/agents",
            "GET /api/v1/internal/control/scorecard",
            "GET /api/v1/internal/control/risks",
          ]}
        />
      </BrandCard>

      <SectionHeading title="Recent runs" />
      <BrandCard>
        <PlaceholderTable
          columns={["Run", "Workflow", "Owner", "State", "Started"]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
