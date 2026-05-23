import { FounderShell } from "../../components/founder-shell";
import { getApprovals } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ApprovalsPage() {
  const items = await getApprovals();
  return (
    <FounderShell>
      <main>
        <h1>Approvals</h1>
        <p>
          A1/A2/A3 approval inbox. Every decision writes audit; A2 needs Sami; A3 cannot be
          automated and must escalate to a human action.
        </p>
        <section className="founder-callout">
          <p className="founder-callout__label">Pending</p>
          <p className="founder-callout__title">{items.length}</p>
          <p className="founder-source">
            Items load from <code>/api/v1/internal/approvals</code>. When the queue is wired, each
            row exposes approve, reject, and request-edit through the audited action endpoints.
          </p>
        </section>
        {items.length === 0 ? (
          <p className="founder-source" style={{ marginTop: 16 }}>
            No pending approvals. Queue source: internal API.
          </p>
        ) : (
          <section className="founder-metric-grid">
            {items.map((item) => (
              <article key={item.id} className="founder-metric">
                <p className="founder-metric__label">
                  {item.approval_class} · {item.risk_level}
                </p>
                <p className="founder-metric__value" style={{ fontSize: 18 }}>
                  {item.company}
                </p>
                <p>{item.summary}</p>
                <p className="founder-source">Type: {item.type} · Status: {item.status}</p>
              </article>
            ))}
          </section>
        )}
      </main>
    </FounderShell>
  );
}
