import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getEvalStatus } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function EvalsPage() {
  const data = await getEvalStatus();
  const suites = (data as { suites?: Array<Record<string, string>> }).suites ?? [];
  const results = (data as { results?: Array<Record<string, string>> }).results ?? [];
  return (
    <FounderShell title="Evals" source={data.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Eval Gate <SourceBadge source={data.source} />
        </h2>
        <p>Configured suites: {suites.length}</p>
        <ul>
          {suites.map((s, i) => (
            <li key={i}>
              <strong>{s.id}</strong>
              {s.severity ? ` — severity ${s.severity}` : ""}
              {s.description ? ` — ${s.description}` : ""}
            </li>
          ))}
        </ul>
      </div>
      <div className="card">
        <h2>Recent Eval Results</h2>
        {results.length === 0 ? <p>No eval runs recorded.</p> : (
          <ul>{results.map((r, i) => <li key={i}>{r.suite ?? r.id} — {r.status}</li>)}</ul>
        )}
      </div>
    </FounderShell>
  );
}
