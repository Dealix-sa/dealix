import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { StatusBadge } from "../../components/brand/status-badge";
import { getAuditEvents } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function AuditPage() {
  const res = await getAuditEvents();
  return (
    <FounderShell title="Audit Trail">
      <BrandCard title="Audit events" subtitle="From trust/approval_decisions.csv" source={res.source}>
        {res.data.items.length === 0 ? (
          <p style={{ color: "var(--dealix-soft-silver)" }}>No audit events yet.</p>
        ) : (
          <table className="dealix-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Actor</th>
                <th>Action</th>
                <th>Risk</th>
              </tr>
            </thead>
            <tbody>
              {res.data.items.map((e) => (
                <tr key={e.id}>
                  <td>{e.ts}</td>
                  <td>{e.actor}</td>
                  <td>{e.action}</td>
                  <td>
                    <StatusBadge tone={e.risk === "high" ? "danger" : e.risk === "medium" ? "warn" : "ok"}>
                      {e.risk}
                    </StatusBadge>
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
