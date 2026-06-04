import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'FAQ',
  description: 'Frequently asked questions about Dealix: safety, pricing, data handling, and the review-only model.',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>FAQ</h1>
      <h3>Is this spam / automated outreach?</h3>
      <p>No. Everything is review-only and the founder sends manually. Opt-out is always honored.</p>
      <h3>Do you guarantee ROI?</h3>
      <p>No. We show evidence and estimates, never guarantees.</p>
      <h3>How is my data handled?</h3>
      <p>PDPL-aware, minimized, and never processed before an agreement.</p>
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        <strong>Safety:</strong> AI prepares and recommends; you approve and act. Nothing is sent or submitted automatically. No ROI guarantees — we show evidence and estimates.
      </p>
    </main>
  );
}
