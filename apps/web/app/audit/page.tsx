import { FounderShell } from "../../components/founder-shell";
import { getAuditEvents } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function AuditPage() {
  const data = await getAuditEvents();
  return (
    <FounderShell title="Audit" source={data.source}>
      <section className="card">
        <h2>Approval decisions</h2>
        <table>
          <thead>
            <tr>
              <th>Decided at</th>
              <th>Approval ID</th>
              <th>Decision</th>
              <th>By</th>
              <th>Policy class</th>
              <th>Reason</th>
            </tr>
          </thead>
          <tbody>
            {data.events.length === 0 ? (
              <tr>
                <td colSpan={6}>No audit events recorded.</td>
              </tr>
            ) : (
              data.events.map((row, i) => (
                <tr key={`${row.id ?? i}`}>
                  <td>{row.decided_at}</td>
                  <td>{row.approval_id}</td>
                  <td>{row.decision}</td>
                  <td>{row.decided_by}</td>
                  <td>{row.policy_class}</td>
                  <td>{row.reason}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </FounderShell>
  );
}
