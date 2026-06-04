import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Services — What We Deliver',
  description: 'Dealix services across the first five verticals — review-only AI ops, delivered with founder oversight.',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>Services</h1>
      <p>We focus on five verticals where manual revenue/ops work is heaviest:</p>
      <ul>
      <li><a href="/verticals/facilities-management">Facilities Management & Maintenance</a> — Reduce manual work-order triage and SLA reporting across multiple sites.</li>
      <li><a href="/verticals/contracting-project-controls">Contracting & Project Controls</a> — Cut manual progress, cost, and variation reporting across active projects.</li>
      <li><a href="/verticals/real-estate-property-ops">Real Estate & Property Operations</a> — Streamline tenant requests, lease tracking, and owner reporting.</li>
      <li><a href="/verticals/legal-professional-services">Legal & Professional Services</a> — Speed up intake, matter reporting, and document draft prep — review-only.</li>
      <li><a href="/verticals/consulting-training-b2b">Consulting, Training & B2B Services</a> — Tighten pipeline, proposal turnaround, and engagement reporting.</li>
      </ul>
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        <strong>Safety:</strong> AI prepares and recommends; you approve and act. Nothing is sent or submitted automatically. No ROI guarantees — we show evidence and estimates.
      </p>
    </main>
  );
}
