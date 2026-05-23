import {
  ConsolePage,
  PlaceholderTable,
  SafeList,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { loadInternal } from "../../lib/runtime-client";

type GrowthSummary = {
  experiments_active: number | null;
  experiments_won_30d: number | null;
  experiments_killed_30d: number | null;
};

export default async function GrowthPage() {
  const payload = await loadInternal<GrowthSummary>(
    "/api/v1/internal/founder/growth",
    { experiments_active: null, experiments_won_30d: null, experiments_killed_30d: null }
  );

  return (
    <ConsolePage
      active="/growth"
      title="Growth Lab"
      subtitle="Experiments, learnings, backlog"
      source={payload.source}
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Active experiments" value={payload.data.experiments_active ?? "—"} />
        <MetricCard label="Wins (30d)" value={payload.data.experiments_won_30d ?? "—"} />
        <MetricCard label="Killed (30d)" value={payload.data.experiments_killed_30d ?? "—"} />
      </div>

      <SectionHeading title="Experiment backlog" />
      <BrandCard>
        <PlaceholderTable
          columns={["Hypothesis", "Stage", "Owner", "Decision date"]}
        />
      </BrandCard>

      <SectionHeading title="Growth principles" />
      <BrandCard>
        <SafeList
          items={[
            "Every experiment writes back to the learning loop.",
            "No vanity metrics on the founder console.",
            "Cut losers within a defined deadline; double down on winners.",
            "Growth is built on proof — no proof, no scaling.",
          ]}
        />
      </BrandCard>
    </ConsolePage>
  );
}
