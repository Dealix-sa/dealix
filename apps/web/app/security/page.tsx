import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getSecurityStatus } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SecurityPage() {
  const s = await getSecurityStatus();
  const checks = (s as { checks?: Array<Record<string, string>> }).checks ?? [];
  return (
    <FounderShell title="Security" source={s.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Production Gates <SourceBadge source={s.source} />
        </h2>
        <ul>
          <li>Internal token set: <strong>{String(s.internal_token_set)}</strong></li>
          <li>Private ops env set: <strong>{String(s.private_ops_env_set)}</strong></li>
          <li>Private ops path: <code>{s.private_ops_path}</code></li>
        </ul>
        {checks.length > 0 && (
          <>
            <h3>Detailed checks</h3>
            <ul>{checks.map((c, i) => <li key={i}>{c.check}: {c.status}</li>)}</ul>
          </>
        )}
      </div>
    </FounderShell>
  );
}
