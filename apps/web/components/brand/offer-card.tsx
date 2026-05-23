import { BrandCard } from "./brand-card";
import { CTAButton } from "./cta-button";

export function OfferCard({
  name,
  positioning,
  scope,
  outcome,
}: {
  name: string;
  positioning: string;
  scope: string;
  outcome: string;
}) {
  return (
    <BrandCard title={name} subtitle={positioning}>
      <p style={{ color: "var(--dealix-white)", margin: "0 0 8px" }}>{scope}</p>
      <p style={{ color: "var(--dealix-soft-silver)", margin: "0 0 12px", fontSize: 13 }}>{outcome}</p>
      <CTAButton variant="secondary">Request brief</CTAButton>
    </BrandCard>
  );
}
