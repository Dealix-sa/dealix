import { FounderShell } from "../../components/founder-shell";
import { getProofLibrary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ProofPage() {
  const data = await getProofLibrary();
  return (
    <FounderShell title="Proof Library" source={data.source}>
      <section className="card">
        <h2>Approved proof artifacts</h2>
        <p className="muted">
          Nothing is published publicly until the founder approves it.
          This view shows the staging area only. Publishing is an A3
          action in the policy file.
        </p>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Status</th>
              <th>Approver</th>
            </tr>
          </thead>
          <tbody>
            {data.items.length === 0 ? (
              <tr>
                <td colSpan={4}>No proof artifacts staged.</td>
              </tr>
            ) : (
              data.items.map((row, i) => (
                <tr key={`${row.id ?? i}`}>
                  <td>{row.id}</td>
                  <td>{row.title}</td>
                  <td>{row.status}</td>
                  <td>{row.approver}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </FounderShell>
  );
}
