import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getProofLibrary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ProofPage() {
  const data = await getProofLibrary();
  const items = (data as { items?: Array<Record<string, string>> }).items ?? [];
  return (
    <FounderShell title="Proof" source={data.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Proof Library <SourceBadge source={data.source} />
        </h2>
        {items.length === 0 ? <p>No proof items yet.</p> : (
          <ul>
            {items.map((p, i) => (
              <li key={i}>
                <strong>{p.title ?? `proof-${i}`}</strong> — {p.status ?? ""}
                {p.anonymized === "true" ? " (anonymized)" : ""}
              </li>
            ))}
          </ul>
        )}
        <p style={{ color: "#64748b" }}>
          Public proof requires explicit A3 founder approval. No proof is published from this UI.
        </p>
      </div>
    </FounderShell>
  );
}
