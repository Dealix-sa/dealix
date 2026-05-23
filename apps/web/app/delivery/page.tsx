import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getDeliveryQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DeliveryPage() {
  const data = await getDeliveryQueue();
  const items = (data as { items?: Array<Record<string, string>> }).items ?? [];
  return (
    <FounderShell title="Delivery" source={data.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Delivery Queue <SourceBadge source={data.source} />
        </h2>
        {items.length === 0 ? <p>No delivery items.</p> : (
          <ul>
            {items.map((it, i) => (
              <li key={i}><strong>{it.id ?? `item-${i}`}</strong> — {it.stage ?? ""} ({it.status ?? ""})</li>
            ))}
          </ul>
        )}
      </div>
    </FounderShell>
  );
}
