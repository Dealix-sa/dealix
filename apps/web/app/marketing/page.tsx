import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { getMarketingSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function MarketingPage() {
  const res = await getMarketingSummary();
  const d = res.data;
  return (
    <FounderShell title="Marketing">
      <BrandCard title="Marketing summary" source={res.source}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 12 }}>
          <MetricCard label="Campaigns" value={d.campaigns} />
          <MetricCard label="Content in pipeline" value={d.content_in_pipeline} />
        </div>
        {d.calendar_next_7_days.length > 0 && (
          <table className="dealix-table" style={{ marginTop: 16 }}>
            <thead>
              <tr>
                <th>Day</th>
                <th>Topic</th>
              </tr>
            </thead>
            <tbody>
              {d.calendar_next_7_days.map((c, i) => (
                <tr key={i}>
                  <td>{c.day}</td>
                  <td>{c.topic}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </BrandCard>
    </FounderShell>
  );
}
