import { FounderShell } from "../../components/founder-shell";

export const dynamic = "force-dynamic";

export default function DeliveryPage() {
  return (
    <FounderShell title="Delivery Center">
      <p className="lead">
        Track paid or approved delivery work, QA, handoff, and client
        feedback. Wires in Phase 2 of the runtime binding plan.
      </p>
      <section className="card">No delivery queue connected yet.</section>
    </FounderShell>
  );
}
