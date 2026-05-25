import type { TrustFlag } from "../../lib/types";

function pillFor(decision: TrustFlag["decision"]): string {
  if (decision === "ALLOW") return "pill pill-ok";
  if (decision === "DENY") return "pill pill-danger";
  return "pill pill-warn";
}

export function TrustFlagList({ flags }: { flags: TrustFlag[] }) {
  return (
    <div className="card">
      <h2>Trust Plane Decisions</h2>
      {flags.length === 0 ? (
        <p style={{ margin: 0, opacity: 0.7 }}>لا توجد إشارات Trust حالياً.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th align="left">ID</th>
              <th align="left">Decision</th>
              <th align="left">Rule</th>
              <th align="left">Actor</th>
              <th align="left">Reason</th>
              <th align="left">At</th>
            </tr>
          </thead>
          <tbody>
            {flags.map((f) => (
              <tr key={f.id}>
                <td>{f.id}</td>
                <td>
                  <span className={pillFor(f.decision)}>{f.decision}</span>
                </td>
                <td>{f.rule}</td>
                <td>{f.actor}</td>
                <td>{f.reason}</td>
                <td>{f.at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
