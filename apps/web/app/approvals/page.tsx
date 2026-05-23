import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getApprovals } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ApprovalsPage() {
  const data = await getApprovals();
  const items = (data as { items?: Array<Record<string, string>> }).items ?? [];
  return (
    <FounderShell title="Approvals" source={data.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Pending approvals <SourceBadge source={data.source} />
        </h2>
        {items.length === 0 ? (
          <p>No pending approvals. (Drafts queued by agents will appear here.)</p>
        ) : (
          <ul>
            {items.map((row, i) => (
              <li key={row.id ?? i} style={{ marginBottom: 12 }}>
                <strong>{row.id ?? `approval-${i}`}</strong> — class {row.class ?? "A?"}
                <div style={{ color: "#475569" }}>{row.summary ?? row.payload ?? ""}</div>
                <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
                  <code>POST /api/v1/internal/approvals/{row.id}/approve</code>
                  <code>POST /api/v1/internal/approvals/{row.id}/reject</code>
                </div>
              </li>
            ))}
          </ul>
        )}
        <p style={{ color: "#64748b", marginTop: 16 }}>
          Action buttons call <code>lib/dealix-actions.ts</code> which posts to the
          internal API. No external send happens from this page.
        </p>
      </div>
    </FounderShell>
  );
}
