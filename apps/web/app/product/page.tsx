import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { OfferCard } from "../../components/brand/offer-card";
import { getProductization } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

const FALLBACK_LADDER = [
  { rung: "1", name: "Free Sample / Diagnostic", positioning: "Show, don't tell." },
  { rung: "2", name: "Revenue Sprint", positioning: "5–10 day focused engagement." },
  { rung: "3", name: "Managed Pilot", positioning: "Pilot one motion end-to-end." },
  { rung: "4", name: "Revenue Desk Retainer", positioning: "Managed revenue ops monthly." },
  { rung: "5", name: "Founder Console", positioning: "Operating cockpit for the customer." },
  { rung: "6", name: "Enterprise Revenue Intelligence OS", positioning: "Full org rollout." },
  { rung: "7", name: "Partner / White-label Revenue OS", positioning: "Channel partner expansion." },
];

export default async function ProductPage() {
  const res = await getProductization();
  const ladder = res.data.ladder?.length ? res.data.ladder : FALLBACK_LADDER;
  return (
    <FounderShell title="Product · Offer Ladder">
      <BrandCard
        title="Dealix Offer Ladder"
        subtitle="Trust-gated. No guaranteed outcomes promised externally."
        source={res.source}
      >
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 12 }}>
          {ladder.map((o: { rung: string; name: string; positioning?: string }) => (
            <OfferCard
              key={o.rung}
              name={o.name}
              positioning={`Rung ${o.rung}`}
              scope={o.positioning ?? ""}
              outcome="Approved, scoped, observable; no guaranteed outcome claims."
            />
          ))}
        </div>
      </BrandCard>
    </FounderShell>
  );
}
