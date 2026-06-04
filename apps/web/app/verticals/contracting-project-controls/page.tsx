import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Contracting & Project Controls — Dealix',
  description: 'Dealix for Contracting & Project Controls: review-only AI ops that reduce manual work. Cut manual progress, cost, and variation reporting across active projects.',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>Contracting & Project Controls</h1>
      <p dir="rtl" lang="ar">المقاولات وضبط المشاريع</p>
      <p>Cut manual progress, cost, and variation reporting across active projects.</p>
      <h2>What we prepare (review-only)</h2>
      <ul>
      <li>Workflow audit findings and prioritized fixes.</li>
      <li>Drafted communications you approve and send manually.</li>
      <li>Reporting templates and evidence capture.</li>
      </ul>
      <h2>Offers (SAR)</h2>
      <ul>
      <li><strong>AI Workflow Audit</strong> — 499–2,500 SAR</li>
      <li><strong>Paid Pilot</strong> — 5,000–25,000 SAR</li>
      <li><strong>Department OS</strong> — 25,000–150,000 SAR</li>
      <li><strong>Monthly Retainer</strong> — 3,000–25,000 SAR/month</li>
      <li><strong>Enterprise Custom OS</strong> — 150,000+ SAR</li>
      </ul>
      <p><a href="/contact">Request an audit →</a></p>
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        <strong>Safety:</strong> AI prepares and recommends; you approve and act. Nothing is sent or submitted automatically. No ROI guarantees — we show evidence and estimates.
      </p>
    </main>
  );
}
