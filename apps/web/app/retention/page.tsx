import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { StatusBadge } from "../../components/brand/status-badge";
import { getRetentionQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function RetentionPage() {
  const res = await getRetentionQueue();
  return (
    <FounderShell title="Retention">
      <BrandCard title="Retention queue" subtitle="Clients with next actions" source={res.source}>
        {res.data.items.length === 0 ? (
          <p style={{ color: "var(--dealix-soft-silver)" }}>No retention actions pending.</p>
        ) : (
          <table className="dealix-table">
            <thead>
              <tr>
                <th>Client</th>
                <th>Health</th>
                <th>Next action</th>
                <th>Due</th>
              </tr>
            </thead>
            <tbody>
              {res.data.items.map((i) => (
                <tr key={i.client}>
                  <td>{i.client}</td>
                  <td>
                    <StatusBadge tone={i.health === "green" ? "ok" : i.health === "red" ? "danger" : "warn"}>
                      {i.health}
                    </StatusBadge>
                  </td>
                  <td>{i.next_action}</td>
                  <td>{i.due}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </BrandCard>
    </FounderShell>
  );
}
