import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Contact',
  description: 'Contact Dealix to request a review-only AI workflow audit. Opt-in only; no auto-submission.',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>Contact</h1>
      <p>Request a review-only AI workflow audit (from 499 SAR). We reply personally — opt-in only.</p>
      <p>This page does not auto-submit or send anything. Reach out via the channel shared by the founder
         during your conversation, or your existing introduction.</p>
      <p><a href="/commercial">Review the offers →</a></p>
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        <strong>Safety:</strong> AI prepares and recommends; you approve and act. Nothing is sent or submitted automatically. No ROI guarantees — we show evidence and estimates.
      </p>
    </main>
  );
}
