import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Trust & Safety',
  description: 'How Dealix stays trustworthy: human-in-the-loop, review-only drafts, no blind automation, PDPL-aware.',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>Trust &amp; Safety</h1>
      <ul>
      <li>Human-in-the-loop: the founder approves every external action.</li>
      <li>Review-only drafts: the system prepares, never sends.</li>
      <li>No scraping, no mass-sending, no automation of outreach.</li>
      <li>PDPL-aware data handling; no sensitive data before an agreement.</li>
      <li>Evidence over claims — no ROI guarantees.</li>
      </ul>
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        <strong>Safety:</strong> AI prepares and recommends; you approve and act. Nothing is sent or submitted automatically. No ROI guarantees — we show evidence and estimates.
      </p>
    </main>
  );
}
