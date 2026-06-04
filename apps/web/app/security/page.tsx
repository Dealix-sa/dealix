export const metadata = {
  title: "Security — Dealix",
  description:
    "Dealix security posture: human-in-the-loop, least privilege, no secrets committed, honest certification status."
};

export default function SecurityPage() {
  return (
    <main className="grid">
      <h1>Security</h1>
      <p>
        We take a conservative, honest approach to security. We do not claim
        certifications we do not hold; status is disclosed transparently.
      </p>

      <h2>Posture</h2>
      <ul>
        <li>Secrets are never committed; least-privilege access.</li>
        <li>Human-in-the-loop for any external-facing action.</li>
        <li>No external sending from automation or CI.</li>
        <li>Incident disclosure is prompt and honest.</li>
      </ul>

      <h2>Certification status</h2>
      <p>
        Formal certifications (e.g. SOC 2, ISO 27001) are not claimed unless and
        until they are actually achieved. Current status is shared on request.
      </p>

      <p>
        See also <a href="/trust">Trust Center</a> and{" "}
        <a href="/privacy">Privacy</a>.
      </p>
    </main>
  );
}
