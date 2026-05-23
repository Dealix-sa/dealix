import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { StatusBadge } from "../../components/brand/status-badge";
import { getExperimentBacklog } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ExperimentsPage() {
  const res = await getExperimentBacklog();
  return (
    <FounderShell title="Experiments">
      <BrandCard title="Experiment backlog" source={res.source}>
        {res.data.items.length === 0 ? (
          <p style={{ color: "var(--dealix-soft-silver)" }}>No experiments yet. Draft one via the performance analyst agent.</p>
        ) : (
          <table className="dealix-table">
            <thead>
              <tr>
                <th>Id</th>
                <th>Hypothesis</th>
                <th>Owner</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {res.data.items.map((e) => (
                <tr key={e.id}>
                  <td>{e.id}</td>
                  <td>{e.hypothesis}</td>
                  <td>{e.owner}</td>
                  <td>
                    <StatusBadge tone={e.status === "shipped" ? "ok" : "warn"}>{e.status}</StatusBadge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </BrandCard>
    </FounderShell>
  );
}
