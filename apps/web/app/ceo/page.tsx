import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getCEOSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function CEOPage() {
  const s = await getCEOSummary();
  return (
    <FounderShell title="CEO" source={s.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Top Action <SourceBadge source={s.source} />
        </h2>
        <p style={{ fontSize: 18 }}>{s.top_action}</p>
        <p>
          Status: <strong>{s.status}</strong>
        </p>
        {Array.isArray(s.risk_flags) && s.risk_flags.length > 0 ? (
          <p>Risk flags: {s.risk_flags.join(", ")}</p>
        ) : null}
      </div>
      <div className="card">
        <h2>Today</h2>
        <ul>
          <li>Leads: {s.leads}</li>
          <li>Approved outreach: {s.approved_outreach}</li>
          <li>Positive replies: {s.positive_replies}</li>
          <li>Proposals due: {s.proposals_due}</li>
          <li>Payment follow-ups: {s.payment_followups}</li>
          <li>Worker failures (24h): {s.worker_failures}</li>
          <li>Cash collected: {s.cash_collected}</li>
        </ul>
      </div>
    </FounderShell>
  );
}
