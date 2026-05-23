import { FounderShell } from "../../components/founder-shell";
import { getRetentionQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function RetentionPage() {
  const queue = await getRetentionQueue();
  return (
    <FounderShell>
      <main className="p-8">
        <h1 className="text-4xl font-bold">Retention</h1>
        <p className="mt-2 max-w-3xl">
          Renewals due and accounts flagged as churn risk. Act here
          before they show up in the finance dashboard as lost cash.
        </p>
        <section className="mt-8 rounded-2xl border p-6">
          {queue.length === 0 ? (
            <p>No retention items in the queue.</p>
          ) : (
            <ul className="grid gap-3">
              {queue.map((item) => (
                <li key={item.id} className="rounded-xl border p-4">
                  <p className="font-semibold">{item.customer}</p>
                  <p className="text-sm">Renewal due: {item.renewal_due}</p>
                  <p className="text-sm">Risk: {item.risk}</p>
                </li>
              ))}
            </ul>
          )}
        </section>
        <p className="mt-6 text-xs">
          Source: retention_queue · Endpoint: /api/v1/internal/retention/queue
        </p>
      </main>
    </FounderShell>
  );
}
