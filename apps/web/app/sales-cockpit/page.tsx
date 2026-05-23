import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { getSalesFunnel } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SalesCockpitPage() {
  const res = await getSalesFunnel();
  return (
    <FounderShell title="Sales Cockpit">
      <BrandCard title="Funnel by stage" subtitle="Counts read from conversation_log.csv" source={res.source}>
        <table className="dealix-table">
          <thead>
            <tr>
              <th>Stage</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            {res.data.stages.map((s) => (
              <tr key={s.stage}>
                <td>{s.stage}</td>
                <td>{s.count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </BrandCard>
    </FounderShell>
  );
}
