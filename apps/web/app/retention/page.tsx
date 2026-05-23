import { FounderShell } from "../../components/founder-shell";

export const dynamic = "force-dynamic";

export default function RetentionPage() {
  return (
    <FounderShell title="Retention Center">
      <p className="lead">
        Track health scores, retainer asks, renewals, referrals, and
        expansion. Wires in Phase 2 of the runtime binding plan.
      </p>
      <section className="card">No retention queue connected yet.</section>
    </FounderShell>
  );
}
