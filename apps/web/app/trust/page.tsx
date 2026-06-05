export const metadata = {
  title: "Trust Center — Dealix",
  description:
    "Dealix is approval-first. No blind automation, no external sending without founder approval."
};

export default function TrustPage() {
  return (
    <main className="grid">
      <h1>Trust Center</h1>
      <p>
        Dealix is <strong>approval-first</strong>. The system prepares,
        analyzes, drafts, ranks, and recommends. The founder reviews, approves,
        and sends manually. Nothing is sent externally by the system.
      </p>

      <h2>Our commitments</h2>
      <ul>
        <li>Human review before anything leaves the building.</li>
        <li>No blind automation — no unattended outbound to people.</li>
        <li>No external sending from CI/CD or scheduled jobs.</li>
        <li>Data minimization by default.</li>
        <li>Auditable decisions and founder approval.</li>
        <li>Only verifiable claims — no fake traction, no guaranteed ROI.</li>
      </ul>

      <p>
        See also <a href="/security">Security</a> and{" "}
        <a href="/privacy">Privacy</a>.
      </p>
    </main>
  );
}
