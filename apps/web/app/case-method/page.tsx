import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Case Method',
  description: 'How Dealix turns delivery into proof: evidence capture, client approval, anonymized case studies.',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>Case Method</h1>
      <p>We turn delivery into proof: capture evidence during delivery, get client approval,
         and publish anonymized outcomes. Every claim is backed by an artifact or labeled an estimate.</p>
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        <strong>Safety:</strong> AI prepares and recommends; you approve and act. Nothing is sent or submitted automatically. No ROI guarantees — we show evidence and estimates.
      </p>
    </main>
  );
}
