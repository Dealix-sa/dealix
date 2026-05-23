import { FounderShell } from "../../components/founder-shell";
import { getRetentionQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function RetentionPage() {
  const queue = await getRetentionQueue();
  return (
    <FounderShell>
      <main>
        <h1>Retention</h1>
        <p>Renewal queue, NPS detractors, churn risk, expansion candidates.</p>
        <section className="founder-metric-grid">
          <div className="founder-metric">
            <p className="founder-metric__label">Open Items</p>
            <p className="founder-metric__value">{queue.length}</p>
          </div>
        </section>
        {queue.length === 0 ? (
          <p className="founder-source" style={{ marginTop: 16 }}>
            No retention work pending. Source: <code>/api/v1/internal/retention/queue</code>.
          </p>
        ) : null}
      </main>
    </FounderShell>
  );
}
