import { getLaunchSummary } from "../../lib/internal-client";

export const dynamic = "force-dynamic";

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="card" style={{ marginBottom: 12 }}>
      <h2 style={{ marginTop: 0, fontSize: 18 }}>{title}</h2>
      {children}
    </section>
  );
}

function Score({ value, decision }: { value: number | null; decision: string | null }) {
  const pct = value != null ? Math.round(value * 100) : null;
  const tone =
    decision === "PASS" ? "#16a34a" : decision === "HOLD" ? "#f59e0b" : "#dc2626";
  return (
    <div style={{ display: "flex", alignItems: "baseline", gap: 16 }}>
      <div style={{ fontSize: 36, fontWeight: 600, color: tone }}>
        {pct == null ? "—" : `${pct}%`}
      </div>
      <div style={{ color: tone, fontWeight: 600 }}>
        {decision ?? "unknown"}
      </div>
    </div>
  );
}

export default async function LaunchPage() {
  const data = await getLaunchSummary();
  return (
    <main className="grid">
      <h1>Launch Command Center</h1>
      <p style={{ marginTop: -8, color: "#64748b" }}>
        Source: <strong>{data.source}</strong>
        {data.reason ? ` — ${data.reason}` : ""}
      </p>

      <Section title="Readiness">
        <Score value={data.readiness_score} decision={data.readiness_decision} />
      </Section>

      <Section title="Top CEO Action — أهم action لليوم">
        <p style={{ margin: 0 }}>{data.next_ceo_action ?? "—"}</p>
      </Section>

      <Section title="Launch Blockers">
        {data.launch_blockers.length === 0 ? (
          <p style={{ margin: 0 }}>No open blockers.</p>
        ) : (
          <ul>
            {data.launch_blockers.map((b, i) => (
              <li key={b.id ?? i}>
                <strong>[{b.severity ?? "?"}] {b.id ?? `B${i}`}</strong> — {b.description}
              </li>
            ))}
          </ul>
        )}
      </Section>

      <Section title="Active Campaign">
        <pre style={{ whiteSpace: "pre-wrap", margin: 0, fontSize: 13 }}>
          {data.active_campaign ?? "— (none active)"}
        </pre>
      </Section>

      <Section title="Target Sector">
        <pre style={{ whiteSpace: "pre-wrap", margin: 0, fontSize: 13 }}>
          {data.target_sector ?? "— (no sector configured)"}
        </pre>
      </Section>

      <Section title="Approved Assets">
        {data.approved_assets.length === 0 ? (
          <p style={{ margin: 0 }}>None approved yet.</p>
        ) : (
          <ul>
            {data.approved_assets.map((a, i) => (
              <li key={a.id ?? i}>
                {a.id ?? "?"} — {a.name} ({a.status ?? "?"})
              </li>
            ))}
          </ul>
        )}
      </Section>

      <Section title="Distribution Queues">
        <pre style={{ whiteSpace: "pre-wrap", margin: 0, fontSize: 12 }}>
          {JSON.stringify(data.distribution_queues, null, 2)}
        </pre>
      </Section>

      <Section title="Trust Risks (high+)">
        {data.trust_risks.length === 0 ? (
          <p style={{ margin: 0 }}>No high or critical risks open.</p>
        ) : (
          <ul>
            {data.trust_risks.map((r, i) => (
              <li key={r.id ?? i}>
                <strong>[{r.severity}] {r.id}</strong> — {r.description} ({r.status})
              </li>
            ))}
          </ul>
        )}
      </Section>

      <Section title="Revenue Forecast">
        <pre style={{ whiteSpace: "pre-wrap", margin: 0, fontSize: 12 }}>
          {data.revenue_forecast ?? "— (run `make revenue-forecast`)"}
        </pre>
      </Section>

      <p style={{ color: "#64748b", fontSize: 12 }}>
        No guaranteed revenue, sales, or meetings are claimed on this page. All
        numbers reflect observed-only state from <code>&lt;private_ops&gt;</code>.
      </p>
    </main>
  );
}
