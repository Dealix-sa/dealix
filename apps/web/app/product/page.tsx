import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getProductization } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ProductPage() {
  const data = await getProductization();
  const cands = (data as { candidates?: Array<Record<string, string>> }).candidates ?? [];
  return (
    <FounderShell title="Productization" source={data.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Productization Candidates <SourceBadge source={data.source} />
        </h2>
        {cands.length === 0 ? <p>No candidates yet.</p> : (
          <ul>
            {cands.map((c, i) => (
              <li key={i}>
                <strong>{c.name ?? `candidate-${i}`}</strong> — repeats: {c.repeats ?? "?"} — owner: {c.owner ?? ""}
              </li>
            ))}
          </ul>
        )}
      </div>
    </FounderShell>
  );
}
