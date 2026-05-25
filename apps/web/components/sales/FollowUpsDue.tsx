import type { FollowUp } from "../../lib/types";

export function FollowUpsDue({ items }: { items: FollowUp[] }) {
  return (
    <div className="card">
      <h2>Follow-ups Due</h2>
      {items.length === 0 ? (
        <p style={{ margin: 0, opacity: 0.7 }}>لا توجد متابعات مستحقة الآن.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th align="left">Lead</th>
              <th align="left">Company</th>
              <th align="left">Channel</th>
              <th align="left">Due</th>
            </tr>
          </thead>
          <tbody>
            {items.map((f) => (
              <tr key={f.leadId}>
                <td>{f.leadId}</td>
                <td>{f.company}</td>
                <td>{f.channel}</td>
                <td>{f.dueAt}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
