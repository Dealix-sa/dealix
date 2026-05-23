import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getRetentionQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function RetentionPage() {
  const data = await getRetentionQueue();
  const items = (data as { items?: Array<Record<string, string>> }).items ?? [];
  return (
    <FounderShell title="Retention" source={data.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Retention Queue <SourceBadge source={data.source} />
        </h2>
        {items.length === 0 ? <p>No retention items.</p> : (
          <ul>
            {items.map((it, i) => (
              <li key={i}>
                <strong>{it.customer ?? `customer-${i}`}</strong> — health: {it.health ?? "?"} — action: {it.next_action ?? ""}
              </li>
            ))}
          </ul>
        )}
      </div>
    </FounderShell>
  );
}
