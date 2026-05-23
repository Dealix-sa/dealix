import { FounderShell } from "../../components/founder-shell";
import { getApprovals } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ApprovalsPage() {
  const data = await getApprovals();
  return (
    <FounderShell title="Approvals" source={data.source}>
      <section className="card">
        <h2>Approval queue</h2>
        <p className="muted">
          Decisions are recorded in <code>trust/approval_decisions.csv</code>.
          No external send happens until the founder approves here.
        </p>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Action</th>
              <th>Target</th>
              <th>Status</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {data.approvals.length === 0 ? (
              <tr>
                <td colSpan={5}>Queue is empty.</td>
              </tr>
            ) : (
              data.approvals.map((row) => (
                <tr key={row.id}>
                  <td>{row.id}</td>
                  <td>{row.action ?? row.action_type ?? "—"}</td>
                  <td>{row.target ?? row.entity ?? "—"}</td>
                  <td>{row.status ?? "—"}</td>
                  <td>{row.created_at ?? "—"}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </FounderShell>
  );
}
