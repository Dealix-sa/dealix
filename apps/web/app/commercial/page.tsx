import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Commercial — Offers & Approach',
  description: 'Dealix commercial offers: review-only AI workflow audits, pilots, department OS, retainers. SAR pricing.',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>Commercial</h1>
      <p>A trust-first path from a low-risk diagnostic to ongoing delivery — always review-only.</p>
      <h2>Offer ladder (SAR)</h2>
      <ul>
      <li><strong>AI Workflow Audit</strong> — 499–2,500 SAR: Review-only diagnostic of one workflow with prioritized fixes.</li>
      <li><strong>Paid Pilot</strong> — 5,000–25,000 SAR: Scoped, time-boxed proof on one workflow.</li>
      <li><strong>Department OS</strong> — 25,000–150,000 SAR: An operating system for one department.</li>
      <li><strong>Monthly Retainer</strong> — 3,000–25,000 SAR/month: Ongoing draft, review, and delivery ops.</li>
      <li><strong>Enterprise Custom OS</strong> — 150,000+ SAR: Multi-department, custom integrations.</li>
      </ul>
      <p><a href="/pricing">Pricing details →</a> · <a href="/contact">Request an audit →</a></p>
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        <strong>Safety:</strong> AI prepares and recommends; you approve and act. Nothing is sent or submitted automatically. No ROI guarantees — we show evidence and estimates.
      </p>
    </main>
  );
}
