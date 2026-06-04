import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Dealix — Trust-first AI Revenue & Ops OS',
  description: 'Dealix is a Saudi/GCC B2B AI Revenue & Operations OS. AI prepares; you approve; nothing sends without you.',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>Dealix — the trust-first AI Revenue &amp; Ops OS</h1>
      <p>For Saudi/GCC B2B operators. AI drafts, scores, and prepares your revenue work.
         You review, approve, and send manually. The system never sends externally.</p>
      <p><a href="/commercial">See the commercial offers →</a> · <a href="/trust">How we keep it safe →</a></p>
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        <strong>Safety:</strong> AI prepares and recommends; you approve and act. Nothing is sent or submitted automatically. No ROI guarantees — we show evidence and estimates.
      </p>
    </main>
  );
}
