export const metadata = {
  title: "Privacy — Dealix",
  description:
    "Dealix privacy posture: data minimization, no customer-sensitive data without agreement, clear retention."
};

export default function PrivacyPage() {
  return (
    <main className="grid">
      <h1>Privacy</h1>
      <p>
        We collect and retain the minimum data necessary to deliver value, and
        we are explicit about boundaries.
      </p>

      <h2>Principles</h2>
      <ul>
        <li>Data minimization by default.</li>
        <li>No customer-sensitive data without a signed agreement.</li>
        <li>Clear separation between demo/sandbox data and customer data.</li>
        <li>Deletion on request and on retention expiry.</li>
      </ul>

      <p>
        See also <a href="/trust">Trust Center</a> and{" "}
        <a href="/security">Security</a>.
      </p>
    </main>
  );
}
