import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getAuditEvents } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function AuditPage() {
  const data = await getAuditEvents();
  const events = (data as { events?: Array<Record<string, string>> }).events ?? [];
  return (
    <FounderShell title="Audit" source={data.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Approval / Audit log <SourceBadge source={data.source} />
        </h2>
        {events.length === 0 ? <p>No audit events yet.</p> : (
          <ol>
            {events.map((e, i) => (
              <li key={i}>
                <code>{e.decided_at}</code> — <strong>{e.decision}</strong> — id <code>{e.id}</code> — {e.reason}
              </li>
            ))}
          </ol>
        )}
      </div>
    </FounderShell>
  );
}
