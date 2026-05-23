import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { StatusBadge } from "../../components/brand/status-badge";
import { getDeliveryQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DeliveryPage() {
  const res = await getDeliveryQueue();
  return (
    <FounderShell title="Delivery">
      <BrandCard title="Delivery queue" subtitle="Sprints awaiting execution" source={res.source}>
        {res.data.items.length === 0 ? (
          <p style={{ color: "var(--dealix-soft-silver)" }}>Queue empty.</p>
        ) : (
          <table className="dealix-table">
            <thead>
              <tr>
                <th>Id</th>
                <th>Client</th>
                <th>Sprint</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {res.data.items.map((i) => (
                <tr key={i.id}>
                  <td>{i.id}</td>
                  <td>{i.client}</td>
                  <td>{i.sprint}</td>
                  <td>
                    <StatusBadge tone={i.status === "done" ? "ok" : "warn"}>{i.status}</StatusBadge>
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
