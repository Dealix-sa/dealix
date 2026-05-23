import {
  ConsolePage,
  PlaceholderTable,
  SafeList,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { loadInternal } from "../../lib/runtime-client";

type ProductSummary = {
  ladder_active: number | null;
  candidates_in_review: number | null;
  retainers_live: number | null;
};

const ladder = [
  "1. Free Sample / Diagnostic",
  "2. Revenue Sprint",
  "3. Managed Pilot",
  "4. Revenue Desk Retainer",
  "5. Founder Console / Command Center",
  "6. Enterprise Revenue Intelligence OS",
  "7. Partner / White-label Revenue OS",
];

export default async function ProductPage() {
  const payload = await loadInternal<ProductSummary>(
    "/api/v1/internal/founder/product",
    { ladder_active: ladder.length, candidates_in_review: null, retainers_live: null }
  );

  return (
    <ConsolePage
      active="/product"
      title="Product Ladder"
      subtitle="Rungs, packaging, pricing guardrails"
      source={payload.source}
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Rungs active" value={payload.data.ladder_active ?? ladder.length} />
        <MetricCard label="Candidates in review" value={payload.data.candidates_in_review ?? "—"} />
        <MetricCard label="Retainers live" value={payload.data.retainers_live ?? "—"} />
      </div>

      <SectionHeading title="Offer ladder" />
      <BrandCard>
        <SafeList items={ladder} />
      </BrandCard>

      <SectionHeading title="Pricing guardrails" />
      <BrandCard>
        <SafeList
          items={[
            "No discount commits without A2 approval.",
            "No pricing or contract terms in autoreply.",
            "Every offer has price band, objections, and proof requirement.",
            "Custom pricing requires margin + delivery review.",
          ]}
        />
      </BrandCard>

      <SectionHeading title="Productization candidates" />
      <BrandCard>
        <PlaceholderTable columns={["Candidate", "Origin", "Stage", "Owner"]} />
      </BrandCard>
    </ConsolePage>
  );
}
