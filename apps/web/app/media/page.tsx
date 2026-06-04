import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Media & Press',
  description: 'Dealix media and press resources. Factual claims only.',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>Media &amp; Press</h1>
      <p>Boilerplate, founder background, and logo usage available on request. We make factual
         claims only — no inflated metrics.</p>
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        <strong>Safety:</strong> AI prepares and recommends; you approve and act. Nothing is sent or submitted automatically. No ROI guarantees — we show evidence and estimates.
      </p>
    </main>
  );
}
