import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getTrustFlags } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function TrustPage() {
  const data = await getTrustFlags();
  const flags = (data as { flags?: Array<Record<string, string>> }).flags ?? [];
  return (
    <FounderShell title="Trust" source={data.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Trust Flags <SourceBadge source={data.source} />
        </h2>
        {flags.length === 0 ? <p>No trust flags raised.</p> : (
          <ul>
            {flags.map((f, i) => (
              <li key={i}>
                <strong>{f.type ?? "flag"}</strong>: {f.detail ?? f.message ?? ""}
                {f.severity ? ` (severity: ${f.severity})` : ""}
              </li>
            ))}
          </ul>
        )}
      </div>
    </FounderShell>
  );
}
