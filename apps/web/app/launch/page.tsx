import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'Launch Status',
  description: 'Dealix launch readiness — what is live, what is review-only, and what remains founder-gated.',
};

export default function Page() {
  return (
    <main className="grid" style={{ maxWidth: 880, margin: "0 auto", padding: "2rem 1rem", lineHeight: 1.6 }}>
      <h1>Launch</h1>
      <p>We launch trust-first. Live now: public site, review-only draft preparation, founder-led
         outreach, paid diagnostics. Always founder-gated: any external sending, paid ads, and
         sensitive-data processing.</p>
      <p><a href="/status">System status →</a></p>
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        <strong>Safety:</strong> AI prepares and recommends; you approve and act. Nothing is sent or submitted automatically. No ROI guarantees — we show evidence and estimates.
      </p>
    </main>
  );
}
