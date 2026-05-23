import type { ApprovalItem } from "../../lib/types";

function pillClass(state: ApprovalItem["state"]): string {
  if (state === "approved") return "pill pill-ok";
  if (state === "rejected" || state === "expired") return "pill pill-danger";
  return "pill pill-warn";
}

export function ApprovalsList({ items }: { items: ApprovalItem[] }) {
  return (
    <div className="card">
      <h2>Approval Inbox</h2>
      {items.length === 0 ? (
        <p style={{ margin: 0, opacity: 0.7 }}>لا توجد طلبات معلّقة.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th align="left">Ticket</th>
              <th align="left">Action</th>
              <th align="left">Requested by</th>
              <th align="left">Risk</th>
              <th align="left">State</th>
              <th align="left">Decide</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.ticketId}>
                <td>{item.ticketId}</td>
                <td>{item.actionType}</td>
                <td>{item.requestedBy}</td>
                <td>{item.riskClass}</td>
                <td>
                  <span className={pillClass(item.state)}>{item.state}</span>
                </td>
                <td>
                  <div style={{ display: "flex", gap: 6 }}>
                    <button type="button" disabled>Approve</button>
                    <button type="button" disabled>Reject</button>
                    <button type="button" disabled>Edit</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <p style={{ marginTop: 12, fontSize: 12, opacity: 0.65 }}>
        Approval actions wired to <code>/api/v1/approvals</code>. UI buttons are disabled until live binding.
      </p>
    </div>
  );
}
