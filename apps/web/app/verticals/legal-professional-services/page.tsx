import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Legal & Professional Services — Dealix',
  description: 'Dealix for Legal & Professional Services: review-only AI ops that reduce manual work. Speed up intake, matter reporting, and document draft prep — review-only.',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>Legal & Professional Services</h1>
      <p dir="rtl" lang="ar">الخدمات القانونية والمهنية</p>
      <p>Speed up intake, matter reporting, and document draft prep — review-only.</p>
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
