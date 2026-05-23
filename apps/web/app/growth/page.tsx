import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { getGrowthTargeting } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function GrowthPage() {
  const res = await getGrowthTargeting();
  return (
    <FounderShell title="Growth · Targeting">
      <BrandCard title="Sector targets" subtitle="From growth/sector_targets.csv" source={res.source}>
        {res.data.segments.length === 0 ? (
          <p style={{ color: "var(--dealix-soft-silver)" }}>No sector targets yet. Seed via the growth strategist agent.</p>
        ) : (
          <table className="dealix-table">
            <thead>
              <tr>
                <th>Sector</th>
                <th>Priority</th>
                <th>Accounts</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {res.data.segments.map((s) => (
                <tr key={s.sector}>
                  <td>{s.sector}</td>
                  <td>{s.priority}</td>
                  <td>{s.accounts}</td>
                  <td>{s.score.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </BrandCard>
    </FounderShell>
  );
}
