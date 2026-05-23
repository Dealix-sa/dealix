import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { getDistributionSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DistributionPage() {
  const res = await getDistributionSummary();
  return (
    <FounderShell title="Distribution">
      <BrandCard title="Channel scorecard" source={res.source}>
        {(res.data.channels?.length ?? 0) === 0 ? (
          <p style={{ color: "var(--dealix-soft-silver)" }}>No channels recorded yet.</p>
        ) : (
          <pre style={{ color: "var(--dealix-soft-silver)", overflowX: "auto" }}>
            {JSON.stringify(res.data.channels, null, 2)}
          </pre>
        )}
      </BrandCard>
      <BrandCard title="Sector scorecard">
        {(res.data.sectors?.length ?? 0) === 0 ? (
          <p style={{ color: "var(--dealix-soft-silver)" }}>No sectors recorded yet.</p>
        ) : (
          <pre style={{ color: "var(--dealix-soft-silver)", overflowX: "auto" }}>
            {JSON.stringify(res.data.sectors, null, 2)}
          </pre>
        )}
      </BrandCard>
    </FounderShell>
  );
}
