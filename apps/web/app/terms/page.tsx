import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Terms of Service',
  description: 'Dealix terms of service (template — pending legal review).',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>Terms of Service</h1>
      <p><em>Template — pending qualified legal review. Not legal advice.</em></p>
      <p>Use of this site is subject to acceptable-use and liability terms finalized with legal counsel
         before any commercial engagement.</p>
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        <strong>Safety:</strong> AI prepares and recommends; you approve and act. Nothing is sent or submitted automatically. No ROI guarantees — we show evidence and estimates.
      </p>
    </main>
  );
}
