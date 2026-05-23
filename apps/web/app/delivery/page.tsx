import { FounderShell } from "../../components/founder-shell";
import { getDeliveryQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DeliveryPage() {
  const queue = await getDeliveryQueue();
  return (
    <FounderShell>
      <main className="p-8">
        <h1 className="text-4xl font-bold">Delivery</h1>
        <p className="mt-2 max-w-3xl">
          Active sprints, data packs, and managed-ops engagements moving
          through the delivery queue.
        </p>
        <section className="mt-8 rounded-2xl border p-6">
          {queue.length === 0 ? (
            <p>No active delivery items.</p>
          ) : (
            <ul className="grid gap-3">
              {queue.map((item) => (
                <li key={item.id} className="rounded-xl border p-4">
                  <p className="font-semibold">{item.customer}</p>
                  <p>{item.offer}</p>
                  <p className="text-sm">Due: {item.due_date}</p>
                  <p className="text-sm">Status: {item.status}</p>
                </li>
              ))}
            </ul>
          )}
        </section>
        <p className="mt-6 text-xs">
          Source: delivery_queue · Endpoint: /api/v1/internal/delivery/queue
        </p>
      </main>
    </FounderShell>
  );
}
