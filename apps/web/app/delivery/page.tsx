import { FounderShell } from "../../components/founder-shell";
import { getDeliveryQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DeliveryPage() {
  const queue = await getDeliveryQueue();
  return (
    <FounderShell>
      <main>
        <h1>Delivery</h1>
        <p>Active sprints, deliverable state, on-time delivery, blockers.</p>
        <section className="founder-metric-grid">
          <div className="founder-metric">
            <p className="founder-metric__label">Active Items</p>
            <p className="founder-metric__value">{queue.length}</p>
          </div>
        </section>
        {queue.length === 0 ? (
          <p className="founder-source" style={{ marginTop: 16 }}>
            No active delivery items. Source: <code>/api/v1/internal/delivery/queue</code>.
          </p>
        ) : null}
      </main>
    </FounderShell>
  );
}
