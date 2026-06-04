import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Privacy Policy',
  description: 'Dealix privacy policy (template — pending legal review). PDPL-aware data handling.',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>Privacy Policy</h1>
      <p><em>Template — pending qualified legal review. Not legal advice.</em></p>
      <p>We collect only what you provide with consent, use it to respond to your request,
         retain it minimally, and honor access/deletion requests. PDPL-aware.</p>
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        <strong>Safety:</strong> AI prepares and recommends; you approve and act. Nothing is sent or submitted automatically. No ROI guarantees — we show evidence and estimates.
      </p>
    </main>
  );
}
